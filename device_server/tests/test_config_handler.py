import os
from unittest import mock

import bec_lib
import pytest
import yaml
from bec_lib import messages
from bec_lib.tests.utils import ConnectorMock, create_session_from_config
from test_device_manager_ds import device_manager

from device_server.devices.config_update_handler import ConfigUpdateHandler
from device_server.devices.devicemanager import DeviceConfigError, DeviceManagerDS

dir_path = os.path.dirname(bec_lib.__file__)


def test_request_response():
    service_mock = mock.MagicMock()
    service_mock.connector = ConnectorMock("")
    device_manager = DeviceManagerDS(service_mock)

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
                    with mock.patch.object(
                        device_manager.config_update_handler, "send_config_request_reply"
                    ) as request_reply:
                        device_manager.config_update_handler.parse_config_request(
                            msg=messages.DeviceConfigMessage(
                                action="update", config={"something": "something"}
                            )
                        )
                        request_reply.assert_called_once()


def test_config_handler_update_config(device_manager):
    handler = ConfigUpdateHandler(device_manager)

    msg = messages.DeviceConfigMessage(action="update", config={"samx": {"enabled": False}})
    handler._update_config(msg)
    assert device_manager.devices.samx.enabled is False
    assert device_manager.devices.samx.initialized is False
    assert device_manager.devices.samx.obj._destroyed is True

    msg = messages.DeviceConfigMessage(action="update", config={"samx": {"enabled": True}})
    handler._update_config(msg)
    assert device_manager.devices.samx.enabled is True
    assert device_manager.devices.samx.initialized is True
    assert device_manager.devices.samx.obj._destroyed is False


def test_config_handler_update_config_raises(device_manager):
    handler = ConfigUpdateHandler(device_manager)

    msg = messages.DeviceConfigMessage(
        action="update", config={"samx": {"deviceConfig": {"doesntexist": True}}}
    )
    old_config = device_manager.devices.samx._config["deviceConfig"].copy()
    with pytest.raises(DeviceConfigError):
        handler._update_config(msg)
    assert device_manager.devices.samx._config["deviceConfig"] == old_config
