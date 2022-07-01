import pytest
from bec_utils import BECMessage as BMessage
from scan_server.scan_guard import ScanGuard

from utils import load_ScanServerMock


def test_check_motors_movable():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    sg._check_motors_movable(
        BMessage.ScanQueueMessage(
            scan_type="fermat_scan",
            parameter={
                "args": {"samx": (-5, 5), "samy": (-5, 5)},
                "kwargs": {"step": 3},
            },
            queue="primary",
        )
    )
    assert sg.scan_acc._accepted == True

    k.dm.devices["samx"].enabled = True
    k.dm.devices["samy"].enabled = False

    sg._check_motors_movable(
        BMessage.ScanQueueMessage(
            scan_type="fermat_scan",
            parameter={
                "args": {"samx": (-5, 5), "samy": (-5, 5)},
                "kwargs": {"step": 3},
            },
            queue="primary",
        )
    )

    assert sg.scan_acc._accepted == False
    assert sg.scan_acc._message == "Device samy is not enabled."


@pytest.mark.parametrize("device,func,is_valid", [("samx", "read", True)])
def test_device_rpc_is_valid(device, func, is_valid):
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    assert sg._device_rpc_is_valid(device, func) == is_valid
