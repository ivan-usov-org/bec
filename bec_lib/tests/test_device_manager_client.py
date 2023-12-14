# pylint: skip-file
from unittest import mock

import pytest

from bec_lib import messages
from bec_lib.devicemanager import Status
from bec_lib.devicemanager_client import RPCError
from bec_lib.endpoints import MessageEndpoints
from bec_lib.tests.utils import bec_client


@pytest.fixture
def dev(bec_client):
    yield bec_client.device_manager.devices


def test_nested_device_root(dev):
    assert dev.dyn_signals.name == "dyn_signals"
    assert dev.dyn_signals.messages.name == "messages"
    assert dev.dyn_signals.root == dev.dyn_signals
    assert dev.dyn_signals.messages.root == dev.dyn_signals


def test_read(dev):
    with mock.patch.object(dev.samx.root.parent.producer, "get") as mock_get:
        mock_get.return_value = messages.DeviceMessage(
            signals={
                "samx": {"value": 0, "timestamp": 1701105880.1711318},
                "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
                "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
            },
            metadata={"scan_id": "scan_id", "scan_type": "scan_type"},
        ).dumps()
        res = dev.samx.read()
        mock_get.assert_called_once_with(MessageEndpoints.device_readback("samx"))
        assert res == {
            "samx": {"value": 0, "timestamp": 1701105880.1711318},
            "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
            "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
        }


def test_read_filtered_hints(dev):
    with mock.patch.object(dev.samx.root.parent.producer, "get") as mock_get:
        mock_get.return_value = messages.DeviceMessage(
            signals={
                "samx": {"value": 0, "timestamp": 1701105880.1711318},
                "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
                "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
            },
            metadata={"scan_id": "scan_id", "scan_type": "scan_type"},
        ).dumps()
        res = dev.samx.read(filter_to_hints=True)
        mock_get.assert_called_once_with(MessageEndpoints.device_readback("samx"))
        assert res == {"samx": {"value": 0, "timestamp": 1701105880.1711318}}


def test_read_use_read(dev):
    with mock.patch.object(dev.samx.root.parent.producer, "get") as mock_get:
        data = {
            "samx": {"value": 0, "timestamp": 1701105880.1711318},
            "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
            "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
        }
        mock_get.return_value = messages.DeviceMessage(
            signals=data, metadata={"scan_id": "scan_id", "scan_type": "scan_type"}
        ).dumps()
        res = dev.samx.read(use_readback=False)
        mock_get.assert_called_once_with(MessageEndpoints.device_read("samx"))
        assert res == data


def test_read_nested_device(dev):
    with mock.patch.object(dev.dyn_signals.root.parent.producer, "get") as mock_get:
        data = {
            "dyn_signals_messages_message1": {"value": 0, "timestamp": 1701105880.0716832},
            "dyn_signals_messages_message2": {"value": 0, "timestamp": 1701105880.071722},
            "dyn_signals_messages_message3": {"value": 0, "timestamp": 1701105880.071739},
            "dyn_signals_messages_message4": {"value": 0, "timestamp": 1701105880.071753},
            "dyn_signals_messages_message5": {"value": 0, "timestamp": 1701105880.071766},
        }
        mock_get.return_value = messages.DeviceMessage(
            signals=data, metadata={"scan_id": "scan_id", "scan_type": "scan_type"}
        ).dumps()
        res = dev.dyn_signals.messages.read()
        mock_get.assert_called_once_with(MessageEndpoints.device_readback("dyn_signals"))
        assert res == data


@pytest.mark.parametrize(
    "kind,cached", [("normal", True), ("hinted", True), ("config", False), ("omitted", False)]
)
def test_read_kind_hinted(dev, kind, cached):
    with mock.patch.object(dev.samx.readback, "_run") as mock_run:
        with mock.patch.object(dev.samx.root.parent.producer, "get") as mock_get:
            data = {
                "samx": {"value": 0, "timestamp": 1701105880.1711318},
                "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
                "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
            }
            mock_get.return_value = messages.DeviceMessage(
                signals=data, metadata={"scan_id": "scan_id", "scan_type": "scan_type"}
            ).dumps()
            dev.samx.readback._signal_info["kind_str"] = f"Kind.{kind}"
            res = dev.samx.readback.read(cached=cached)
            if cached:
                mock_get.assert_called_once_with(MessageEndpoints.device_readback("samx"))
                mock_run.assert_not_called()
                assert res == {"samx": {"value": 0, "timestamp": 1701105880.1711318}}
            else:
                mock_run.assert_called_once_with(cached=False, fcn=dev.samx.readback.read)
                mock_get.assert_not_called()


@pytest.mark.parametrize(
    "is_signal,is_config_signal,method",
    [
        (True, False, "read"),
        (False, True, "read_configuration"),
        (False, False, "read_configuration"),
    ],
)
def test_read_configuration_not_cached(dev, is_signal, is_config_signal, method):
    with mock.patch.object(
        dev.samx.readback, "_get_rpc_signal_info", return_value=(is_signal, is_config_signal, False)
    ):
        with mock.patch.object(dev.samx.readback, "_run") as mock_run:
            dev.samx.readback.read_configuration(cached=False)
            mock_run.assert_called_once_with(cached=False, fcn=getattr(dev.samx.readback, method))


@pytest.mark.parametrize(
    "is_signal,is_config_signal,method",
    [(True, False, "read"), (False, True, "redis"), (False, False, "redis")],
)
def test_read_configuration_cached(dev, is_signal, is_config_signal, method):
    with mock.patch.object(
        dev.samx.readback, "_get_rpc_signal_info", return_value=(is_signal, is_config_signal, True)
    ):
        with mock.patch.object(dev.samx.root.parent.producer, "get") as mock_get:
            mock_get.return_value = messages.DeviceMessage(
                signals={
                    "samx": {"value": 0, "timestamp": 1701105880.1711318},
                    "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
                    "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
                },
                metadata={"scan_id": "scan_id", "scan_type": "scan_type"},
            ).dumps()
            with mock.patch.object(dev.samx.readback, "read") as mock_read:
                dev.samx.readback.read_configuration(cached=True)
                if method == "redis":
                    mock_get.assert_called_once_with(
                        MessageEndpoints.device_read_configuration("samx")
                    )
                    mock_read.assert_not_called()
                else:
                    mock_read.assert_called_once_with(cached=True)
                    mock_get.assert_not_called()


def test_run_rpc_call(dev):
    with mock.patch.object(dev.samx.setpoint, "_get_rpc_response") as mock_rpc:
        dev.samx.setpoint.set(1)
        mock_rpc.assert_called_once()


def test_get_rpc_func_name_decorator(dev):
    with mock.patch.object(dev.samx.setpoint, "_run_rpc_call") as mock_rpc:
        dev.samx.setpoint.set(1)
        mock_rpc.assert_called_once_with("samx", "setpoint.set", 1)


def test_get_rpc_func_name_read(dev):
    with mock.patch.object(dev.samx, "_run_rpc_call") as mock_rpc:
        dev.samx.read(cached=False)
        mock_rpc.assert_called_once_with("samx", "read")


@pytest.mark.parametrize(
    "kind,cached", [("normal", True), ("hinted", True), ("config", False), ("omitted", False)]
)
def test_get_rpc_func_name_readback_get(dev, kind, cached):
    with mock.patch.object(dev.samx.readback, "_run") as mock_rpc:
        with mock.patch.object(dev.samx.root.parent.producer, "get") as mock_get:
            mock_get.return_value = messages.DeviceMessage(
                signals={
                    "samx": {"value": 0, "timestamp": 1701105880.1711318},
                    "samx_setpoint": {"value": 0, "timestamp": 1701105880.1693492},
                    "samx_motor_is_moving": {"value": 0, "timestamp": 1701105880.16935},
                },
                metadata={"scan_id": "scan_id", "scan_type": "scan_type"},
            ).dumps()
            dev.samx.readback._signal_info["kind_str"] = f"Kind.{kind}"
            dev.samx.readback.get(cached=cached)
            if cached:
                mock_get.assert_called_once_with(MessageEndpoints.device_readback("samx"))
                mock_rpc.assert_not_called()
            else:
                mock_rpc.assert_called_once_with(cached=False, fcn=dev.samx.readback.get)
                mock_get.assert_not_called()


def test_get_rpc_func_name_nested(dev):
    with mock.patch.object(
        dev.samx._custom_rpc_methods["dummy_controller"]._custom_rpc_methods["_func_with_args"],
        "_run_rpc_call",
    ) as mock_rpc:
        dev.samx.dummy_controller._func_with_args(1, 2)
        mock_rpc.assert_called_once_with("samx", "dummy_controller._func_with_args", 1, 2)


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
    msg = messages.DeviceRPCMessage(device="samx", return_val={"a": "b"}, out="done", success=True)
    assert dev.samx._handle_rpc_response(msg) == {"a": "b"}


def test_run_rpc_call_calls_stop_on_keyboardinterrupt(dev):
    with mock.patch.object(dev.samx.setpoint, "_prepare_rpc_msg") as mock_rpc:
        mock_rpc.side_effect = [KeyboardInterrupt]
        with pytest.raises(RPCError):
            with mock.patch.object(dev.samx, "stop") as mock_stop:
                dev.samx.setpoint.set(1)
        mock_rpc.assert_called_once()
        mock_stop.assert_called_once()
