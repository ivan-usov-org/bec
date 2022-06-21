import pytest
from bec_utils import BECMessage as BMessage
from koss.devicemanager import DeviceManagerKOSS
from koss.scan_guard import ScanGuard

from utils import ConnectorMock, KossMock, dummy_devices


def test_check_motors_movable():
    devices = dummy_devices(True)
    connector = ConnectorMock("")
    dm = DeviceManagerKOSS(connector, "")
    dm._config = devices
    dm._load_config_device()
    k = KossMock(dm, connector)

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

    devices = dummy_devices(False)
    dm._config = devices
    dm._load_config_device()

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
    devices = dummy_devices(True)
    connector = ConnectorMock("")
    dm = DeviceManagerKOSS(connector, "")
    dm._config = devices
    dm._load_config_device()
    k = KossMock(dm, connector)

    sg = ScanGuard(parent=k)
    assert sg._device_rpc_is_valid(device, func) == is_valid
