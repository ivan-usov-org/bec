import builtins
import os

import bec_utils
import pytest
import yaml
from bec_utils import BECMessage, ServiceConfig
from bec_utils.tests.utils import ConnectorMock, create_session_from_config

from bec_client.bec_client import BECClient
from bec_client.devicemanager_client import DMClient
from bec_client.scans import Scans

dir_path = os.path.dirname(bec_utils.__file__)

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


class ScansMock(Scans):
    def _import_scans(self):
        pass

    def open_scan_def(self):
        pass

    def close_scan_def(self):
        pass

    def close_scan_group(self):
        pass

    def umv(self):
        pass


class ClientMock(BECClient):
    def _load_scans(self):
        self.scans = ScansMock(self)
        builtins.scans = self.scans

    def start(self):
        self._start_scan_queue()
        self._start_alarm_handler()


class DMClientMock(DMClient):
    def _get_device_info(self, device_name) -> BECMessage.DeviceInfoMessage:
        session_info = self.get_device(device_name)
        device_base_class = (
            "positioner"
            if session_info["acquisitionConfig"]["acquisitionGroup"] in ["motor"]
            else "signal"
        )
        if device_base_class == "positioner":
            signals = [
                "readback",
                "setpoint",
                "motor_is_moving",
                "velocity",
                "acceleration",
                "high_limit_travel",
                "low_limit_travel",
                "unused",
            ]
        elif device_base_class == "signal":
            signals = [
                "readback",
                "velocity",
                "acceleration",
                "high_limit_travel",
                "low_limit_travel",
                "unused",
            ]
        dev_info = {
            "device_name": device_name,
            "device_info": {"device_base_class": device_base_class, "signals": signals},
            "custom_user_acces": {},
        }
        return BECMessage.DeviceInfoMessage(device=device_name, info=dev_info, metadata={})

    def get_device(self, device_name):
        for dev in self._session["devices"]:
            if dev["name"] == device_name:
                return dev


@pytest.fixture()
def bec_client():
    client = ClientMock()
    client.initialize(
        ServiceConfig(redis={"host": "host", "port": 123}, scibec={"host": "host", "port": 123}),
        ConnectorMock,
    )
    device_manager = DMClientMock(client)
    if not "test_session" in builtins.__dict__:
        with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
            builtins.__dict__["test_session"] = create_session_from_config(yaml.safe_load(f))
    device_manager._session = builtins.__dict__["test_session"]
    device_manager.producer = device_manager.connector.producer()
    client.wait_for_service = lambda service_name: None
    device_manager._load_session()
    for name, dev in device_manager.devices.items():
        dev._info["hints"] = {"fields": [name]}
    client.device_manager = device_manager
    yield client
    del ClientMock._client
    device_manager.devices.flush()
