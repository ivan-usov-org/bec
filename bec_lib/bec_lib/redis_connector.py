from __future__ import annotations

import collections
import queue
import sys
import threading
import warnings
from functools import wraps
from typing import TYPE_CHECKING

import louie
import redis
import redis.client

from bec_lib.connector import ConnectorBase, MessageObject
from bec_lib.endpoints import MessageEndpoints
from bec_lib.messages import AlarmMessage, BECMessage, LogMessage
from bec_lib.serialization import MsgpackSerialization

if TYPE_CHECKING:
    from bec_lib.alarm_handler import Alarms


def catch_connection_error(func):
    """catch connection errors"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError:
            warnings.warn("Failed to connect to redis. Is the server running?")
            return None

    return wrapper


class RedisConnector(ConnectorBase):
    def __init__(self, bootstrap: list, redis_cls=None):
        super().__init__(bootstrap)
        self.host, self.port = (
            bootstrap[0].split(":") if isinstance(bootstrap, list) else bootstrap.split(":")
        )

        if redis_cls:
            self._redis_conn = redis_cls(host=self.host, port=self.port)
        else:
            self._redis_conn = redis.Redis(host=self.host, port=self.port)

        # main pubsub connection
        self._pubsub_conn = self._redis_conn.pubsub()
        self._pubsub_conn.ignore_subscribe_messages = True
        # keep track of topics and callbacks
        self._topics_cb = collections.defaultdict(list)

        self._events_listener_thread = None
        self._events_dispatcher_thread = None
        self._messages_queue = queue.Queue()
        self._stop_events_listener_thread = threading.Event()

        self.stream_keys = {}

    def shutdown(self):
        if self._events_listener_thread:
            self._stop_events_listener_thread.set()
            self._events_listener_thread.join()
            self._events_listener_thread = None
        if self._events_dispatcher_thread:
            self._messages_queue.put(StopIteration)
            self._events_dispatcher_thread.join()
            self._events_dispatcher_thread = None
        # release all connections
        self._pubsub_conn.close()
        self._redis_conn.close()

    @catch_connection_error
    def log_warning(self, msg):
        """send a warning"""
        self.send(MessageEndpoints.log(), LogMessage(log_type="warning", log_msg=msg))

    @catch_connection_error
    def log_message(self, msg):
        """send a log message"""
        self.send(MessageEndpoints.log(), LogMessage(log_type="log", log_msg=msg))

    @catch_connection_error
    def log_error(self, msg):
        """send an error as log"""
        self.send(MessageEndpoints.log(), LogMessage(log_type="error", log_msg=msg))

    @catch_connection_error
    def raise_alarm(
        self,
        severity: Alarms,
        alarm_type: str,
        source: str,
        msg: str,
        metadata: dict,
    ):
        """raise an alarm"""
        alarm_msg = AlarmMessage(
            severity=severity,
            alarm_type=alarm_type,
            source=source,
            msg=msg,
            metadata=metadata,
        )
        self.set_and_publish(MessageEndpoints.alarm(), alarm_msg)

    def pipeline(self):
        """Create a new pipeline"""
        return self._redis_conn.pipeline()

    @catch_connection_error
    def execute_pipeline(self, pipeline):
        """Execute the pipeline and returns the results with decoded BECMessages"""
        ret = []
        results = pipeline.execute()
        for res in results:
            try:
                ret.append(MsgpackSerialization.loads(res))
            except RuntimeError:
                ret.append(res)
        return ret

    @catch_connection_error
    def raw_send(self, topic: str, msg: bytes, pipe=None):
        """send to redis without any check on message type"""
        client = pipe if pipe is not None else self._redis_conn
        client.publish(topic, msg)

    def send(self, topic: str, msg: BECMessage, pipe=None) -> None:
        """send to redis"""
        if not isinstance(msg, BECMessage):
            raise TypeError(f"Message {msg} is not a BECMessage")
        self.raw_send(topic, MsgpackSerialization.dumps(msg), pipe)

    def register(self, topics=None, patterns=None, cb=None, start_thread=True, **kwargs):
        if self._events_listener_thread is None:
            # create the thread that will get all messages for this connector;
            # under the hood, it uses asyncio - this lets the possibility to stop
            # the loop on demand
            self._events_listener_thread = threading.Thread(
                target=self._get_messages_loop,
                args=(self._pubsub_conn,),
            )
            self._events_listener_thread.start()
        # make a weakref from the callable, using louie;
        # it can create safe refs for simple functions as well as methods
        cb_ref = louie.saferef.safe_ref(cb)

        if patterns is not None:
            if isinstance(patterns, str):
                patterns = [patterns]

            self._pubsub_conn.psubscribe(patterns)
            for pattern in patterns:
                self._topics_cb[pattern].append((cb_ref, kwargs))
        else:
            if isinstance(topics, str):
                topics = [topics]

            self._pubsub_conn.subscribe(topics)
            for topic in topics:
                self._topics_cb[topic].append((cb_ref, kwargs))

        if start_thread and self._events_dispatcher_thread is None:
            # start dispatcher thread
            self._events_dispatcher_thread = threading.Thread(target=self.dispatch_events)
            self._events_dispatcher_thread.start()

    def _get_messages_loop(self, pubsub) -> None:
        """
        Start a listening coroutine to deal with redis events and wait for completion
        """
        while not self._stop_events_listener_thread.is_set():
            try:
                msg = pubsub.get_message(timeout=1)
            except Exception:
                sys.excepthook(*sys.exc_info())
            else:
                if msg is not None:
                    self._messages_queue.put(msg)

    def _handle_message(self, msg):
        if msg["type"].endswith("subscribe"):
            # ignore subscribe messages
            return False
        channel = msg["channel"].decode()
        if msg["pattern"] is not None:
            callbacks = self._topics_cb[msg["pattern"].decode()]
        else:
            callbacks = self._topics_cb[channel]
        msg = MessageObject(
            topic=channel,
            value=MsgpackSerialization.loads(msg["data"]),
        )
        for cb_ref, kwargs in callbacks:
            cb = cb_ref()
            if cb:
                try:
                    cb(msg, **kwargs)
                except Exception:
                    sys.excepthook(*sys.exc_info())
        return True

    def poll_messages(self, timeout=None) -> None:
        while True:
            try:
                msg = self._messages_queue.get(timeout=timeout)
            except queue.Empty:
                raise TimeoutError(
                    f"{self}: poll_messages: did not receive a message within {timeout} seconds"
                )
            else:
                if msg is StopIteration:
                    return False
                if self._handle_message(msg):
                    return True
                else:
                    continue

    def dispatch_events(self):
        while self.poll_messages():
            ...

    @catch_connection_error
    def lpush(
        self, topic: str, msg: str, pipe=None, max_size: int = None, expire: int = None
    ) -> None:
        """Time complexity: O(1) for each element added, so O(N) to
        add N elements when the command is called with multiple arguments.
        Insert all the specified values at the head of the list stored at key.
        If key does not exist, it is created as empty list before
        performing the push operations. When key holds a value that
        is not a list, an error is returned."""
        client = pipe if pipe is not None else self.pipeline()
        if isinstance(msg, BECMessage):
            msg = MsgpackSerialization.dumps(msg)
        client.lpush(topic, msg)
        if max_size:
            client.ltrim(topic, 0, max_size)
        if expire:
            client.expire(topic, expire)
        if not pipe:
            client.execute()

    @catch_connection_error
    def lset(self, topic: str, index: int, msg: str, pipe=None) -> None:
        client = pipe if pipe is not None else self._redis_conn
        if isinstance(msg, BECMessage):
            msg = MsgpackSerialization.dumps(msg)
        return client.lset(topic, index, msg)

    @catch_connection_error
    def rpush(self, topic: str, msg: str, pipe=None) -> int:
        """O(1) for each element added, so O(N) to add N elements when the
        command is called with multiple arguments. Insert all the specified
        values at the tail of the list stored at key. If key does not exist,
        it is created as empty list before performing the push operation. When
        key holds a value that is not a list, an error is returned."""
        client = pipe if pipe is not None else self._redis_conn
        if isinstance(msg, BECMessage):
            msg = MsgpackSerialization.dumps(msg)
        return client.rpush(topic, msg)

    @catch_connection_error
    def lrange(self, topic: str, start: int, end: int, pipe=None):
        """O(S+N) where S is the distance of start offset from HEAD for small
        lists, from nearest end (HEAD or TAIL) for large lists; and N is the
        number of elements in the specified range. Returns the specified elements
        of the list stored at key. The offsets start and stop are zero-based indexes,
        with 0 being the first element of the list (the head of the list), 1 being
        the next element and so on."""
        client = pipe if pipe is not None else self._redis_conn
        cmd_result = client.lrange(topic, start, end)
        if pipe:
            return cmd_result
        else:
            # in case of command executed in a pipe, use 'execute_pipeline' method
            ret = []
            for msg in cmd_result:
                try:
                    ret.append(MsgpackSerialization.loads(msg))
                except RuntimeError:
                    ret.append(msg)
            return ret

    def set_and_publish(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        """piped combination of self.publish and self.set"""
        client = pipe if pipe is not None else self.pipeline()
        if not isinstance(msg, BECMessage):
            raise TypeError(f"Message {msg} is not a BECMessage")
        msg = MsgpackSerialization.dumps(msg)
        self.set(topic, msg, pipe=client, expire=expire)
        self.raw_send(topic, msg, pipe=client)
        if not pipe:
            client.execute()

    @catch_connection_error
    def set(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        """set redis value"""
        client = pipe if pipe is not None else self._redis_conn
        if isinstance(msg, BECMessage):
            msg = MsgpackSerialization.dumps(msg)
        client.set(topic, msg, ex=expire)

    @catch_connection_error
    def keys(self, pattern: str) -> list:
        """returns all keys matching a pattern"""
        return self._redis_conn.keys(pattern)

    @catch_connection_error
    def delete(self, topic, pipe=None):
        """delete topic"""
        client = pipe if pipe is not None else self._redis_conn
        client.delete(topic)

    @catch_connection_error
    def get(self, topic: str, pipe=None):
        """retrieve entry, either via hgetall or get"""
        client = pipe if pipe is not None else self._redis_conn
        data = client.get(topic)
        if pipe:
            return data
        else:
            try:
                return MsgpackSerialization.loads(data)
            except RuntimeError:
                return data

    @catch_connection_error
    def xadd(self, topic: str, msg_dict: dict, max_size=None, pipe=None, expire: int = None):
        """
        add to stream

        Args:
            topic (str): redis topic
            msg_dict (dict): message to add
            max_size (int, optional): max size of stream. Defaults to None.
            pipe (Pipeline, optional): redis pipe. Defaults to None.
            expire (int, optional): expire time. Defaults to None.

        Examples:
            >>> redis.xadd("test", {"test": "test"})
            >>> redis.xadd("test", {"test": "test"}, max_size=10)
        """
        if pipe:
            client = pipe
        elif expire:
            client = self.pipeline()
        else:
            client = self._redis_conn

        for key, msg in msg_dict.items():
            msg_dict[key] = MsgpackSerialization.dumps(msg)

        if max_size:
            client.xadd(topic, msg_dict, maxlen=max_size)
        else:
            client.xadd(topic, msg_dict)
        if expire:
            client.expire(topic, expire)
        if not pipe and expire:
            client.execute()

    @catch_connection_error
    def get_last(self, topic: str, key="data"):
        """retrieve last entry from stream"""
        client = self._redis_conn
        try:
            _, msg_dict = client.xrevrange(topic, "+", "-", count=1)[0]
        except TypeError:
            return None
        else:
            msg_dict = {k.decode(): MsgpackSerialization.loads(msg) for k, msg in msg_dict.items()}

            if key is None:
                return msg_dict
            return msg_dict.get(key)

    @catch_connection_error
    def xread(
        self,
        topic: str,
        id: str = None,
        count: int = None,
        block: int = None,
        from_start=False,
    ) -> list:
        """
        read from stream

        Args:
            topic (str): redis topic
            id (str, optional): id to read from. Defaults to None.
            count (int, optional): number of messages to read. Defaults to None.
            block (int, optional): block for x milliseconds. Defaults to None.
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
        client = self._redis_conn
        if from_start:
            self.stream_keys[topic] = "0-0"
        if topic not in self.stream_keys:
            if id is None:
                try:
                    msg = client.xrevrange(topic, "+", "-", count=1)
                    if msg:
                        self.stream_keys[topic] = msg[0][0]
                        out = {}
                        for key, val in msg[0][1].items():
                            out[key.decode()] = MsgpackSerialization.loads(val)
                        return [out]
                    self.stream_keys[topic] = "0-0"
                except redis.exceptions.ResponseError:
                    self.stream_keys[topic] = "0-0"
        if id is None:
            id = self.stream_keys[topic]

        msg = client.xread({topic: id}, count=count, block=block)
        return self._decode_stream_messages_xread(msg)

    def _decode_stream_messages_xread(self, msg):
        out = []
        for topic, msgs in msg:
            for index, record in msgs:
                out.append(
                    {k.decode(): MsgpackSerialization.loads(msg) for k, msg in record.items()}
                )
                self.stream_keys[topic] = index
        return out if out else None

    @catch_connection_error
    def xrange(self, topic: str, min: str, max: str, count: int = None):
        """
        read a range from stream

        Args:
            topic (str): redis topic
            min (str): min id. Use "-" to read from start
            max (str): max id. Use "+" to read to end
            count (int, optional): number of messages to read. Defaults to None.
        """
        client = self._redis_conn
        msgs = []
        for reading in client.xrange(topic, min, max, count=count):
            index, msg_dict = reading
            msgs.append(
                {k.decode(): MsgpackSerialization.loads(msg) for k, msg in msg_dict.items()}
            )
        return msgs

    def producer(self):
        """Return itself as a producer, to be compatible with old code"""
        warnings.warn(
            "RedisConnector.producer() is deprecated and should not be used anymore. A Connector is a producer now, just use the connector object.",
            FutureWarning,
        )
        return self

    def consumer(
        self,
        topics=None,
        patterns=None,
        group_id=None,
        event=None,
        cb=None,
        threaded=True,
        name=None,
        **kwargs,
    ):
        """Return a fake thread object to be compatible with old code

        In order to keep this fail-safe and simple it uses 'mock'...
        """
        from unittest.mock import (
            Mock,
        )  # import is done here, to not pollute the file with something normally in tests

        warnings.warn(
            "RedisConnector.consumer() is deprecated and should not be used anymore. Use RedisConnector.register() with 'topics', 'patterns', 'cb' or 'start_thread' instead. Additional keyword args are transmitted to the callback. For the caller, the main difference with RedisConnector.register() is that it does not return a new thread.",
            FutureWarning,
        )
        dummy_thread = Mock(spec=threading.Thread)
        dummy_thread.start.side_effet = lambda: self.register(
            topics, patterns, cb, threaded, **kwargs
        )
        return dummy_thread
