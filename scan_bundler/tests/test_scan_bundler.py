import os
from unittest import mock

import bec_lib
import pytest
import yaml
from bec_lib import DeviceManagerBase, MessageEndpoints, ServiceConfig, messages
from bec_lib.messages import BECStatus
from bec_lib.tests.utils import ConnectorMock, create_session_from_config, get_device_info_mock

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


def load_ScanBundlerMock():
    service_mock = mock.MagicMock()
    service_mock.connector = ConnectorMock("")
    device_manager = ScanBundlerDeviceManagerMock(service_mock, "")
    device_manager.producer = service_mock.connector.producer()
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    return ScanBundlerMock(device_manager, service_mock.connector)


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


def test_device_read_callback():
    scan_bundler = load_ScanBundlerMock()
    msg = MessageMock()
    dev_msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scanID": "laksjd", "readout_priority": "monitored"},
    )
    msg.value = dev_msg
    msg.topic = MessageEndpoints.device_read("samx")

    with mock.patch.object(scan_bundler, "_add_device_to_storage") as add_dev:
        scan_bundler._device_read_callback(msg, scan_bundler)
        add_dev.assert_called_once_with([dev_msg], "samx")


@pytest.mark.parametrize(
    "scanID,storageID,scan_msg",
    [
        ("adlk-jalskdj", None, []),
        (
            "adlk-jalskdjs",
            "adlk-jalskdjs",
            [
                messages.ScanStatusMessage(
                    scanID="adlk-jalskdjs",
                    status="open",
                    info={
                        "scan_motors": ["samx"],
                        "readout_priority": {
                            "monitored": ["samx"],
                            "baseline": [],
                            "on_request": [],
                        },
                        "queueID": "my-queue-ID",
                        "scan_number": 5,
                        "scan_type": "step",
                    },
                )
            ],
        ),
        (
            "adlk-jalskdjs",
            "",
            [
                messages.ScanStatusMessage(
                    scanID="adlk-jalskdjs",
                    status="open",
                    info={
                        "scan_motors": ["samx"],
                        "readout_priority": {
                            "monitored": ["samx"],
                            "baseline": [],
                            "on_request": [],
                        },
                        "queueID": "my-queue-ID",
                        "scan_number": 5,
                        "scan_type": "step",
                    },
                )
            ],
        ),
    ],
)
def test_wait_for_scanID(scanID, storageID, scan_msg):
    sb = load_ScanBundlerMock()
    sb.storage_initialized.add(storageID)
    with mock.patch.object(sb, "_get_scan_status_history", return_value=scan_msg) as get_scan_msgs:
        if not storageID and not scan_msg:
            with pytest.raises(TimeoutError):
                sb._wait_for_scanID(scanID, 1)
            return
        sb._wait_for_scanID(scanID)


@pytest.mark.parametrize(
    "msgs",
    [
        [
            messages.ScanStatusMessage(
                scanID="scanID",
                status="open",
                info={
                    "primary": ["samx"],
                    "queueID": "my-queue-ID",
                    "scan_number": 5,
                    "scan_type": "step",
                },
            )
        ],
        [],
    ],
)
def test_get_scan_status_history(msgs):
    sb = load_ScanBundlerMock()
    with mock.patch.object(sb.producer, "lrange", return_value=[msg for msg in msgs]) as lrange:
        res = sb._get_scan_status_history(5)
        lrange.assert_called_once_with(MessageEndpoints.scan_status() + "_list", -5, -1)
        assert res == msgs


def test_add_device_to_storage_returns_without_scanID():
    msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"readout_priority": "monitored"},
    )
    sb = load_ScanBundlerMock()
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


def test_add_device_to_storage_returns_without_signal():
    msg = messages.DeviceMessage(
        signals={}, metadata={"scanID": "scanID", "readout_priority": "monitored"}
    )
    sb = load_ScanBundlerMock()
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


def test_add_device_to_storage_returns_on_timeout():
    msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scanID": "scanID", "readout_priority": "monitored"},
    )
    sb = load_ScanBundlerMock()
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


@pytest.mark.parametrize("scan_status", ["aborted", "closed"])
def test_add_device_to_storage_returns_without_scan_info(scan_status):
    msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scanID": "scanID", "readout_priority": "monitored"},
    )
    sb = load_ScanBundlerMock()
    sb.sync_storage["scanID"] = {"info": {}}
    sb.sync_storage["scanID"]["status"] = scan_status
    sb._add_device_to_storage([msg], "samx", timeout_time=1)
    assert "samx" not in sb.device_storage


@pytest.mark.parametrize(
    "msg,scan_type",
    [
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "scanID", "readout_priority": "monitored"},
            ),
            "step",
        ),
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "scanID", "readout_priority": "monitored"},
            ),
            "fly",
        ),
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "scanID", "readout_priority": "monitored"},
            ),
            "wrong",
        ),
    ],
)
def test_add_device_to_storage_primary(msg, scan_type):
    sb = load_ScanBundlerMock()
    sb.sync_storage["scanID"] = {"info": {"scan_type": scan_type, "monitor_sync": "bec"}}
    sb.sync_storage["scanID"]["status"] = "open"
    sb.monitored_devices["scanID"] = {"devices": [sb.device_manager.devices.samx]}
    sb.storage_initialized.add("scanID")
    if scan_type == "step":
        with mock.patch.object(sb, "_step_scan_update") as step_update:
            sb._add_device_to_storage([msg], "samx", timeout_time=1)
            step_update.assert_called_once_with(
                "scanID", "samx", msg.content["signals"], msg.metadata
            )
        return
    if scan_type == "fly":
        with mock.patch.object(sb, "_fly_scan_update") as fly_update:
            sb._add_device_to_storage([msg], "samx", timeout_time=1)
            fly_update.assert_called_once_with(
                "scanID", "samx", msg.content["signals"], msg.metadata
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
                metadata={"scanID": "scanID"},
            ),
            "fly",
        ),
        (
            messages.DeviceMessage(
                signals={
                    "flyer": {"flyer": 0.51, "flyer_setpoint": 0.5, "flyer_motor_is_moving": 0}
                },
                metadata={"scanID": "scanID"},
            ),
            "fly",
        ),
    ],
)
def test_add_device_to_storage_primary_flyer(msg, scan_type):
    sb = load_ScanBundlerMock()
    sb.sync_storage["scanID"] = {"info": {"scan_type": scan_type, "monitor_sync": "flyer"}}
    sb.sync_storage["scanID"]["status"] = "open"
    sb.storage_initialized.add("scanID")
    sb.monitored_devices["scanID"] = {"devices": [sb.device_manager.devices.samx], "pointID": {}}
    sb.readout_priority["scanID"] = {
        "monitored": [],
        "baseline": [],
        "on_request": [],
        "triggering_master": "flyer",
    }
    with mock.patch.object(sb, "_fly_scan_update") as fly_update:
        sb._add_device_to_storage([msg], "samx", timeout_time=1)
        fly_update.assert_called_once_with("scanID", "samx", msg.content["signals"], msg.metadata)
    return


@pytest.mark.parametrize(
    "msg,scan_type",
    [
        (
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={"scanID": "scanID", "readout_priority": "baseline"},
            ),
            "step",
        )
    ],
)
def test_add_device_to_storage_baseline(msg, scan_type):
    sb = load_ScanBundlerMock()
    sb.sync_storage["scanID"] = {"info": {"scan_type": scan_type, "monitor_sync": "bec"}}
    sb.sync_storage["scanID"]["status"] = "open"
    sb.monitored_devices["scanID"] = {"devices": []}
    sb.storage_initialized.add("scanID")
    with mock.patch.object(sb, "_baseline_update") as step_update:
        sb._add_device_to_storage([msg], "samx", timeout_time=1)
        step_update.assert_called_once_with("scanID", "samx", msg.content["signals"])


@pytest.mark.parametrize(
    "queue_msg",
    [
        messages.ScanQueueStatusMessage(
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
                                    "readout_priority": {
                                        "monitored": ["samx", "samy"],
                                        "baseline": [],
                                        "on_request": [],
                                    },
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
        )
    ],
)
def test_scan_queue_callback(queue_msg):
    sb = load_ScanBundlerMock()
    msg = MessageMock()
    msg.value = queue_msg
    sb._scan_queue_callback(msg, sb)
    assert sb.current_queue == queue_msg.content["queue"]["primary"].get("info")


@pytest.mark.parametrize(
    "scan_msg",
    [
        messages.ScanStatusMessage(
            scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="closed",
            info={
                "readout_priority": "monitored",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scanID": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queueID": "84e5bc19-e2fc-4b03-b706-004420322813",
                "primary": ["samx", "samy"],
                "num_points": 143,
            },
        )
    ],
)
def test_scan_status_callback(scan_msg):
    sb = load_ScanBundlerMock()
    msg = MessageMock()
    msg.value = scan_msg

    with mock.patch.object(sb, "handle_scan_status_message") as handle_scan_status_message_mock:
        sb._scan_status_callback(msg, sb)
        handle_scan_status_message_mock.assert_called_once_with(scan_msg)


@pytest.mark.parametrize(
    "scan_msg, sync_storage",
    [
        [
            messages.ScanStatusMessage(
                scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
                status="closed",
                info={
                    "readout_priority": "monitored",
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
            messages.ScanStatusMessage(
                scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
                status="open",
                info={
                    "readout_priority": "monitored",
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
    msg = messages.ScanStatusMessage(
        scanID=scanID,
        status="closed",
        info={"primary": ["samx"], "queueID": "my-queue-ID", "scan_number": 5, "scan_type": "step"},
    )
    scan_bundler._scan_status_modification(msg)
    assert scan_bundler.sync_storage[scanID]["status"] == "closed"

    scanID = "scanID_not_available"
    msg = messages.ScanStatusMessage(
        scanID=scanID,
        status="closed",
        info={"primary": ["samx"], "queueID": "my-queue-ID", "scan_number": 5, "scan_type": "step"},
    )
    scan_bundler._scan_status_modification(msg)
    assert scan_bundler.sync_storage[scanID]["info"] == {}


@pytest.mark.parametrize(
    "scan_msg",
    [
        messages.ScanStatusMessage(
            scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="closed",
            info={
                "readout_priority": "monitored",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scanID": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queueID": "84e5bc19-e2fc-4b03-b706-004420322813",
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
            scanID="6ff7a89a-79e5-43ad-828b-c1e1aeed5803",
            status="open",
            info={
                "readout_priority": "monitored",
                "DIID": 4,
                "RID": "a53538b4-79f3-4132-91b5-d044e438f460",
                "scanID": "3ea07f69-b0ee-44fa-8451-b85824a37397",
                "queueID": "84e5bc19-e2fc-4b03-b706-004420322813",
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
def test_initialize_scan_container(scan_msg):
    sb = load_ScanBundlerMock()
    scanID = scan_msg.content["scanID"]
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
        assert sb.scan_motors[scanID] == scan_motors
        assert sb.sync_storage[scanID] == {"info": scan_info, "status": "open", "sent": set()}
        assert sb.monitored_devices[scanID] == {
            "devices": sb.device_manager.devices.monitored_devices(
                readout_priority=readout_priority
            ),
            "pointID": {},
        }
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
            messages.DeviceMessage(
                signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
                metadata={
                    "scanID": "adlk-jalskdja",
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
                    "scanID": "adlk-jalskdjb",
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
                metadata={"scanID": "adlk-jalskdjc", "readout_priority": "monitored"},
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

    monitored_devices = sb.monitored_devices[scanID] = {
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
            sb._step_scan_update(scanID, device, signal, metadata)

            if "pointID" not in metadata:
                assert sb.sync_storage[scanID] == {"info": {}, "status": "open", "sent": set()}
                return

            assert sb.sync_storage[scanID][pointID] == {
                **sb.sync_storage[scanID].get(pointID, {}),
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


@pytest.mark.parametrize("scanID,pointID,sent", [("lkasjd", 1, True), ("alskjd", 2, False)])
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


def test_run_emitter():
    sb = load_ScanBundlerMock()
    with mock.patch("scan_bundler.scan_bundler.logger") as logger:
        sb.run_emitter("on_init", "jlaksjd", "jlkasjd")
        logger.error.assert_called()

    sb._emitter = [EmitterBase(sb)]
    with mock.patch.object(sb._emitter[0], "on_init") as init:
        sb.run_emitter("on_init", "jlaksjd")
        init.assert_called_once_with("jlaksjd")


@pytest.mark.parametrize(
    "scanID,device,signal,metadata",
    [
        ("scanID-lkjd", "bpm4r", {"value": 5}, {"pointID": 2}),
        ("scanID-lkjd", "bpm4r", {"value": 5}, {}),
    ],
)
def test_fly_scan_update(scanID, device, signal, metadata):
    sb = load_ScanBundlerMock()
    sb.sync_storage[scanID] = {}
    with mock.patch.object(sb, "_update_monitor_signals") as update_signals:
        with mock.patch.object(sb, "_send_scan_point") as send_point:
            sb.sync_storage[scanID]["info"] = {"monitor_sync": "flyer"}
            sb._fly_scan_update(scanID, device, signal, metadata)
            pointID = metadata.get("pointID")
            if pointID:
                update_signals.assert_called_once_with(scanID, pointID)
                send_point.assert_called_once_with(scanID, pointID)


@pytest.mark.parametrize("scanID,device,signal", [("scanID-lkjd", "bpm4r", {"value": 5})])
def test_baseline_update(scanID, device, signal):
    sb = load_ScanBundlerMock()
    sb.baseline_devices[scanID] = {"done": {device: False}}
    sb.sync_storage[scanID] = {}
    sb.scan_motors[scanID] = []
    sb.readout_priority[scanID] = {}
    with mock.patch.object(sb, "run_emitter") as emitter:
        sb._baseline_update(scanID, device, signal)
        emitter.assert_called_once_with("on_baseline_emit", scanID)


def test_update_monitor_signals():
    scanID = "ljlaskdj"
    pointID = 2
    sb = load_ScanBundlerMock()
    sb.sync_storage[scanID] = {"info": {"scan_type": "fly"}, pointID: {}}
    sb.monitored_devices[scanID] = {
        "devices": sb.device_manager.devices.monitored_devices([]),
        "pointID": {},
    }
    num_devices = len(sb.device_manager.devices.monitored_devices([]))
    with mock.patch.object(
        sb, "_get_last_device_readback", return_value=[{"value": 400} for _ in range(num_devices)]
    ):
        sb._update_monitor_signals(scanID, pointID)
        assert sb.sync_storage[scanID][pointID]["bpm3a"] == {"value": 400}


def test_get_last_device_readback():
    sb = load_ScanBundlerMock()
    dev_msg = messages.DeviceMessage(
        signals={"samx": {"samx": 0.51, "setpoint": 0.5, "motor_is_moving": 0}},
        metadata={"scanID": "laksjd", "readout_priority": "monitored"},
    )
    with mock.patch.object(sb, "producer") as producer_mock:
        producer_mock.execute_pipeline.return_value = [dev_msg]
        ret = sb._get_last_device_readback([sb.device_manager.devices.samx])
        assert producer_mock.get.mock_calls == [
            mock.call(MessageEndpoints.device_readback("samx"), producer_mock.pipeline())
        ]
        assert ret == [dev_msg.content["signals"]]
