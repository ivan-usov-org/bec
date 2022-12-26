from unittest import mock

import pytest
from bec_utils import BECMessage, MessageEndpoints
from bec_utils.tests.utils import ConnectorMock
from ophyd import Staged
from test_device_manager_ds import load_device_manager

from device_server import DeviceServer

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
        )
    ],
)
def test_read_device(instr):
    device_server = load_DeviceServerMock()
    device_server._read_device(instr)
    res = [
        msg
        for msg in device_server.producer.message_sent
        if msg["queue"] == MessageEndpoints.device_read("samx")
    ]
    assert BECMessage.DeviceMessage.loads(res[-1]["msg"]).metadata["RID"] == "test"


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
