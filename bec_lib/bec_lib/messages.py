import enum
import time
import warnings
from copy import deepcopy
from typing import Any, ClassVar, Literal

import numpy as np
from pydantic import BaseModel, Field, field_validator, model_validator


class BECStatus(enum.Enum):
    """BEC status enum"""

    RUNNING = 2
    BUSY = 1
    IDLE = 0
    ERROR = -1


class BECMessage(BaseModel):
    msg_type: ClassVar[str]
    metadata: dict | None = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def check_metadata(cls, v):
        if v is None:
            return {}
        return v

    @property
    def content(self):
        content = self.__dict__.copy()  # dataclasses.asdict(self)
        content.pop("metadata", None)
        return content

    def __eq__(self, other):
        if not isinstance(other, BECMessage):
            # don't attempt to compare against unrelated types
            return False

        try:
            np.testing.assert_equal(self.model_dump(), other.model_dump())
        except AssertionError:
            return False

        return self.msg_type == other.msg_type and self.metadata == other.metadata

    def loads(self):
        warnings.warn(
            "BECMessage.loads() is deprecated and should not be used anymore. When calling Connector methods, it can be omitted. When a message needs to be deserialized call the appropriate function from bec_lib.serialization",
            FutureWarning,
        )
        return self

    def dumps(self):
        warnings.warn(
            "BECMessage.dumps() is deprecated and should not be used anymore. When calling Connector methods, it can be omitted. When a message needs to be serialized call the appropriate function from bec_lib.serialization",
            FutureWarning,
        )
        return self


class BundleMessage(BECMessage):
    """Bundle of BECMessages"""

    msg_type: ClassVar[str] = "bundle_message"
    messages: list = Field(default_factory=list[BECMessage])

    def append(self, msg: BECMessage):
        """append a new BECMessage to the bundle"""
        if not isinstance(msg, BECMessage):
            raise AttributeError(f"Cannot append message of type {msg.__class__.__name__}")
        self.messages.append(msg)

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        yield from self.messages


class ScanQueueMessage(BECMessage):
    """Message type for sending scan requests to the scan queue
    Sent by the API server / user to the scan_queue topic. It will be consumed by the scan server.
        Args:
            scan_type (str): one of the registered scan types; either rpc calls or scan types defined in the scan server
            parameter (dict): required parameters for the given scan_stype
            queue (str): either "primary" or "interception"
            metadata (dict, optional): additional metadata to describe the scan
        Examples:
            >>> ScanQueueMessage(scan_type="dscan", parameter={"motor1": "samx", "from_m1:": -5, "to_m1": 5, "steps_m1": 10, "motor2": "samy", "from_m2": -5, "to_m2": 5, "steps_m2": 10, "exp_time": 0.1})
    """

    msg_type: ClassVar[str] = "scan_queue_message"
    scan_type: str
    parameter: dict
    queue: str = Field(default="primary")


class ScanQueueHistoryMessage(BECMessage):
    """Sent after removal from the active queue. Contains information about the scan.
    Sent by the API server / user to the scan_queue topic. It will be consumed by the scan server.
    Args:
        status(str):  current scan status
        queue_id(str): unique queue ID
        info(dict): dictionary containing additional information about the scan
        queue (str): either "primary" or "interception"
        metadata (dict, optional): additional metadata to describe the scan
    """

    msg_type: ClassVar[str] = "queue_history"
    status: str
    queue_id: str
    info: dict
    queue: str = Field(default="primary")


class ScanStatusMessage(BECMessage):
    """Message type for sending scan status updates
    Args:
        scan_id(str): unique scan ID
        status(str): scan status ("open", "paused", "aborted", "halted", "closed")
        info(dict): dictionary containing additional information about the scan
        timestamp(float, optional): timestamp of the scan status update. If None, the current time is used.
        metadata(dict, optional): additional metadata to describe and identify the scan.

    Examples:
        >>> ScanStatusMessage(scan_id="1234", status="open", info={"positions": {"samx": 0.5, "samy": 0.5}})
    """

    msg_type: ClassVar[str] = "scan_status"
    scan_id: str | None
    status: Literal["open", "paused", "aborted", "halted", "closed"]
    info: dict
    timestamp: float = Field(default_factory=time.time)

    def __str__(self):
        content = deepcopy(self.__dict__)
        if content["info"].get("positions"):
            content["info"]["positions"] = "..."
        return f"{self.__class__.__name__}({content, self.metadata}))"


class ScanQueueModificationMessage(BECMessage):
    """Message type for sending scan queue modifications
    Args:
        scan_id(str): unique scan ID
        action(str): one of the actions defined in ACTIONS
                     ("pause", "deferred_pause", "continue", "abort", "clear", "restart", "halt")
        parameter(dict): additional parameters for the action
        metadata(dict, optional): additional metadata to describe and identify the scan.
    """

    ACTIONS: ClassVar[list] = [
        "pause",
        "deferred_pause",
        "continue",
        "abort",
        "clear",
        "restart",
        "halt",
        "resume",
    ]
    msg_type: ClassVar[str] = "scan_queue_modification"
    scan_id: str | list[str] | None
    action: str
    parameter: dict

    @field_validator("action")
    @classmethod
    def check_action(cls, v):
        """Validate the action"""
        if v not in cls.ACTIONS:
            raise ValueError(f"Invalid action {v}. Must be one of {cls.ACTIONS}")
        return v


class ScanQueueStatusMessage(BECMessage):
    """Message type for sending scan queue status updates
    Args:
        queue(dict): dictionary containing the current queue status
        metadata(dict, optional): additional metadata to describe and identify the scan.
    """

    msg_type: ClassVar[str] = "scan_queue_status"
    queue: dict

    @field_validator("queue")
    @classmethod
    def check_queue(cls, v):
        """Validate the queue"""
        if not isinstance(v, dict):
            raise ValueError(f"Invalid queue {v}. Must be a dictionary")
        if "primary" not in v:
            raise ValueError(f"Invalid queue {v}. Must contain a 'primary' key")
        return v


class RequestResponseMessage(BECMessage):
    """Message type for sending back decisions on the acceptance of requests
    Args:
        accepted (bool): True if the request was accepted
        message (str): String describing the decision, e.g. "Invalid request"
        metadata (dict, optional): additional metadata to describe and identify the request / response
    """

    msg_type: ClassVar[str] = "request_response"
    accepted: bool
    message: str | dict | None = Field(default=None)


class DeviceInstructionMessage(BECMessage):
    """Message type for sending device instructions to the device server
    Args:
        device (str): device name
        action (str): device action, e.g. method call
        parameter (dict): device action parameter
        metadata (dict, optional): metadata to describe the conditions of the device instruction
    """

    msg_type: ClassVar[str] = "device_instruction"
    device: str | list[str] | None
    action: str
    parameter: dict


class DeviceMessage(BECMessage):
    """Message type for sending device readings from the device server
    Args:
        signals (dict): dictionary of device signals
        metadata (dict, optional): metadata to describe the conditions of the device reading
    Examples:
        >>> BECMessage.DeviceMessage(signals={'samx': {'value': 14.999033949016491, 'timestamp': 1686385306.0265112}, 'samx_setpoint': {'value': 15.0, 'timestamp': 1686385306.016806}, 'samx_motor_is_moving': {'value': 0, 'timestamp': 1686385306.026888}}}, metadata={'stream': 'primary', 'DIID': 353, 'RID': 'd3471acc-309d-43b7-8ff8-f986c3fdecf1', 'point_id': 49, 'scan_id': '8e234698-358e-402d-a272-73e168a72f66', 'queue_id': '7a232746-6c90-44f5-81f5-74ab0ea22d4a'})
    """

    msg_type: ClassVar[str] = "device_message"
    signals: dict = Field(default_factory=dict)


class DeviceRPCMessage(BECMessage):
    """Message type for sending device RPC return values from the device server
    Args:
        device (str): device name
        return_val (Any): return value of the RPC call
        out (str): output of the RPC call
        success (bool, optional): True if the RPC call was successful
        metadata (dict, optional): metadata to describe the conditions of the device RPC call
    """

    msg_type: ClassVar[str] = "device_rpc_message"
    device: str
    return_val: Any
    out: str | dict
    success: bool = Field(default=True)


class DeviceStatusMessage(BECMessage):
    """Message type for sending device status updates from the device server
    Args:
        device (str): device name
        status (int): device status
        metadata (dict, optional): additional metadata to describe the conditions of the device status
    """

    msg_type: ClassVar[str] = "device_status_message"
    device: str
    status: int


class DeviceReqStatusMessage(BECMessage):
    """Message type for sending device request status updates from the device server
    Args:
        device (str): device name
        success (bool): True if the request was successful
        metadata (dict, optional): additional metadata to describe the conditions of the device request status
    """

    msg_type: ClassVar[str] = "device_req_status_message"
    device: str
    success: bool


class DeviceInfoMessage(BECMessage):
    """Message type for sending device info updates from the device server
    Args:
        device (str): device name
        info (dict): device info as dictionary
        metadata (dict, optional): additional metadata to describe the conditions of the device info
    """

    msg_type: ClassVar[str] = "device_info_message"
    device: str
    info: dict


class DeviceMonitorMessage(BECMessage):
    """Message type for sending device monitor updates from the device server
    Args:
        device (str): device name
        data (list): dictionary with device monitor data, #TODO should this be a list or better dictionary?
        metadata (dict, optional): additional metadata to describe the conditions of the device monitor
    """

    msg_type: ClassVar[str] = "device_monitor_message"
    device: str
    data: np.ndarray

    class Config:
        arbitrary_types_allowed = True


class ScanMessage(BECMessage):
    """Message type for sending scan segment data from the scan bundler
    Args:
        point_id (int): point ID from scan segment
        scan_id (str): scan ID
        data (dict): scan segment data
        metadata (dict, optional): additional metadata to describe the conditions of the scan segment
    """

    msg_type: ClassVar[str] = "scan_message"
    point_id: int
    scan_id: str
    data: dict


class ScanBaselineMessage(BECMessage):
    """Message type for sending scan baseline data from the scan bundler
    Args:
        scan_id (str): scan ID
        data (dict): scan baseline data
        metadata (dict, optional): additional metadata to describe the conditions of the scan baseline
    """

    msg_type: ClassVar[str] = "scan_baseline_message"
    scan_id: str
    data: dict


class DeviceConfigMessage(BECMessage):
    """Message type for sending device config updates
    Args:
        action (str): set, update or reload
        config (dict): device config (add, set, update) or None (reload)
        metadata (dict, optional): additional metadata to describe the conditions of the device config
    """

    msg_type: ClassVar[str] = "device_config_message"
    action: Literal["add", "set", "update", "reload", "remove"] = Field(
        default=None, validate_default=True
    )
    config: dict | None = Field(default=None)

    @model_validator(mode="after")
    @classmethod
    def check_config(cls, values):
        """Validate the config"""
        if values.action in ["add", "set", "update"] and not values.config:
            raise ValueError(f"Invalid config {values.config}. Must be a dictionary")
        return values


class LogMessage(BECMessage):
    """Log message
    Args:
        log_type (str): log, warning or error
        log_msg (dict or str): log message
        metadata (dict, optional):
    """

    msg_type: ClassVar[str] = "log_message"
    log_type: str
    log_msg: dict | str


class AlarmMessage(BECMessage):
    """Alarm message
    Severity 1: Minor alarm, no user interaction needed. The system can continue.
    Severity 2: Major alarm, user interaction needed. If the alarm was raised during the execution of a request, the request will be paused until the alarm is resolved.
    Severity 3: Major alarm, user interaction needed. The system cannot recover by itself.

    Args:
        severity (int): severity level (1-3)
        source (str): source of the problem (where did it occur?)
        msg (str): problem description (what happened?)
        metadata (dict, optional): Additional metadata.
    """

    msg_type: ClassVar[str] = "alarm_message"
    severity: int
    alarm_type: str
    source: dict
    msg: str


class StatusMessage(BECMessage):
    """Status message
    Args:
        name (str): name of the status
        status (BECStatus): value of the BECStatus enum
        (RUNNING = 2
        BUSY = 1
        IDLE = 0
        ERROR = -1))
        info (dict): status info
        metadata (dict, optional): additional metadata
    """

    msg_type: ClassVar[str] = "status_message"
    name: str
    status: BECStatus
    info: dict


class FileMessage(BECMessage):
    """File message to inform about the status of a file writing operation
    Args:
        file_path (str): path to the file
        done (bool, optional): True if the file writing operation is done. Defaults to True.
        successful (bool, optional): True if the file writing operation was successful. Defaults to True.
        metadata (dict, optional): status metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "file_message"
    file_path: str
    done: bool = Field(default=True)
    successful: bool = Field(default=True)


class FileContentMessage(BECMessage):
    """File content message to inform about the content of a file
    Args:
        file_path (str): path to the file
        data (str): content of the file
        metadata (dict, optional): status metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "file_content_message"
    file_path: str
    data: dict


class VariableMessage(BECMessage):
    """Message to inform about a global variable
    Args:
        value (any): Variable value
        metadata (dict, optional): additional metadata
    """

    msg_type: ClassVar[str] = "var_message"
    value: Any


class ObserverMessage(BECMessage):
    """Message for observer updates
    Args:
        observer (list[dict]): list of observer descriptions (dictionaries)
        metadata (dict, optional): additional metadata
    """

    msg_type: ClassVar[str] = "observer_message"
    observer: list[dict]


class ServiceMetricMessage(BECMessage):
    """Message for service metrics
    Args:
        name (str): name of the service
        metrics (dict): dictionary with service metrics
        metadata (dict, optional): additional metadata
    """

    msg_type: ClassVar[str] = "service_metric_message"
    name: str
    metrics: dict


class ProcessedDataMessage(BECMessage):
    """Message for processed data
    Args:
        data (str): processed data
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "processed_data_message"
    data: dict | list[dict]


class DAPConfigMessage(BECMessage):
    """Message for DAP configuration
    Args:
        config (dict): DAP configuration
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "dap_config_message"
    config: dict


class DAPRequestMessage(BECMessage):
    """Message for DAP requests
    Args:
        dap_cls (str): DAP class name
        dap_type (Literal["continuous", "on_demand"]): DAP type. Either "continuous" or "on_demand"
        config (dict): DAP configuration
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "dap_request_message"
    dap_cls: str
    dap_type: Literal["continuous", "on_demand"]
    config: dict

    @field_validator("dap_type")
    @classmethod
    def check_dap_type(cls, v):
        """Validate the dap_type"""
        if v not in ["continuous", "on_demand"]:
            raise ValueError(f"Invalid dap_type {v}. Must be one of ['continuous', 'on_demand']")
        return v


class DAPResponseMessage(BECMessage):
    """
    Message for DAP responses
    Args:
        success (bool): True if the request was successful
        data (tuple, optional): DAP data (tuple of data and metadata). Defaults to None.
        error (dict, optional): DAP error. Defaults to None.
        dap_request (dict, optional): DAP request. Defaults to None.
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "dap_response_message"
    success: bool
    data: tuple | None = Field(default_factory=lambda: ({}, None))
    error: str | None = None
    dap_request: BECMessage | None = Field(default=None)


class AvailableResourceMessage(BECMessage):
    """Message for available resources such as scans, data processing plugins etc
    Args:
        resource (dict): resource description
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "available_resource_message"
    resource: dict | list[dict]


class ProgressMessage(BECMessage):
    """Message for communicating the progress of a long running task
    Args:
        value (float): current progress value
        max_value (float): maximum progress value
        done (bool): True if the task is done
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "progress_message"
    value: float
    max_value: float
    done: bool


class GUIConfigMessage(BECMessage):
    """Message for GUI configuration
    Args:
        config (dict): GUI configuration
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "gui_config_message"
    config: dict


class GUIDataMessage(BECMessage):
    """Message for GUI data
    Args:
        data (dict): GUI data
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "gui_data_message"
    data: dict


class GUIInstructionMessage(BECMessage):
    """Message for GUI instructions
    Args:
        instruction (str): GUI instruction
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "gui_instruction_message"
    action: str
    parameter: dict


class ServiceResponseMessage(BECMessage):
    """Message for service responses
    Args:
        response (dict): service response
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "service_response_message"
    response: dict


class CredentialsMessage(BECMessage):
    """Message for credentials
    Args:
        credentials (dict): credentials
        metadata (dict, optional): metadata. Defaults to None.
    """

    msg_type: ClassVar[str] = "credentials_message"
    credentials: dict
