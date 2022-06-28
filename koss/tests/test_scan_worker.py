import pytest
from bec_utils import BECMessage
from koss.scan_worker import ScanWorker

from utils import load_KossMock


def get_scan_worker() -> ScanWorker:
    k = load_KossMock()
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
        worker.dm.devices[dev] for dev in devices
    ]
