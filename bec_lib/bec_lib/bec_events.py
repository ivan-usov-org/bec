""" Module for handling BEC events. The class is attached to BECClient."""

from bec_lib.device import Device
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger

logger = bec_logger.logger


class DeviceMonitorPlugin:

    def __init__(self, connector):
        self._connector = connector

    def get_data(self, device: str | Device, count: int) -> list:
        """Load the last <count> entries of the device data monitor stream.

        Args:
            device_name (str | Device): Device or name of the device
            count (int): number of images to retrieve

        Returns:
            list: List of numpy arrays
        """
        if isinstance(device, Device):
            device = device.name
        msgs = self._connector.get_last(MessageEndpoints.device_monitor(device), count=count)
        if msgs is None:
            logger.warning(f"No data found for device {device}. Returning None.")
            return None
        if not isinstance(msgs, list):
            msgs = [msgs]
        im = [sub_msg["data"].data for sub_msg in msgs]
        return im

    def get_data_for_scan(self, device: str | Device, scan: str | int) -> list:
        """Load all available images from the monitor endpoint for a given scan.

        Args:
            device (str | Device): Device or name of the device
            scan (str | int): scan id as string or scan_number as int

        Returns:
            list: List of numpy arrays
        """
        scan_id = None
        if isinstance(device, Device):
            device = device.name
        msgs = self._connector.xrange(MessageEndpoints.device_monitor(device), min="-", max="+")
        if msgs is None:
            logger.warning(f"No data found for device {device}. Returning None.")
            return None

        if isinstance(scan, int):
            queue_msgs = self._connector.lrange(MessageEndpoints.scan_queue_history(), 0, -1)
            for msg in queue_msgs:
                if msg.content["info"]["scan_number"][0] == scan:
                    scan_id = msg.content["info"]["scan_id"][0]
                    break
            if scan_id is None:
                logger.warning(
                    f"No scan found with scan_number {scan} in queue history. Returning None."
                )
                return None
        elif isinstance(scan, str):
            scan_id = scan
        else:
            raise ValueError(
                f"Value for scan: {scan} must be either scan_number (int) or scan_id (str)"
            )
        im = [
            sub_img["data"].data
            for sub_img in msgs
            if sub_img["data"].metadata.get("scan_id") == scan_id
        ]
        if len(im) == 0:
            logger.warning(
                f"No data found for scan_id: {scan_id} on device {device}. Returning None."
            )
            return None
        return im


class DeviceReadPlugin:

    def __init__(self, connector, endpoint: MessageEndpoints):
        self._connector = connector
        self._endpoint = endpoint

    def get_data(self, device: str | Device) -> tuple[dict]:
        """Get the last readback data for a device.

        Args:
            device_name (str | Device): Device or name of the device

        Returns:
            tuple: Tuple of two dictionaries, one for the last readback data and one for the last readback metadata
        """
        if isinstance(device, Device):
            device = device.name
        msg = self._connector.get(self._endpoint(device))
        if msg is None:
            logger.warning(f"No data found for device {device}. Returning tuple of Nones.")
            return None, None
        return msg.content, msg.metadata


class EndpointReadPlugin:

    def __init__(self, connector, endpoint: MessageEndpoints):
        self._connector = connector
        self._endpoint = endpoint

    def get_data(self) -> tuple[dict]:
        """Get the last message for an endpoint.

        Returns:
            tuple: Tuple of two dictionaries, one for the content of the message and the other for the metadata
        """
        msg = self._connector.get(self._endpoint())
        if msg is None:
            logger.warning(
                f"No data found for endpoint {self._endpoint}. Returning tuple of Nones."
            )
            return None, None
        return msg.content, msg.metadata


class FileEventPlugin:

    def __init__(self, connector):
        self._connector = connector

    def get_file_for_device(self, device: str | Device) -> tuple[dict, dict]:
        """Get the last file event for a device.

        Args:
            device_name (str | Device): Device or name of the device

        Returns:
            dict: Dictionary containing the file event data
        """
        if isinstance(device, Device):
            device = device.name
        msg = self._connector.get(MessageEndpoints.file_event(device))
        if msg is None:
            logger.warning(f"No data found for device {device}. Returning empty dict.")
            return None, None
        return msg.content, msg.metadata

    def get_files_for_scan(self, scan: str | int) -> list[tuple[dict, dict]]:
        """Get all file events for a given scan.

        Args:
            scan (str | int): scan id as string or scan_number as int

        Returns:
            list: List of dictionaries containing the file event data
        """
        scan_id = None
        if isinstance(scan, int):
            queue_msgs = self._connector.lrange(MessageEndpoints.scan_queue_history(), 0, -1)
            for msg in queue_msgs:
                if msg.content["info"]["scan_number"][0] == scan:
                    scan_id = msg.content["info"]["scan_id"][0]
                    break
            if scan_id is None:
                logger.warning(
                    f"No scan found with scan_number {scan} in queue history. Returning empty list."
                )
                return None
        elif isinstance(scan, str):
            scan_id = scan
        else:
            raise ValueError(
                f"Value for scan: {scan} must be either scan_number (int) or scan_id (str)"
            )
        endpoints = self._connector.keys(
            f"{MessageEndpoints.public_file(scan_id=scan_id, name='').endpoint}*"
        )
        if endpoints is None:
            logger.warning(f"No data found for scan {scan_id}. Returning empty list.")
            return None
        msgs = [self._connector.get(endpoint.decode()) for endpoint in endpoints]
        return [(msg.content, msg.metadata) for msg in msgs]


class BECEvents:
    """Class to handle BEC events, attached to BECClient.

    Args:
        parent (BECClient): The parent BECClient instance.
    """

    def __init__(self, parent):
        self._parent = parent
        self.device_monitor = DeviceMonitorPlugin(self._parent.connector)
        self.device_readback = DeviceReadPlugin(
            self._parent.connector, MessageEndpoints.device_readback
        )
        self.device_config_readback = DeviceReadPlugin(
            self._parent.connector, MessageEndpoints.device_read_configuration
        )
        self.device_progress = DeviceReadPlugin(
            self._parent.connector, MessageEndpoints.device_progress
        )
        self.file_event = FileEventPlugin(self._parent.connector)
        self.scan_status = EndpointReadPlugin(self._parent.connector, MessageEndpoints.scan_status)
        self.queue_status = EndpointReadPlugin(
            self._parent.connector, MessageEndpoints.scan_queue_status
        )
        self.pre_scan_macros = EndpointReadPlugin(
            self._parent.connector, MessageEndpoints.pre_scan_macros
        )
