import numpy as np
import pytest
from bec_utils import BECMessage as BMessage
from bec_utils.tests.utils import ProducerMock
from scan_plugins.LamNIFermatScan import LamNIFermatScan
from scan_server.scans import FermatSpiralScan, Move, Scan

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


class DeviceMock:
    def __init__(self, name: str):
        self.name = name
        self.read_buffer = None
        self.config = {"deviceConfig": {"limits": [-50, 50]}}

    def read(self):
        return self.read_buffer

    def readback(self):
        return self.read_buffer


class DMMock:
    devices = {}
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
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    device_manager.add_device("samy")
    device_manager.devices["samy"].read_buffer = {"value": 0}
    device_manager.add_device("samz")
    device_manager.devices["samz"].read_buffer = {"value": 0}
    s = Move(parameter=mv_msg.content.get("parameter"), device_manager=device_manager)
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
                    parameter={
                        "primary": ["samx"],
                        "num_points": 3,
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
    device_manager = DMMock()
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    msg_list = []
    for step in Scan.scan(
        parameter=scan_msg.content.get("parameter"), device_manager=device_manager
    ):
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
    scan.prepare_positions()
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
                scan_type="lamni_fermat_scan",
                parameter={
                    "args": {},
                    "kwargs": {"fov_size": [5], "exp_time": 0.1, "step": 2, "angle": 10},
                },
                queue="primary",
            ),
            [
                BMessage.DeviceInstructionMessage(
                    device=["rtx", "rty"],
                    action="read",
                    parameter={"group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 0},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["rtx", "rty"],
                    action="wait",
                    parameter={"type": "read", "group": "scan_motor", "wait_group": "scan_motor"},
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
                    parameter={"value": 10, "group": "scan_motor", "wait_group": "scan_motor"},
                    metadata={"stream": "primary", "DIID": 3},
                ),
                BMessage.DeviceInstructionMessage(
                    device=["lsamrot"],
                    action="wait",
                    parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
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
                        "value": -0.7700589354581364,
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 17},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rty",
                    action="set",
                    parameter={
                        "value": -0.8406005210092851,
                        "group": "scan_motor",
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
                    parameter={"type": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 21},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "target": "primary",
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
                        "value": 1.3681828686580249,
                        "group": "scan_motor",
                        "wait_group": "scan_motor",
                    },
                    metadata={"stream": "primary", "DIID": 24},
                ),
                BMessage.DeviceInstructionMessage(
                    device="rty",
                    action="set",
                    parameter={
                        "value": 2.1508313829565298,
                        "group": "scan_motor",
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
                    parameter={"type": "trigger", "time": 0.1},
                    metadata={"stream": "primary", "DIID": 29},
                ),
                BMessage.DeviceInstructionMessage(
                    device=None,
                    action="read",
                    parameter={
                        "target": "primary",
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
    device_manager.add_device("samx")
    device_manager.devices["samx"].read_buffer = {"value": 0}
    device_manager.add_device("samy")
    device_manager.devices["samy"].read_buffer = {"value": 0}
    scan = LamNIFermatScan(
        parameter=scan_msg.content.get("parameter"), device_manager=device_manager
    )
    scan._get_from_rpc = lambda x: 0
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
    assert scan_instructions == reference_scan_list
