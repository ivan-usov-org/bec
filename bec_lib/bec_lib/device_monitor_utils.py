from typing import TYPE_CHECKING

from bec_lib.endpoints import MessageEndpoints
from bec_lib.serialization import MsgpackSerialization


def get_monitor_images(device_name: str, count: int) -> list:
    """
    Load the last <count> entries of the device data monitor stream.
    This function is meant to be used from within BEC. Outside of BEC,
    bec.connector needs to be changed to a RedisConnector instance.

    Args:
        device_name (str): name of the device
        count (int): number of images to retrieve

    Returns:
        list: List of numpy arrays
    """
    # pylint: disable=import-outside-toplevel
    im = bec.connector.get_last(MessageEndpoints.device_monitor(device_name), count=count)
    im = [sub_img["data"].data for sub_img in im]
    return im
