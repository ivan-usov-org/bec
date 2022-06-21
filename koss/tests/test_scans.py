import numpy as np
import pytest
from bec_utils import BECMessage as BMessage
from koss.scans import FermatSpiralScan, Move, Scan


class DeviceMock:
    def __init__(self, name: str):
        self.name = name
        self.read_buffer = None
        self._device_config = {"limits": [-50, 50]}

    def read(self):
        return self.read_buffer

    def readback(self):
        return self.read_buffer

    @property
    def deviceConfig(self):
        return self._device_config


class DMMock:
    devices = {}

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
                    parameter={"value": 1, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 3},
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
                    parameter={"value": 1, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="set",
                    parameter={"value": 2, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 1},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samz",
                    action="set",
                    parameter={"value": 3, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 2},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samy",
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samz",
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 5},
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
                    parameter={"value": 1, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device="samx",
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 1},
                ),
            ],
        ),
    ],
)
def test_scan_move(mv_msg, reference_msg_list):
    msg_list = []
    dm = DMMock()
    dm.add_device("samx")
    dm.devices["samx"].read_buffer = {"value": 0}
    dm.add_device("samy")
    dm.devices["samy"].read_buffer = {"value": 0}
    dm.add_device("samz")
    dm.devices["samz"].read_buffer = {"value": 0}
    s = Move(parameter=mv_msg.content.get("parameter"), devicemanager=dm)
    for step in s.run():
        msg_list.append(step)

    assert msg_list == reference_msg_list


# def test_scan_positions():
#     samx = DummyObject("samx")
#     pos = []
#     for s in Scan.scan(samx, -5, 5, 10, exp_time=0.1):
#         pos.append(s)


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
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["samx"],
                    action="wait",
                    parameter={
                        "type": "read",
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="open_scan",
                    parameter={"primary": ["samx"], "num_points": 3, "scan_name": "grid_scan"},
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
                        "group": "scan_motor",
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
                    parameter={"type": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 4},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "target": "primary",
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
                        "group": "scan_motor",
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
                    parameter={"type": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 11},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "target": "primary",
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
                        "group": "scan_motor",
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
                        "time": 0.1,
                    },
                    metadata={"stream": "primary", "DIID": 18},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "target": "primary",
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
                        "group": "scan_motor",
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
    dm = DMMock()
    dm.add_device("samx")
    dm.devices["samx"].read_buffer = {"value": 0}
    msg_list = []
    for step in Scan.scan(parameter=scan_msg.content.get("parameter"), devicemanager=dm):
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
    dm = DMMock()
    dm.add_device("samx")
    dm.devices["samx"].read_buffer = {"value": 0}
    dm.add_device("samy")
    dm.devices["samy"].read_buffer = {"value": 0}
    scan = FermatSpiralScan(parameter=scan_msg.content.get("parameter"), devicemanager=dm)
    scan.prepare_positions()
    # pylint: disable=protected-access
    pos = list(scan._get_position())
    assert pytest.approx(np.vstack(np.array(pos, dtype=object)[:, 1])) == np.vstack(
        np.array(reference_scan_list, dtype=object)[:, 1]
    )
