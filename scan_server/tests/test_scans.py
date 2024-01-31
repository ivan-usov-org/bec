import collections
import inspect
from unittest import mock

import numpy as np
import pytest
from bec_lib import messages
from bec_lib.devicemanager import DeviceContainer
from bec_lib.tests.utils import ConnectorMock

from scan_plugins.LamNIFermatScan import LamNIFermatScan
from scan_plugins.otf_scan import OTFScan
from scan_plugins.owis_grid import OwisGrid
from scan_server.errors import ScanAbortion
from scan_server.scans import (
    Acquire,
    AddInteractiveScanPoint,
    CloseInteractiveScan,
    ContLineScan,
    DeviceRPC,
    FermatSpiralScan,
    LineScan,
    ListScan,
    MonitorScan,
    Move,
    OpenInteractiveScan,
    RequestBase,
    RoundROIScan,
    RoundScan,
    RoundScanFlySim,
    Scan,
    ScanBase,
    TimeScan,
    UpdatedMove,
    get_2D_raster_pos,
    get_fermat_spiral_pos,
    get_round_roi_scan_positions,
    get_round_scan_positions,
    unpack_scan_args,
)

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


class DeviceMock:
    def __init__(self, name: str):
        self.name = name
        self.read_buffer = None
        self._config = {"deviceConfig": {"limits": [-50, 50]}, "userParameter": None}
        self._read_only = False
        self._enabled = True

    def read(self):
        return self.read_buffer

    def readback(self):
        return self.read_buffer

    @property
    def read_only(self) -> bool:
        return self._read_only

    @read_only.setter
    def read_only(self, val: bool):
        self._read_only = val

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, val: bool):
        self._enabled = val

    @property
    def user_parameter(self):
        return self._config["userParameter"]


class DMMock:
    devices = DeviceContainer()
    connector = ConnectorMock()

    def add_device(self, name):
        self.devices[name] = DeviceMock(name)


def test_unpack_scan_args_empty_dict():
    scan_args = {}
    expected_args = []
    assert unpack_scan_args(scan_args) == expected_args


def test_unpack_scan_args_non_dict_input():
    scan_args = [1, 2, 3]
    assert unpack_scan_args(scan_args) == scan_args


def test_unpack_scan_args_valid_input():
    scan_args = {"cmd1": [1, 2, 3], "cmd2": ["a", "b", "c"]}
    expected_args = ["cmd1", 1, 2, 3, "cmd2", "a", "b", "c"]
    assert unpack_scan_args(scan_args) == expected_args


@pytest.mark.parametrize(
    "mv_msg,reference_msg_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,), "samy": (2,)}, "kwargs": {}},
                queue="primary",
            ),
            [
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 0, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 1, "response": True},
                ),
            ],
        ),
        (
            messages.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,), "samy": (2,), "samz": (3,)}, "kwargs": {}},
                queue="primary",
            ),
            [
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 0, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 1, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="samz",
                    action="set",
                    parameter={"value": 3, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 2, "response": True},
                ),
            ],
        ),
        (
            messages.ScanQueueMessage(
                scan_type="mv", parameter={"args": {"samx": (1,)}, "kwargs": {}}, queue="primary"
            ),
            [
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 0, "response": True},
                )
            ],
        ),
    ],
)
def test_scan_move(mv_msg, reference_msg_list):
    msg_list = []
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.add_device("samy")
    device_manager.add_device("samz")

    def offset_mock():
        yield None

    s = Move(parameter=mv_msg.content.get("parameter"), device_manager=device_manager)
    s._set_position_offset = offset_mock
    for step in s.run():
        if step:
            msg_list.append(step)

    assert msg_list == reference_msg_list


@pytest.mark.parametrize(
    "mv_msg,reference_msg_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="umv",
                parameter={"args": {"samx": (1,), "samy": (2,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "0bab7ee3-b384-4571-b...0fff984c05"},
            ),
            [
                messages.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={
                        "readback": {
                            "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                            "devices": ["samx", "samy"],
                            "start": [0, 0],
                            "end": [1.0, 2.0],
                        }
                    },
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 0,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1.0, "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 1,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2.0, "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 2,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 3,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samy",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 4,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
            ],
        ),
        (
            messages.ScanQueueMessage(
                scan_type="umv",
                parameter={"args": {"samx": (1,), "samy": (2,), "samz": (3,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "0bab7ee3-b384-4571-b...0fff984c05"},
            ),
            [
                messages.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={
                        "readback": {
                            "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                            "devices": ["samx", "samy", "samz"],
                            "start": [0, 0, 0],
                            "end": [1.0, 2.0, 3.0],
                        }
                    },
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 0,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1.0, "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 1,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2.0, "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 2,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samz",
                    action="set",
                    parameter={"value": 3.0, "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 3,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 4,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samy",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 5,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samz",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 6,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
            ],
        ),
        (
            messages.ScanQueueMessage(
                scan_type="umv",
                parameter={"args": {"samx": (1,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "0bab7ee3-b384-4571-b...0fff984c05"},
            ),
            [
                messages.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={
                        "readback": {
                            "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                            "devices": ["samx"],
                            "start": [0],
                            "end": [1.0],
                        }
                    },
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 0,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1.0, "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 1,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "readout_priority": "monitored",
                        "DIID": 2,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
            ],
        ),
    ],
)
def test_scan_updated_move(mv_msg, reference_msg_list):
    msg_list = []
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.add_device("samy")
    device_manager.add_device("samz")

    def offset_mock():
        yield None

    s = UpdatedMove(
        parameter=mv_msg.content.get("parameter"),
        device_manager=device_manager,
        metadata=mv_msg.metadata,
    )
    s._set_position_offset = offset_mock
    for step in s.run():
        if step:
            msg_list.append(step)

    assert msg_list == reference_msg_list


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
            ),
            [
                messages.DeviceInstructionMessage(
                    device=["samx"],
                    action="read",
                    parameter={"wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=["samx"],
                    action="wait",
                    parameter={"type": "read", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 4},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "scan_motors": ["samx"],
                        "readout_priority": {
                            "monitored": ["samx"],
                            "baseline": [],
                            "on_request": [],
                            "async": [],
                        },
                        "num_points": 3,
                        "positions": [[-5.0], [0.0], [5.0]],
                        "scan_name": "grid_scan",
                        "scan_type": "step",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"readout_priority": "baseline", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    **{
                        "device": "samx",
                        "action": "set",
                        "parameter": {"value": -5.0, "wait_group": "scan_motor"},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 8},
                ),
                messages.DeviceInstructionMessage(
                    **{
                        "device": None,
                        "action": "wait",
                        "parameter": {
                            "type": "move",
                            "group": "scan_motor",
                            "wait_group": "scan_motor",
                        },
                    },
                    metadata={"readout_priority": "monitored", "DIID": 9},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "pre_scan", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 7},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": -5.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 2},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 0, "readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0},
                    metadata={"readout_priority": "monitored", "DIID": 4},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"pointID": 0, "readout_priority": "monitored", "DIID": 5},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 6},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 0.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 7},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 8},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 9},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 1, "readout_priority": "monitored", "DIID": 10},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0},
                    metadata={"readout_priority": "monitored", "DIID": 11},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"pointID": 1, "readout_priority": "monitored", "DIID": 12},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 13},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 5.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 14},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 15},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 16},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 2, "readout_priority": "monitored", "DIID": 17},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0},
                    metadata={"readout_priority": "monitored", "DIID": 18},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"pointID": 2, "readout_priority": "monitored", "DIID": 19},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 20},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 0.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 21},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 22},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 23},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "complete", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 31},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 24},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 25},
                ),
            ],
        )
    ],
)
def test_scan_scan(scan_msg, reference_scan_list):
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    msg_list = []

    def offset_mock():
        yield None

    scan = Scan(parameter=scan_msg.content.get("parameter"), device_manager=device_manager)
    scan._set_position_offset = offset_mock
    for step in scan.run():
        if step:
            msg_list.append(step)
    scan_uid = msg_list[0].metadata.get("scanID")
    for ii, _ in enumerate(reference_scan_list):
        if reference_scan_list[ii].metadata.get("scanID") is not None:
            reference_scan_list[ii].metadata["scanID"] = scan_uid
        reference_scan_list[ii].metadata["DIID"] = ii
    assert msg_list == reference_scan_list


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
                queue="primary",
            ),
            [
                (0, np.array([-1.1550884, -1.26090078])),
                (1, np.array([2.4090456, 0.21142208])),
                (2, np.array([-2.35049217, 1.80207841])),
                (3, np.array([0.59570227, -3.36772012])),
                (4, np.array([2.0522743, 3.22624707])),
                (5, np.array([-4.04502068, -1.08738572])),
                (6, np.array([4.01502502, -2.08525157])),
                (7, np.array([-1.6591442, 4.54313114])),
                (8, np.array([-1.95738438, -4.7418927])),
                (9, np.array([4.89775337, 2.29194501])),
            ],
        ),
        (
            messages.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={
                    "args": {"samx": (-5, 5), "samy": (-5, 5)},
                    "kwargs": {"step": 3, "spiral_type": 1},
                },
                queue="primary",
            ),
            [
                (0, np.array([1.1550884, 1.26090078])),
                (1, np.array([2.4090456, 0.21142208])),
                (2, np.array([2.35049217, -1.80207841])),
                (3, np.array([0.59570227, -3.36772012])),
                (4, np.array([-2.0522743, -3.22624707])),
                (5, np.array([-4.04502068, -1.08738572])),
                (6, np.array([-4.01502502, 2.08525157])),
                (7, np.array([-1.6591442, 4.54313114])),
                (8, np.array([1.95738438, 4.7418927])),
                (9, np.array([4.89775337, 2.29194501])),
            ],
        ),
    ],
)
def test_fermat_scan(scan_msg, reference_scan_list):
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    device_manager.add_device("samy")
    device_manager.devices["samy"].read_buffer = {"value": 0}
    args = unpack_scan_args(scan_msg.content.get("parameter").get("args"))
    kwargs = scan_msg.content.get("parameter").get("kwargs")
    scan = FermatSpiralScan(
        *args, parameter=scan_msg.content.get("parameter"), device_manager=device_manager, **kwargs
    )

    def offset_mock():
        yield None

    scan._set_position_offset = offset_mock
    next(scan.prepare_positions())
    # pylint: disable=protected-access
    pos = list(scan._get_position())
    assert pytest.approx(np.vstack(np.array(pos, dtype=object)[:, 1])) == np.vstack(
        np.array(reference_scan_list, dtype=object)[:, 1]
    )


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="cont_line_scan",
                parameter={"args": {"samx": (-5, 5)}, "kwargs": {"steps": 3, "exp_time": 0.1}},
                queue="primary",
            ),
            [
                messages.DeviceInstructionMessage(
                    device=["samx"],
                    action="read",
                    parameter={"wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=["samx"],
                    action="wait",
                    parameter={"type": "read", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 4},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "scan_motors": ["samx"],
                        "readout_priority": {
                            "monitored": ["samx"],
                            "baseline": [],
                            "on_request": [],
                            "async": [],
                        },
                        "num_points": 3,
                        "positions": [[-5.0], [0.0], [5.0]],
                        "scan_name": "cont_line_scan",
                        "scan_type": "step",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"readout_priority": "baseline", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    **{
                        "device": "samx",
                        "action": "set",
                        "parameter": {"value": -5.0, "wait_group": "scan_motor"},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 5},
                ),
                messages.DeviceInstructionMessage(
                    **{
                        "device": None,
                        "action": "wait",
                        "parameter": {
                            "type": "move",
                            "group": "scan_motor",
                            "wait_group": "scan_motor",
                        },
                    },
                    metadata={"readout_priority": "monitored", "DIID": 6},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "pre_scan", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 7},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": -105.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 2},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 5.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 7},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 0, "readout_priority": "monitored", "DIID": 8},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "primary"},
                    metadata={"pointID": 0, "readout_priority": "monitored", "DIID": 9},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 1, "readout_priority": "monitored", "DIID": 10},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "primary"},
                    metadata={"pointID": 1, "readout_priority": "monitored", "DIID": 11},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 2, "readout_priority": "monitored", "DIID": 12},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "primary"},
                    metadata={"pointID": 2, "readout_priority": "monitored", "DIID": 13},
                ),
                messages.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 0.0, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 14},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 15},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 16},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "complete", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 31},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 17},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 18},
                ),
            ],
        )
    ],
)
def test_cont_line_scan(scan_msg, reference_scan_list):
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    msg_list = []

    def offset_mock():
        yield None

    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    scan = ContLineScan(
        *args, parameter=scan_msg.content.get("parameter"), device_manager=device_manager, **kwargs
    )
    scan._set_position_offset = offset_mock

    readback = collections.deque()
    readback.extend([{"value": -10}, {"value": -5}, {"value": 0.1}, {"value": 5}, {"value": 10}])

    def mock_readback():
        if len(readback) > 1:
            return readback.popleft()
        return readback[0]

    with mock.patch.object(scan.device_manager.devices["samx"], "readback", mock_readback):
        msg_list = [val for val in list(scan.run()) if val is not None]

        scan_uid = msg_list[0].metadata.get("scanID")
        for ii, _ in enumerate(reference_scan_list):
            if reference_scan_list[ii].metadata.get("scanID") is not None:
                reference_scan_list[ii].metadata["scanID"] = scan_uid
            reference_scan_list[ii].metadata["DIID"] = ii
        assert msg_list == reference_scan_list


def test_device_rpc():
    device_manager = DMMock()
    parameter = {
        "device": "samx",
        "rpc_id": "baf7c4c0-4948-4046-8fc5-ad1e9d188c10",
        "func": "read",
        "args": [],
        "kwargs": {},
    }

    scan = DeviceRPC(parameter=parameter, device_manager=device_manager)
    scan_instructions = list(scan.run())
    assert scan_instructions == [
        messages.DeviceInstructionMessage(
            device="samx",
            action="rpc",
            parameter=parameter,
            metadata={"readout_priority": "monitored", "DIID": 0},
        )
    ]


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="acquire",
                parameter={"args": [], "kwargs": {"exp_time": 1.0}},
                queue="primary",
            ),
            [
                messages.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "scan_motors": [],
                        "readout_priority": {
                            "monitored": [],
                            "baseline": [],
                            "on_request": [],
                            "async": [],
                        },
                        "num_points": 1,
                        "positions": [],
                        "scan_name": "acquire",
                        "scan_type": "step",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"readout_priority": "baseline", "DIID": 2},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="pre_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 0, "readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 1},
                    metadata={"readout_priority": "monitored", "DIID": 4},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"pointID": 0, "readout_priority": "monitored", "DIID": 5},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 6},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "complete", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 31},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 17},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 18},
                ),
            ],
        )
    ],
)
def test_acquire(scan_msg, reference_scan_list):
    device_manager = DMMock()

    scan = Acquire(exp_time=1, device_manager=device_manager)
    scan_instructions = list(scan.run())
    scan_uid = scan_instructions[0].metadata.get("scanID")
    for ii, _ in enumerate(reference_scan_list):
        if reference_scan_list[ii].metadata.get("scanID") is not None:
            reference_scan_list[ii].metadata["scanID"] = scan_uid
        reference_scan_list[ii].metadata["DIID"] = ii
    assert scan_instructions == reference_scan_list


def test_pre_scan_macro():
    def pre_scan_macro(devices: dict, request: RequestBase):
        pass

    device_manager = DMMock()
    device_manager.add_device("samx")
    macros = [inspect.getsource(pre_scan_macro).encode()]
    scan_msg = messages.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    with mock.patch.object(
        request.device_manager.connector,
        "lrange",
        new_callable=mock.PropertyMock,
        return_value=macros,
    ) as macros_mock:
        with mock.patch.object(request, "_get_func_name_from_macro", return_value="pre_scan_macro"):
            with mock.patch("builtins.eval") as eval_mock:
                request.initialize()
                eval_mock.assert_called_once_with("pre_scan_macro")


# def test_scan_report_devices():
#     device_manager = DMMock()
#     device_manager.add_device("samx")
#     parameter = {
#         "args": {"samx": (-5, 5), "samy": (-5, 5)},
#         "kwargs": {"step": 3},
#     }
#     request = RequestBase(device_manager=device_manager, parameter=parameter)
#     assert request.scan_report_devices == ["samx", "samy"]
#     request.scan_report_devices = ["samx", "samz"]
#     assert request.scan_report_devices == ["samx", "samz"]


@pytest.mark.parametrize("in_args,reference_positions", [((5, 5, 1, 1), [[1, 0], [2, 0], [-2, 0]])])
def test_round_roi_scan_positions(in_args, reference_positions):
    positions = get_round_roi_scan_positions(*in_args)
    assert np.isclose(positions, reference_positions).all()


def test_round_roi_scan():
    device_manager = DMMock()
    device_manager.add_device("samx")
    scan_msg = messages.ScanQueueMessage(
        scan_type="round_roi_scan",
        parameter={
            "args": {"samx": (10,), "samy": (10,)},
            "kwargs": {"dr": 2, "nth": 4, "exp_time": 2, "relative": True},
        },
        queue="primary",
    )
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    request = RoundROIScan(
        *args, device_manager=device_manager, parameter=scan_msg.content["parameter"], **kwargs
    )
    assert set(request.scan_report_devices) == set(["samx", "samy"])
    assert request.dr == 2
    assert request.nth == 4
    assert request.exp_time == 2
    assert request.relative is True


@pytest.mark.parametrize(
    "in_args,reference_positions", [((1, 5, 1, 1), [[0, -3], [0, -7], [0, 7]])]
)
def test_round_scan_positions(in_args, reference_positions):
    positions = get_round_scan_positions(*in_args)
    assert np.isclose(positions, reference_positions).all()


@pytest.mark.parametrize(
    "in_args,reference_positions,snaked",
    [
        (([list(range(2)), list(range(2))],), [[0, 1], [0, 0], [1, 0], [1, 1]], True),
        (
            ([list(range(2)), list(range(3))],),
            [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]],
            False,
        ),
    ],
)
def test_raster_scan_positions(in_args, reference_positions, snaked):
    positions = get_2D_raster_pos(*in_args, snaked=snaked)
    assert np.isclose(positions, reference_positions).all()


@pytest.mark.parametrize(
    "in_args, center, reference_positions",
    [
        (
            [-2, 2, -2, 2],
            False,
            [
                [-0.38502947, -0.42030026],
                [0.8030152, 0.07047403],
                [-0.78349739, 0.6006928],
                [0.19856742, -1.12257337],
                [0.68409143, 1.07541569],
                [-1.34834023, -0.36246191],
                [1.33834167, -0.69508386],
                [-0.55304807, 1.51437705],
                [-0.65246146, -1.5806309],
                [1.63258446, 0.76398167],
                [-1.80382449, 0.565789],
                [0.99004828, -1.70839234],
                [-1.74471832, -1.22660425],
                [-1.46933912, 1.74339971],
                [1.70582397, 1.71416585],
                [1.95717083, -1.63324289],
            ],
        ),
        (
            [-1, 1, -1, 1],
            1,
            [
                [0.0, 0.0],
                [-0.38502947, -0.42030026],
                [0.8030152, 0.07047403],
                [-0.78349739, 0.6006928],
            ],
        ),
    ],
)
def test_get_fermat_spiral_pos(in_args, center, reference_positions):
    positions = get_fermat_spiral_pos(*in_args, center=center)
    assert np.isclose(positions, reference_positions).all()


def test_get_func_name_from_macro():
    def pre_scan_macro(devices: dict, request: RequestBase):
        pass

    device_manager = DMMock()
    device_manager.add_device("samx")
    macros = [inspect.getsource(pre_scan_macro).encode()]
    scan_msg = messages.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    assert request._get_func_name_from_macro(macros[0].decode().strip()) == "pre_scan_macro"


def test_scan_report_devices():
    device_manager = DMMock()
    device_manager.add_device("samx")
    scan_msg = messages.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    assert set(request.scan_report_devices) == set(["samx", "samy"])

    request.scan_report_devices = ["samx", "samy", "samz"]
    assert request.scan_report_devices == ["samx", "samy", "samz"]


def test_request_base_check_limits():
    class RequestBaseMock(RequestBase):
        def run(self):
            pass

    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.add_device("samy")
    scan_msg = messages.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    request = RequestBaseMock(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )

    assert request.scan_motors == ["samx", "samy"]
    assert request.device_manager.devices["samy"]._config["deviceConfig"].get("limits", [0, 0]) == [
        -50,
        50,
    ]
    request.device_manager.devices["samy"]._config["deviceConfig"]["limits"] = [5, -5]
    assert request.device_manager.devices["samy"]._config["deviceConfig"].get("limits", [0, 0]) == [
        5,
        -5,
    ]

    request.positions = [[-100, 30]]

    for ii, dev in enumerate(request.scan_motors):
        low_limit, high_limit = (
            request.device_manager.devices[dev]._config["deviceConfig"].get("limits", [0, 0])
        )
        for pos in request.positions:
            pos_axis = pos[ii]
            if low_limit >= high_limit:
                continue
            if not low_limit <= pos_axis <= high_limit:
                with pytest.raises(Exception) as exc_info:
                    request._check_limits()
                assert (
                    exc_info.value.args[0]
                    == f"Target position {pos} for motor {dev} is outside of range: [{low_limit},"
                    f" {high_limit}]"
                )
            else:
                request._check_limits()

    assert request.positions == [[-100, 30]]


def test_request_base_get_scan_motors():
    class RequestBaseMock(RequestBase):
        def run(self):
            pass

    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.add_device("samz")
    scan_msg = messages.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={"args": {"samx": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    request = RequestBaseMock(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )

    assert request.scan_motors == ["samx"]
    request.caller_args = ""
    request._get_scan_motors()
    assert request.scan_motors == ["samx"]

    request.arg_bundle_size = {"bundle": 2, "min": None, "max": None}
    request.caller_args = {"samz": (-2, 2), "samy": (-1, 2)}
    request._get_scan_motors()
    assert request.scan_motors == ["samz", "samy"]

    request.caller_args = {"samx"}
    request.arg_bundle_size = {"bundle": 0, "min": None, "max": None}
    request._get_scan_motors()
    assert request.scan_motors == ["samz", "samy", "samx"]


def test_scan_base_init():
    device_manager = DMMock()
    device_manager.add_device("samx")

    class ScanBaseMock(ScanBase):
        scan_name = ""

        def _calculate_positions(self):
            pass

    scan_msg = messages.ScanQueueMessage(
        scan_type="",
        parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    with pytest.raises(ValueError) as exc_info:
        request = ScanBaseMock(
            device_manager=device_manager, parameter=scan_msg.content["parameter"]
        )
    assert exc_info.value.args[0] == "scan_name cannot be empty"


def test_scan_base_set_position_offset():
    device_manager = DMMock()
    device_manager.add_device("samx")

    scan_msg = messages.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )

    assert request.positions == []
    request._set_position_offset()
    assert request.positions == []

    request.relative == True
    request._set_position_offset()

    start_pos_ref = [0, 0]
    request.positions += start_pos_ref
    assert request.positions == [0, 0]
    assert request.start_pos == start_pos_ref


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="lamni_fermat_scan",
                parameter={
                    "args": {},
                    "kwargs": {
                        "fov_size": [5],
                        "exp_time": 0.1,
                        "step": 2,
                        "angle": 10,
                        "scan_type": "step",
                    },
                },
                queue="primary",
                metadata={"RID": "1234"},
            ),
            [
                messages.DeviceInstructionMessage(
                    device=["rtx", "rty"],
                    action="read",
                    parameter={"wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=["rtx", "rty"],
                    action="wait",
                    parameter={"type": "read", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "controller.clear_trajectory_generator",
                        "rpc_id": "e4897d7b-f8d9-4792-ac27-375d72d02aef",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 2, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="lsamrot",
                    action="rpc",
                    parameter={
                        "device": "lsamrot",
                        "func": "user_setpoint.get",
                        "rpc_id": "7feb8d9e-b536-4958-9965-708a27c5e5f9",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 2, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={
                        "readback": {
                            "RID": "1234",
                            "devices": ["lsamrot"],
                            "start": [0],
                            "end": [10],
                        }
                    },
                    metadata={"readout_priority": "monitored", "DIID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device="lsamrot",
                    action="set",
                    parameter={"value": 10, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=["lsamrot"],
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 4},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "controller.feedback_disable",
                        "rpc_id": "a5f5167b-61f2-4c24-8a08-698c0b52a971",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 5, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "readback.get",
                        "rpc_id": "409d1afc-39a5-442b-87e5-18145e59f367",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 6, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="rty",
                    action="rpc",
                    parameter={
                        "device": "rty",
                        "func": "readback.get",
                        "rpc_id": "80e560c8-c11a-4b6c-87e3-11addea3e80d",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 7, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="lsamx",
                    action="rpc",
                    parameter={
                        "device": "lsamx",
                        "func": "readback.get",
                        "rpc_id": "5cef7087-3537-40fc-b558-8a2256019783",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 8, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="lsamy",
                    action="rpc",
                    parameter={
                        "device": "lsamy",
                        "func": "readback.get",
                        "rpc_id": "61a7376c-36cf-41af-94b1-76c1ba821d47",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 9, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "readback.get",
                        "rpc_id": "a1d3c021-12fb-483e-a5b9-95a59d3c1304",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 10, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="rty",
                    action="rpc",
                    parameter={
                        "device": "rty",
                        "func": "readback.get",
                        "rpc_id": "bde7e130-b7b7-41d0-a56a-c83d740450df",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 11, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "controller.feedback_enable_without_reset",
                        "rpc_id": "aa2117b4-ef44-4c0d-8537-6b6ccea86d1e",
                        "args": (),
                        "kwargs": {},
                    },
                    metadata={"readout_priority": "monitored", "DIID": 12, "response": True},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "scan_motors": ["rtx", "rty"],
                        "readout_priority": {
                            "monitored": [],
                            "baseline": [],
                            "on_request": [],
                            "async": [],
                        },
                        "num_points": 2,
                        "positions": [
                            [1.3681828686580249, 2.1508313829565298],
                            [-0.7700589354581364, -0.8406005210092851],
                        ],
                        "scan_name": "lamni_fermat_scan",
                        "scan_type": "step",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 13},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 14},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"readout_priority": "baseline", "DIID": 15},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="set",
                    parameter={"value": 1.3681828686580249, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 17},
                ),
                messages.DeviceInstructionMessage(
                    device="rty",
                    action="set",
                    parameter={"value": 2.1508313829565298, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 18},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 19},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 20, "pointID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0.1},
                    metadata={"readout_priority": "monitored", "DIID": 21},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 22, "pointID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 23},
                ),
                messages.DeviceInstructionMessage(
                    device="rtx",
                    action="set",
                    parameter={"value": -0.7700589354581364, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 24},
                ),
                messages.DeviceInstructionMessage(
                    device="rty",
                    action="set",
                    parameter={"value": -0.8406005210092851, "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 25},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 26},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 27},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 28, "pointID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0.1},
                    metadata={"readout_priority": "monitored", "DIID": 29},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 30, "pointID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 31},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 16},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "complete", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 31},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 17},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 18},
                ),
            ],
        )
    ],
)
def test_LamNIFermatScan(scan_msg, reference_scan_list):
    device_manager = DMMock()
    device_manager.add_device("lsamx")
    device_manager.devices["lsamx"]._config["userParameter"] = {"center": 8.1}
    device_manager.add_device("lsamy")
    device_manager.devices["lsamy"]._config["userParameter"] = {"center": 10}
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    device_manager.add_device("samy")
    device_manager.devices["samy"].read_buffer = {"value": 0}
    scan = LamNIFermatScan(
        parameter=scan_msg.content.get("parameter"),
        device_manager=device_manager,
        metadata=scan_msg.metadata,
        **scan_msg.content["parameter"]["kwargs"],
    )
    scan.stubs._get_from_rpc = lambda x: 0
    with mock.patch.object(scan, "_check_min_positions") as check_min_pos:
        scan_instructions = list(scan.run())
        check_min_pos.assert_called_once()
        scan_uid = scan_instructions[0].metadata.get("scanID")
        for ii, instr in enumerate(reference_scan_list):
            if instr.metadata.get("scanID") is not None:
                instr.metadata["scanID"] = scan_uid
            instr.metadata["DIID"] = ii
            instr.metadata["RID"] = scan.metadata.get("RID")
            if instr.content["action"] == "rpc":
                reference_scan_list[ii].content["parameter"]["rpc_id"] = scan_instructions[
                    ii
                ].content["parameter"]["rpc_id"]
            if instr.content["parameter"].get("value"):
                assert np.isclose(
                    instr.content["parameter"].get("value"),
                    scan_instructions[ii].content["parameter"].get("value"),
                )
                instr.content["parameter"]["value"] = scan_instructions[ii].content["parameter"][
                    "value"
                ]
            if instr.content["parameter"].get("positions"):
                assert np.isclose(
                    instr.content["parameter"].get("positions"),
                    scan_instructions[ii].content["parameter"].get("positions"),
                ).all()
                instr.content["parameter"]["positions"] = scan_instructions[ii].content[
                    "parameter"
                ]["positions"]
        assert scan_instructions == reference_scan_list


def test_LamNIFermatScan_min_positions():
    scan_msg = messages.ScanQueueMessage(
        scan_type="lamni_fermat_scan",
        parameter={
            "args": {},
            "kwargs": {
                "fov_size": [5],
                "exp_time": 0.1,
                "step": 2,
                "angle": 10,
                "scan_type": "step",
            },
        },
        queue="primary",
        metadata={"RID": "1234"},
    )
    device_manager = DMMock()
    device_manager.add_device("lsamx")
    device_manager.devices["lsamx"]._config["userParameter"] = {"center": 8.1}
    device_manager.add_device("lsamy")
    device_manager.devices["lsamy"]._config["userParameter"] = {"center": 10}
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    device_manager.add_device("samy")
    device_manager.devices["samy"].read_buffer = {"value": 0}
    scan = LamNIFermatScan(
        parameter=scan_msg.content.get("parameter"),
        device_manager=device_manager,
        metadata=scan_msg.metadata,
    )
    with pytest.raises(ScanAbortion):
        instructions = list(scan.run())


def test_round_scan_fly_sim_get_scan_motors():
    device_manager = DMMock()
    device_manager.add_device("flyer_sim")
    scan_msg = messages.ScanQueueMessage(
        scan_type="round_scan_fly",
        parameter={"args": {"flyer_sim": (0, 50, 5, 3)}, "kwargs": {"realtive": True}},
        queue="primary",
    )
    request = RoundScanFlySim(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )

    request._get_scan_motors()
    assert request.scan_motors == []
    assert request.flyer == list(scan_msg.content["parameter"]["args"].keys())[0]


def test_round_scan_fly_sim_prepare_positions():
    device_manager = DMMock()
    device_manager.add_device("flyer_sim")
    scan_msg = messages.ScanQueueMessage(
        scan_type="round_scan_fly",
        parameter={"args": {"flyer_sim": (0, 50, 5, 3)}, "kwargs": {"realtive": True}},
        queue="primary",
    )
    request = RoundScanFlySim(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    request._calculate_positions = mock.MagicMock()
    request._check_limits = mock.MagicMock()
    pos = [1, 2, 3, 4]
    request.positions = pos

    next(request.prepare_positions())

    request._calculate_positions.assert_called_once()
    assert request.num_pos == len(pos)
    request._check_limits.assert_called_once()


@pytest.mark.parametrize(
    "in_args,reference_positions", [((1, 5, 1, 1), [[0, -3], [0, -7], [0, 7]])]
)
def test_round_scan_fly_sim_calculate_positions(in_args, reference_positions):
    device_manager = DMMock()
    device_manager.add_device("flyer_sim")
    scan_msg = messages.ScanQueueMessage(
        scan_type="round_scan_fly",
        parameter={"args": {"flyer_sim": in_args}, "kwargs": {"realtive": True}},
        queue="primary",
    )
    request = RoundScanFlySim(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )

    request._calculate_positions()
    assert np.isclose(request.positions, reference_positions).all()


@pytest.mark.parametrize(
    "in_args,reference_positions", [((1, 5, 1, 1), [[0, -3], [0, -7], [0, 7]])]
)
def test_round_scan_fly_sim_scan_core(in_args, reference_positions):
    device_manager = DMMock()
    device_manager.add_device("flyer_sim")
    scan_msg = messages.ScanQueueMessage(
        scan_type="round_scan_fly",
        parameter={"args": {"flyer_sim": in_args}, "kwargs": {"realtive": True}},
        queue="primary",
    )
    request = RoundScanFlySim(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    request.positions = np.array(reference_positions)

    ret = next(request.scan_core())
    assert ret == messages.DeviceInstructionMessage(
        device="flyer_sim",
        action="kickoff",
        parameter={
            "configure": {"num_pos": None, "positions": reference_positions, "exp_time": 0},
            "wait_group": "kickoff",
        },
        metadata={"readout_priority": "monitored", "DIID": 0},
    )


@pytest.mark.parametrize(
    "in_args,reference_positions",
    [
        (
            [[-3, 3], [-2, 2]],
            [
                [-3.0, -2.0],
                [-2.33333333, -1.55555556],
                [-1.66666667, -1.11111111],
                [-1.0, -0.66666667],
                [-0.33333333, -0.22222222],
                [0.33333333, 0.22222222],
                [1.0, 0.66666667],
                [1.66666667, 1.11111111],
                [2.33333333, 1.55555556],
                [3.0, 2.0],
            ],
        ),
        (
            [[-1, 1], [-1, 2]],
            [
                [-1.0, -1.0],
                [-0.77777778, -0.66666667],
                [-0.55555556, -0.33333333],
                [-0.33333333, 0.0],
                [-0.11111111, 0.33333333],
                [0.11111111, 0.66666667],
                [0.33333333, 1.0],
                [0.55555556, 1.33333333],
                [0.77777778, 1.66666667],
                [1.0, 2.0],
            ],
        ),
    ],
)
def test_line_scan_calculate_positions(in_args, reference_positions):
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="line_scan",
        parameter={
            "args": {"samx": in_args[0], "samy": in_args[1]},
            "kwargs": {"relative": True, "steps": 10},
        },
        queue="primary",
    )
    request = LineScan(
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )

    request._calculate_positions()
    assert np.isclose(request.positions, reference_positions).all()


def test_list_scan_calculate_positions():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="list_scan",
        parameter={
            "args": {"samx": [[0, 1, 2, 3, 4]], "samy": [[0, 1, 2, 3, 4]]},
            "kwargs": {"realtive": True},
        },
        queue="primary",
    )

    request = ListScan(device_manager=device_manager, parameter=scan_msg.content["parameter"])
    request._calculate_positions()
    assert np.isclose(request.positions, [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]).all()


def test_list_scan_raises_for_different_lengths():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="list_scan",
        parameter={
            "args": {"samx": [[0, 1, 2, 3, 4]], "samy": [[0, 1, 2, 3]]},
            "kwargs": {"realtive": True},
        },
        queue="primary",
    )
    with pytest.raises(ValueError):
        ListScan(device_manager=device_manager, parameter=scan_msg.content["parameter"])


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="time_scan",
                parameter={
                    "args": {},
                    "kwargs": {"points": 3, "interval": 1, "exp_time": 0.1, "relative": True},
                },
                queue="primary",
            ),
            [
                messages.DeviceInstructionMessage(
                    device=[],
                    action="read",
                    parameter={"wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=[],
                    action="wait",
                    parameter={"type": "read", "wait_group": "scan_motor"},
                    metadata={"readout_priority": "monitored", "DIID": 1},
                ),
                None,
                None,
                messages.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "scan_motors": [],
                        "readout_priority": {
                            "monitored": [],
                            "baseline": [],
                            "on_request": [],
                            "async": [],
                        },
                        "num_points": 3,
                        "positions": [],
                        "scan_name": "time_scan",
                        "scan_type": "step",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 2},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 3},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"readout_priority": "baseline", "DIID": 4},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "pre_scan", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 5},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 6, "pointID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "time": 0.1, "group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 7},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 8, "pointID": 0},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "time": 0.9, "group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 9},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 10},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 11, "pointID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "time": 0.1, "group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 12},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 13, "pointID": 1},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "time": 0.9, "group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 14},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 15},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 16, "pointID": 2},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "time": 0.1, "group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 17},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 18, "pointID": 2},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "time": 0.9, "group": "trigger"},
                    metadata={"readout_priority": "monitored", "DIID": 19},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 20},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "complete", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 21},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 22},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 23},
                ),
            ],
        )
    ],
)
def test_time_scan(scan_msg, reference_scan_list):
    device_manager = DMMock()
    request = TimeScan(
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )
    scan_instructions = list(request.run())
    assert scan_instructions == reference_scan_list


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            messages.ScanQueueMessage(
                scan_type="otf_scan",
                parameter={"args": {}, "kwargs": {"e1": 700, "e2": 740, "time": 4}},
                queue="primary",
                metadata={"RID": "1234"},
            ),
            [
                None,
                None,
                None,
                messages.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "scan_motors": [],
                        "readout_priority": {
                            "monitored": [],
                            "baseline": [],
                            "on_request": [],
                            "async": [],
                        },
                        "num_points": 0,
                        "positions": [],
                        "scan_name": "otf_scan",
                        "scan_type": "fly",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 0, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 1, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"readout_priority": "baseline", "DIID": 2, "RID": "1234"},
                ),
                None,
                messages.DeviceInstructionMessage(
                    device="mono",
                    action="set",
                    parameter={"value": 700, "wait_group": "flyer"},
                    metadata={"readout_priority": "monitored", "DIID": 3, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=["mono"],
                    action="wait",
                    parameter={"type": "move", "wait_group": "flyer"},
                    metadata={"readout_priority": "monitored", "DIID": 4, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device="otf",
                    action="kickoff",
                    parameter={
                        "configure": {"e1": 700, "e2": 740, "time": 4},
                        "wait_group": "kickoff",
                    },
                    metadata={"readout_priority": "monitored", "DIID": 5, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=["otf"],
                    action="wait",
                    parameter={"type": "move", "wait_group": "kickoff"},
                    metadata={"readout_priority": "monitored", "DIID": 6, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device="otf",
                    action="complete",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 7, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={"group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 8, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 9, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"readout_priority": "monitored", "DIID": 10, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    **{"device": None, "action": "complete", "parameter": {}},
                    metadata={"readout_priority": "monitored", "DIID": 11, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 12, "RID": "1234"},
                ),
                messages.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"readout_priority": "monitored", "DIID": 13, "RID": "1234"},
                ),
            ],
        )
    ],
)
def test_otf_scan(scan_msg, reference_scan_list):
    device_manager = DMMock()
    request = OTFScan(
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        metadata=scan_msg.metadata,
    )
    with mock.patch.object(request.stubs, "get_req_status", return_value=1):
        scan_instructions = list(request.run())
    assert scan_instructions == reference_scan_list


@pytest.mark.parametrize(
    "scan_msg",
    [
        messages.ScanQueueMessage(
            scan_type="owis_grid",
            parameter={
                "args": {
                    "start_y": 0,
                    "end_y": 1,
                    "interval_y": 10,
                    "start_x": 0,
                    "end_x": 1,
                    "interval_x": 5,
                },
                "kwargs": {"exp_time": 0.1, "readout_time": 3e-3},
            },
            queue="primary",
            metadata={"RID": "1234"},
        )
    ],
)
def test_owis_grid(scan_msg):
    dm = mock.MagicMock()
    request = OwisGrid(*scan_msg.content["parameter"]["args"].values(), device_manager=dm)
    request.high_velocity = 10
    request.high_acc_time = 0.2
    request.base_velocity = 0.0625
    # pylint: disable=protected-access
    request.stubs._get_from_rpc = lambda x: mock.MagicMock()
    with mock.patch.object(request.stubs, "get_req_status", return_value=1), mock.patch.object(
        request, "get_initial_motor_properties"
    ) as mock_get_init_motor_properties:
        scan_instructions = list(request.run())
        mock_get_init_motor_properties.assert_called_once()
        assert request.pointID == scan_msg.content["parameter"]["args"]["interval_x"]
        assert np.isclose(
            request.target_velocity,
            (
                (
                    scan_msg.content["parameter"]["args"]["end_y"]
                    - scan_msg.content["parameter"]["args"]["start_y"]
                )
                / scan_msg.content["parameter"]["args"]["interval_y"]
            )
            / (
                scan_msg.content["parameter"]["kwargs"]["exp_time"]
                + scan_msg.content["parameter"]["kwargs"]["readout_time"]
            ),
            rtol=1e-2,
        )


def test_monitor_scan():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="monitor_scan",
        parameter={"args": {"samx": [-5, 5]}, "kwargs": {"relative": True, "exp_time": 0.1}},
        queue="primary",
    )
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    request = MonitorScan(
        *args,
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )
    request._calculate_positions()
    assert np.isclose(request.positions, [[-5], [5]]).all()


def test_monitor_scan_run():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="monitor_scan",
        parameter={"args": {"samx": [-5, 5]}, "kwargs": {"relative": True, "exp_time": 0.1}},
        queue="primary",
    )
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    request = MonitorScan(
        *args,
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )
    with mock.patch.object(request, "_get_flyer_status") as flyer_status:
        with mock.patch.object(request, "_check_limits") as check_limits:
            with mock.patch.object(request, "_set_position_offset") as position_offset:
                flyer_status.side_effect = [
                    (None, None),
                    (None, None),
                    (None, messages.DeviceMessage(signals={"rb1": {"value": 1}})),
                    (True, None),
                ]
                ref_list = list(request.run())
                assert ref_list == [
                    messages.DeviceInstructionMessage(
                        device=["samx"],
                        action="read",
                        parameter={"wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 0},
                    ),
                    messages.DeviceInstructionMessage(
                        device=["samx"],
                        action="wait",
                        parameter={"type": "read", "wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 1},
                    ),
                    None,
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="open_scan",
                        parameter={
                            "scan_motors": ["samx"],
                            "readout_priority": {
                                "monitored": ["samx"],
                                "baseline": [],
                                "on_request": [],
                                "async": [],
                            },
                            "num_points": 0,
                            "positions": [[-5], [5]],
                            "scan_name": "monitor_scan",
                            "scan_type": "fly",
                        },
                        metadata={"readout_priority": "monitored", "DIID": 2},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="stage",
                        parameter={},
                        metadata={"readout_priority": "monitored", "DIID": 3},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="baseline_reading",
                        parameter={},
                        metadata={"readout_priority": "baseline", "DIID": 4},
                    ),
                    messages.DeviceInstructionMessage(
                        device="samx",
                        action="set",
                        parameter={"value": -5, "wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 5},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="wait",
                        parameter={
                            "type": "move",
                            "group": "scan_motor",
                            "wait_group": "scan_motor",
                        },
                        metadata={"readout_priority": "monitored", "DIID": 6},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="pre_scan",
                        parameter={},
                        metadata={"readout_priority": "monitored", "DIID": 7},
                    ),
                    messages.DeviceInstructionMessage(
                        device="samx",
                        action="set",
                        parameter={"value": -5, "wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 8},
                    ),
                    messages.DeviceInstructionMessage(
                        device="samx",
                        action="wait",
                        parameter={"type": "move", "wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 9},
                    ),
                    messages.DeviceInstructionMessage(
                        device="samx",
                        action="set",
                        parameter={"value": 5, "wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 10, "response": True},
                    ),
                    messages.DeviceInstructionMessage(
                        device="samx",
                        action="publish_data_as_read",
                        parameter={"data": {"samx": {"rb1": {"value": 1}}}},
                        metadata={"readout_priority": "monitored", "DIID": 11, "pointID": 0},
                    ),
                    messages.DeviceInstructionMessage(
                        device="samx",
                        action="set",
                        parameter={"value": 0, "wait_group": "scan_motor"},
                        metadata={"readout_priority": "monitored", "DIID": 12},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="wait",
                        parameter={
                            "type": "move",
                            "group": "scan_motor",
                            "wait_group": "scan_motor",
                        },
                        metadata={"readout_priority": "monitored", "DIID": 13},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="wait",
                        parameter={
                            "type": "read",
                            "group": "primary",
                            "wait_group": "readout_primary",
                        },
                        metadata={"readout_priority": "monitored", "DIID": 14},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="complete",
                        parameter={},
                        metadata={"readout_priority": "monitored", "DIID": 15},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="unstage",
                        parameter={},
                        metadata={"readout_priority": "monitored", "DIID": 16},
                    ),
                    messages.DeviceInstructionMessage(
                        device=None,
                        action="close_scan",
                        parameter={},
                        metadata={"readout_priority": "monitored", "DIID": 17},
                    ),
                ]


def test_OpenInteractiveScan():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="open_interactive_scan",
        parameter={"args": {"samx": []}, "kwargs": {"relative": True, "exp_time": 0.1}},
        queue="primary",
    )
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    request = OpenInteractiveScan(
        *args,
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )
    ref_list = list(request.run())
    assert ref_list == [
        messages.DeviceInstructionMessage(
            device=None,
            action="open_scan_def",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 0},
        ),
        messages.DeviceInstructionMessage(
            device=["samx"],
            action="read",
            parameter={"wait_group": "scan_motor"},
            metadata={"readout_priority": "monitored", "DIID": 1},
        ),
        messages.DeviceInstructionMessage(
            device=["samx"],
            action="wait",
            parameter={"type": "read", "wait_group": "scan_motor"},
            metadata={"readout_priority": "monitored", "DIID": 2},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="open_scan",
            parameter={
                "scan_motors": ["samx"],
                "readout_priority": {
                    "monitored": ["samx"],
                    "baseline": [],
                    "on_request": [],
                    "async": [],
                },
                "num_points": None,
                "positions": [],
                "scan_name": "open_interactive_scan",
                "scan_type": "step",
            },
            metadata={"readout_priority": "monitored", "DIID": 3},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="stage",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 4},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="baseline_reading",
            parameter={},
            metadata={"readout_priority": "baseline", "DIID": 5},
        ),
    ]


def test_AddInteractiveScanPointn():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="interactive_scan_trigger",
        parameter={"args": {"samx": []}, "kwargs": {"relative": True, "exp_time": 0.1}},
        queue="primary",
    )
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    request = AddInteractiveScanPoint(
        *args,
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )
    ref_list = list(request.run())
    assert ref_list == [
        messages.DeviceInstructionMessage(
            device=None,
            action="open_scan",
            parameter={
                "scan_motors": ["samx"],
                "readout_priority": {
                    "monitored": ["samx"],
                    "baseline": [],
                    "on_request": [],
                    "async": [],
                },
                "num_points": None,
                "positions": [],
                "scan_name": "interactive_scan_trigger",
                "scan_type": "step",
            },
            metadata={"readout_priority": "monitored", "DIID": 0},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="trigger",
            parameter={"group": "trigger"},
            metadata={"readout_priority": "monitored", "DIID": 1, "pointID": 0},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="wait",
            parameter={"type": "trigger", "time": 0.1, "group": "trigger"},
            metadata={"readout_priority": "monitored", "DIID": 2},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="read",
            parameter={"group": "primary", "wait_group": "readout_primary"},
            metadata={"readout_priority": "monitored", "DIID": 3, "pointID": 0},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="wait",
            parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
            metadata={"readout_priority": "monitored", "DIID": 4},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="close_scan",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 5},
        ),
    ]


def test_CloseInteractiveScan():
    device_manager = DMMock()
    device_manager.add_device("samx")
    scan_msg = messages.ScanQueueMessage(
        scan_type="close_interactive_scan",
        parameter={"args": {"samx": []}, "kwargs": {"relative": True, "exp_time": 0.1}},
        queue="primary",
    )
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    kwargs = scan_msg.content["parameter"]["kwargs"]
    request = CloseInteractiveScan(
        *args,
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )
    ref_list = list(request.run())
    assert ref_list == [
        messages.DeviceInstructionMessage(
            device="samx",
            action="set",
            parameter={"value": 0, "wait_group": "scan_motor"},
            metadata={"readout_priority": "monitored", "DIID": 0},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="wait",
            parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
            metadata={"readout_priority": "monitored", "DIID": 1},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="wait",
            parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
            metadata={"readout_priority": "monitored", "DIID": 2},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="complete",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 3},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="unstage",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 4},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="close_scan",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 5},
        ),
        messages.DeviceInstructionMessage(
            device=None,
            action="close_scan_def",
            parameter={},
            metadata={"readout_priority": "monitored", "DIID": 6},
        ),
    ]


def test_RoundScan():
    device_manager = DMMock()
    scan_msg = messages.ScanQueueMessage(
        scan_type="round_scan",
        parameter={
            "args": {"samx": ["samy", 1, 2, 1, 3]},
            "kwargs": {"relative": True, "steps": 10},
        },
        queue="primary",
    )
    #     "motor_1": ScanArgType.DEVICE,
    # "motor_2": ScanArgType.DEVICE,
    # "inner_ring": ScanArgType.FLOAT,
    # "outer_ring": ScanArgType.FLOAT,
    # "number_of_rings": ScanArgType.INT,
    # "number_of_positions_in_first_ring": ScanArgType.INT,
    args = unpack_scan_args(scan_msg.content["parameter"]["args"])
    request = RoundScan(
        *args,
        device_manager=device_manager,
        parameter=scan_msg.content["parameter"],
        **scan_msg.content["parameter"]["kwargs"],
    )

    with mock.patch.object(request, "_check_limits") as check_limits:
        with mock.patch.object(request, "_set_position_offset") as position_offset:
            ref = list(request.run())
            assert len(ref) == 88
