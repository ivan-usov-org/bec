import os
from unittest import mock

import bec_lib
import numpy as np
import pytest
import yaml
from bec_lib import MessageEndpoints, messages
from bec_lib.tests.utils import ConnectorMock, ProducerMock, create_session_from_config

from device_server.devices.devicemanager import DeviceManagerDS

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_lib.__file__)


class ControllerMock:
    def __init__(self, parent) -> None:
        self.parent = parent

    def on(self):
        self.parent._connected = True

    def off(self):
        self.parent._connected = False


class DeviceMock:
    def __init__(self) -> None:
        self._connected = False
        self.name = "name"

    @property
    def connected(self):
        return self._connected


class DeviceControllerMock(DeviceMock):
    def __init__(self) -> None:
        super().__init__()
        self.controller = ControllerMock(self)


class EpicsDeviceMock(DeviceMock):
    def wait_for_connection(self, timeout):
        self._connected = True


def load_device_manager():
    connector = ConnectorMock("", store_data=False)
    device_manager = DeviceManagerDS(connector, "")
    device_manager.producer = connector.producer()
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    return device_manager


@pytest.fixture(scope="function")
def device_manager():
    device_manager = load_device_manager()
    yield device_manager
    device_manager.shutdown()


def test_device_init(device_manager):
    for dev in device_manager.devices.values():
        if not dev.enabled:
            continue
        assert dev.initialized is True


@pytest.mark.parametrize(
    "obj,raises_error",
    [(DeviceMock(), True), (DeviceControllerMock(), False), (EpicsDeviceMock(), False)],
)
def test_conntect_device(device_manager, obj, raises_error):
    if raises_error:
        with pytest.raises(ConnectionError):
            device_manager.connect_device(obj)
        return
    device_manager.connect_device(obj)


def test_disable_unreachable_devices():
    connector = ConnectorMock("")
    device_manager = DeviceManagerDS(connector)

    def get_config_from_mock():
        with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
            device_manager._session = create_session_from_config(yaml.safe_load(session_file))
        device_manager._load_session()

    def mocked_failed_connection(obj):
        if obj.name == "samx":
            raise ConnectionError

    config_reply = messages.RequestResponseMessage(accepted=True, message="")

    with mock.patch.object(device_manager, "connect_device", wraps=mocked_failed_connection):
        with mock.patch.object(device_manager, "_get_config", get_config_from_mock):
            with mock.patch.object(
                device_manager.config_helper, "wait_for_config_reply", return_value=config_reply
            ):
                with mock.patch.object(device_manager.config_helper, "wait_for_service_response"):
                    device_manager.initialize("")
                    assert device_manager.config_update_handler is not None
                    assert device_manager.devices.samx.enabled is False
                    msg = messages.DeviceConfigMessage(
                        action="update", config={"samx": {"enabled": False}}
                    )


def test_flyer_event_callback():
    device_manager = load_device_manager()
    samx = device_manager.devices.samx
    samx.metadata = {"scanID": "12345"}

    device_manager._obj_flyer_callback(
        obj=samx.obj, value={"data": {"idata": np.random.rand(20), "edata": np.random.rand(20)}}
    )
    pipe = device_manager.producer.pipeline()
    bundle, progress = pipe._pipe_buffer[-2:]

    # check producer method
    assert bundle[0] == "send"
    assert progress[0] == "set_and_publish"

    # check endpoint
    assert bundle[1][0] == MessageEndpoints.device_read("samx")
    assert progress[1][0] == MessageEndpoints.device_progress("samx")

    # check message
    bundle_msg = messages.DeviceMessage.loads(bundle[1][1])
    assert len(bundle_msg) == 20

    progress_msg = messages.DeviceStatusMessage.loads(progress[1][1])
    assert progress_msg.content["status"] == 20


def test_obj_progress_callback():
    device_manager = load_device_manager()
    samx = device_manager.devices.samx
    samx.metadata = {"scanID": "12345"}

    with mock.patch.object(device_manager, "producer") as mock_producer:
        device_manager._obj_progress_callback(obj=samx.obj, value=1, max_value=2, done=False)
        mock_producer.set_and_publish.assert_called_once_with(
            MessageEndpoints.device_progress("samx"),
            messages.ProgressMessage(
                value=1, max_value=2, done=False, metadata={"scanID": "12345"}
            ).dumps(),
        )
