from unittest import mock

import pytest
from utils import load_ScanServerMock

from bec_client_lib.core import BECMessage
from scan_server.scan_guard import ScanGuard, ScanRejection


@pytest.mark.parametrize(
    "scan_queue_msg",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={
                    "args": {"samx": (-5, 5), "samy": (-5, 5)},
                    "kwargs": {"step": 3},
                },
                queue="primary",
            )
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="device_rpc",
                parameter={
                    "device": "samy",
                    "args": {},
                    "kwargs": {},
                },
                queue="primary",
            )
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="device_rpc",
                parameter={
                    "device": ["samy"],
                    "args": {},
                    "kwargs": {},
                },
                queue="primary",
            )
        ),
    ],
)
def test_check_motors_movable_enabled(scan_queue_msg):
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    sg._check_motors_movable(scan_queue_msg)
    config_reply = BECMessage.RequestResponseMessage(accepted=True, message="")
    with mock.patch.object(
        k.device_manager.config_helper, "wait_for_config_reply", return_value=config_reply
    ):
        k.device_manager.devices["samx"].enabled = True
        k.device_manager.devices["samy"].enabled = False
        with pytest.raises(ScanRejection) as scan_rejection:
            sg._check_motors_movable(scan_queue_msg)
        assert "Device samy is not enabled." in scan_rejection.value.args


@pytest.mark.parametrize("device,func,is_valid", [("samx", "read", True)])
def test_device_rpc_is_valid(device, func, is_valid):
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    assert sg._device_rpc_is_valid(device, func) == is_valid


@pytest.mark.parametrize(
    "scan_queue_msg,valid",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={
                    "args": {"samx": (-5, 5), "samy": (-5, 5)},
                    "kwargs": {"step": 3},
                },
                queue="primary",
            ),
            True,
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="device_rpc",
                parameter={
                    "device": "samy",
                    "args": {},
                    "kwargs": {},
                },
                queue="primary",
            ),
            True,
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="device_rpc",
                parameter={
                    "device": ["samy"],
                    "args": {},
                    "kwargs": {},
                },
                queue="primary",
            ),
            True,
        ),
    ],
)
def test_valid_request(scan_queue_msg, valid):
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    config_reply = BECMessage.RequestResponseMessage(accepted=True, message="")
    with mock.patch.object(
        k.device_manager.config_helper, "wait_for_config_reply", return_value=config_reply
    ):
        with mock.patch.object(sg, "_check_valid_scan") as valid_scan:
            k.device_manager.devices["samx"].enabled = True
            k.device_manager.devices["samy"].enabled = True
            status = sg._is_valid_scan_request(scan_queue_msg)
            valid_scan.assert_called_once_with(scan_queue_msg)
            assert status.accepted == valid
