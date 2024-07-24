from bec_lib.device import Device
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger

logger = bec_logger.logger


class DeviceMonitorPlugin:

    def __init__(self, connector):
        self._connector = connector

    def _check_device_avail_for_endpoint(
        self, device_name: str, endpoint: MessageEndpoints
    ) -> bool:
        """Check if the device is available for the given endpoint.

        Args:
            device_name (str): Name of the device
            endpoint (str): Endpoint to check

        Returns:
            bool: True if device is available for the endpoint
        """
        entries = self._connector.keys(f"{endpoint('').endpoint}*")
        avail_devices = [entry.decode().split("/")[-1] for entry in entries]
        return device_name in avail_devices

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
        if not self._check_device_avail_for_endpoint(device, MessageEndpoints.device_monitor_2d):
            logger.warning(
                f"Device {device} not available for endpoint MessageEndpoints.device_monitor_2d. Returning None."
            )
            return None
        msgs = self._connector.get_last(MessageEndpoints.device_monitor_2d(device), count=count)
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
        if not self._check_device_avail_for_endpoint(device, MessageEndpoints.device_monitor_2d):
            logger.warning(
                f"Device {device} not available for endpoint MessageEndpoints.device_monitor_2d. Returning None."
            )
            return None
        msgs = self._connector.xrange(MessageEndpoints.device_monitor_2d(device), min="-", max="+")
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
