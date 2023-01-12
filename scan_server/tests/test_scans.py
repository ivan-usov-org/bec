import collections
import inspect
from unittest import mock

import numpy as np
import pytest
from bec_utils import BECMessage as BMessage
from bec_utils.devicemanager import DeviceContainer
from bec_utils.tests.utils import ProducerMock

from scan_plugins.LamNIFermatScan import LamNIFermatScan
from scan_server.scans import (
    Acquire,
    ContLineScan,
    DeviceRPC,
    FermatSpiralScan,
    Move,
    RequestBase,
    ScanBase,
    Scan,
    UpdatedMove,
    get_2D_raster_pos,
    get_fermat_spiral_pos,
    get_round_roi_scan_positions,
    get_round_scan_positions,
)

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


class DeviceMock:
    def __init__(self, name: str):
        self.name = name
        self.read_buffer = None
        self._config = {"deviceConfig": {"limits": [-50, 50]}, "userParameter": None}
        self._enabled_set = True
        self._enabled = True

    def read(self):
        return self.read_buffer

    def readback(self):
        return self.read_buffer

    @property
    def enabled_set(self) -> bool:
        return self._enabled_set

    @enabled_set.setter
    def enabled_set(self, val: bool):
        self._enabled_set = val

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
    producer = ProducerMock()

    def add_device(self, name):
        self.devices[name] = DeviceMock(name)


@pytest.mark.parametrize(
    "mv_msg,reference_msg_list",
    [
        (
            BMessage.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,), "samy": (2,)}, "kwargs": {}},
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0, "response": True},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 1, "response": True},
                ),
            ],
        ),
        (
            BMessage.ScanQueueMessage(
                scan_type="mv",
                parameter={
                    "args": {"samx": (1,), "samy": (2,), "samz": (3,)},
                    "kwargs": {},
                },
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0, "response": True},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 1, "response": True},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samz",
                    action="set",
                    parameter={"value": 3, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 2, "response": True},
                ),
            ],
        ),
        (
            BMessage.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,)}, "kwargs": {}},
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0, "response": True},
                ),
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
            BMessage.ScanQueueMessage(
                scan_type="umv",
                parameter={"args": {"samx": (1,), "samy": (2,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "0bab7ee3-b384-4571-b...0fff984c05"},
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={"readback": "0bab7ee3-b384-4571-b...0fff984c05"},
                    metadata={
                        "stream": "primary",
                        "DIID": 0,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1.0, "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 1,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2.0, "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 2,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 3,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 4,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
            ],
        ),
        (
            BMessage.ScanQueueMessage(
                scan_type="umv",
                parameter={
                    "args": {"samx": (1,), "samy": (2,), "samz": (3,)},
                    "kwargs": {},
                },
                queue="primary",
                metadata={"RID": "0bab7ee3-b384-4571-b...0fff984c05"},
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={"readback": "0bab7ee3-b384-4571-b...0fff984c05"},
                    metadata={
                        "stream": "primary",
                        "DIID": 0,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1.0, "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 1,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2.0, "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 2,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samz",
                    action="set",
                    parameter={"value": 3.0, "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 3,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 4,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 5,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samz",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 6,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
            ],
        ),
        (
            BMessage.ScanQueueMessage(
                scan_type="umv",
                parameter={"args": {"samx": (1,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "0bab7ee3-b384-4571-b...0fff984c05"},
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="scan_report_instruction",
                    parameter={"readback": "0bab7ee3-b384-4571-b...0fff984c05"},
                    metadata={
                        "stream": "primary",
                        "DIID": 0,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={"value": 1.0, "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
                        "DIID": 1,
                        "RID": "0bab7ee3-b384-4571-b...0fff984c05",
                    },
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={
                        "stream": "primary",
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
            BMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=["samx"],
                    action="read",
                    parameter={
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["samx"],
                    action="wait",
                    parameter={
                        "type": "read",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "primary": ["samx"],
                        "num_points": 3,
                        "positions": [[-5.0], [0.0], [5.0]],
                        "scan_name": "grid_scan",
                        "scan_type": "step",
                    },
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"stream": "baseline", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": -5.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "move",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 0, "stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"pointID": 0, "stream": "primary", "DIID": 5},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 6},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": 0.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 7},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "move",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 8},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 9},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 1, "stream": "primary", "DIID": 10},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 11},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"pointID": 1, "stream": "primary", "DIID": 12},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 13},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": 5.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 14},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "move",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 15},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 16},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 2, "stream": "primary", "DIID": 17},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "trigger",
                        "group": "trigger",
                        "time": 0.1,
                    },
                    metadata={"stream": "primary", "DIID": 18},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"pointID": 2, "stream": "primary", "DIID": 19},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 20},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": 0.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 21},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "move",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 22},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 23},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 24},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 25},
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
            BMessage.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={
                    "args": {"samx": (-5, 5), "samy": (-5, 5)},
                    "kwargs": {"step": 3},
                },
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
            BMessage.ScanQueueMessage(
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
    scan = FermatSpiralScan(
        parameter=scan_msg.content.get("parameter"), device_manager=device_manager
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
            BMessage.ScanQueueMessage(
                scan_type="cont_line_scan",
                parameter={"args": {"samx": (-5, 5)}, "kwargs": {"steps": 3, "exp_time": 0.1}},
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=["samx"],
                    action="read",
                    parameter={
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["samx"],
                    action="wait",
                    parameter={
                        "type": "read",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "primary": ["samx"],
                        "num_points": 3,
                        "positions": [[-5.0], [0.0], [5.0]],
                        "scan_name": "cont_line_scan",
                        "scan_type": "step",
                    },
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"stream": "baseline", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": -105.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "move",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": 5.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 7},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 0, "stream": "primary", "DIID": 8},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "primary",
                    },
                    metadata={"pointID": 0, "stream": "primary", "DIID": 9},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 1, "stream": "primary", "DIID": 10},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "primary",
                    },
                    metadata={"pointID": 1, "stream": "primary", "DIID": 11},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 2, "stream": "primary", "DIID": 12},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "primary",
                    },
                    metadata={"pointID": 2, "stream": "primary", "DIID": 13},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="set",
                    parameter={
                        "value": 0.0,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 14},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "move",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 15},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 16},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 17},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 18},
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

    scan = ContLineScan(parameter=scan_msg.content.get("parameter"), device_manager=device_manager)
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
        BMessage.DeviceInstructionMessage(
            device="samx",
            action="rpc",
            parameter=parameter,
            metadata={"stream": "primary", "DIID": 0},
        )
    ]


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            BMessage.ScanQueueMessage(
                scan_type="acquire",
                parameter={"args": [], "kwargs": {"exp_time": 1.0}},
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "primary": [],
                        "num_points": 1,
                        "positions": [],
                        "scan_name": "acquire",
                        "scan_type": "step",
                    },
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"stream": "baseline", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"pointID": 0, "stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 1},
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"pointID": 0, "stream": "primary", "DIID": 5},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"stream": "primary", "DIID": 6},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 17},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 18},
                ),
            ],
        )
    ],
)
def test_acquire(scan_msg, reference_scan_list):
    device_manager = DMMock()
    parameter = {
        "args": [],
        "kwargs": {"exp_time": 1},
    }

    scan = Acquire(parameter=parameter, device_manager=device_manager)
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
    scan_msg = BMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    with mock.patch.object(
        request.device_manager.producer,
        "lrange",
        new_callable=mock.PropertyMock,
        return_value=macros,
    ) as macros_mock:
        with mock.patch.object(request, "_get_func_name_from_macro", return_value="pre_scan_macro"):
            with mock.patch("builtins.eval") as eval_mock:
                request.initialize()
                eval_mock.assert_called_once_with("pre_scan_macro")


def test_scan_report_devices():
    device_manager = DMMock()
    device_manager.add_device("samx")
    parameter = {
        "args": {"samx": (-5, 5), "samy": (-5, 5)},
        "kwargs": {"step": 3},
    }
    request = FermatSpiralScan(device_manager=device_manager, parameter=parameter)
    assert request.scan_report_devices == ["samx", "samy"]
    request.scan_report_devices = ["samx", "samz"]
    assert request.scan_report_devices == ["samx", "samz"]


@pytest.mark.parametrize("in_args,reference_positions", [((5, 5, 1, 1), [[1, 0], [2, 0], [-2, 0]])])
def test_round_roi_scan_positions(in_args, reference_positions):
    positions = get_round_roi_scan_positions(*in_args)
    assert np.isclose(positions, reference_positions).all()


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
    "in_args",
    [
        ([-2, 2, -2, 2]),
        ([-1, 1, -3, 3]),
    ],
)
def test_get_fermat_spiral_pos(in_args):
    positions = get_fermat_spiral_pos(*in_args)

    ref_positions = []
    phi = 2 * np.pi * ((1 + np.sqrt(5)) / 2.0)

    start = 1

    length_axis1 = abs(in_args[1] - in_args[0])
    length_axis2 = abs(in_args[3] - in_args[2])
    n_max = int(length_axis1 * length_axis2 * 3.2)

    for ii in range(start, n_max):
        radius = 0.57 * np.sqrt(ii)
        if abs(radius * np.sin(ii * phi)) > length_axis1 / 2:
            continue
        if abs(radius * np.cos(ii * phi)) > length_axis2 / 2:
            continue
        ref_positions.extend([(radius * np.sin(ii * phi), radius * np.cos(ii * phi))])
    ref_positions = np.array(ref_positions)

    assert np.isclose(positions, ref_positions).all()


def test_get_func_name_from_macro():
    def pre_scan_macro(devices: dict, request: RequestBase):
        pass

    device_manager = DMMock()
    device_manager.add_device("samx")
    macros = [inspect.getsource(pre_scan_macro).encode()]
    scan_msg = BMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    assert request._get_func_name_from_macro(macros[0].decode().strip()) == "pre_scan_macro"


def test_scan_report_devices():
    device_manager = DMMock()
    device_manager.add_device("samx")
    scan_msg = BMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )
    assert request.scan_report_devices == ["samx", "samy"]

    request.scan_report_devices = ["samx", "samy", "samz"]
    assert request.scan_report_devices == ["samx", "samy", "samz"]


def test_request_base_check_limits():
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.add_device("samy")
    scan_msg = BMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    request = FermatSpiralScan(
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
                    == f"Target position {pos} for motor {dev} is outside of range: [{low_limit}, {high_limit}]"
                )
            else:
                request._check_limits()

    assert request.positions == [[-100, 30]]


def test_request_get_scan_motors():
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.add_device("samz")
    scan_msg = BMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    request = FermatSpiralScan(
        device_manager=device_manager, parameter=scan_msg.content["parameter"]
    )

    assert request.caller_args == scan_msg.content["parameter"]["args"]
    assert request.scan_motors == ["samx", "samy"]

    request.caller_args = {"samz": (-2, 2)}
    request.arg_bundle_size = 0
    request._get_scan_motors()
    assert request.scan_motors == ["samx", "samy", "samz"]


def test_scan_base_init():
    device_manager = DMMock()
    device_manager.add_device("samx")

    class ScanBaseMock(ScanBase):
        scan_name = ""

        def _calculate_positions(self):
            pass

    scan_msg = BMessage.ScanQueueMessage(
        scan_type="",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    with pytest.raises(ValueError) as exc_info:
        request = ScanBaseMock(
            device_manager=device_manager, parameter=scan_msg.content["parameter"]
        )
    assert exc_info.value.args[0] == "scan_name cannot be empty"


@pytest.mark.parametrize(
    "scan_msg,reference_scan_list",
    [
        (
            BMessage.ScanQueueMessage(
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
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=["rtx", "rty"],
                    action="read",
                    parameter={"wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["rtx", "rty"],
                    action="wait",
                    parameter={"type": "read", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "controller.clear_trajectory_generator",
                        "rpc_id": "e4897d7b-f8d9-4792-ac27-375d72d02aef",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device="lsamrot",
                    action="rpc",
                    parameter={
                        "device": "lsamrot",
                        "func": "user_setpoint.get",
                        "rpc_id": "7feb8d9e-b536-4958-9965-708a27c5e5f9",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device="lsamrot",
                    action="set",
                    parameter={"value": 10, "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["lsamrot"],
                    action="wait",
                    parameter={"type": "move", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "controller.feedback_disable",
                        "rpc_id": "a5f5167b-61f2-4c24-8a08-698c0b52a971",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 5},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "readback.get",
                        "rpc_id": "409d1afc-39a5-442b-87e5-18145e59f367",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 6},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rty",
                    action="rpc",
                    parameter={
                        "device": "rty",
                        "func": "readback.get",
                        "rpc_id": "80e560c8-c11a-4b6c-87e3-11addea3e80d",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 7},
                ),
                BMessage.DeviceInstructionMessage(
                    device="lsamx",
                    action="rpc",
                    parameter={
                        "device": "lsamx",
                        "func": "readback.get",
                        "rpc_id": "5cef7087-3537-40fc-b558-8a2256019783",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 8},
                ),
                BMessage.DeviceInstructionMessage(
                    device="lsamy",
                    action="rpc",
                    parameter={
                        "device": "lsamy",
                        "func": "readback.get",
                        "rpc_id": "61a7376c-36cf-41af-94b1-76c1ba821d47",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 9},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "readback.get",
                        "rpc_id": "a1d3c021-12fb-483e-a5b9-95a59d3c1304",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 10},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rty",
                    action="rpc",
                    parameter={
                        "device": "rty",
                        "func": "readback.get",
                        "rpc_id": "bde7e130-b7b7-41d0-a56a-c83d740450df",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 11},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="rpc",
                    parameter={
                        "device": "rtx",
                        "func": "controller.feedback_enable_without_reset",
                        "rpc_id": "aa2117b4-ef44-4c0d-8537-6b6ccea86d1e",
                        "args": [],
                        "kwargs": {},
                    },
                    metadata={"stream": "primary", "DIID": 12},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={
                        "primary": ["rtx", "rty"],
                        "num_points": 2,
                        "positions": [
                            [1.3681828686580249, 2.1508313829565298],
                            [-0.7700589354581364, -0.8406005210092851],
                        ],
                        "scan_name": "lamni_fermat_scan",
                        "scan_type": "step",
                    },
                    metadata={"stream": "primary", "DIID": 13},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="stage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 14},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="baseline_reading",
                    parameter={},
                    metadata={"stream": "baseline", "DIID": 15},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="set",
                    parameter={
                        "value": 1.3681828686580249,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 17},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rty",
                    action="set",
                    parameter={
                        "value": 2.1508313829565298,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 18},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 19},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"stream": "primary", "DIID": 20, "pointID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 21},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 22, "pointID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 23},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rtx",
                    action="set",
                    parameter={
                        "value": -0.7700589354581364,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 24},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rty",
                    action="set",
                    parameter={
                        "value": -0.8406005210092851,
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 25},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 26},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"stream": "primary", "DIID": 27},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="trigger",
                    parameter={"group": "trigger"},
                    metadata={"stream": "primary", "DIID": 28, "pointID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "trigger", "group": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 29},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "group": "primary",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 30, "pointID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "readout_primary",
                    },
                    metadata={"stream": "primary", "DIID": 31},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="wait",
                    parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
                    metadata={"stream": "primary", "DIID": 16},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="unstage",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 17},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="close_scan",
                    parameter={},
                    metadata={"stream": "primary", "DIID": 18},
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
        parameter=scan_msg.content.get("parameter"), device_manager=device_manager
    )
    scan.stubs._get_from_rpc = lambda x: 0
    scan_instructions = list(scan.run())
    scan_uid = scan_instructions[0].metadata.get("scanID")
    for ii, instr in enumerate(reference_scan_list):
        if instr.metadata.get("scanID") is not None:
            instr.metadata["scanID"] = scan_uid
        instr.metadata["DIID"] = ii
        if instr.content["action"] == "rpc":
            reference_scan_list[ii].content["parameter"]["rpc_id"] = scan_instructions[ii].content[
                "parameter"
            ]["rpc_id"]
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
            instr.content["parameter"]["positions"] = scan_instructions[ii].content["parameter"][
                "positions"
            ]
    assert scan_instructions == reference_scan_list
