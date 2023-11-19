# pylint: skip-file
from unittest import mock

import pytest
from bec_lib import Alarms, MessageEndpoints, messages
from ophyd import StatusBase

from device_server.rpc_mixin import RPCMixin


@pytest.fixture
def rpc_cls():
    rpc_mixin = RPCMixin()
    rpc_mixin.connector = mock.MagicMock()
    rpc_mixin.producer = mock.MagicMock()
    rpc_mixin.device_manager = mock.MagicMock()
    yield rpc_mixin


@pytest.mark.parametrize(
    "instr_params",
    [
        ({"args": (1, 2, 3), "kwargs": {"a": 1, "b": 2}}),
        ({"args": (1, 2, 3)}),
        ({"kwargs": {"a": 1, "b": 2}}),
        ({}),
    ],
)
def test_get_result_from_rpc(rpc_cls, instr_params):
    rpc_var = mock.MagicMock()
    rpc_var.return_value = 1
    out = rpc_cls._get_result_from_rpc(
        rpc_var=rpc_var,
        instr_params=instr_params,
    )
    if instr_params:
        if instr_params.get("args") and instr_params.get("kwargs"):
            rpc_var.assert_called_once_with(*instr_params["args"], **instr_params["kwargs"])
        elif instr_params.get("args"):
            rpc_var.assert_called_once_with(*instr_params["args"])
        elif instr_params.get("kwargs"):
            rpc_var.assert_called_once_with(**instr_params["kwargs"])
        else:
            rpc_var.assert_called_once_with()
    assert out == 1


@pytest.mark.parametrize(
    "instr_params",
    [
        ({"args": (1, 2, 3), "kwargs": {"a": 1, "b": 2}}),
        ({}),
    ],
)
def test_get_result_from_rpc_var(rpc_cls, instr_params):
    rpc_var = 5
    out = rpc_cls._get_result_from_rpc(
        rpc_var=rpc_var,
        instr_params=instr_params,
    )
    assert out == 5


def test_get_result_from_rpc_not_serializable(rpc_cls):
    rpc_var = mock.MagicMock()
    rpc_var.return_value = mock.MagicMock()
    rpc_var.return_value.__str__.side_effect = Exception
    out = rpc_cls._get_result_from_rpc(
        rpc_var=rpc_var,
        instr_params={},
    )
    assert out is None
    rpc_cls.connector.raise_alarm.assert_called_once_with(
        severity=Alarms.WARNING,
        alarm_type="TypeError",
        source={},
        content="Return value of rpc call {} is not serializable.",
        metadata={},
    )


def test_get_result_from_rpc_ophyd_status(rpc_cls):
    rpc_var = mock.MagicMock()
    rpc_var.return_value = StatusBase()
    out = rpc_cls._get_result_from_rpc(
        rpc_var=rpc_var,
        instr_params={},
    )
    assert out is rpc_var.return_value


def test_get_result_from_rpc_list_from_stage(rpc_cls):
    rpc_var = mock.MagicMock()
    rpc_var.return_value = [mock.MagicMock(), mock.MagicMock()]
    rpc_var.return_value[0]._staged = True
    rpc_var.return_value[1]._staged = False
    out = rpc_cls._get_result_from_rpc(
        rpc_var=rpc_var,
        instr_params={"func": "stage"},
    )
    assert out == [True, False]


def test_send_rpc_exception(rpc_cls):
    instr = messages.DeviceInstructionMessage(
        device="device", action="rpc", parameter={"rpc_id": "rpc_id"}
    )
    rpc_cls._send_rpc_exception(Exception(), instr)
    rpc_cls.producer.set.assert_called_once_with(
        MessageEndpoints.device_rpc("rpc_id"),
        messages.DeviceRPCMessage(
            device="device",
            return_val=None,
            out={"error": "Exception", "msg": (), "traceback": "NoneType: None\n"},
            success=False,
        ).dumps(),
    )


def test_send_rpc_result_to_client(rpc_cls):
    result = mock.MagicMock()
    result.getvalue.return_value = "result"
    rpc_cls._send_rpc_result_to_client("device", {"rpc_id": "rpc_id"}, 1, result)
    rpc_cls.producer.set.assert_called_once_with(
        MessageEndpoints.device_rpc("rpc_id"),
        messages.DeviceRPCMessage(
            device="device",
            return_val=1,
            out="result",
            success=True,
        ).dumps(),
        expire=1800,
    )


def test_run_rpc(rpc_cls):
    instr = messages.DeviceInstructionMessage(
        device="device", action="rpc", parameter={"rpc_id": "rpc_id"}
    )
    rpc_cls._assert_device_is_enabled = mock.MagicMock()
    with mock.patch.object(
        rpc_cls, "_process_rpc_instruction"
    ) as _process_rpc_instruction, mock.patch.object(
        rpc_cls, "_send_rpc_result_to_client"
    ) as _send_rpc_result_to_client:
        _process_rpc_instruction.return_value = 1
        rpc_cls.run_rpc(instr)
        rpc_cls._assert_device_is_enabled.assert_called_once_with(instr)
        _process_rpc_instruction.assert_called_once_with(instr)
        _send_rpc_result_to_client.assert_called_once_with(
            "device", {"rpc_id": "rpc_id"}, 1, mock.ANY
        )


def test_run_rpc_sends_rpc_exception(rpc_cls):
    instr = messages.DeviceInstructionMessage(
        device="device", action="rpc", parameter={"rpc_id": "rpc_id"}
    )
    rpc_cls._assert_device_is_enabled = mock.MagicMock()
    with mock.patch.object(
        rpc_cls, "_process_rpc_instruction"
    ) as _process_rpc_instruction, mock.patch.object(
        rpc_cls, "_send_rpc_exception"
    ) as _send_rpc_exception:
        _process_rpc_instruction.side_effect = Exception
        rpc_cls.run_rpc(instr)
        rpc_cls._assert_device_is_enabled.assert_called_once_with(instr)
        _process_rpc_instruction.assert_called_once_with(instr)
        _send_rpc_exception.assert_called_once_with(mock.ANY, instr)


@pytest.mark.parametrize(
    "func, read_called",
    [("read", True), ("readback", False), ("read_configuration", False), ("readback.read", True)],
)
def test_process_rpc_instruction_read(rpc_cls, func, read_called):
    instr = messages.DeviceInstructionMessage(
        device="device", action="rpc", parameter={"rpc_id": "rpc_id", "func": func}
    )
    rpc_cls._read_and_update_devices = mock.MagicMock()
    rpc_cls._process_rpc_instruction(instr)
    if read_called:
        rpc_cls._read_and_update_devices.assert_called_once_with(["device"], {})
    else:
        rpc_cls._read_and_update_devices.assert_not_called()
