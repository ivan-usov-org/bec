"""
Connector defines the interface for a connector
"""

from __future__ import annotations

import abc

from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.messages import BECMessage, LogMessage

logger = bec_logger.logger


class ConsumerConnectorError(Exception):
    """
    ConsumerConnectorError is raised when there is an error with the connector
    """


class MessageObject:
    """
    MessageObject is a wrapper for a message and its topic
    """

    def __init__(self, topic: str, value: BECMessage) -> None:
        self.topic = topic
        self._value = value

    @property
    def value(self) -> BECMessage:
        """
        Get the message
        """
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
        """Create a pipeline for batch operations"""

    def execute_pipeline(self, pipeline):
        """Execute a pipeline"""

    def lpush(
        self, topic: str, msg: str, pipe=None, max_size: int = None, expire: int = None
    ) -> None:
        """Push a message to the left of the list"""
        raise NotImplementedError

    def lset(self, topic: str, index: int, msg: str, pipe=None) -> None:
        """Set a value in the list at the given index"""
        raise NotImplementedError

    def rpush(self, topic: str, msg: str, pipe=None) -> int:
        """Push a message to the right of the list"""
        raise NotImplementedError

    def lrange(self, topic: str, start: int, end: int, pipe=None):
        """Get a range of values from the list"""
        raise NotImplementedError

    def set(self, topic: str, msg, pipe=None, expire: int = None) -> None:
        """Set a value"""
        raise NotImplementedError

    def keys(self, pattern: str) -> list:
        """Get keys that match the pattern"""
        raise NotImplementedError

    def delete(self, topic, pipe=None):
        """Delete a key"""
        raise NotImplementedError

    def get(self, topic: str, pipe=None):
        """Get a value"""
        raise NotImplementedError

    def xadd(self, topic: str, msg_dict: dict, max_size=None, pipe=None, expire: int = None):
        """Add a message to the stream"""
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
        """Read from the stream"""
        raise NotImplementedError

    def xrange(self, topic: str, min: str, max: str, count: int = None, pipe=None):
        """Read from the stream"""
        raise NotImplementedError


class PubSubInterface(abc.ABC):
    """PubSubBase defines the interface for a pub/sub connector"""

    def raw_send(self, topic: str, msg: bytes) -> None:
        """Send a raw message without using the BECMessage class"""
        raise NotImplementedError

    def send(self, topic: str, msg: BECMessage) -> None:
        """Send a message"""
        raise NotImplementedError

    def register(self, topics=None, patterns=None, cb=None, start_thread=True, **kwargs):
        """Register a callback for a topic or pattern"""
        raise NotImplementedError

    def poll_messages(self, timeout=None):
        """Poll for new messages, receive them and execute callbacks"""
        raise NotImplementedError

    def run_messages_loop(self):
        """Run the message loop"""
        raise NotImplementedError

    def shutdown(self):
        """Shutdown the connector"""


class ConnectorBase(PubSubInterface, StoreInterface):
    """ConnectorBase defines the interface for a connector"""

    def raise_warning(self, msg):
        """Raise a warning"""
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
        """Set a value and publish it"""
        raise NotImplementedError
