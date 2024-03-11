import copy
import os
from unittest import mock

import bec_lib
import pytest
import yaml
from bec_lib import messages
from bec_lib.tests.utils import ConnectorMock, create_session_from_config, load_test_config
from test_device_manager_ds import device_manager

from device_server.devices.config_update_handler import ConfigUpdateHandler
from device_server.devices.devicemanager import DeviceConfigError, DeviceManagerDS

dir_path = os.path.dirname(bec_lib.__file__)


def test_request_response():
    service_mock = mock.MagicMock()
    service_mock.connector = ConnectorMock("")
    device_manager = DeviceManagerDS(service_mock)

    def get_config_from_mock():
        device_manager._session = copy.deepcopy(load_test_config())
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

    # bpm4i doesn't have a controller, so it should be destroyed
    msg = messages.DeviceConfigMessage(action="update", config={"bpm4i": {"enabled": False}})
    handler._update_config(msg)
    assert device_manager.devices.bpm4i.enabled is False
    assert device_manager.devices.bpm4i.initialized is False
    assert device_manager.devices.bpm4i.obj._destroyed is True

    msg = messages.DeviceConfigMessage(action="update", config={"bpm4i": {"enabled": True}})
    handler._update_config(msg)
    assert device_manager.devices.bpm4i.enabled is True
    assert device_manager.devices.bpm4i.initialized is True
    assert device_manager.devices.bpm4i.obj._destroyed is False


def test_config_handler_update_config_raises(device_manager):
    handler = ConfigUpdateHandler(device_manager)

    msg = messages.DeviceConfigMessage(
        action="update", config={"samx": {"deviceConfig": {"doesntexist": True}}}
    )
    old_config = device_manager.devices.samx._config["deviceConfig"].copy()
    with pytest.raises(DeviceConfigError):
        handler._update_config(msg)
    assert device_manager.devices.samx._config["deviceConfig"] == old_config


def test_reload_action(device_manager):
    handler = ConfigUpdateHandler(device_manager)
    dm = handler.device_manager
    with mock.patch.object(dm.devices.samx.obj, "destroy") as obj_destroy:
        with mock.patch.object(dm, "_get_config") as get_config:
            handler._reload_config()
            obj_destroy.assert_called_once()
            get_config.assert_called_once()


def test_parse_config_request_update(device_manager):
    handler = ConfigUpdateHandler(device_manager)
    msg = messages.DeviceConfigMessage(
        action="update", config={"samx": {"deviceConfig": {"doesntexist": True}}}
    )
    with mock.patch.object(handler, "_update_config") as update_config:
        handler.parse_config_request(msg)
        update_config.assert_called_once_with(msg)


def test_parse_config_request_reload(device_manager):
    handler = ConfigUpdateHandler(device_manager)
    dm = handler.device_manager
    dm.failed_devices = ["samx"]
    msg = messages.DeviceConfigMessage(action="reload", config={})
    with mock.patch.object(handler, "_reload_config") as reload_config:
        handler.parse_config_request(msg)
        reload_config.assert_called_once()
        assert msg.metadata["failed_devices"] == ["samx"]
