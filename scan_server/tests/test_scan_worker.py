import uuid
from unittest import mock

import pytest
from bec_utils import BECMessage, MessageEndpoints, DeviceStatus
from scan_server.errors import ScanAbortion, DeviceMessageError
from scan_server.scan_worker import ScanWorker

from utils import load_ScanServerMock
import time
from scan_server.scan_queue import InstructionQueueStatus


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
        (
            BECMessage.DeviceInstructionMessage(
                device="",
                action="wait",
                parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            ["samx", "samy"],
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="",
                action="wait",
                parameter={"type": "move", "group": "primary", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            ["samx", "samy"],
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="",
                action="wait",
                parameter={"type": "move", "group": "nogroup", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            ["samx", "samy"],
        ),
    ],
)
def test_get_devices_from_instruction(instruction, devices):
    worker = get_scan_worker()
    worker.scan_motors = devices

    returned_devices = worker._get_devices_from_instruction(instruction)

    if not instruction.content.get("device"):
        group = instruction.content["parameter"].get("group")
        if group == "primary":
            assert returned_devices == worker.device_manager.devices.primary_devices(
                worker.scan_motors
            )
        elif group == "scan_motor":
            assert returned_devices == devices
        else:
            assert returned_devices == []
    else:
        assert returned_devices == [worker.device_manager.devices[dev] for dev in devices]


@pytest.mark.parametrize(
    "instructions",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device="samx",
                action="set",
                parameter={"value": 10, "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            )
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="set",
            parameter={"value": 10, "wait_group": "scan_motor"},
            metadata={"stream": "primary", "DIID": None},
        ),
    ],
)
def test_add_wait_group(instructions):
    worker = get_scan_worker()
    if instructions.metadata["DIID"]:
        worker._add_wait_group(instructions)
        assert worker._groups == {"scan_motor": [("samx", 3)]}

        worker._groups["scan_motor"] = [("samy", 2)]
        worker._add_wait_group(instructions)
        assert worker._groups == {"scan_motor": [("samy", 2), ("samx", 3)]}

    else:
        with pytest.raises(DeviceMessageError) as exc_info:
            worker._add_wait_group(instructions)
        assert exc_info.value.args[0] == "Device message metadata does not contain a DIID entry."


@pytest.mark.parametrize(
    "instructions,wait_type",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device="samy",
                action="wait",
                parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            "move",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samy",
                action="wait",
                parameter={"type": "read", "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            "read",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samy",
                action="wait",
                parameter={"type": "trigger", "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            "trigger",
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samy",
                action="wait",
                parameter={"type": None, "group": "scan_motor", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3},
            ),
            None,
        ),
    ],
)
def test_wait_for_devices(instructions, wait_type):
    worker = get_scan_worker()

    with mock.patch.object(worker, "_wait_for_idle") as idle_mock:
        with mock.patch.object(worker, "_wait_for_read") as read_mock:
            with mock.patch.object(worker, "_wait_for_trigger") as trigger_mock:

                if wait_type:
                    worker._wait_for_devices(instructions)

                if wait_type == "move":
                    idle_mock.assert_called_once_with(instructions)
                elif wait_type == "read":
                    read_mock.assert_called_once_with(instructions)
                elif wait_type == "trigger":
                    trigger_mock.assert_called_once_with(instructions)
                else:
                    with pytest.raises(DeviceMessageError) as exc_info:
                        worker._wait_for_devices(instructions)
                    assert exc_info.value.args[0] == "Unknown wait command"


@pytest.mark.parametrize(
    "device_status,devices,instr,abort",
    [
        (
            [
                BECMessage.DeviceReqStatusMessage(
                    device="samx",
                    success=True,
                    metadata={
                        "stream": "primary",
                        "DIID": 3,
                        "scanID": "scanID",
                        "RID": "requestID",
                    },
                )
            ],
            [("samx", 4)],
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            False,
        ),
        (
            [
                BECMessage.DeviceReqStatusMessage(
                    device="samx",
                    success=False,
                    metadata={
                        "stream": "primary",
                        "DIID": 3,
                        "scanID": "scanID",
                        "RID": "request",
                    },
                )
            ],
            [("samx", 4)],
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            False,
        ),
        (
            [
                BECMessage.DeviceReqStatusMessage(
                    device="samx",
                    success=False,
                    metadata={
                        "stream": "primary",
                        "DIID": 4,
                        "scanID": "scanID",
                        "RID": "requestID",
                    },
                )
            ],
            [("samx", 4)],
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            True,
        ),
        (
            [
                BECMessage.DeviceReqStatusMessage(
                    device="samx",
                    success=False,
                    metadata={
                        "stream": "primary",
                        "DIID": 3,
                        "scanID": "scanID",
                        "RID": "requestID",
                    },
                )
            ],
            [("samx", 4)],
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            False,
        ),
    ],
)
def test_check_for_failed_movements(device_status, devices, instr, abort):
    worker = get_scan_worker()
    if abort:
        with pytest.raises(ScanAbortion):
            worker.device_manager.producer._get_buffer[
                MessageEndpoints.device_readback("samx")
            ] = BECMessage.DeviceMessage(signals={"samx": {"value": 4}}, metadata={}).dumps()
            worker._check_for_failed_movements(device_status, devices, instr)
    else:
        worker._check_for_failed_movements(device_status, devices, instr)


@pytest.mark.parametrize(
    "msg1,msg2,req_msg",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device="samx",
                action="set",
                parameter={"value": 10, "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ),
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            BECMessage.DeviceReqStatusMessage(
                device="samx",
                success=False,
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ),
        ),
        (
            BECMessage.DeviceInstructionMessage(
                device="samx",
                action="set",
                parameter={"value": 10, "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ),
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            BECMessage.DeviceReqStatusMessage(
                device="samx",
                success=True,
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ),
        ),
    ],
)
def test_wait_for_idle(msg1, msg2, req_msg: BECMessage.DeviceReqStatusMessage):
    worker = get_scan_worker()

    with mock.patch(
        "scan_server.scan_worker.ScanWorker._get_device_status", return_value=[req_msg.dumps()]
    ) as device_status:
        worker.device_manager.producer._get_buffer[
            MessageEndpoints.device_readback("samx")
        ] = BECMessage.DeviceMessage(signals={"samx": {"value": 4}}, metadata={}).dumps()

        worker._add_wait_group(msg1)
        if req_msg.content["success"]:
            worker._wait_for_idle(msg2)
        else:
            with pytest.raises(ScanAbortion):
                worker._wait_for_idle(msg2)


@pytest.mark.parametrize(
    "msg1,msg2,req_msg",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="set",
                parameter={"value": 10, "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ),
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="wait",
                parameter={"type": "move", "wait_group": "scan_motor"},
                metadata={"stream": "primary", "DIID": 4, "scanID": "scanID", "RID": "requestID"},
            ),
            BECMessage.DeviceStatusMessage(
                device="samx",
                status=0,
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ),
        ),
    ],
)
def test_wait_for_read(msg1, msg2, req_msg: BECMessage.DeviceReqStatusMessage):
    worker = get_scan_worker()

    with mock.patch(
        "scan_server.scan_worker.ScanWorker._get_device_status", return_value=[req_msg.dumps()]
    ) as device_status:
        with mock.patch.object(worker, "_check_for_interruption") as interruption_mock:
            assert worker._groups == {}
            worker._groups["scan_motor"] = [("samx", 3), "samy"]
            worker.device_manager.producer._get_buffer[
                MessageEndpoints.device_readback("samx")
            ] = BECMessage.DeviceMessage(signals={"samx": {"value": 4}}, metadata={}).dumps()
            worker._add_wait_group(msg1)
            worker._wait_for_read(msg2)
            assert worker._groups == {"scan_motor": ["samy"]}
            interruption_mock.assert_called_once()


@pytest.mark.parametrize(
    "instr",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="set",
                parameter={"value": 10, "wait_group": "scan_motor", "time": 30},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            )
        ),
    ],
)
def test_wait_for_trigger(instr):
    worker = get_scan_worker()

    with mock.patch("time.sleep", return_value=None) as patched_time_sleep:
        worker._wait_for_trigger(instr)
    patched_time_sleep.assert_called_once_with(instr.content["parameter"]["time"])


def test_wait_for_stage():
    worker = get_scan_worker()
    devices = ["samx", "samy"]
    with mock.patch.object(worker, "_get_device_status") as status_mock:
        with mock.patch.object(worker, "_check_for_interruption") as interruption_mock:
            worker._wait_for_stage(True, devices, {})
            status_mock.assert_called_once_with(MessageEndpoints.device_staged, devices)
            interruption_mock.assert_called_once()


def test_wait_for_device_server():
    worker = get_scan_worker()
    with mock.patch.object(worker.parent, "wait_for_service") as service_mock:
        worker._wait_for_device_server()
        service_mock.assert_called_once_with("DeviceServer")


@pytest.mark.parametrize(
    "instr",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="set",
                parameter={"value": 10, "wait_group": "scan_motor", "time": 30},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            )
        ),
    ],
)
def test_set_devices(instr):
    worker = get_scan_worker()
    with mock.patch.object(worker.device_manager.producer, "send") as send_mock:
        worker._set_devices(instr)
        send_mock.assert_called_once_with(MessageEndpoints.device_instructions(), instr.dumps())


@pytest.mark.parametrize(
    "instr",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="trigger",
                parameter={"value": 10, "wait_group": "scan_motor", "time": 30},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            )
        ),
    ],
)
def test_trigger_devices(instr):
    worker = get_scan_worker()
    with mock.patch.object(worker.device_manager.producer, "send") as send_mock:

        worker._trigger_devices(instr)
        devices = [dev.name for dev in worker.device_manager.devices.detectors()]

        send_mock.assert_called_once_with(
            MessageEndpoints.device_instructions(),
            BECMessage.DeviceInstructionMessage(
                device=devices,
                action="trigger",
                parameter={"value": 10, "wait_group": "scan_motor", "time": 30},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            ).dumps(),
        )


@pytest.mark.parametrize(
    "instr",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=["samx"],
                action="trigger",
                parameter={"value": 10, "wait_group": "scan_motor", "time": 30},
                metadata={"stream": "primary", "DIID": 3, "scanID": "scanID", "RID": "requestID"},
            )
        ),
    ],
)
def test_send_rpc(instr):
    worker = get_scan_worker()
    with mock.patch.object(worker.device_manager.producer, "send") as send_mock:
        worker._send_rpc(instr)
        send_mock.assert_called_once_with(MessageEndpoints.device_instructions(), instr.dumps())


def test_check_for_interruption():
    worker = get_scan_worker()
    worker.status = InstructionQueueStatus.STOPPED
    with pytest.raises(ScanAbortion) as exc_info:
        worker._check_for_interruption()


@pytest.mark.parametrize(
    "msg,scan_id,max_point_id,exp_num_points",
    [
        (
            BECMessage.DeviceInstructionMessage(
                device=None,
                action="close_scan",
                parameter={},
                metadata={"stream": "primary", "DIID": 18, "scanID": "12345"},
            ),
            "12345",
            19,
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
            200,
            19,
        ),
    ],
)
def test_close_scan(msg, scan_id, max_point_id, exp_num_points):
    worker = get_scan_worker()
    worker.scan_id = scan_id
    worker.current_scan_info["num_points"] = 19

    reset = bool(worker.scan_id == msg.metadata["scanID"])
    with mock.patch(
        "scan_server.scan_worker.ScanWorker._send_scan_status"
    ) as send_scan_status_mock:
        worker._close_scan(msg, max_point_id=max_point_id)
        if reset:
            send_scan_status_mock.assert_called_once()
            send_scan_status_mock.assert_called_with("closed")
            assert worker.scan_id == None
        else:
            assert worker.scan_id == scan_id
    assert worker.current_scan_info["num_points"] == exp_num_points


@pytest.mark.parametrize(
    "status,expire",
    [
        (
            "open",
            None,
        ),
        (
            "closed",
            1800,
        ),
        (
            "aborted",
            1800,
        ),
    ],
)
def test_send_scan_status(status, expire):
    worker = get_scan_worker()
    worker.current_scanID = str(uuid.uuid4())
    worker._send_scan_status(status)
    scan_info_msgs = [
        msg
        for msg in worker.device_manager.producer.message_sent
        if msg["queue"] == MessageEndpoints.public_scan_info(scanID=worker.current_scanID)
    ]
    assert len(scan_info_msgs) == 1
    assert scan_info_msgs[0]["expire"] == expire


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
