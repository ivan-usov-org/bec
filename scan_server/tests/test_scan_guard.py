from unittest import mock

import msgpack
import pytest
from bec_client_lib.core import BECMessage, MessageEndpoints
from bec_client_lib.core.redis_connector import MessageObject
from utils import load_ScanServerMock

from scan_server.scan_guard import ScanGuard, ScanRejection, ScanStatus


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


def test_check_valid_scan_raises_for_unknown_scan():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    sg.producer = mock.MagicMock()
    sg.producer.get.return_value = msgpack.dumps({"fermat_scan": "fermat_scan"})

    request = BECMessage.ScanQueueMessage(
        scan_type="unknown_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )

    with pytest.raises(ScanRejection) as scan_rejection:
        sg._check_valid_scan(request)


def test_check_valid_scan_accepts_known_scan():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    sg.producer = mock.MagicMock()
    sg.producer.get.return_value = msgpack.dumps({"fermat_scan": "fermat_scan"})

    request = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )

    sg._check_valid_scan(request)


def test_check_valid_scan_device_rpc():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    sg.producer = mock.MagicMock()
    sg.producer.get.return_value = msgpack.dumps({"device_rpc": "device_rpc"})
    request = BECMessage.ScanQueueMessage(
        scan_type="device_rpc",
        parameter={
            "device": "samy",
            "func": "read",
            "args": {},
            "kwargs": {},
        },
        queue="primary",
    )
    with mock.patch.object(sg, "_device_rpc_is_valid") as rpc_valid:
        sg._check_valid_scan(request)
        rpc_valid.assert_called_once_with(device="samy", func="read")


def test_check_valid_scan_device_rpc_raises():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    sg.producer = mock.MagicMock()
    sg.producer.get.return_value = msgpack.dumps({"device_rpc": "device_rpc"})
    request = BECMessage.ScanQueueMessage(
        scan_type="device_rpc",
        parameter={
            "device": "samy",
            "func": "read",
            "args": {},
            "kwargs": {},
        },
        queue="primary",
    )
    with pytest.raises(ScanRejection) as scan_rejection:
        with mock.patch.object(sg, "_device_rpc_is_valid") as rpc_valid:
            rpc_valid.return_value = False
            sg._check_valid_scan(request)
            rpc_valid.assert_called_once_with(device="samy", func="read")
        assert "Rejected rpc: " in scan_rejection.value.args


def test_handle_scan_modification_request():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueModificationMessage(
        scanID="scanID",
        action="abort",
        parameter={},
        metadata={"RID": "RID"},
    )
    with mock.patch.object(sg.device_manager.producer, "send") as send:
        sg._handle_scan_modification_request(msg.dumps())
        send.assert_called_once_with(
            MessageEndpoints.scan_queue_modification(),
            msg.dumps(),
        )


def test_handle_scan_modification_request_restart():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueModificationMessage(
        scanID="scanID",
        action="restart",
        parameter={"RID": "RID"},
        metadata={"RID": "new_RID"},
    )
    with mock.patch.object(sg, "_send_scan_request_response") as send_response:
        with mock.patch("scan_server.scan_guard.ScanStatus") as scan_status:
            sg._handle_scan_modification_request(msg.dumps())
            send_response.assert_called_once_with(scan_status(), {"RID": "RID"})


def test_append_to_scan_queue():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    with mock.patch.object(sg.device_manager.producer, "send") as send:
        sg._append_to_scan_queue(msg)
        send.assert_called_once_with(
            MessageEndpoints.scan_queue_insert(),
            msg.dumps(),
        )


def test_scan_queue_request_callback():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    msg_obj = MessageObject(msg.dumps(), MessageEndpoints.scan_queue_request())
    with mock.patch.object(sg, "_handle_scan_request") as handle:
        sg._scan_queue_request_callback(msg_obj, sg)
        handle.assert_called_once_with(msg.dumps())


def test_scan_queue_modification_request_callback():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueModificationMessage(
        scanID="scanID",
        action="abort",
        parameter={},
        metadata={"RID": "RID"},
    )
    msg_obj = MessageObject(msg.dumps(), MessageEndpoints.scan_queue_modification())
    with mock.patch.object(sg, "_handle_scan_modification_request") as handle:
        sg._scan_queue_modification_request_callback(msg_obj, sg)
        handle.assert_called_once_with(msg.dumps())


def test_scan_queue_modification_request_callback_wrong_msg():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    msg_obj = MessageObject(msg.dumps(), MessageEndpoints.scan_queue_modification())
    with mock.patch.object(sg, "_handle_scan_modification_request") as handle:
        sg._scan_queue_modification_request_callback(msg_obj, sg)
        handle.assert_not_called()


def test_send_scan_request_response():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    with mock.patch.object(sg.device_manager.producer, "send") as send:
        sg._send_scan_request_response(ScanStatus(), {"RID": "RID"})
        send.assert_called_once_with(
            MessageEndpoints.scan_queue_request_response(),
            BECMessage.RequestResponseMessage(
                accepted=True,
                message="",
                metadata={"RID": "RID"},
            ).dumps(),
        )


def test_handle_scan_request():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    with mock.patch.object(sg, "_is_valid_scan_request") as valid:
        with mock.patch.object(sg, "_append_to_scan_queue") as append:
            valid.return_value = ScanStatus(accepted=True, message="")
            sg._handle_scan_request(msg.dumps())
            append.assert_called_once_with(msg)


def test_handle_scan_request_rejected():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    with mock.patch.object(sg, "_is_valid_scan_request") as valid:
        with mock.patch.object(sg, "_append_to_scan_queue") as append:
            valid.return_value = ScanStatus(accepted=False, message="")
            sg._handle_scan_request(msg.dumps())
            append.assert_not_called()


def test_is_valid_scan_request_returns_scan_status_on_error():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    msg = BECMessage.ScanQueueMessage(
        scan_type="fermat_scan",
        parameter={
            "args": {"samx": (-5, 5), "samy": (-5, 5)},
            "kwargs": {"step": 3},
        },
        queue="primary",
    )
    with mock.patch.object(sg, "_check_valid_scan") as valid:
        valid.side_effect = Exception("Test exception")
        status = sg._is_valid_scan_request(msg)
        assert status.accepted == False
        assert "Test exception" in status.message


def test_check_valid_request_raises_for_empty_request():
    k = load_ScanServerMock()

    sg = ScanGuard(parent=k)
    with pytest.raises(ScanRejection) as scan_rejection:
        sg._check_valid_request(None)
    assert "Invalid request." in scan_rejection.value.args
