import enum
import time

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
    def __init__(self, bootstrap: list, redis_cls=None):
        super().__init__(bootstrap)
        self.redis_cls = redis_cls
        self.host, self.port = (
            bootstrap[0].split(":") if isinstance(bootstrap, list) else bootstrap.split(":")
        )
        self._notifications_producer = RedisProducer(
            host=self.host, port=self.port, redis_cls=self.redis_cls
        )

    def producer(self, **kwargs):
        return RedisProducer(host=self.host, port=self.port, redis_cls=self.redis_cls)

    # pylint: disable=too-many-arguments
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
        if cb is None:
            raise ValueError("The callback function must be specified.")

        if threaded:
            if topics is None and pattern is None:
                raise ValueError("Topics must be set for threaded consumer")
            listener = RedisConsumerThreaded(
                self.host,
                self.port,
                topics,
                pattern,
                group_id,
                event,
                cb,
                redis_cls=self.redis_cls,
                **kwargs,
            )
            self._threads.append(listener)
            return listener
        return RedisConsumer(
            self.host,
            self.port,
            topics,
            pattern,
            group_id,
            event,
            cb,
            redis_cls=self.redis_cls,
            **kwargs,
        )

    def log_warning(self, msg):
        """send a warning"""
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="warning", content=msg).dumps()
        )

    def log_message(self, msg):
        """send a log message"""
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="log", content=msg).dumps()
        )

    def log_error(self, msg):
        """send an error as log"""
        self._notifications_producer.send(
            MessageEndpoints.log(), LogMessage(log_type="error", content=msg).dumps()
        )

    def raise_alarm(
        self, severity: Alarms, alarm_type: str, source: str, content: dict, metadata: dict
    ):
        """raise an alarm"""
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
    def __init__(self, host: str, port: int, redis_cls=None) -> None:
        # pylint: disable=invalid-name
        if redis_cls:
            self.r = redis_cls(host=host, port=port)
            return
        self.r = redis.Redis(host=host, port=port)
        self.stream_keys = {}

    def send(self, topic: str, msg, pipe=None) -> None:
        """send to redis"""
        client = pipe if pipe is not None else self.r
        client.publish(f"{topic}:sub", msg)

    def lpush(
        self, topic: str, msgs: str, pipe=None, max_size: int = None, expire: int = None
    ) -> None:
        """Time complexity: O(1) for each element added, so O(N) to
        add N elements when the command is called with multiple arguments.
        Insert all the specified values at the head of the list stored at key.
        If key does not exist, it is created as empty list before
        performing the push operations. When key holds a value that
        is not a list, an error is returned."""

        client = pipe if pipe is not None else self.pipeline()
        client.lpush(f"{topic}:val", msgs)
        if max_size:
            client.ltrim(f"{topic}:val", 0, max_size)
        if expire:
            client.expire(f"{topic}:val", expire)
        if not pipe:
            client.execute()

    def lset(self, topic: str, index: int, msgs: str, pipe=None) -> None:
        client = pipe if pipe is not None else self.r
        return client.lset(f"{topic}:val", index, msgs)

    def rpush(self, topic: str, msgs: str, pipe=None) -> int:
        """O(1) for each element added, so O(N) to add N elements when the
        command is called with multiple arguments. Insert all the specified
        values at the tail of the list stored at key. If key does not exist,
        it is created as empty list before performing the push operation. When
        key holds a value that is not a list, an error is returned."""

        client = pipe if pipe is not None else self.r
        return client.rpush(f"{topic}:val", msgs)

    def lrange(self, topic: str, start: int, end: int, pipe=None):
        """O(S+N) where S is the distance of start offset from HEAD for small
        lists, from nearest end (HEAD or TAIL) for large lists; and N is the
        number of elements in the specified range. Returns the specified elements
        of the list stored at key. The offsets start and stop are zero-based indexes,
        with 0 being the first element of the list (the head of the list), 1 being
        the next element and so on."""

        client = pipe if pipe is not None else self.r
        return client.lrange(f"{topic}:val", start, end)

    def set_and_publish(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        """piped combination of self.publish and self.set"""
        client = pipe if pipe is not None else self.pipeline()
        client.publish(f"{topic}:sub", msg)
        client.set(f"{topic}:val", msg)
        if expire:
            client.expire(f"{topic}:val", expire)
        if not pipe:
            client.execute()

    def set(self, topic: str, msg, pipe=None, is_dict=False, expire: int = None) -> None:
        """set redis value"""
        client = pipe if pipe is not None else self.pipeline()
        if is_dict:
            client.hmset(f"{topic}:val", msg)
        else:
            client.set(f"{topic}:val", msg)
        if expire:
            client.expire(f"{topic}:val", expire)
        if not pipe:
            client.execute()

    def keys(self, pattern: str) -> list:
        """returns all keys matching a pattern"""
        return self.r.keys(pattern)

    def pipeline(self):
        """create a new pipeline"""
        return self.r.pipeline()

    def delete(self, topic, pipe=None):
        """delete topic"""
        client = pipe if pipe is not None else self.r
        client.delete(topic)

    def get(self, topic: str, pipe=None, is_dict=False):
        """retrieve entry, either via hgetall or get"""
        client = pipe if pipe is not None else self.r
        if is_dict:
            return client.hgetall(f"{topic}:val")
        return client.get(f"{topic}:val")

    def xadd(self, topic: str, msg: dict, max_size=None, pipe=None):
        """add to stream"""
        client = pipe if pipe is not None else self.r
        if max_size:
            client.xadd(f"{topic}:val", msg, maxlen=max_size)
        else:
            client.xadd(f"{topic}:val", msg)

    def xread(
        self,
        topic: str,
        id: str = None,
        count: int = None,
        block: int = None,
        pipe=None,
        from_start=False,
    ) -> list:
        """
        read from stream

        Args:
            topic (str): redis topic
            id (str, optional): id to read from. Defaults to None.
            count (int, optional): number of messages to read. Defaults to None.
            block (int, optional): block for x milliseconds. Defaults to None.
            pipe (Pipeline, optional): redis pipe. Defaults to None.
            from_start (bool, optional): read from start. Defaults to False.

        Returns:
            [list]: list of messages

        Examples:
            >>> redis.xread("test", "0-0")
            >>> redis.xread("test", "0-0", count=1)

            # read one message at a time
            >>> key = 0
            >>> msg = redis.xread("test", key, count=1)
            >>> key = msg[0][1][0][0]
            >>> next_msg = redis.xread("test", key, count=1)
        """
        client = pipe if pipe is not None else self.r
        if topic not in self.stream_keys:
            if from_start:
                self.stream_keys[topic] = "0-0"
            else:
                try:
                    self.stream_keys[topic] = client.xinfo_stream(f"{topic}:val")[
                        "last-generated-id"
                    ]
                except redis.exceptions.ResponseError:
                    self.stream_keys[topic] = "0-0"
        if id is None:
            id = self.stream_keys[topic]

        msg = client.xread({f"{topic}:val": id}, count=count, block=block)
        if msg:
            self.stream_keys[topic] = msg[0][1][-1][0]
        return msg


class RedisConsumerMixin:
    def _init_topics_and_pattern(self, topics, pattern):
        if topics:
            if isinstance(topics, list):
                topics = [f"{topic}:sub" for topic in topics]
            else:
                topics = [f"{topics}:sub"]
        if pattern:
            if isinstance(pattern, list):
                pattern = [f"{pat}:sub" for pat in pattern]
            else:
                pattern = [f"{pattern}:sub"]
        return topics, pattern

    def _init_redis_cls(self, redis_cls):
        # pylint: disable=invalid-name
        if redis_cls:
            self.r = redis_cls(host=self.host, port=self.port)
        else:
            self.r = redis.Redis(host=self.host, port=self.port)

    def initialize_connector(self) -> None:
        if self.pattern is not None:
            self.pubsub.psubscribe(self.pattern)
        else:
            self.pubsub.subscribe(self.topics)


class RedisConsumer(RedisConsumerMixin, ConsumerConnector):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        redis_cls=None,
        **kwargs,
    ):
        self.host = host
        self.port = port

        bootstrap_server = "".join([host, ":", port])
        topics, pattern = self._init_topics_and_pattern(topics, pattern)
        super().__init__(
            bootstrap_server=bootstrap_server,
            topics=topics,
            pattern=pattern,
            group_id=group_id,
            event=event,
            cb=cb,
            **kwargs,
        )

        self._init_redis_cls(redis_cls)

        self.pubsub = self.r.pubsub()

        self.initialize_connector()

    def poll_messages(self) -> None:
        """
        Poll messages from self.connector and call the callback function self.cb

        """
        messages = self.pubsub.get_message(ignore_subscribe_messages=True)
        if messages is not None:
            msg = MessageObject(topic=messages["channel"], value=messages["data"])
            return self.cb(msg, **self.kwargs)

        time.sleep(0.01)
        return None

    def shutdown(self):
        """shutdown the consumer"""
        self.pubsub.close()


class RedisConsumerThreaded(RedisConsumerMixin, ConsumerConnectorThreaded):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        host,
        port,
        topics=None,
        pattern=None,
        group_id=None,
        event=None,
        cb=None,
        redis_cls=None,
        **kwargs,
    ):
        self.host = host
        self.port = port

        bootstrap_server = "".join([host, ":", port])
        topics, pattern = self._init_topics_and_pattern(topics, pattern)
        super().__init__(
            bootstrap_server=bootstrap_server,
            topics=topics,
            pattern=pattern,
            group_id=group_id,
            event=event,
            cb=cb,
            **kwargs,
        )

        self._init_redis_cls(redis_cls)
        self.pubsub = self.r.pubsub()

        self.sleep_times = [0.005, 0.1]
        self.last_received_msg = 0
        self.idle_time = 30

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
        super().shutdown()
        self.pubsub.close()
