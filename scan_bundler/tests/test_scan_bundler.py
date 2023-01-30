import os
import time
from concurrent.futures import wait
from unittest import mock

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
    msg.value = scan_msg.dumps()

    with mock.patch.object(sb, "handle_scan_status_message") as handle_scan_status_message_mock:
        sb._scan_status_callback(msg, sb)
        handle_scan_status_message_mock.assert_called_once_with(scan_msg)


@pytest.mark.parametrize(
    "scan_msg, sync_storage",
    [
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
            [],
        ],
        [
            BECMessage.ScanStatusMessage(
                scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
                status="open",
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
            ["6ff7a89a-79e5-43ad-828b-c1e1aeed5803"],
        ],
    ],
)
def test_handle_scan_status_message(scan_msg, sync_storage):
    sb = load_ScanBundlerMock()
    scanID = scan_msg.content["scanID"]
    sb.sync_storage = sync_storage

    with mock.patch.object(sb, "cleanup_storage") as cleanup_storage_mock:
        with mock.patch.object(sb, "_initialize_scan_container") as init_mock:
            with mock.patch.object(sb, "_scan_status_modification") as status_mock:

                sb.handle_scan_status_message(scan_msg)
                if not scanID in sb.sync_storage:
                    init_mock.assert_called_once_with(scan_msg)
                    assert scanID in sb.scanID_history
                else:
                    init_mock.assert_not_called()

                if scan_msg.content.get("status") != "open":
                    status_mock.assert_called_once_with(scan_msg)
                else:
                    status_mock.assert_not_called()


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
                "scan_number": 5,
                "primary": ["samx", "samy"],
                "num_points": 143,
            },
        ),
        BECMessage.ScanStatusMessage(
            scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="open",
            info={
                "stream": "primary",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scanID": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queueID": "84e5bc19-e2fc-4b03-b706-004420322813",
                "scan_number": 5,
                "primary": ["samx", "samy", "eyex", "bpm3a"],
                "num_points": 143,
            },
        ),
    ],
)
def test_initialize_scan_container(scan_msg):
    sb = load_ScanBundlerMock()
    scanID = scan_msg.content["scanID"]
    scan_info = scan_msg.content["info"]
    scan_motors = list(set(sb.device_manager.devices[m] for m in scan_info["primary"]))
    bl_devs = sb.device_manager.devices.baseline_devices(scan_motors)

    with mock.patch.object(sb, "run_emitter") as emitter_mock:

        sb._initialize_scan_container(
            scan_msg
        )  # The sb.device_manager.devices[m] will crash if m is not a motor in devices

        if scan_msg.content.get("status") != "open":
            return
        assert sb.scan_motors[scanID] == scan_motors
        assert sb.sync_storage[scanID] == {"info": scan_info, "status": "open", "sent": set()}
        assert sb.primary_devices[scanID] == {
            "devices": sb.device_manager.devices.primary_devices(scan_motors),
            "pointID": {},
        }
        assert sb.monitor_devices[scanID] == sb.device_manager.devices.acquisition_group("monitor")
        assert "eyex" not in [dev.name for dev in bl_devs]
        assert sb.baseline_devices[scanID] == {
            "devices": bl_devs,
            "done": {dev.name: False for dev in bl_devs},
        }

        assert scanID in sb.storage_initialized
        emitter_mock.assert_called_once_with("on_init", scanID)


@pytest.mark.parametrize(
    "scan_msg, pointID, primary",
    [
        [
            BECMessage.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "adlk-jalskdja", "stream": "primary", "pointID": 23},
            ),
            23,
            True,
        ],
        [
            BECMessage.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "adlk-jalskdjb", "stream": "primary", "pointID": 23},
            ),
            23,
            False,
        ],
        [
            BECMessage.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "adlk-jalskdjc", "stream": "primary"},
            ),
            23,
            False,
        ],
    ],
)
def test_step_scan_update(scan_msg, pointID, primary):

    sb = load_ScanBundlerMock()

    metadata = scan_msg.metadata
    scanID = metadata.get("scanID")
    device = "samx"
    signal = scan_msg.content.get("signals")
    sb.sync_storage[scanID] = {"info": {}, "status": "open", "sent": set()}
    scan_motors = list(set(sb.device_manager.devices[m] for m in ["samx", "samy"]))

    primary_devices = sb.primary_devices[scanID] = {
        "devices": sb.device_manager.devices.primary_devices(scan_motors),
        "pointID": {},
    }

    dev = {device: signal}
    if primary:
        primary_devices["pointID"][pointID] = {dev.name: True for dev in primary_devices["devices"]}

    with mock.patch.object(sb, "_update_monitor_signals") as update_mock:
        with mock.patch.object(sb, "_send_scan_point") as send_mock:

            sb._step_scan_update(scanID, device, signal, metadata)

            if "pointID" not in metadata:
                assert sb.sync_storage[scanID] == {"info": {}, "status": "open", "sent": set()}
                return

            assert sb.sync_storage[scanID][pointID] == {
                **sb.sync_storage[scanID].get(pointID, {}),
                **dev,
            }

            assert primary_devices["pointID"][pointID][device] == True

            if primary:
                update_mock.assert_called_once()
                send_mock.assert_called_once()

            else:
                pd_test = {dev.name: False for dev in primary_devices["devices"]}
                pd_test["samx"] = True
                assert primary_devices["pointID"][pointID] == pd_test


@pytest.mark.parametrize(
    "scanID,storage,remove",
    [
        ("lkasjd", {"status": "open"}, False),
        ("alskjd", {"status": "closed"}, True),
        ("poiflkj", {"status": "aborted"}, True),
    ],
)
def test_cleanup_storage(scanID, storage, remove):
    sb = load_ScanBundlerMock()
    sb.sync_storage[scanID] = storage
    sb.storage_initialized.add(scanID)
    with mock.patch.object(sb, "run_emitter") as emitter:
        sb.cleanup_storage()
        if remove:
            emitter.assert_called_once_with("on_cleanup", scanID)
            assert scanID not in sb.storage_initialized
        else:
            emitter.assert_not_called()
            assert scanID in sb.storage_initialized


@pytest.mark.parametrize(
    "scanID,pointID,sent",
    [
        ("lkasjd", 1, True),
        ("alskjd", 2, False),
    ],
)
def test_send_scan_point(scanID, pointID, sent):
    sb = load_ScanBundlerMock()
    sb.sync_storage[scanID] = {"sent": set([1])}
    sb.sync_storage[scanID][pointID] = {}
    with mock.patch.object(sb, "run_emitter") as emitter:
        with mock.patch("scan_bundler.scan_bundler.logger") as logger:
            sb._send_scan_point(scanID, pointID)
            emitter.assert_called_once_with("on_scan_point_emit", scanID, pointID)
            if sent:
                logger.debug.assert_called_once()
