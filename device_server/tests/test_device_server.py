from unittest import mock

import pytest
import bec_utils
from bec_utils import BECMessage, MessageEndpoints
from bec_utils.BECMessage import BECStatus
from bec_utils.tests.utils import ConnectorMock
from ophyd import Staged
from test_device_manager_ds import load_device_manager

from device_server import DeviceServer
from device_server.device_server import InvalidDeviceError


# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


def load_DeviceServerMock():
    connector = ConnectorMock("")
    device_manager = load_device_manager()
    return DeviceServerMock(device_manager, connector)


class DeviceServerMock(DeviceServer):
    def __init__(self, device_manager, connector_cls) -> None:
        super().__init__(bootstrap_server="dummy", connector_cls=ConnectorMock, scibec_url="dummy")
        self.device_manager = device_manager

    def _start_device_manager(self):
        pass


def test_start():
    device_server = load_DeviceServerMock()

    device_server.start()

    assert device_server.threads
    assert type(device_server.threads[0]) == bec_utils.tests.utils.ConsumerMock
    assert device_server.status == BECStatus.RUNNING


@pytest.mark.parametrize("status", [BECStatus.ERROR, BECStatus.RUNNING, BECStatus.IDLE])
def test_update_status(status):
    device_server = load_DeviceServerMock()
    assert device_server.status == BECStatus.BUSY

    device_server.update_status(status)

    assert device_server.status == status


def test_stop():
    device_server = load_DeviceServerMock()
    device_server.stop()
    assert device_server.status == BECStatus.IDLE


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1},
        ),
        BECMessage.DeviceInstructionMessage(
            device=["samx", "samy"],
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1},
        ),
        BECMessage.DeviceInstructionMessage(
            device="ring_current_sim",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1},
        ),
    ],
)
def test_stage_device(instr):
    device_server = load_DeviceServerMock()
    device_server._stage_device(instr)
    devices = instr.content["device"]
    devices = devices if isinstance(devices, list) else [devices]
    dev_man = device_server.device_manager.devices
    for dev in devices:
        if not hasattr(dev_man[dev].obj, "_staged"):
            continue
        assert device_server.device_manager.devices[dev].obj._staged == Staged.yes
    device_server._unstage_device(instr)
    for dev in devices:
        if not hasattr(dev_man[dev].obj, "_staged"):
            continue
        assert device_server.device_manager.devices[dev].obj._staged == Staged.no


def test_stop_devices():
    device_server = load_DeviceServerMock()
    dev = device_server.device_manager.devices
    assert len(dev) > len(dev.enabled_devices)
    with mock.patch.object(dev.samx.obj, "stop") as stop:
        device_server.stop_devices()
        stop.assert_called_once()

    with mock.patch.object(dev.motor1_disabled.obj, "stop") as stop:
        device_server.stop_devices()
        stop.assert_not_called()

    with mock.patch.object(dev.motor1_disabled_set.obj, "stop") as stop:
        device_server.stop_devices()
        stop.assert_not_called()


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="read",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device=["samx", "samy"],
            action="read",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test2"},
        ),
    ],
)
def test_read_device(instr):
    device_server = load_DeviceServerMock()
    device_server._read_device(instr)
    devices = instr.content["device"]
    if not isinstance(devices, list):
        devices = [devices]
    for device in devices:
        res = [
            msg
            for msg in device_server.producer.message_sent
            if msg["queue"] == MessageEndpoints.device_read(device)
        ]
        assert (
            BECMessage.DeviceMessage.loads(res[-1]["msg"]).metadata["RID"] == instr.metadata["RID"]
        )
        assert BECMessage.DeviceMessage.loads(res[-1]["msg"]).metadata["stream"] == "primary"


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="set",
            parameter={"value": 5},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        )
    ],
)
def test_set_device(instr):
    device_server = load_DeviceServerMock()
    device_server._set_device(instr)
    while True:
        res = [
            msg
            for msg in device_server.producer.message_sent
            if msg["queue"] == MessageEndpoints.device_req_status("samx")
        ]
        if res:
            break
    msg = BECMessage.DeviceReqStatusMessage.loads(res[0]["msg"])
    assert msg.metadata["RID"] == "test"
    assert msg.content["success"]


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="eiger",
            action="trigger",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        )
    ],
)
def test_trigger_device(instr):
    device_server = load_DeviceServerMock()
    with mock.patch.object(device_server.device_manager.devices.eiger.obj, "trigger") as trigger:
        device_server._trigger_device(instr)
        trigger.assert_called_once()


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="flyer_sim",
            action="kickoff",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        )
    ],
)
def test_kickoff_device(instr):
    device_server = load_DeviceServerMock()
    with mock.patch.object(
        device_server.device_manager.devices.flyer_sim.obj, "kickoff"
    ) as kickoff:
        device_server._kickoff_device(instr)
        kickoff.assert_called_once()


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="eiger",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device=["samx", "samy"],
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="motor2_disabled",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="motor1_disabled",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_assert_device_is_enabled(instr):
    device_server = load_DeviceServerMock()
    devices = instr.content["device"]

    if not isinstance(devices, list):
        devices = [devices]

    for dev in devices:
        if not device_server.device_manager.devices[dev].enabled:
            with pytest.raises(Exception) as exc_info:
                device_server._assert_device_is_enabled(instr)
            assert exc_info.value.args[0] == f"Cannot access disabled device {dev}."
        else:
            device_server._assert_device_is_enabled(instr)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="not_a_valid_device",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device=None,
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_assert_device_is_valid(instr):
    device_server = load_DeviceServerMock()
    devices = instr.content["device"]

    if not devices:
        with pytest.raises(InvalidDeviceError):
            device_server._assert_device_is_valid(instr)
        return

    if not isinstance(devices, list):
        devices = [devices]

    for dev in devices:
        if dev not in device_server.device_manager.devices:
            with pytest.raises(InvalidDeviceError) as exc_info:
                device_server._assert_device_is_valid(instr)
            assert exc_info.value.args[0] == f"There is no device with the name {dev}."
        else:
            device_server._assert_device_is_enabled(instr)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="set",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="read",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="rpc",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="kickoff",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="trigger",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="unstage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="run",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions(instr):
    device_server = load_DeviceServerMock()

    device_server._assert_device_is_valid = mock.MagicMock()
    device_server._assert_device_is_enabled = mock.MagicMock()
    device_server._update_device_metadata = mock.MagicMock()

    device_server._set_device = mock.MagicMock()
    device_server._read_device = mock.MagicMock()
    device_server._run_rpc = mock.MagicMock()
    device_server._kickoff_device = mock.MagicMock()
    device_server._trigger_device = mock.MagicMock()
    device_server._stage_device = mock.MagicMock()
    device_server._unstage_device = mock.MagicMock()

    msg = BECMessage.DeviceInstructionMessage.dumps(instr)

    device_server.handle_device_instructions(msg)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)
    action = instructions.content["action"]

    if instructions.content["device"] is not None:
        device_server._assert_device_is_valid.assert_called_once_with(instructions)
        if action != "rpc":
            # rpc has its own error handling
            device_server._assert_device_is_enabled.assert_called_once_with(instructions)
        device_server._update_device_metadata.assert_called_once_with(instructions)

    if action == "set":
        device_server._set_device.assert_called_once_with(instructions)
    elif action == "read":
        device_server._read_device.assert_called_once_with(instructions)
    elif action == "rpc":
        device_server._run_rpc.assert_called_once_with(instructions)
    elif action == "kickoff":
        device_server._kickoff_device.assert_called_once_with(instructions)
    elif action == "trigger":
        device_server._trigger_device.assert_called_once_with(instructions)
    elif action == "stage":
        device_server._stage_device.assert_called_once_with(instructions)
    elif action == "unstage":
        device_server._unstage_device.assert_called_once_with(instructions)
