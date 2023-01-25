import os
import time
from concurrent.futures import wait
from unittest import mock
import threading

import bec_utils
import pytest
import yaml
from bec_utils import BECMessage, MessageEndpoints
from bec_utils.tests.utils import ConnectorMock, create_session_from_config
from scan_bundler import ScanBundler
from scan_bundler.devicemanager_sb import DeviceManagerSB

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_utils.__file__)


class MessageMock:
    value = None
    topic: str = ""


def load_ScanBundlerMock():
    connector = ConnectorMock("")
    device_manager = DeviceManagerSB(connector, "")
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


def test_start_buffered_producer():
    sb = load_ScanBundlerMock()
    assert isinstance(sb._buffered_producer_thread, threading.Thread)
    sb._start_buffered_producer()
    with pytest.raises(Exception) as exc_info:
        sb._buffered_producer_thread.start()
    assert exc_info.value.args[0] == "threads can only be started once"


def test_start_device_manager():
    sb = load_ScanBundlerMock()
    assert isinstance(sb.device_manager, DeviceManagerSB)


@pytest.mark.parametrize(
    "scanID,storageID", [("adlk-jalskdj", None), ("adlk-jalskdj", "adlk-jalskdj")]
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
        metadata={"scanID": "adlk-jalskdj", "stream": "primary"},
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
    assert "samx" in scan_bundler.device_storage


@pytest.mark.parametrize(
    "queue_msg",
    [
        BECMessage.ScanQueueStatusMessage(
            queue={
                "primary": {
                    "info": [
                        {
                            "queueID": "7c15c9a2-71d4-4f2a-91a7-c4a63088fa38",
                            "scanID": ["bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5"],
                            "is_scan": [True],
                            "request_blocks": [
                                {
                                    "msg": b"\x84\xa8msg_type\xa4scan\xa7content\x83\xa9scan_type\xabfermat_scan\xa9parameter\x82\xa4args\x82\xa4samx\x92\xfe\x02\xa4samy\x92\xfe\x02\xa6kwargs\x83\xa4step\xcb?\xf8\x00\x00\x00\x00\x00\x00\xa8exp_time\xcb?\x94z\xe1G\xae\x14{\xa8relative\xc3\xa5queue\xa7primary\xa8metadata\x81\xa3RID\xd9$cd8fc68f-fe65-4031-9a37-e0e7ba9df542\xa7version\xcb?\xf0\x00\x00\x00\x00\x00\x00",
                                    "RID": "cd8fc68f-fe65-4031-9a37-e0e7ba9df542",
                                    "scan_motors": ["samx", "samy"],
                                    "is_scan": True,
                                    "scan_number": 25,
                                    "scanID": "bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5",
                                    "metadata": {"RID": "cd8fc68f-fe65-4031-9a37-e0e7ba9df542"},
                                    "content": {
                                        "scan_type": "fermat_scan",
                                        "parameter": {
                                            "args": {"samx": [-2, 2], "samy": [-2, 2]},
                                            "kwargs": {
                                                "step": 1.5,
                                                "exp_time": 0.02,
                                                "relative": True,
                                            },
                                        },
                                        "queue": "primary",
                                    },
                                }
                            ],
                            "scan_number": [25],
                            "status": "PENDING",
                            "active_request_block": None,
                        }
                    ],
                    "status": "RUNNING",
                }
            }
        ),
    ],
)
def test_scan_queue_callback(queue_msg):
    sb = load_ScanBundlerMock()
    msg = MessageMock()
    msg.value = queue_msg.dumps()
    sb._scan_queue_callback(msg, sb)
    assert sb.current_queue == queue_msg.content["queue"]["primary"].get("info")


@pytest.mark.parametrize(
    "scan_msg",
    [
        BECMessage.ScanStatusMessage(
            scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="closed",
            info={
                "stream": "primary",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scanID": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queueID": "84e5bc19-e2fc-4b03-b706-004420322813",
                "primary": ["samx", "samy"],
                "num_points": 143,
            },
        ),
    ],
)
def test_scan_status_callback(scan_msg):
    sb = load_ScanBundlerMock()
    msg = MessageMock()
    sb.handle_scan_status_message = mock.MagicMock()
    msg.value = scan_msg.dumps()
    sb._scan_status_callback(msg, sb)
    sb.handle_scan_status_message.assert_called_once_with(scan_msg)


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
