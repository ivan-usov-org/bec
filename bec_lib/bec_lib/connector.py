from __future__ import annotations

import _thread
import abc
import threading
import traceback

from bec_lib.logger import bec_logger
from bec_lib.messages import BECMessage, LogMessage
from bec_lib.endpoints import MessageEndpoints

logger = bec_logger.logger


class ConsumerConnectorError(Exception):
    pass


class MessageObject:
    def __init__(self, topic: str, value: BECMessage) -> None:
        self.topic = topic
        self._value = value

    @property
    def value(self) -> BECMessage:
        return self._value

    def __eq__(self, ref_val: MessageObject) -> bool:
        if not isinstance(ref_val, MessageObject):
            return False
        return self._value == ref_val.value and self.topic == ref_val.topic

    def __str__(self):
        return f"MessageObject(topic={self.topic}, value={self._value})"


class StoreInterface(abc.ABC):
    """StoreBase defines the interface for storing data"""

    def __init__(self, store):
        pass

    def pipeline(self):
        pass

    def execute_pipeline(self):
        pass

    def lpush(
        self, topic: str, msg: str, pipe=None, max_size: int = None, expire: int = None
    ) -> None:
        raise NotImplementedError

    def lset(self, topic: str, index: int, msg: str, pipe=None) -> None:
        raise NotImplementedError

    def rpush(self, topic: str, msg: str, pipe=None) -> int:
        raise NotImplementedError

    def lrange(self, topic: str, start: int, end: int, pipe=None):
        raise NotImplementedError

    def set(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        raise NotImplementedError

    def keys(self, pattern: str) -> list:
        raise NotImplementedError

    def delete(self, topic, pipe=None):
        raise NotImplementedError

    def get(self, topic: str, pipe=None):
        raise NotImplementedError

    def xadd(self, topic: str, msg: dict, max_size=None, pipe=None, expire: int = None):
        raise NotImplementedError

    def xread(
        self,
        topic: str,
        id: str = None,
        count: int = None,
        block: int = None,
        pipe=None,
        from_start=False,
    ) -> list:
        raise NotImplementedError

    def xrange(self, topic: str, min: str, max: str, count: int = None, pipe=None):
        raise NotImplementedError


class PubSubInterface(abc.ABC):
    def raw_send(self, topic: str, msg: bytes) -> None:
        raise NotImplementedError

    def send(self, topic: str, msg: BECMessage) -> None:
        raise NotImplementedError

    def register(self, topics=None, pattern=None, cb=None, start_thread=True, **kwargs):
        raise NotImplementedError

    def unregister(self, topics=None, pattern=None, cb=None):
        raise NotImplementedError

    def poll_messages(self, timeout=None):
        """Poll for new messages, receive them and execute callbacks"""
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError


class ConnectorBase(PubSubInterface, StoreInterface):
    def raise_warning(self, msg):
        raise NotImplementedError

    def log_warning(self, msg):
        """send a warning"""
        self.send(MessageEndpoints.log(), LogMessage(log_type="warning", log_msg=msg))

    def log_message(self, msg):
        """send a log message"""
        self.send(MessageEndpoints.log(), LogMessage(log_type="log", log_msg=msg))

    def log_error(self, msg):
        """send an error as log"""
        self.send(MessageEndpoints.log(), LogMessage(log_type="error", log_msg=msg))

    def set_and_publish(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        raise NotImplementedError
