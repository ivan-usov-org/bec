import os
from unittest import mock

import pytest
import yaml

import bec_lib
from bec_lib import DeviceManagerBase, MessageEndpoints, ServiceConfig, messages
from bec_lib.messages import BECStatus
from bec_lib.tests.utils import (
    ConnectorMock,
    create_session_from_config,
    get_device_info_mock,
    threads_check,
)
from scan_bundler import ScanBundler
from scan_bundler.emitter import EmitterBase

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_lib.__file__)


class ScanBundlerDeviceManagerMock(DeviceManagerBase):
    def _get_device_info(self, device_name) -> messages.DeviceInfoMessage:
        return get_device_info_mock(device_name, self.get_device(device_name)["deviceClass"])

    def get_device(self, device_name):
        for dev in self._session["devices"]:
            if dev["name"] == device_name:
                return dev


class MessageMock:
    value = None
    topic: str = ""


@pytest.fixture
def scan_bundler(threads_check):
    service_mock = mock.MagicMock()
    service_mock.connector = ConnectorMock("")
    device_manager = ScanBundlerDeviceManagerMock(service_mock, "")
    device_manager.connector = service_mock.connector
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    scan_bundler_mock = ScanBundlerMock(device_manager, service_mock.connector)
    yield scan_bundler_mock
    scan_bundler_mock.shutdown()


class ScanBundlerMock(ScanBundler):
    def __init__(self, device_manager, connector_cls) -> None:
        super().__init__(
            ServiceConfig(redis={"host": "dummy", "port": 6379}), connector_cls=ConnectorMock
        )
        self.device_manager = device_manager

    def _start_device_manager(self):
        pass

    def _start_metrics_emitter(self):
        pass

    def _start_update_service_info(self):
        pass

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass


def test_device_read_callback(scan_bundler):
    msg = MessageMock()
    dev_msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scan_id": "laksjd", "readout_priority": "monitored"},
    )
    msg.value = dev_msg
    msg.topic = MessageEndpoints.device_read("samx").endpoint

    with mock.patch.object(scan_bundler, "_add_device_to_storage") as add_dev:
        scan_bundler._device_read_callback(msg)
        add_dev.assert_called_once_with([dev_msg], "samx")


@pytest.mark.parametrize(
    "scan_id,storageID,scan_msg",
    [
        ("adlk-jalskdj", None, None),
        (
            "adlk-jalskdjs",
            "adlk-jalskdjs",
            messages.ScanStatusMessage(
                scan_id="adlk-jalskdjs",
                status="open",
                info={
                    "scan_motors": ["samx"],
                    "readout_priority": {"monitored": ["samx"], "baseline": [], "on_request": []},
                    "queue_id": "my-queue-ID",
                    "scan_number": 5,
                    "scan_type": "step",
                },
            ),
        ),
        (
            "adlk-jalskdjs",
            "",
            messages.ScanStatusMessage(
                scan_id="adlk-jalskdjs",
                status="open",
                info={
                    "scan_motors": ["samx"],
                    "readout_priority": {"monitored": ["samx"], "baseline": [], "on_request": []},
                    "queue_id": "my-queue-ID",
                    "scan_number": 5,
                    "scan_type": "step",
                },
            ),
        ),
    ],
)
def test_wait_for_scan_id(scan_bundler, scan_id, storageID, scan_msg):
    sb = scan_bundler
    sb.storage_initialized.add(storageID)
    with mock.patch.object(sb.connector, "get", return_value=scan_msg) as get_scan_msgs:
        if not storageID and not scan_msg:
            with pytest.raises(TimeoutError):
                sb._wait_for_scan_id(scan_id, 1)
            return
        sb._wait_for_scan_id(scan_id)


def test_add_device_to_storage_returns_without_scan_id(scan_bundler):
    msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"readout_priority": "monitored"},
    )
    sb = scan_bundler
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


def test_add_device_to_storage_returns_without_signal(scan_bundler):
    msg = messages.DeviceMessage(
        signals={}, metadata={"scan_id": "scan_id", "readout_priority": "monitored"}
    )
    sb = scan_bundler
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


def test_add_device_to_storage_returns_on_timeout(scan_bundler):
    msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scan_id": "scan_id", "readout_priority": "monitored"},
    )
    sb = scan_bundler
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


@pytest.mark.parametrize("scan_status", ["aborted", "closed"])
def test_add_device_to_storage_returns_without_scan_info(scan_bundler, scan_status):
    msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scan_id": "scan_id", "readout_priority": "monitored"},
    )
    sb = scan_bundler
    sb.sync_storage["scan_id"] = {"info": {}}
    sb.sync_storage["scan_id"]["status"] = scan_status
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


@pytest.mark.parametrize(
    "msg,scan_type",
    [
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scan_id": "scan_id", "readout_priority": "monitored"},
            ),
            "step",
        ),
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scan_id": "scan_id", "readout_priority": "monitored"},
            ),
            "fly",
        ),
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scan_id": "scan_id", "readout_priority": "monitored"},
            ),
            "wrong",
        ),
    ],
)
def test_add_device_to_storage_primary(scan_bundler, msg, scan_type):
    sb = scan_bundler
    sb.sync_storage["scan_id"] = {"info": {"scan_type": scan_type, "monitor_sync": "bec"}}
    sb.sync_storage["scan_id"]["status"] = "open"
    sb.monitored_devices["scan_id"] = {"devices": [sb.device_manager.devices.samx]}
    sb.storage_initialized.add("scan_id")
    if scan_type == "step":
        with mock.patch.object(sb, "_step_scan_update") as step_update:
            sb._add_device_to_storage([msg], "samx", timeout_time=1)
            step_update.assert_called_once_with(
                "scan_id", "samx", msg.content["signals"], msg.metadata
            )
        return
    if scan_type == "fly":
        with mock.patch.object(sb, "_fly_scan_update") as fly_update:
            sb._add_device_to_storage([msg], "samx", timeout_time=1)
            fly_update.assert_called_once_with(
                "scan_id", "samx", msg.content["signals"], msg.metadata
            )
        return
    with pytest.raises(RuntimeError):
        sb._add_device_to_storage([msg], "samx", timeout_time=1)


@pytest.mark.parametrize(
    "msg,scan_type",
    [
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scan_id": "scan_id"},
            ),
            "fly",
        ),
        (
            messages.DeviceMessage(
                signals={
                    "flyer": {"flyer": 0.51, "flyer_setpoint": 0.5, "flyer_motor_is_moving": 0}
                },
                metadata={"scan_id": "scan_id"},
            ),
            "fly",
        ),
    ],
)
def test_add_device_to_storage_primary_flyer(scan_bundler, msg, scan_type):
    sb = scan_bundler
    sb.sync_storage["scan_id"] = {"info": {"scan_type": scan_type, "monitor_sync": "flyer"}}
    sb.sync_storage["scan_id"]["status"] = "open"
    sb.storage_initialized.add("scan_id")
    sb.monitored_devices["scan_id"] = {"devices": [sb.device_manager.devices.samx], "pointID": {}}
    sb.readout_priority["scan_id"] = {
        "monitored": [],
        "baseline": [],
        "on_request": [],
        "triggering_master": "flyer",
    }
    with mock.patch.object(sb, "_fly_scan_update") as fly_update:
        sb._add_device_to_storage([msg], "samx", timeout_time=1)
        fly_update.assert_called_once_with("scan_id", "samx", msg.content["signals"], msg.metadata)
    return


@pytest.mark.parametrize(
    "msg,scan_type",
    [
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scan_id": "scan_id", "readout_priority": "baseline"},
            ),
            "step",
        )
    ],
)
def test_add_device_to_storage_baseline(scan_bundler, msg, scan_type):
    sb = scan_bundler
    sb.sync_storage["scan_id"] = {"info": {"scan_type": scan_type, "monitor_sync": "bec"}}
    sb.sync_storage["scan_id"]["status"] = "open"
    sb.monitored_devices["scan_id"] = {"devices": []}
    sb.storage_initialized.add("scan_id")
    with mock.patch.object(sb, "_baseline_update") as step_update:
        sb._add_device_to_storage([msg], "samx", timeout_time=1)
        step_update.assert_called_once_with("scan_id", "samx", msg.content["signals"])


@pytest.mark.parametrize(
    "queue_msg",
    [
        messages.ScanQueueStatusMessage(
            queue={
                "primary": {
                    "info": [
                        {
                            "queue_id": "7c15c9a2-71d4-4f2a-91a7-c4a63088fa38",
                            "scan_id": ["bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5"],
                            "is_scan": [True],
                            "request_blocks": [
                                {
                                    "msg": b"\x84\xa8msg_type\xa4scan\xa7content\x83\xa9scan_type\xabfermat_scan\xa9parameter\x82\xa4args\x82\xa4samx\x92\xfe\x02\xa4samy\x92\xfe\x02\xa6kwargs\x83\xa4step\xcb?\xf8\x00\x00\x00\x00\x00\x00\xa8exp_time\xcb?\x94z\xe1G\xae\x14{\xa8relative\xc3\xa5queue\xa7primary\xa8metadata\x81\xa3RID\xd9$cd8fc68f-fe65-4031-9a37-e0e7ba9df542\xa7version\xcb?\xf0\x00\x00\x00\x00\x00\x00",
                                    "RID": "cd8fc68f-fe65-4031-9a37-e0e7ba9df542",
                                    "scan_motors": ["samx", "samy"],
                                    "readout_priority": {
                                        "monitored": ["samx", "samy"],
                                        "baseline": [],
                                        "on_request": [],
                                    },
                                    "is_scan": True,
                                    "scan_number": 25,
                                    "scan_id": "bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5",
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
        )
    ],
)
def test_scan_queue_callback(scan_bundler, queue_msg):
    sb = scan_bundler
    msg = MessageMock()
    msg.value = queue_msg
    sb._scan_queue_callback(msg)
    assert sb.current_queue == queue_msg.content["queue"]["primary"].get("info")


@pytest.mark.parametrize(
    "scan_msg",
    [
        messages.ScanStatusMessage(
            scan_id="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="closed",
            info={
                "readout_priority": "monitored",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scan_id": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queue_id": "84e5bc19-e2fc-4b03-b706-004420322813",
                "primary": ["samx", "samy"],
                "num_points": 143,
            },
        )
    ],
)
def test_scan_status_callback(scan_bundler, scan_msg):
    sb = scan_bundler
    msg = MessageMock()
    msg.value = scan_msg

    with mock.patch.object(sb, "handle_scan_status_message") as handle_scan_status_message_mock:
        sb._scan_status_callback(msg)
        handle_scan_status_message_mock.assert_called_once_with(scan_msg)


@pytest.mark.parametrize(
    "scan_msg, sync_storage",
    [
        [
            messages.ScanStatusMessage(
                scan_id="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
                status="closed",
                info={
                    "readout_priority": "monitored",
                    "DIID": 4,
                    "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                    "scan_id": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                    "queue_id": "84e5bc19-e2fc-4b03-b706-004420322813",
                    "primary": ["samx", "samy"],
                    "num_points": 143,
                },
            ),
            [],
        ],
        [
            messages.ScanStatusMessage(
                scan_id="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
                status="open",
                info={
                    "readout_priority": "monitored",
                    "DIID": 4,
                    "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                    "scan_id": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                    "queue_id": "84e5bc19-e2fc-4b03-b706-004420322813",
                    "primary": ["samx", "samy"],
                    "num_points": 143,
                },
            ),
            ["6ff7a89a-79e5-43ad-828b-c1e1aeed5803"],
        ],
    ],
)
def test_handle_scan_status_message(scan_bundler, scan_msg, sync_storage):
    sb = scan_bundler
    scan_id = scan_msg.content["scan_id"]
    sb.sync_storage = sync_storage

    with mock.patch.object(sb, "cleanup_storage") as cleanup_storage_mock:
        with mock.patch.object(sb, "_initialize_scan_container") as init_mock:
            with mock.patch.object(sb, "_scan_status_modification") as status_mock:
                sb.handle_scan_status_message(scan_msg)
                if not scan_id in sb.sync_storage:
                    init_mock.assert_called_once_with(scan_msg)
                    assert scan_id in sb.scan_id_history
                else:
                    init_mock.assert_not_called()

                if scan_msg.content.get("status") != "open":
                    status_mock.assert_called_once_with(scan_msg)
                else:
                    status_mock.assert_not_called()


def test_status_modification(scan_bundler):
    scan_id = "test_scan_id"
    scan_bundler.sync_storage[scan_id] = {"status": "open"}
    msg = messages.ScanStatusMessage(
        scan_id=scan_id,
        status="closed",
        info={
            "primary": ["samx"],
            "queue_id": "my-queue-ID",
            "scan_number": 5,
            "scan_type": "step",
        },
    )
    scan_bundler._scan_status_modification(msg)
    assert scan_bundler.sync_storage[scan_id]["status"] == "closed"

    scan_id = "scan_id_not_available"
    msg = messages.ScanStatusMessage(
        scan_id=scan_id,
        status="closed",
        info={
            "primary": ["samx"],
            "queue_id": "my-queue-ID",
            "scan_number": 5,
            "scan_type": "step",
        },
    )
    scan_bundler._scan_status_modification(msg)
    assert scan_bundler.sync_storage[scan_id]["info"] == {}


@pytest.mark.parametrize(
    "scan_msg",
    [
        messages.ScanStatusMessage(
            scan_id="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="closed",
            info={
                "readout_priority": "monitored",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scan_id": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queue_id": "84e5bc19-e2fc-4b03-b706-004420322813",
                "scan_number": 5,
                "scan_motors": ["samx", "samy"],
                "readout_priority": {
                    "monitored": ["samx", "samy"],
                    "baseline": [],
                    "on_request": [],
                },
                "num_points": 143,
            },
        ),
        messages.ScanStatusMessage(
            scan_id="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="open",
            info={
                "readout_priority": "monitored",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scan_id": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queue_id": "84e5bc19-e2fc-4b03-b706-004420322813",
                "scan_number": 5,
                "scan_motors": ["samx", "samy", "eyex", "bpm3a"],
                "readout_priority": {
                    "monitored": ["samx", "samy", "eyex", "bpm3a"],
                    "baseline": [],
                    "on_request": [],
                },
                "num_points": 143,
            },
        ),
    ],
)
def test_initialize_scan_container(scan_bundler, scan_msg):
    sb = scan_bundler
    scan_id = scan_msg.content["scan_id"]
    scan_info = scan_msg.content["info"]
    scan_motors = list(set(sb.device_manager.devices[m] for m in scan_info["scan_motors"]))
    readout_priority = scan_info["readout_priority"]
    bl_devs = sb.device_manager.devices.baseline_devices(readout_priority=readout_priority)

    with mock.patch.object(sb, "run_emitter") as emitter_mock:
        sb._initialize_scan_container(
            scan_msg
        )  # The sb.device_manager.devices[m] will crash if m is not a motor in devices

        if scan_msg.content.get("status") != "open":
            return
        assert sb.scan_motors[scan_id] == scan_motors
        assert sb.sync_storage[scan_id] == {"info": scan_info, "status": "open", "sent": set()}
        assert sb.monitored_devices[scan_id] == {
            "devices": sb.device_manager.devices.monitored_devices(
                readout_priority=readout_priority
            ),
            "pointID": {},
        }
        assert "eyex" not in [dev.name for dev in bl_devs]
        assert sb.baseline_devices[scan_id] == {
            "devices": bl_devs,
            "done": {dev.name: False for dev in bl_devs},
        }

        assert scan_id in sb.storage_initialized
        emitter_mock.assert_called_once_with("on_init", scan_id)


@pytest.mark.parametrize(
    "scan_msg, pointID, primary",
    [
        [
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={
                    "scan_id": "adlk-jalskdja",
                    "readout_priority": "monitored",
                    "pointID": 23,
                },
            ),
            23,
            True,
        ],
        [
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={
                    "scan_id": "adlk-jalskdjb",
                    "readout_priority": "monitored",
                    "pointID": 23,
                },
            ),
            23,
            False,
        ],
        [
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scan_id": "adlk-jalskdjc", "readout_priority": "monitored"},
            ),
            23,
            False,
        ],
    ],
)
def test_step_scan_update(scan_bundler, scan_msg, pointID, primary):
    sb = scan_bundler

    metadata = scan_msg.metadata
    scan_id = metadata.get("scan_id")
    device = "samx"
    signal = scan_msg.content.get("signals")
    sb.sync_storage[scan_id] = {"info": {}, "status": "open", "sent": set()}
    scan_motors = list(set(sb.device_manager.devices[m] for m in ["samx", "samy"]))

    monitored_devices = sb.monitored_devices[scan_id] = {
        "devices": sb.device_manager.devices.monitored_devices(scan_motors),
        "pointID": {},
    }

    dev = {device: signal}
    if primary:
        monitored_devices["pointID"][pointID] = {
            dev.name: True for dev in monitored_devices["devices"]
        }

    with mock.patch.object(sb, "_update_monitor_signals") as update_mock:
        with mock.patch.object(sb, "_send_scan_point") as send_mock:
            sb._step_scan_update(scan_id, device, signal, metadata)

            if "pointID" not in metadata:
                assert sb.sync_storage[scan_id] == {"info": {}, "status": "open", "sent": set()}
                return

            assert sb.sync_storage[scan_id][pointID] == {
                **sb.sync_storage[scan_id].get(pointID, {}),
                **dev,
            }

            assert monitored_devices["pointID"][pointID][device] == True

            if primary:
                update_mock.assert_called_once()
                send_mock.assert_called_once()

            else:
                pd_test = {dev.name: False for dev in monitored_devices["devices"]}
                pd_test["samx"] = True
                assert monitored_devices["pointID"][pointID] == pd_test


@pytest.mark.parametrize(
    "scan_id,storage,remove",
    [
        ("lkasjd", {"status": "open"}, False),
        ("alskjd", {"status": "closed"}, True),
        ("poiflkj", {"status": "aborted"}, True),
    ],
)
def test_cleanup_storage(scan_bundler, scan_id, storage, remove):
    sb = scan_bundler
    sb.sync_storage[scan_id] = storage
    sb.storage_initialized.add(scan_id)
    with mock.patch.object(sb, "run_emitter") as emitter:
        sb.cleanup_storage()
        if remove:
            emitter.assert_called_once_with("on_cleanup", scan_id)
            assert scan_id not in sb.storage_initialized
        else:
            emitter.assert_not_called()
            assert scan_id in sb.storage_initialized


@pytest.mark.parametrize("scan_id,pointID,sent", [("lkasjd", 1, True), ("alskjd", 2, False)])
def test_send_scan_point(scan_bundler, scan_id, pointID, sent):
    sb = scan_bundler
    sb.sync_storage[scan_id] = {"sent": set([1])}
    sb.sync_storage[scan_id][pointID] = {}
    with mock.patch.object(sb, "run_emitter") as emitter:
        with mock.patch("scan_bundler.scan_bundler.logger") as logger:
            sb._send_scan_point(scan_id, pointID)
            emitter.assert_called_once_with("on_scan_point_emit", scan_id, pointID)
            if sent:
                logger.debug.assert_called_once()


def test_run_emitter(scan_bundler):
    sb = scan_bundler
    with mock.patch("scan_bundler.scan_bundler.logger") as logger:
        sb.run_emitter("on_init", "jlaksjd", "jlkasjd")
        logger.error.assert_called()

    with mock.patch.object(sb._emitter[0], "on_init") as init:
        sb.run_emitter("on_init", "jlaksjd")
        init.assert_called_once_with("jlaksjd")


@pytest.mark.parametrize(
    "scan_id,device,signal,metadata",
    [
        ("scan_id-lkjd", "bpm4r", {"value": 5}, {"pointID": 2}),
        ("scan_id-lkjd", "bpm4r", {"value": 5}, {}),
    ],
)
def test_fly_scan_update(scan_bundler, scan_id, device, signal, metadata):
    sb = scan_bundler
    sb.sync_storage[scan_id] = {}
    with mock.patch.object(sb, "_update_monitor_signals") as update_signals:
        with mock.patch.object(sb, "_send_scan_point") as send_point:
            sb.sync_storage[scan_id]["info"] = {"monitor_sync": "flyer"}
            sb._fly_scan_update(scan_id, device, signal, metadata)
            pointID = metadata.get("pointID")
            if pointID:
                update_signals.assert_called_once_with(scan_id, pointID)
                send_point.assert_called_once_with(scan_id, pointID)


@pytest.mark.parametrize("scan_id,device,signal", [("scan_id-lkjd", "bpm4r", {"value": 5})])
def test_baseline_update(scan_bundler, scan_id, device, signal):
    sb = scan_bundler
    sb.baseline_devices[scan_id] = {"done": {device: False}}
    sb.sync_storage[scan_id] = {}
    sb.scan_motors[scan_id] = []
    sb.readout_priority[scan_id] = {}
    with mock.patch.object(sb, "run_emitter") as emitter:
        sb._baseline_update(scan_id, device, signal)
        emitter.assert_called_once_with("on_baseline_emit", scan_id)


def test_update_monitor_signals(scan_bundler):
    scan_id = "ljlaskdj"
    pointID = 2
    sb = scan_bundler
    sb.sync_storage[scan_id] = {"info": {"scan_type": "fly"}, pointID: {}}
    sb.monitored_devices[scan_id] = {
        "devices": sb.device_manager.devices.monitored_devices([]),
        "pointID": {},
    }
    num_devices = len(sb.device_manager.devices.monitored_devices([]))
    with mock.patch.object(
        sb, "_get_last_device_readback", return_value=[{"value": 400} for _ in range(num_devices)]
    ):
        sb._update_monitor_signals(scan_id, pointID)
        assert sb.sync_storage[scan_id][pointID]["bpm3a"] == {"value": 400}


def test_get_last_device_readback(scan_bundler):
    sb = scan_bundler
    dev_msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scan_id": "laksjd", "readout_priority": "monitored"},
    )
    with mock.patch.object(sb, "connector") as connector_mock:
        connector_mock.execute_pipeline.return_value = [dev_msg]
        ret = sb._get_last_device_readback([sb.device_manager.devices.samx])
        assert connector_mock.get.mock_calls == [
            mock.call(MessageEndpoints.device_readback("samx"), connector_mock.pipeline())
        ]
        assert ret == [dev_msg.content["signals"]]
