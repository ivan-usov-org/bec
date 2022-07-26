import enum
import time
from typing import Tuple

import redis

from .BECMessage import AlarmMessage, LogMessage
from .connector import (
    ConnectorBase,
    ConsumerConnector,
    ConsumerConnectorThreaded,
    MessageObject,
    ProducerConnector,
)
from .endpoints import MessageEndpoints


class Alarms(int, enum.Enum):
    WARNING = 0
    MINOR = 1
    MAJOR = 2


class RedisConnector(ConnectorBase):
    def __init__(self, bootstrap: list):
        super().__init__(bootstrap)
        self.host, self.port = (
            bootstrap[0].split(":") if isinstance(bootstrap, list) else bootstrap.split(":")
        )
        self._notifications_producer = RedisProducer(host=self.host, port=self.port)

    def producer(self, **kwargs):
        return RedisProducer(host=self.host, port=self.port)

    def consumer(
        self,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        threaded=True,
        **kwargs,
    ):
        if threaded:
            if topics is None and pattern is None:
                raise ValueError("Topics must be set for threaded consumer")
            listener = RedisConsumerThreaded(
                self.host, self.port, topics, pattern, group_id, event, cb, **kwargs
            )
            self._threads.append(listener)
            return listener
        else:
            return RedisConsumer(
                self.host, self.port, topics, pattern, group_id, event, cb, **kwargs
            )

    def log_warning(self, msg):
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="warning", content=msg).dumps()
        )

    def log_message(self, msg):
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="log", content=msg).dumps()
        )

    def log_error(self, msg):
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="error", content=msg).dumps()
        )

    def raise_alarm(
        self, severity: Alarms, alarm_type: str, source: str, content: dict, metadata: dict
    ):
        self._notifications_producer.set_and_publish(
            MessageEndpoints.alarm(),
            AlarmMessage(
                severity=severity,
                alarm_type=alarm_type,
                source=source,
                content=content,
                metadata=metadata,
            ).dumps(),
        )


class RedisProducer(ProducerConnector):
    def __init__(self, host: str, port: int) -> None:
        self.r = redis.Redis(host=host, port=port)

    def send(self, topic: str, msg) -> None:
        self.r.publish(f"{topic}:sub", msg)

    def lpush(self, topic: str, msgs: str) -> None:
        self.r.lpush(f"{topic}:val", msgs)

    def rpush(self, topic: str, msgs: str) -> None:
        self.r.rpush(f"{topic}:val", msgs)

    def lrange(self, topic: str, start: int, end: int):
        return self.r.lrange(f"{topic}:val", start, end)

    def set_and_publish(self, topic: str, msg, pipe=None) -> None:
        client = pipe if pipe is not None else self.r
        client.publish(f"{topic}:sub", msg)
        client.set(f"{topic}:val", msg)

    def set(self, topic: str, msg, pipe=None, is_dict=False) -> None:
        client = pipe if pipe is not None else self.r
        if is_dict:
            client.hmset(f"{topic}:val", msg)
        else:
            client.set(f"{topic}:val", msg)

    def pipeline(self):
        return self.r.pipeline()

    def delete(self, topic, pipe=None):
        client = pipe if pipe is not None else self.r
        client.delete(topic)

    def get(self, topic: str, pipe=None, is_dict=False):
        client = pipe if pipe is not None else self.r
        if is_dict:
            return client.hgetall(f"{topic}:val")
        else:
            return client.get(f"{topic}:val")


class RedisConsumer(ConsumerConnector):
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        **kwargs,
    ):
        bootstrap_server = "".join([host, ":", port])
        if isinstance(topics, list):
            topics = [f"{topic}:sub" for topic in topics]
        else:
            topics = [f"{topics}:sub"]
        if pattern:
            if isinstance(pattern, list):
                pattern = [f"{pattern}:sub" for pattern in self.pattern]
            else:
                pattern = [f"{pattern}:sub"]
        super().__init__(bootstrap_server, topics, pattern, group_id, event, cb, **kwargs)
        self.r = redis.Redis(host=host, port=port)
        self.pubsub = self.r.pubsub()
        self.host = host
        self.port = port
        self.initialize_connector()

    def initialize_connector(self) -> None:
        if self.pattern is not None:
            self.pubsub.psubscribe(self.pattern)
        else:
            self.pubsub.subscribe(self.topics)

    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        messages = self.pubsub.get_message(ignore_subscribe_messages=True)
        if messages is not None:
            msg = MessageObject(topic=messages["channel"], value=messages["data"])
            return self.cb(msg, **self.kwargs)
        else:
            time.sleep(0.01)

    def shutdown(self):
        self.pubsub.close()


class RedisConsumerThreaded(ConsumerConnectorThreaded):
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        **kwargs,
    ):
        bootstrap_server = "".join([host, ":", port])
        if isinstance(topics, list):
            topics = [f"{topic}:sub" for topic in topics]
        else:
            topics = [f"{topics}:sub"]
        if pattern:
            if isinstance(pattern, list):
                pattern = [f"{pattern}:sub" for pattern in self.pattern]
            else:
                pattern = [f"{pattern}:sub"]
        super().__init__(bootstrap_server, topics, pattern, group_id, event, cb, **kwargs)
        self.r = redis.Redis(host=host, port=port)
        self.pubsub = self.r.pubsub()
        self.host = host
        self.port = port
        self.sleep_times = [None, 0.1]
        self.last_received_msg = 0
        self.idle_time = 30

    def initialize_connector(self) -> None:
        if self.pattern is not None:
            self.pubsub.psubscribe(self.pattern)
        else:
            self.pubsub.subscribe(self.topics)

    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        messages = self.pubsub.get_message(ignore_subscribe_messages=True)
        if messages is not None:
            if f"{MessageEndpoints.log()}".encode() not in messages["channel"]:
                # no need to update the update frequency just for logs
                self.last_received_msg = time.time()
            msg = MessageObject(topic=messages["channel"], value=messages["data"])
            self.cb(msg, **self.kwargs)
        else:
            sleep_time = int(bool(time.time() - self.last_received_msg > self.idle_time))
            if self.sleep_times[sleep_time]:
                time.sleep(self.sleep_times[sleep_time])

    def shutdown(self):
        self.pubsub.close()
