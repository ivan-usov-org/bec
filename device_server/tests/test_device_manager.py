import os

import bec_utils
import pytest
import yaml
from bec_utils.tests.utils import ConnectorMock
from device_server.devices.devicemanager import DeviceManagerDS

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_utils.__file__)


class ControllerMock:
    def __init__(self, parent) -> None:
        self.parent = parent

    def on(self):
        self.parent._connected = True

    def off(self):
        self.parent._connected = False


class DeviceMock:
    def __init__(self) -> None:
        self._connected = False
        self.name = "name"

    @property
    def connected(self):
        return self._connected


class DeviceControllerMock(DeviceMock):
    def __init__(self) -> None:
        super().__init__()
        self.controller = ControllerMock(self)


class EpicsDeviceMock(DeviceMock):
    def wait_for_connection(self, timeout):
        self._connected = True


def load_device_manager():
    connector = ConnectorMock("")
    device_manager = DeviceManagerDS(connector, "")
    device_manager.producer = connector.producer()
    with open(f"{dir_path}/tests/test_session.yaml", "r") as session_file:
        device_manager._session = yaml.safe_load(session_file)
    device_manager._load_session()
    return device_manager


def test_device_init():
    device_manager = load_device_manager()
    for dev in device_manager.devices.values():
        if not dev.enabled:
            continue
        assert dev.initialized is True


@pytest.mark.parametrize(
    "obj,raises_error",
    [(DeviceMock(), True), (DeviceControllerMock(), False), (EpicsDeviceMock(), False)],
)
def test_conntect_device(obj, raises_error):
    device_manager = load_device_manager()
    if raises_error:
        with pytest.raises(ConnectionError):
            device_manager.connect_device(obj)
        return
    device_manager.connect_device(obj)
