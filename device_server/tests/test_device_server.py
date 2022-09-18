import pytest
from bec_utils.tests.utils import ConnectorMock
from device_server import DeviceServer

from test_device_manager import load_device_manager


def load_DeviceServerMock():
    connector = ConnectorMock("")
    device_manager = load_device_manager()
    return DeviceServerMock(device_manager, connector)


class DeviceServerMock(DeviceServer):
    def __init__(self, device_manager, connector_cls) -> None:
        super().__init__(bootstrap_server="dummy", connector_cls=ConnectorMock, scibec_url="dummy")
        self.device_manager = device_manager

    def _start_device_manager(self):
        pass


def test_connect_device():
    device_server = load_DeviceServerMock()
