import uuid
from unittest import mock

import pytest
from bec_utils import BECMessage, MessageEndpoints
from scan_server.scan_worker import ScanWorker

from utils import load_ScanServerMock


def get_scan_worker() -> ScanWorker:
    k = load_ScanServerMock()
    return ScanWorker(parent=k)


@pytest.mark.parametrize(
    "instruction,devices",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device="samy",
                action="wait",
                parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            ["samy"],
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx", "samy"],
                action="wait",
                parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            ["samx", "samy"],
        ),
    ],
)
def test_get_devices_from_instruction(instruction, devices):
    worker = get_scan_worker()
    assert worker._get_devices_from_instruction(instruction) == [
        worker.device_manager.devices[dev] for dev in devices
    ]


def test_add_wait_group():
    worker = get_scan_worker()
    msg1 = BECMessage.DeviceInstructionMessage(
        device="samx",
        action="set",
        parameter={"value": 10, "wait_group": "scan_motor"},
        metadata={"stream": "primary", "DIID": 3},
    )
    worker._add_wait_group(msg1)

    assert worker._groups == {"scan_motor": [("samx", 3)]}


def test_wait_for_idle():
    worker = get_scan_worker()
    scanID = str(uuid.uuid4())
    requestID = str(uuid.uuid4())
    msg1 = BECMessage.DeviceInstructionMessage(
        device="samx",
        action="set",
        parameter={"value": 10, "wait_group": "scan_motor"},
        metadata={"stream": "primary", "DIID": 3, "scanID": scanID, "RID": requestID},
    )
    msg2 = BECMessage.DeviceInstructionMessage(
        device=["samx"],
        action="wait",
        parameter={"type": "move", "wait_group": "scan_motor"},
        metadata={"stream": "primary", "DIID": 4, "scanID": scanID, "RID": requestID},
    )
    req_msg = BECMessage.DeviceReqStatusMessage(
        device="samx",
        success=True,
        metadata={"stream": "primary", "DIID": 3, "scanID": scanID, "RID": requestID},
    )
    worker.device_manager.producer._get_buffer = {
        MessageEndpoints.device_req_status("samx"): req_msg.dumps()
    }
    worker._add_wait_group(msg1)
    worker._wait_for_idle(msg2)


@pytest.mark.parametrize(
    "msg,scan_id,num_points,exp_num_points",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="close_scan",
                parameter={},
                metadata={"stream": "primary", "DIID": 18, "scanID": "12345"},
            ),
            "12345",
            20,
            20,
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="close_scan",
                parameter={},
                metadata={"stream": "primary", "DIID": 18, "scanID": "12345"},
            ),
            "0987",
            20,
            19,
        ),
    ],
)
def test_close_scan(msg, scan_id, num_points, exp_num_points):
    worker = get_scan_worker()
    worker.scan_id = scan_id
    worker.current_scan_info["points"] = 19

    def send_scan_status_mock(*args):
        pass

    reset = bool(worker.scan_id == msg.metadata["scanID"])
    # worker._send_scan_status = send_scan_status_mock
    with mock.patch(
        "scan_server.scan_worker.ScanWorker._send_scan_status"
    ) as send_scan_status_mock:
        worker._close_scan(msg, max_point_id=num_points)
        if reset:
            send_scan_status_mock.assert_called_once()
            send_scan_status_mock.assert_called_with("closed")
            assert worker.scan_id == None
        else:
            assert worker.scan_id == scan_id
    assert worker.current_scan_info["points"] == exp_num_points


@pytest.mark.parametrize(
    "msg,method",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="open_scan",
                parameter={},
                metadata={"stream": "primary", "DIID": 18, "scanID": "12345"},
            ),
            "_open_scan",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="close_scan",
                parameter={},
                metadata={"stream": "primary", "DIID": 18, "scanID": "12345"},
            ),
            "_close_scan",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "12345", "RID": "123456"},
            ),
            "_wait_for_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="trigger",
                parameter={"group": "trigger"},
                metadata={"stream": "primary", "DIID": 20, "pointID": 0},
            ),
            "_trigger_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samx",
                action="set",
                parameter={
                    "value": 1.3681828686580249,
                    "wait_group": "scan_motor",
                },
                metadata={"stream": "primary", "DIID": 24},
            ),
            "_set_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="read",
                parameter={
                    "group": "primary",
                    "wait_group": "readout_primary",
                },
                metadata={"stream": "primary", "DIID": 30, "pointID": 1},
            ),
            "_read_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="stage",
                parameter={},
                metadata={"stream": "primary", "DIID": 17},
            ),
            "_stage_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="unstage",
                parameter={},
                metadata={"stream": "primary", "DIID": 17},
            ),
            "_unstage_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samx",
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
            "_send_rpc",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samx", action="kickoff", parameter={}, metadata={}
            ),
            "_kickoff_devices",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="baseline_reading",
                parameter={},
                metadata={"stream": "baseline", "DIID": 15},
            ),
            "_baseline_reading",
        ),
        (
            BECMessage.DeviceInstructionMessage(device=None, action="close_scan_def", parameter={}),
            "_close_scan",
        ),
    ],
)
def test_instruction_step(msg, method):
    worker = get_scan_worker()
    with mock.patch(f"scan_server.scan_worker.ScanWorker.{method}") as instruction_method:
        worker._instruction_step(msg)
        instruction_method.assert_called_once()
