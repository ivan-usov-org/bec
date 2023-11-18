# pylint: skip-file
from unittest import mock

import pytest

from bec_lib import messages
from bec_lib.devicemanager import Status
from bec_lib.devicemanager_client import RPCError
from bec_lib.tests.utils import bec_client


@pytest.fixture
def dev(bec_client):
    yield bec_client.device_manager.devices


def test_nested_device_root(dev):
    assert dev.dyn_signals.name == "dyn_signals"
    assert dev.dyn_signals.messages.name == "messages"
    assert dev.dyn_signals.root == dev.dyn_signals
    assert dev.dyn_signals.messages.root == dev.dyn_signals


def test_run_rpc_call(dev):
    with mock.patch.object(dev.samx.setpoint, "_get_rpc_response") as mock_rpc:
        dev.samx.setpoint.set(1)
        mock_rpc.assert_called_once()


def test_handle_rpc_response(dev):
    msg = messages.DeviceRPCMessage(device="samx", return_val=1, out="done", success=True)
    assert dev.samx._handle_rpc_response(msg) == 1


def test_handle_rpc_response_returns_status(dev, bec_client):
    msg = messages.DeviceRPCMessage(
        device="samx", return_val={"type": "status", "RID": "request_id"}, out="done", success=True
    )
    assert dev.samx._handle_rpc_response(msg) == Status(
        bec_client.device_manager.producer, "request_id"
    )


def test_handle_rpc_response_raises(dev):
    msg = messages.DeviceRPCMessage(
        device="samx",
        return_val={"type": "status", "RID": "request_id"},
        out={
            "msg": "Didn't work...",
            "traceback": "Traceback (most recent call last):",
            "error": "error",
        },
        success=False,
    )
    with pytest.raises(RPCError):
        dev.samx._handle_rpc_response(msg)


def test_handle_rpc_response_returns_dict(dev):
    msg = messages.DeviceRPCMessage(
        device="samx",
        return_val={"a": "b"},
        out="done",
        success=True,
    )
    assert dev.samx._handle_rpc_response(msg) == {"a": "b"}


def test_run_rpc_call_calls_stop_on_keyboardinterrupt(dev):
    with mock.patch.object(dev.samx.setpoint, "_prepare_rpc_msg") as mock_rpc:
        mock_rpc.side_effect = [KeyboardInterrupt]
        with pytest.raises(RPCError):
            with mock.patch.object(dev.samx, "stop") as mock_stop:
                dev.samx.setpoint.set(1)
        mock_rpc.assert_called_once()
        mock_stop.assert_called_once()
