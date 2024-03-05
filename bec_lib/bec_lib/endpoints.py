"""
Endpoints for communication within the BEC.
"""

# pylint: disable=too-many-public-methods
import enum
from dataclasses import dataclass

from bec_lib import messages


class MessageOp(list[str], enum.Enum):
    """Message operation enum"""

    SET_PUBLISH = ["register", "set_and_publish", "delete", "get", "keys"]
    SEND = ["send", "register"]
    STREAM = ["xadd", "xrange", "xread", "register_stream", "keys"]
    LIST = ["lpush", "lrange", "rpush", "ltrim", "keys"]
    SET = ["set", "get", "delete", "keys"]


@dataclass
class EndpointInfo:
    """
    Dataclass for endpoint info.

    Args:
        endpoint (str): Endpoint.
        message_type (messages.BECMessage): Message type.
        message_op (MessageOp): Message operation.
    """

    endpoint: str
    message_type: messages.BECMessage
    message_op: MessageOp


class MessageEndpoints:
    """
    Class for message endpoints.
    """

    # devices feedback
    @staticmethod
    def device_status(device: str) -> EndpointInfo:
        """
        Endpoint for device status. This endpoint is used by the device server to publish
        the device status using a messages.DeviceStatusMessage message.

        Args:
            device (str): Device name, e.g. "samx".
        """
        endpoint = f"internal/devices/status/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceStatusMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def device_read(device: str) -> EndpointInfo:
        """
        Endpoint for device readings. This endpoint is used by the device server to publish
        the device readings using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device readings of the specified device.
        """
        endpoint = f"internal/devices/read/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def device_read_configuration(device: str) -> EndpointInfo:
        """
        Endpoint for device configuration readings. This endpoint is used by the device server
        to publish the device configuration readings using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device configuration readings of the specified device.
        """
        endpoint = f"internal/devices/read_configuration/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def device_readback(device: str) -> EndpointInfo:
        """
        Endpoint for device readbacks. This endpoint is used by the device server to publish
        the device readbacks using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device readbacks of the specified device.
        """
        endpoint = f"internal/devices/readback/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def device_limits(device: str) -> EndpointInfo:
        """
        Endpoint for device limits. This endpoint is used by the device server to publish
        the device limits using a messages.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device limits of the specified device.
        """
        endpoint = f"internal/devices/limits/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def device_req_status(device: str) -> EndpointInfo:
        """
        Endpoint for device request status. This endpoint is used by the device server to publish
        the device request status using a messages.DeviceReqStatusMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device request status of the specified device.
        """
        endpoint = f"internal/devices/req_status/{device}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.DeviceReqStatusMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def device_req_status_container(RID: str) -> EndpointInfo:
        """
        Endpoint for device request status container. This endpoint is used by the device server to publish
        the device request status using a messages.DeviceReqStatusMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            EndpointInfo: Endpoint for device request status container.
        """
        endpoint = f"internal/devices/req_status_container/{RID}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.DeviceReqStatusMessage,
            message_op=MessageOp.LIST,
        )

    @staticmethod
    def device_progress(device: str) -> EndpointInfo:
        """
        Endpoint for device progress. This endpoint is used by the device server to publish
        the device progress using a messages.ProgressMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device progress of the specified device.
        """
        endpoint = f"internal/devices/progress/{device}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ProgressMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    # device config
    @staticmethod
    def device_config_request() -> EndpointInfo:
        """
        Endpoint for device config request. This endpoint can be used to
        request a modification to the device config. The request is sent using
        a messages.DeviceConfigMessage message.

        Returns:
            EndpointInfo: Endpoint for device config request.
        """
        endpoint = "internal/devices/config_request"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceConfigMessage, message_op=MessageOp.SEND
        )

    @staticmethod
    def device_config_request_response(RID: str) -> EndpointInfo:
        """
        Endpoint for device config request response. This endpoint is used by the
        device server and scihub connector to inform about whether the device config
        request was accepted or rejected. The response is sent using a
        messages.RequestResponseMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            EndpointInfo: Endpoint for device config request response.
        """
        endpoint = f"internal/devices/config_request_response/{RID}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.RequestResponseMessage,
            message_op=MessageOp.SET,
        )

    @staticmethod
    def device_server_config_request() -> EndpointInfo:
        """
        Endpoint for device server config request. This endpoint can be used to
        request changes to config. Typically used by the scihub connector following a
        device config request and validate a new configuration with the device server.
        The request is sent using a messages.DeviceConfigMessage message.

        Returns:
            EndpointInfo: Endpoint for device server config request.
        """
        endpoint = "internal/devices/device_server_config_update"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceConfigMessage, message_op=MessageOp.SEND
        )

    @staticmethod
    def device_config_update() -> EndpointInfo:
        """
        Endpoint for device config update. This endpoint is used by the scihub connector
        to inform about a change to the device config. The update is sent using a
        messages.DeviceConfigMessage message.

        Returns:
            EndpointInfo: Endpoint for device config update.

        """
        endpoint = "internal/devices/config_update"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceConfigMessage, message_op=MessageOp.SEND
        )

    @staticmethod
    def device_config() -> EndpointInfo:
        """
        Endpoint for device config. This endpoint is used by the scihub connector
        to set the device config.

        Returns:
            EndpointInfo: Endpoint for device config.
        """
        endpoint = "internal/devices/config"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceConfigMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def device_config_history() -> EndpointInfo:
        """
        Endpoint for device config history. This endpoint is used to keep track of the
        device config history using a messages.AvailableResourceMessage message. The endpoint is
        connected to a redis list.

        Returns:
            EndpointInfo: Endpoint for device config history.
        """
        endpoint = "internal/devices/config_history"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.AvailableResourceMessage,
            message_op=MessageOp.LIST,
        )

    @staticmethod
    def device_info(device: str) -> EndpointInfo:
        """
        Endpoint for device info. This endpoint is used by the device server to publish
        the device info using a messages.DeviceInfoMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for device info of the specified device.
        """
        endpoint = f"internal/devices/info/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceInfoMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def device_staged(device: str) -> EndpointInfo:
        """
        Endpoint for the device stage status. This endpoint is used by the device server
        to publish the device stage status using a messages.DeviceStatusMessage message.
        A device is staged when it is ready to be used in a scan. A DeviceStatus of 1 means
        that the device is staged, 0 means that the device is not staged.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            EndpointInfo: Endpoint for the device stage status of the specified device.
        """
        endpoint = f"internal/devices/staged/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceStatusMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def device_async_readback(scanID: str, device: str) -> EndpointInfo:
        """
        Endpoint for receiving an async device readback over Redis streams.
        This endpoint is used by the device server to publish async device
        readbacks using a messages.DeviceMessage. In addition tp scan metadata,
        the message metadata contains information on how to concatenate multiple readings.
        Further keyword arguments for GUI handling might be attached.

        Args:
            scanID (str): unique scan identifier
            device (str): Device name, e.g. "mcs".

        Returns:
            EndpointInfo: Endpoint for device async readback of the specified device.
        """
        endpoint = f"internal/devices/async_readback/{scanID}/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceMessage, message_op=MessageOp.STREAM
        )

    @staticmethod
    def device_monitor(device: str) -> EndpointInfo:
        """
        Endpoint for device monitoring.
        This endpoint is used to publish image or wavefrom data from a monitor. An
        example can be a 2D area dertector or a 1D waveform (XRF), for which we
        forward a subset from the data to the monitoring endpoing for visualization
        purposes. Details on shape and type of data need to be specified in
        dtype/dshape of the dev.<device>.describe() method.

        Args:
            device (str): Device name, e.g. "eiger".

        Returns:
            EndpointInfo: Endpoint for device monitoring.
        """
        endpoint = f"internal/devices/monitor/{device}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceMessage, message_op=MessageOp.STREAM
        )

    # scan queue
    @staticmethod
    def scan_queue_modification() -> EndpointInfo:
        """
        Endpoint for scan queue modification. This endpoint is used to publish accepted
        scan queue modifications using a messages.ScanQueueModificationMessage message.

        Returns:
            EndpointInfo: Endpoint for scan queue modification.
        """
        endpoint = "internal/queue/queue_modification"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ScanQueueModificationMessage,
            message_op=MessageOp.SEND,
        )

    @staticmethod
    def scan_queue_modification_request() -> EndpointInfo:
        """
        Endpoint for scan queue modification request. This endpoint is used to request
        a scan queue modification using a messages.ScanQueueModificationMessage message.
        If accepted, the modification is published using the scan_queue_modification
        endpoint.

        Returns:
            EndpointInfo: Endpoint for scan queue modification request.
        """
        endpoint = "internal/queue/queue_modification_request"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ScanQueueModificationMessage,
            message_op=MessageOp.SEND,
        )

    @staticmethod
    def scan_queue_insert() -> EndpointInfo:
        """
        Endpoint for scan queue inserts. This endpoint is used to publish accepted
        scans using a messages.ScanQueueMessage message.
        The message will be picked up by the scan queue manager and inserted into the
        scan queue.

        Returns:
            EndpointInfo: Endpoint for scan queue inserts.
        """
        endpoint = "internal/queue/queue_insert"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ScanQueueMessage, message_op=MessageOp.SEND
        )

    @staticmethod
    def scan_queue_request() -> EndpointInfo:
        """
        Endpoint for scan queue request. This endpoint is used to request the new scans.
        The request is sent using a messages.ScanQueueMessage message.

        Returns:
            EndpointInfo: Endpoint for scan queue request.
        """
        endpoint = "internal/queue/queue_request"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ScanQueueMessage, message_op=MessageOp.SEND
        )

    @staticmethod
    def scan_queue_request_response() -> EndpointInfo:
        """
        Endpoint for scan queue request response. This endpoint is used to publish the
        information on whether the scan request was accepted or rejected. The response
        is sent using a messages.RequestResponseMessage message.

        Returns:
            EndpointInfo: Endpoint for scan queue request response.

        """
        endpoint = "internal/queue/queue_request_response"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.RequestResponseMessage,
            message_op=MessageOp.SEND,
        )

    @staticmethod
    def scan_queue_status() -> EndpointInfo:
        """
        Endpoint for scan queue status. This endpoint is used to publish the scan queue
        status using a messages.ScanQueueStatusMessage message.

        Returns:
            EndpointInfo: Endpoint for scan queue status.
        """
        endpoint = "internal/queue/queue_status"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ScanQueueStatusMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def scan_queue_history() -> EndpointInfo:
        """
        Endpoint for scan queue history. This endpoint is used to keep track of the
        scan queue history using a messages.ScanQueueHistoryMessage message. The endpoint is
        connected to a redis list.

        Returns:
            EndpointInfo: Endpoint for scan queue history.
        """
        endpoint = "internal/queue/queue_history"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ScanQueueHistoryMessage,
            message_op=MessageOp.LIST,
        )

    # scan info
    @staticmethod
    def scan_number() -> EndpointInfo:
        """
        Endpoint for scan number. This endpoint is used to publish the scan number. The
        scan number is incremented after each scan and set in redis as an integer.

        Returns:
            str: Endpoint for scan number.
        """
        endpoint = "scans/scan_number"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.VariableMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def dataset_number() -> EndpointInfo:
        """
        Endpoint for dataset number. This endpoint is used to publish the dataset number.
        The dataset number is incremented after each dataset and set in redis as an integer.

        Returns:
            str: Endpoint for dataset number.
        """
        endpoint = "scans/dataset_number"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.VariableMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def scan_status() -> EndpointInfo:
        """
        Endpoint for scan status. This endpoint is used to publish the scan status using
        a messages.ScanStatusMessage message.

        Returns:
            EndpointInfo: Endpoint for scan status.
        """
        endpoint = "scans/scan_status"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ScanStatusMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def available_scans() -> EndpointInfo:
        """
        Endpoint for available scans. This endpoint is used to publish the available scans
        using an AvailableResourceMessage.

        Returns:
            EndpointInfo: Endpoint for available scans.
        """
        endpoint = "scans/available_scans"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.AvailableResourceMessage,
            message_op=MessageOp.SET,
        )

    @staticmethod
    def bluesky_events() -> str:
        """
        Endpoint for bluesky events. This endpoint is used by the scan bundler to
        publish the bluesky events using a direct msgpack dump of the bluesky event.

        Returns:
            str: Endpoint for bluesky events.
        """
        return "scans/bluesky-events"

    @staticmethod
    def scan_segment() -> EndpointInfo:
        """
        Endpoint for scan segment. This endpoint is used by the scan bundler to publish
        the scan segment using a messages.ScanMessage message.

        Returns:
            str: Endpoint for scan segments.
        """
        endpoint = "scans/scan_segment"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ScanMessage, message_op=MessageOp.SEND
        )

    @staticmethod
    def scan_baseline() -> EndpointInfo:
        """
        Endpoint for scan baseline readings. This endpoint is used by the scan bundler to
        publish the scan baseline readings using a messages.ScanBaselineMessage message.

        Returns:
            str: Endpoint for scan baseline readings.
        """
        endpoint = "scans/scan_baseline"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ScanBaselineMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    # instructions
    @staticmethod
    def device_instructions() -> EndpointInfo:
        """
        Endpoint for device instructions. This endpoint is used by the scan server to
        publish the device instructions using a messages.DeviceInstructionMessage message.
        The device instructions are used to instruct the device server to perform
        certain actions, e.g. to move a motor.

        Returns:
            str: Endpoint for device instructions.
        """
        endpoint = "internal/devices/instructions"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.DeviceInstructionMessage,
            message_op=MessageOp.SEND,
        )

    @staticmethod
    def device_rpc(rpc_id: str) -> EndpointInfo:
        """
        Endpoint for device rpc. This endpoint is used by the device server to publish
        the result of a device rpc using a messages.DeviceRPCMessage message.

        Args:
            rpc_id (str): RPC ID.

        Returns:
            str: Endpoint for device rpc.
        """
        endpoint = f"internal/devices/rpc/{rpc_id}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.DeviceRPCMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def pre_scan_macros() -> str:
        """
        Endpoint for pre scan macros. This endpoint is used to keep track of the pre scan
        macros. The endpoint is connected to a redis list.

        Returns:
            str: Endpoint for pre scan macros.
        """
        return "internal/pre_scan_macros"

    @staticmethod
    def post_scan_macros() -> str:
        """
        Endpoint for post scan macros. This endpoint is used to keep track of the post scan
        macros. The endpoint is connected to a redis list.

        Returns:
            str: Endpoint for post scan macros.
        """
        return "internal/post_scan_macros"

    @staticmethod
    def public_scan_info(scanID: str) -> EndpointInfo:
        """
        Endpoint for scan info. This endpoint is used by the scan worker to publish the
        scan info using a messages.ScanStatusMessage message. In contrast to the scan_info endpoint,
        this endpoint is specific to a scan and has a retentioni time of 30 minutes.

        Args:
            scanID (str): Scan ID.

        Returns:
            str: Endpoint for scan info.

        """
        endpoint = f"public/{scanID}/scan_info"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ScanStatusMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def public_scan_segment(scanID: str, pointID: int) -> EndpointInfo:
        """
        Endpoint for public scan segments. This endpoint is used by the scan bundler to
        publish the scan segment using a messages.ScanMessage message. In contrast to the
        scan_segment endpoint, this endpoint is specific to a scan and has a retention time
        of 30 minutes.

        Args:
            scanID (str): Scan ID.
            pointID (int): Point ID to specify a single point in a scan.

        Returns:
            str: Endpoint for scan segments.

        """
        endpoint = f"public/{scanID}/scan_segment/{pointID}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ScanMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def public_scan_baseline(scanID: str) -> EndpointInfo:
        """
        Endpoint for public scan baseline readings. This endpoint is used by the scan bundler
        to publish the scan baseline readings using a messages.ScanBaselineMessage message.
        In contrast to the scan_baseline endpoint, this endpoint is specific to a scan and has
        a retention time of 30 minutes.

        Args:
            scanID (str): Scan ID.

        Returns:
            str: Endpoint for scan baseline readings.
        """
        endpoint = f"public/{scanID}/scan_baseline"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ScanBaselineMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def public_file(scanID: str, name: str) -> EndpointInfo:
        """
        Endpoint for public file. This endpoint is used by the file writer to publish the
        status of the file writing using a messages.FileMessage message.

        Args:
            scanID (str): Scan ID.
            name (str): File name.

        Returns:
            str: Endpoint for public files.
        """
        endpoint = f"public/{scanID}/file/{name}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.FileMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def file_event(name: str) -> EndpointInfo:
        """
        Endpoint for public file_event. This endpoint is used by the file writer to publish the
        status of the file writing using a messages.FileMessage message.

        Args:
            name (str): File name.

        Returns:
            str: Endpoint for public file_events.
        """
        endpoint = f"public/file_event/{name}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.FileMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def file_content() -> EndpointInfo:
        """
        Endpoint for file content. This endpoint is used by the file writer to publish the
        file content using a messages.FileContentMessage message.

        Returns:
            str: Endpoint for file content.
        """
        endpoint = "internal/file_content"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.FileContentMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    # log
    @staticmethod
    def log() -> EndpointInfo:
        """
        Endpoint for log. This endpoint is used by the redis connector to publish logs using
        a messages.LogMessage message.

        Returns:
            str: Endpoint for log.
        """
        endpoint = "internal/log"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.LogMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def alarm() -> EndpointInfo:
        """
        Endpoint for alarms. This endpoint is used by the redis connector to publish alarms
        using a messages.AlarmMessage message.

        Returns:
            str: Endpoint for alarms.
        """
        endpoint = "internal/alarms"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.AlarmMessage, message_op=MessageOp.SET_PUBLISH
        )

    # service
    @staticmethod
    def service_status(service_id: str) -> EndpointInfo:
        """
        Endpoint for service status. This endpoint is used by all BEC services to publish
        their status using a messages.StatusMessage message.
        The status message also contains the service info such as user, host, etc.

        Args:
            service_id (str): Service ID, typically a uuid4 string.
        """
        endpoint = f"internal/services/status/{service_id}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.StatusMessage, message_op=MessageOp.SET_PUBLISH
        )

    @staticmethod
    def metrics(service_id: str) -> EndpointInfo:
        """
        Endpoint for metrics. This endpoint is used by all BEC services to publish their
        performance metrics using a messages.ServiceMetricMessage message.

        Args:
            service_id (str): Service ID, typically a uuid4 string.

        Returns:
            str: Endpoint for metrics.
        """
        endpoint = f"internal/services/metrics/{service_id}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ServiceMetricMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def service_response(RID: str) -> EndpointInfo:
        """
        Endpoint for service response. This endpoint is used by all BEC services to publish
        the result of a service request using a messages.ServiceResponseMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for service response.
        """
        endpoint = f"internal/services/response/{RID}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ServiceResponseMessage,
            message_op=MessageOp.LIST,
        )

    # misc
    @staticmethod
    def global_vars(var_name: str) -> EndpointInfo:
        """
        Endpoint for global variables. This endpoint is used to publish global variables
        using a messages.VariableMessage message.

        Args:
            var_name (str): Variable name.

        Returns:
            str: Endpoint for global variables.
        """
        endpoint = f"public/vars/{var_name}"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.VariableMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def observer() -> EndpointInfo:
        """
        Endpoint for observer. This endpoint is used to keep track of observer states using a.
        messages.ObserverMessage message. This endpoint is currently not used.

        Returns:
            str: Endpoint for observer.
        """
        endpoint = "internal/observer"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.ObserverMessage, message_op=MessageOp.SET
        )

    @staticmethod
    def progress(var_name) -> EndpointInfo:
        """
        Endpoint for progress. This endpoint is used to publish the current progress
        using a messages.ProgressMessage message.

        Args:
            var_name (str): Variable name.

        Returns:
            str: Endpoint for progress.
        """
        endpoint = f"public/progress/{var_name}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ProgressMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    # logbook
    @staticmethod
    def logbook() -> EndpointInfo:
        """
        Endpoint for logbook. This endpoint is used to publish logbook info such as
        url, user and token using a direct msgpack dump of a dictionary.

        Returns:
            str: Endpoint for logbook.
        """
        endpoint = "internal/logbook"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.CredentialsMessage, message_op=MessageOp.SET
        )

    # scibec
    @staticmethod
    def scibec() -> EndpointInfo:
        """
        Endpoint for scibec. This endpoint is used to publish scibec info such as
        url, user and token using a CredentialsMessage.

        Returns:
            str: Endpoint for scibec.
        """
        endpoint = "internal/scibec"
        return EndpointInfo(
            endpoint=endpoint, message_type=messages.CredentialsMessage, message_op=MessageOp.SET
        )

    # experiment
    @staticmethod
    def account() -> str:
        """
        Endpoint for account. This endpoint is used to publish the current account.
        The value is set directly as a string.
        """
        return "internal/account"

    # data processing
    @staticmethod
    def processed_data(process_id: str) -> EndpointInfo:
        """
        Endpoint for processed data. This endpoint is used to publish new processed data
        streams using a messages.ProcessedDataMessage message.

        Args:
            process_id (str): Process ID, typically a uuid4 string.

        Returns:
            str: Endpoint for processed data.
        """
        endpoint = f"public/processed_data/{process_id}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.ProcessedDataMessage,
            message_op=MessageOp.STREAM,
        )

    @staticmethod
    def dap_config() -> EndpointInfo:
        """
        Endpoint for DAP configuration. This endpoint is used to publish the DAP configuration
        using a messages.DAPConfigMessage message.

        Returns:
            str: Endpoint for DAP configuration.
        """
        endpoint = "internal/dap/config"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.DAPConfigMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def dap_available_plugins(plugin_id: str) -> EndpointInfo:
        """
        Endpoint for available DAP plugins. This endpoint is used to publish the available DAP
        plugins using a messages.AvailableResourceMessage message.

        Args:
            plugin_id (str): Plugin ID.

        Returns:
            str: Endpoint for available DAP plugins.
        """
        endpoint = f"internal/dap/available_plugins/{plugin_id}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.AvailableResourceMessage,
            message_op=MessageOp.SET,
        )

    @staticmethod
    def dap_request() -> EndpointInfo:
        """
        Endpoint for DAP request. This endpoint is used to request a DAP using a
        messages.DAPRequestMessage message.

        Returns:
            str: Endpoint for DAP request.
        """
        endpoint = "internal/dap/request"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.DAPRequestMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def dap_response(RID: str) -> EndpointInfo:
        """
        Endpoint for DAP response. This endpoint is used to publish the DAP response using a
        messages.DAPResponseMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for DAP response.
        """
        endpoint = f"internal/dap/response/{RID}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.DAPResponseMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    # GUI
    @staticmethod
    def gui_config(gui_id: str) -> EndpointInfo:
        """
        Endpoint for GUI configuration. This endpoint is used to publish the GUI configuration
        using a messages.GUIConfigMessage message.

        Returns:
            str: Endpoint for GUI configuration.
        """
        endpoint = f"public/gui/config/{gui_id}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.GUIConfigMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def gui_data(gui_id: str) -> EndpointInfo:
        """
        Endpoint for GUI data. This endpoint is used to publish the GUI data using a
        messages.GUIDataMessage message.

        Returns:
            str: Endpoint for GUI data.
        """
        endpoint = f"public/gui/data/{gui_id}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.GUIDataMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def gui_instructions(gui_id: str) -> EndpointInfo:
        """
        Endpoint for GUI instructions. This endpoint is used to publish the GUI instructions
        using a messages.GUIInstructionMessage message.

        Returns:
            str: Endpoint for GUI instructions.
        """
        endpoint = f"public/gui/instruction/{gui_id}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.GUIInstructionMessage,
            message_op=MessageOp.SET_PUBLISH,
        )

    @staticmethod
    def gui_instruction_response(RID: str) -> EndpointInfo:
        """
        Endpoint for GUI instruction response. This endpoint is used to publish the GUI instruction response
        using a messages.RequestResponseMessage message.

        Returns:
            str: Endpoint for GUI instruction response.
        """
        endpoint = f"public/gui/instruction_response/{RID}"
        return EndpointInfo(
            endpoint=endpoint,
            message_type=messages.RequestResponseMessage,
            message_op=MessageOp.SET_PUBLISH,
        )
