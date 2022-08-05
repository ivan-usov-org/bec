import os

import bec_utils
import yaml
from bec_client.bec_client import BKClient
from bec_client.devicemanager_client import DMClient
from bec_client.scan_queue import ScanQueue
from bec_utils import BECMessage
from bec_utils.tests.utils import ConnectorMock

dir_path = os.path.dirname(bec_utils.__file__)


class ClientMock(BKClient):
    def _load_scans(self):
        pass


class DMClientMock(DMClient):
    def _get_device_info(self, device_name) -> BECMessage.DeviceInfoMessage:
        session_info = self.get_device(device_name)
        device_base_class = (
            "positioner"
            if session_info["deviceGroup"] in ["userMotor", "beamlineMotor"]
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


def get_bec_client_mock():
    client = ClientMock([], ConnectorMock, "")
    device_manager = DMClientMock(client, "")
    with open(f"{dir_path}/tests/test_session.yaml", "r") as f:
        device_manager._session = yaml.safe_load(f)
    device_manager.producer = device_manager.connector.producer()
    device_manager._load_session()
    return client


def test_scan_update():
    bec_client = get_bec_client_mock()
    queue = ScanQueue(bec_client)
