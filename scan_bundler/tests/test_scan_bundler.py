import os
import time
from concurrent.futures import wait

import bec_utils
import pytest
import yaml
from bec_utils import BECMessage
from bec_utils import DeviceManagerBase as DeviceManager
from bec_utils import MessageEndpoints
from bec_utils.tests.utils import ConnectorMock, create_session_from_config

from scan_bundler import ScanBundler

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_utils.__file__)


class MessageMock:
    value = None
    topic: str = ""


def load_ScanBundlerMock():
    connector = ConnectorMock("")
    device_manager = DeviceManager(connector, "")
    device_manager.producer = connector.producer()
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    return ScanBundlerMock(device_manager, connector)


class ScanBundlerMock(ScanBundler):
    def __init__(self, device_manager, connector_cls) -> None:
        super().__init__(bootstrap_server="dummy", connector_cls=ConnectorMock, scibec_url="dummy")
        self.device_manager = device_manager

    def _start_device_manager(self):
        pass


@pytest.mark.parametrize(
    "scanID,storageID", [("adlk-jalskdj", None), ("adlk-jalskdjs", "adlk-jalskdjs")]
)
def test_device_read_callback(scanID, storageID):
    scan_bundler = load_ScanBundlerMock()
    for name, dev in scan_bundler.device_manager.devices.items():
        dev._signals = {
            name: {"value": 0, "timestamp": time.time()},
            "setpoint": {"value": 0, "timestamp": time.time()},
            "motor_is_moving": {"value": 0, "timestamp": time.time()},
        }
    msg = MessageMock()
    msg.value = BECMessage.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scanID": scanID, "stream": "primary"},
    ).dumps()
    msg.topic = MessageEndpoints.device_read("samx").encode()

    if storageID:
        scan_bundler.handle_scan_status_message(
            BECMessage.ScanStatusMessage(
                scanID=storageID,
                status="open",
                info={
                    "primary": ["samx"],
                    "queueID": "my-queue-ID",
                    "scan_number": 5,
                    "scan_type": "step",
                },
            )
        )
    scan_bundler._device_read_callback(msg, scan_bundler)
    wait(scan_bundler.executor_tasks)
    if scanID != storageID:
        assert not scan_bundler.device_storage
        return
    assert (
        "samx" in scan_bundler.device_storage
    )  # fails second time line 318, should not enter that while-loop...


def test_status_modification():
    scanID = "test_scanID"
    scan_bundler = load_ScanBundlerMock()
    scan_bundler.sync_storage[scanID] = {"status": "open"}
    msg = BECMessage.ScanStatusMessage(
        scanID=scanID,
        status="closed",
        info={
            "primary": ["samx"],
            "queueID": "my-queue-ID",
            "scan_number": 5,
            "scan_type": "step",
        },
    )
    scan_bundler._scan_status_modification(msg)
    assert scan_bundler.sync_storage[scanID]["status"] == "closed"

    scanID = "scanID_not_available"
    msg = BECMessage.ScanStatusMessage(
        scanID=scanID,
        status="closed",
        info={
            "primary": ["samx"],
            "queueID": "my-queue-ID",
            "scan_number": 5,
            "scan_type": "step",
        },
    )
    scan_bundler._scan_status_modification(msg)
    assert scan_bundler.sync_storage[scanID]["info"] == {}
