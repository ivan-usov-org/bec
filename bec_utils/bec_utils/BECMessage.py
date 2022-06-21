import enum
from typing import Any, Union

import msgpack


class becStatus(enum.Enum):
    ERROR = -1
    OFF = 0
    IDLE = 1
    RUNNING = 2


class BECMessage:
    msg_type: str
    content: dict
    metadata: dict

    def __init__(self, *, msg_type: str, content: dict, metadata: dict = None) -> None:
        self.msg_type = msg_type
        self.content = content
        self.metadata = metadata if metadata is not None else {}
        self.version = 1.0

    @classmethod
    def loads(cls, msg):
        if isinstance(msg, bytes):
            msg = msgpack.loads(msg, raw=False)
            return cls._validated_return(msg)
        elif isinstance(msg, dict):
            return cls(**msg)

    def dumps(self):
        return msgpack.dumps(
            {
                "msg_type": self.msg_type,
                "content": self.content,
                "metadata": self.metadata,
                "version": self.version,
            }
        )

    @classmethod
    def _validated_return(cls, msg):
        if cls.msg_type != msg.get("msg_type"):
            return None
        msg_conv = cls(**msg.get("content"), metadata=msg.get("metadata"))
        return msg_conv if msg_conv._is_valid() else None

    def _is_valid(self) -> bool:
        return True

    def __eq__(self, other):
        if not isinstance(other, BECMessage):
            # don't attempt to compare against unrelated types
            return False
        return (
            self.content == other.content
            and self.msg_type == other.msg_type
            and self.metadata == other.metadata
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.content, self.metadata}))"

    def __str__(self):
        return f"{self.__class__.__name__}({self.content, self.metadata}))"


class MessageReader(BECMessage):
    def __init__(self, *, msg_type: str, content: dict, metadata: dict = None, **_kwargs) -> None:
        super().__init__(msg_type=msg_type, content=content, metadata=metadata)

    @classmethod
    def _validated_return(cls, msg):
        msg_conv = cls(**msg)
        return msg_conv


class ScanQueueMessage(BECMessage):
    msg_type = "scan"

    def __init__(
        self, *, scan_type: str, parameter: dict, queue="primary", metadata: dict = None
    ) -> None:
        """
        Sent by the API server / user to the scan_queue topic. It will be consumed by the scan server.
        Args:
            scan_type: one of the registered scan types; either scan stubs (set, read, ...) or scans (dscan, ct, ...)
            parameter: required parameters for the given scan_stype
            queue: either "primary" or "interception"
            metadata: additional metadata to describe the scan
        Examples:
            >>> ScanQueueMessage(scan_type="dscan", parameter={"motor1": "samx", "from_m1:": -5, "to_m1": 5, "steps_m1": 10, "motor2": "samy", "from_m2": -5, "to_m2": 5, "steps_m2": 10, "exp_time": 0.1})
        """

        self.content = {"scan_type": scan_type, "parameter": parameter, "queue": queue}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class ScanStatusMessage(BECMessage):
    msg_type = "scan_status"

    def __init__(self, *, scanID: str, status: dict, info: dict, metadata: dict = None) -> None:

        self.content = {"scanID": scanID, "status": status, "info": info}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class ScanQueueModificationMessage(BECMessage):
    msg_type = "scan_queue_modification"
    ACTIONS = ["pause", "deferred_pause", "continue", "abort", "clear"]

    def __init__(self, *, scanID: str, action: str, parameter: dict, metadata: dict = None) -> None:

        self.content = {"scanID": scanID, "action": action, "parameter": parameter}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)

    def _is_valid(self) -> bool:
        if not self.content.get("action") in self.ACTIONS:
            return False
        return True


class ScanQueueStatusMessage(BECMessage):
    msg_type = "scan_queue_status"

    def __init__(self, *, queue: dict, metadata: dict = None) -> None:

        self.content = {"queue": queue}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)

    def _is_valid(self) -> bool:
        if (
            not isinstance(self.content["queue"], dict)
            or not "primary" in self.content["queue"]
            or not isinstance(self.content["queue"]["primary"], dict)
        ):
            return False
        return True


class RequestResponseMessage(BECMessage):
    msg_type = "request_response"

    def __init__(self, *, decision: str, message: str, metadata: dict = None) -> None:
        """
        Message type for sending back decisions on the acceptance of requests.
        Args:
            decision: String describing the decision, e.g. accepted, rejected, queued etc.
            message: String describing the decision, e.g. "Invalid request"
            metadata: additional metadata to describe and identify the request / response
        """

        self.content = {"decision": decision, "message": message}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class DeviceInstructionMessage(BECMessage):
    msg_type = "device_instruction"

    def __init__(self, *, device: str, action: str, parameter: dict, metadata: dict = None) -> None:
        """

        Args:
            device:
            action:
            parameter:
        """
        self.content = {"device": device, "action": action, "parameter": parameter}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class DeviceMessage(BECMessage):
    msg_type = "device_message"

    def __init__(self, *, signals: dict, metadata: dict = None) -> None:
        """

        Args:
            signals:
            metadata:
        """
        self.content = {"signals": signals}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)

    def _is_valid(self) -> bool:
        if not isinstance(self.content["signals"], dict):
            return False
        return True


class DeviceRPCMessage(BECMessage):
    msg_type = "device_rpc_message"

    def __init__(
        self, *, device: str, return_val: Any, out: str, success: bool = True, metadata: dict = None
    ) -> None:
        """

        Args:
            signals:
            metadata:
        """
        self.content = {"device": device, "return_val": return_val, "out": out, "success": success}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)

    def _is_valid(self) -> bool:
        if not isinstance(self.content["device"], str):
            return False
        return True


class DeviceStatusMessage(BECMessage):
    msg_type = "device_status_message"

    def __init__(self, *, device: str, status: int, metadata: dict = None) -> None:
        """

        Args:
            signals:
            metadata:
        """
        self.content = {"device": device, "status": status}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class DeviceInfoMessage(BECMessage):
    msg_type = "device_info_message"

    def __init__(self, *, device: str, info: dict, metadata: dict = None) -> None:
        """

        Args:
            device:
            info:
            metadata:
        """
        self.content = {"device": device, "info": info}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class ScanMessage(BECMessage):
    msg_type = "scan_message"

    def __init__(self, *, point_id: int, scanID: int, data: dict, metadata: dict = None) -> None:
        """

        Args:
            point_id:
            scanID:
            data:
        """
        self.content = {"point_id": point_id, "scanID": scanID, "data": data}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class DeviceConfigMessage(BECMessage):
    msg_type = "device_config_message"

    def __init__(self, *, action: str, config: dict, metadata: dict = None) -> None:
        """

        Args:
            action: post or patch
            config:
        """
        self.content = {"action": action, "config": config}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class LogMessage(BECMessage):
    msg_type = "log_message"

    def __init__(self, *, log_type: str, content: Union[dict, str], metadata: dict = None) -> None:
        """

        Args:
            type: log, warning or error
            content: log's content
        """
        self.content = {"log_type": log_type, "content": content}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class AlarmMessage(BECMessage):
    msg_type = "alarm_message"

    def __init__(
        self, *, severity: int, alarm_type=str, source: str, content: dict, metadata: dict = None
    ) -> None:
        """Alarm message
        Severity 1: Minor alarm, no user interaction needed. The system can continue.
        Severity 2: Major alarm, user interaction needed. If the alarm was raised during the execution of a request, the request will be paused until the alarm is resolved.
        Severity 3: Major alarm, user interaction needed. The system cannot recover by itself.

        Args:
            severity (int): severity level (1-3)
            source (str): source of the problem (where did it occur?)
            content (dict): problem description (what happened?)
            metadata (dict, optional)
        """
        self.content = {
            "severity": severity,
            "alarm_type": alarm_type,
            "source": source,
            "content": content,
        }
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)


class StatusMessage(BECMessage):
    msg_type = "status_message"

    def __init__(self, *, status: becStatus, metadata: dict = None) -> None:
        """

        Args:
            status: error, off, idle or running
            metadata: status metadata
        """
        self.content = {"status": status.value}
        super().__init__(msg_type=self.msg_type, content=self.content, metadata=metadata)
