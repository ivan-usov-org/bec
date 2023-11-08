import traceback
from unittest import mock
from unittest.mock import ANY

import pytest
from ophyd import Staged
from ophyd.utils import errors as ophyd_errors
from test_device_manager_ds import device_manager, load_device_manager

import bec_lib.core
from bec_lib.core import Alarms, BECMessage, MessageEndpoints, ServiceConfig
from bec_lib.core.BECMessage import BECStatus
from bec_lib.core.tests.utils import ConnectorMock
from device_server import DeviceServer
from device_server.device_server import InvalidDeviceError

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


@pytest.fixture(scope="function")
def device_server_mock(device_manager):
    connector = ConnectorMock("")
    device_server = DeviceServerMock(device_manager, connector)
    yield device_server
    device_server.shutdown()


def load_DeviceServerMock():
    connector = ConnectorMock("")
    device_manager = load_device_manager()
    return DeviceServerMock(device_manager, connector)


class DeviceServerMock(DeviceServer):
    def __init__(self, device_manager, connector_cls) -> None:
        config = ServiceConfig(redis={"host": "dummy", "port": 6379})
        super().__init__(config, connector_cls=ConnectorMock)
        self.device_manager = device_manager

    def _start_device_manager(self):
        pass

    def _start_metrics_emitter(self):
        pass

    def _start_update_service_info(self):
        pass


def test_start(device_server_mock):
    device_server = device_server_mock

    device_server.start()

    assert device_server.threads
    assert type(device_server.threads[0]) == bec_lib.core.tests.utils.ConsumerMock
    assert device_server.status == BECStatus.RUNNING


@pytest.mark.parametrize("status", [BECStatus.ERROR, BECStatus.RUNNING, BECStatus.IDLE])
def test_update_status(device_server_mock, status):
    device_server = device_server_mock
    assert device_server.status == BECStatus.BUSY

    device_server.update_status(status)

    assert device_server.status == status


def test_stop(device_server_mock):
    device_server = device_server_mock
    device_server.stop()
    assert device_server.status == BECStatus.IDLE


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
def test_update_device_metadata(device_server_mock, instr):
    device_server = device_server_mock

    devices = instr.content["device"]
    if not isinstance(devices, list):
        devices = [devices]

    device_server._update_device_metadata(instr)

    for dev in devices:
        assert device_server.device_manager.devices.get(dev).metadata == instr.metadata


def test_stop_devices(device_server_mock):
    device_server = device_server_mock
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
def test_assert_device_is_enabled(device_server_mock, instr):
    device_server = device_server_mock
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
def test_assert_device_is_valid(device_server_mock, instr):
    device_server = device_server_mock
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
    ],
)
def test_handle_device_instructions_set(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_assert_device_is_valid") as assert_device_is_valid_mock:
        with mock.patch.object(
            device_server, "_assert_device_is_enabled"
        ) as assert_device_is_enabled_mock:
            with mock.patch.object(
                device_server, "_update_device_metadata"
            ) as update_device_metadata_mock:
                with mock.patch.object(device_server, "_set_device") as set_mock:
                    device_server.handle_device_instructions(msg)

                    assert_device_is_valid_mock.assert_called_once_with(instructions)
                    assert_device_is_enabled_mock.assert_called_once_with(instructions)
                    update_device_metadata_mock.assert_called_once_with(instructions)

                    set_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="set",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_exception(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_assert_device_is_valid") as valid_mock:
        with mock.patch.object(device_server.connector, "log_error") as log_mock:
            with mock.patch.object(device_server.connector, "raise_alarm") as alarm_mock:
                valid_mock.side_effect = Exception("Exception")
                device_server.handle_device_instructions(msg)

                valid_mock.assert_called_once_with(instructions)
                log_mock.assert_called_once_with({"source": msg, "message": ANY})
                alarm_mock.assert_called_once_with(
                    severity=Alarms.MAJOR,
                    source=instructions.content,
                    content=ANY,  # could you set this to anything? or how do i find the traceback?
                    alarm_type="Exception",
                    metadata=instructions.metadata,
                )


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="set",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_limit_error(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server.connector, "raise_alarm") as alarm_mock:
        with mock.patch.object(device_server, "_set_device") as set_mock:
            set_mock.side_effect = ophyd_errors.LimitError("Wrong limits")
            device_server.handle_device_instructions(msg)

            alarm_mock.assert_called_once_with(
                severity=Alarms.MAJOR,
                source=instructions.content,
                content=ANY,
                alarm_type="LimitError",
                metadata=instructions.metadata,
            )


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="read",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_read(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_read_device") as read_mock:
        device_server.handle_device_instructions(msg)
        read_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="rpc",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_rpc(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)
    with mock.patch.object(device_server, "_assert_device_is_valid") as assert_device_is_valid_mock:
        with mock.patch.object(
            device_server, "_assert_device_is_enabled"
        ) as assert_device_is_enabled_mock:
            with mock.patch.object(
                device_server, "_update_device_metadata"
            ) as update_device_metadata_mock:
                with mock.patch.object(device_server, "_run_rpc") as rpc_mock:
                    device_server.handle_device_instructions(msg)
                    rpc_mock.assert_called_once_with(instructions)

                    assert_device_is_valid_mock.assert_called_once_with(instructions)
                    assert_device_is_enabled_mock.assert_not_called()
                    update_device_metadata_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="kickoff",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_kickoff(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_kickoff_device") as kickoff_mock:
        device_server.handle_device_instructions(msg)
        kickoff_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="complete",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_complete(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_complete_device") as complete_mock:
        device_server.handle_device_instructions(msg)
        complete_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="flyer_sim",
            action="complete",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device="bpm4i",
            action="complete",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device=None,
            action="complete",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_complete_device(device_server_mock, instr):
    device_server = device_server_mock
    complete_mock = mock.MagicMock()
    device_server.device_manager.devices.flyer_sim.obj.complete = complete_mock
    device_server._complete_device(instr)
    if instr.content["device"] == "flyer_sim" or instr.content["device"] is None:
        complete_mock.assert_called_once()
    else:
        complete_mock.assert_not_called()


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="pre_scan",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_pre_scan(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_pre_scan") as pre_scan_mock:
        device_server.handle_device_instructions(msg)
        pre_scan_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="trigger",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_trigger(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_trigger_device") as trigger_mock:
        device_server.handle_device_instructions(msg)
        trigger_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="stage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_stage(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_stage_device") as stage_mock:
        device_server.handle_device_instructions(msg)
        stage_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="samx",
            action="unstage",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_handle_device_instructions_unstage(device_server_mock, instr):
    device_server = device_server_mock
    msg = BECMessage.DeviceInstructionMessage.dumps(instr)
    instructions = BECMessage.DeviceInstructionMessage.loads(msg)

    with mock.patch.object(device_server, "_unstage_device") as unstage_mock:
        device_server.handle_device_instructions(msg)
        unstage_mock.assert_called_once_with(instructions)


@pytest.mark.parametrize(
    "instr",
    [
        BECMessage.DeviceInstructionMessage(
            device="eiger",
            action="trigger",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
        BECMessage.DeviceInstructionMessage(
            device=["samx", "samy"],
            action="trigger",
            parameter={},
            metadata={"stream": "primary", "DIID": 1, "RID": "test"},
        ),
    ],
)
def test_trigger_device(device_server_mock, instr):
    device_server = device_server_mock
    devices = instr.content["device"]
    if not isinstance(devices, list):
        devices = [devices]
    for dev in devices:
        with mock.patch.object(
            device_server.device_manager.devices.get(dev).obj, "trigger"
        ) as trigger:
            device_server._trigger_device(instr)
            trigger.assert_called_once()
        assert device_server.device_manager.devices.get(dev).metadata == instr.metadata


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
def test_kickoff_device(device_server_mock, instr):
    device_server = device_server_mock
    with mock.patch.object(
        device_server.device_manager.devices.flyer_sim.obj, "kickoff"
    ) as kickoff:
        device_server._kickoff_device(instr)
        kickoff.assert_called_once()


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
def test_set_device(device_server_mock, instr):
    device_server = device_server_mock
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
def test_read_device(device_server_mock, instr):
    device_server = device_server_mock
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
def test_stage_device(device_server_mock, instr):
    device_server = device_server_mock
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


def test_reload_action(device_server_mock):
    device_server = device_server_mock
    dm = device_server.device_manager
    with mock.patch.object(dm.devices.samx.obj, "destroy") as obj_destroy:
        with mock.patch.object(dm, "_get_config") as get_config:
            dm._reload_action()
            obj_destroy.assert_called_once()
            get_config.assert_called_once()
