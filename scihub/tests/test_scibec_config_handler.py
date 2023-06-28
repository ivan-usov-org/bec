from unittest import mock

import pytest
from bec_lib.core import BECMessage, Device
from bec_lib.core.bec_errors import DeviceConfigError
from fastjsonschema import JsonSchemaException
from test_scibec_connector import SciHubMock

from scihub.scibec import SciBecConnector


def test_parse_config_request_update(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="update", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "_update_config") as update_config, mock.patch.object(
        config_handler.device_manager, "check_request_validity"
    ) as req_validity:
        config_handler.parse_config_request(msg)
        req_validity.assert_called_once_with(msg)
        update_config.assert_called_once_with(msg)


def test_parse_config_request_reload(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(action="reload", config={}, metadata={})
    with mock.patch.object(config_handler, "_reload_config") as reload_config, mock.patch.object(
        config_handler.device_manager, "check_request_validity"
    ) as req_validity:
        config_handler.parse_config_request(msg)
        req_validity.assert_called_once_with(msg)
        reload_config.assert_called_once_with(msg)


def test_parse_config_request_set(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="set", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "_set_config") as set_config, mock.patch.object(
        config_handler.device_manager, "check_request_validity"
    ) as req_validity:
        config_handler.parse_config_request(msg)
        req_validity.assert_called_once_with(msg)
        set_config.assert_called_once_with(msg)


def test_parse_config_request_exception(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="update", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
        with mock.patch("scihub.scibec.config_handler.traceback.format_exc") as exc:
            with mock.patch.object(config_handler, "_update_config", side_effect=AttributeError()):
                config_handler.parse_config_request(msg)
                req_reply.assert_called_once_with(accepted=False, error_msg=exc(), metadata={})


def test_config_handler_reload_config(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(action="reload", config={}, metadata={})
    with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
        with mock.patch.object(config_handler, "send_config") as send:
            config_handler.parse_config_request(msg)
            send.assert_called_once_with(msg)


def test_config_handler_reload_config_with_scibec(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(action="reload", config={}, metadata={})
    with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
        with mock.patch.object(scibec_connector, "scibec"):
            with mock.patch.object(scibec_connector, "update_session") as update_session:
                with mock.patch.object(config_handler, "send_config") as send:
                    config_handler.parse_config_request(msg)
                    send.assert_called_once_with(msg)
                    update_session.assert_called_once()


def test_config_handler_set_config(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="set", config={"samx": {"status": {"enabled": True}}}, metadata={}
    )
    with mock.patch.object(config_handler.validator, "validate_device") as validator:
        with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
            config_handler._set_config(msg)
            req_reply.assert_called_once_with(accepted=True, error_msg=None, metadata={})
            validator.assert_called_once_with({"enabled": True, "name": "samx"})


def test_config_handler_set_invalid_config_raises(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="set", config={"samx": {"status": {"enabled": True}}}, metadata={}
    )
    with pytest.raises(JsonSchemaException):
        with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
            config_handler._set_config(msg)
            req_reply.assert_called_once_with(accepted=True, error_msg=None, metadata={})


def test_config_handler_set_config_with_scibec(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="set", config={"samx": {"enabled": True}}, metadata={}
    )
    scibec_connector.scibec_info = {"beamline": {"info": [], "activeExperiment": "12345"}}
    with mock.patch.object(scibec_connector, "scibec") as scibec:
        with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
            with mock.patch.object(scibec_connector, "update_session") as update_session:
                config_handler._set_config(msg)
                scibec.set_session_data.assert_called_once_with(
                    "12345", {"samx": {"enabled": True}}
                )
                req_reply.assert_called_once_with(accepted=True, error_msg=None, metadata={})
                update_session.assert_called_once()


def test_config_handler_update_config(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    dev = config_handler.device_manager.devices
    dev.samx = Device("samx", {})
    msg = BECMessage.DeviceConfigMessage(
        action="update", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(
        config_handler, "_update_device_config", return_value=True
    ) as update_device_config:
        with mock.patch.object(config_handler, "update_config_in_redis") as update_config_in_redis:
            with mock.patch.object(config_handler, "send_config") as send_config:
                with mock.patch.object(
                    config_handler, "send_config_request_reply"
                ) as send_config_request_reply:
                    config_handler._update_config(msg)
                    update_device_config.assert_called_once_with(dev["samx"], {"enabled": True})
                    update_config_in_redis.assert_called_once_with(dev["samx"])

                    send_config.assert_called_once_with(msg)
                    send_config_request_reply.assert_called_once_with(
                        accepted=True, error_msg=None, metadata={}
                    )


def test_config_handler_update_config_not_updated(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    dev = config_handler.device_manager.devices
    dev.samx = Device("samx", {})
    msg = BECMessage.DeviceConfigMessage(
        action="update", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(
        config_handler, "_update_device_config", return_value=False
    ) as update_device_config:
        with mock.patch.object(config_handler, "update_config_in_redis") as update_config_in_redis:
            with mock.patch.object(config_handler, "send_config") as send_config:
                with mock.patch.object(
                    config_handler, "send_config_request_reply"
                ) as send_config_request_reply:
                    config_handler._update_config(msg)
                    update_device_config.assert_called_once_with(dev["samx"], {"enabled": True})
                    update_config_in_redis.assert_not_called()

                    send_config.assert_not_called()
                    send_config_request_reply.assert_not_called()


def test_config_handler_update_device_config_enable(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    dev = config_handler.device_manager.devices
    dev.samx = Device("samx", {})
    with mock.patch.object(config_handler, "_update_device_server") as update_dev_server:
        with mock.patch.object(
            config_handler, "_wait_for_device_server_update", return_value=True
        ) as wait:
            with mock.patch("scihub.scibec.config_handler.uuid") as uuid:
                device = dev["samx"]
                rid = str(uuid.uuid4())
                config_handler._update_device_config(device, {"enabled": True})
                # mock doesn't copy the data, hence the popped result:
                update_dev_server.assert_called_once_with(rid, {device.name: {}})
                wait.assert_called_once_with(rid)


def test_config_handler_update_device_config_deviceConfig(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    dev = config_handler.device_manager.devices
    dev.samx = Device("samx", {})
    with mock.patch.object(config_handler, "_update_device_server") as update_dev_server:
        with mock.patch.object(
            config_handler, "_wait_for_device_server_update", return_value=True
        ) as wait:
            with mock.patch("scihub.scibec.config_handler.uuid") as uuid:
                device = dev["samx"]
                rid = str(uuid.uuid4())
                config_handler._update_device_config(
                    device, {"deviceConfig": {"something": "to_update"}}
                )
                # mock doesn't copy the data, hence the popped result:
                update_dev_server.assert_called_once_with(rid, {device.name: {}})
                wait.assert_called_once_with(rid)


def test_config_handler_update_device_config_misc(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    dev = config_handler.device_manager.devices
    dev.samx = Device("samx", {})
    with mock.patch.object(config_handler, "_validate_update") as validate_update:
        device = dev["samx"]
        config_handler._update_device_config(device, {"enabled_set": False})
        validate_update.assert_called_once_with({"enabled_set": False})


def test_config_handler_update_device_config_raise(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    dev = config_handler.device_manager.devices
    dev.samx = Device("samx", {})
    with mock.patch.object(config_handler, "_validate_update") as validate_update:
        device = dev["samx"]
        with pytest.raises(DeviceConfigError):
            config_handler._update_device_config(device, {"doesnt_exist": False})
