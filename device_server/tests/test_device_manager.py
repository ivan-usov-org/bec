import os

import bec_utils
import yaml
from bec_utils.tests.utils import ConnectorMock
from device_server.devices.devicemanager import DeviceManagerDS

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_utils.__file__)


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
