from unittest import mock

import pytest
from bec_lib import DeviceBase, messages
from bec_lib.bec_errors import DeviceConfigError
from bec_lib.tests.utils import ConnectorMock
from fastjsonschema import JsonSchemaException
from test_scibec_connector import SciBecMock, SciHubMock

from scihub import SciHub
from scihub.scibec import ConfigHandler, SciBecConnector


@pytest.fixture()
def config_handler(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    with mock.patch.object(scibec_connector, "_start_config_request_handler"):
        with mock.patch.object(scibec_connector, "_start_metadata_handler"):
            with mock.patch.object(scibec_connector, "_start_scibec_account_update"):
                scibec_connector.scibec = None
                yield scibec_connector.config_handler


def test_parse_config_request_update(config_handler):
    msg = messages.DeviceConfigMessage(
        action="update", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "_update_config") as update_config, mock.patch.object(
        config_handler.device_manager, "check_request_validity"
    ) as req_validity:
        config_handler.parse_config_request(msg)
        req_validity.assert_called_once_with(msg)
        update_config.assert_called_once_with(msg)


def test_parse_config_request_reload(config_handler):
    msg = messages.DeviceConfigMessage(action="reload", config={}, metadata={})
    with mock.patch.object(config_handler, "_reload_config") as reload_config, mock.patch.object(
        config_handler.device_manager, "check_request_validity"
    ) as req_validity:
        config_handler.parse_config_request(msg)
        req_validity.assert_called_once_with(msg)
        reload_config.assert_called_once_with(msg)


def test_parse_config_request_set(config_handler):
    msg = messages.DeviceConfigMessage(
        action="set", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "_set_config") as set_config, mock.patch.object(
        config_handler.device_manager, "check_request_validity"
    ) as req_validity:
        config_handler.parse_config_request(msg)
        req_validity.assert_called_once_with(msg)
        set_config.assert_called_once_with(msg)


def test_parse_config_request_exception(config_handler):
    msg = messages.DeviceConfigMessage(
        action="update", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
        with mock.patch("scihub.scibec.config_handler.traceback.format_exc") as exc:
            with mock.patch.object(config_handler, "_update_config", side_effect=AttributeError()):
                config_handler.parse_config_request(msg)
                req_reply.assert_called_once_with(accepted=False, error_msg=exc(), metadata={})


def test_config_handler_reload_config(config_handler):
    msg = messages.DeviceConfigMessage(action="reload", config={}, metadata={})
    with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
        with mock.patch.object(config_handler, "send_config") as send:
            config_handler.parse_config_request(msg)
            send.assert_called_once_with(msg)


### Commented out as config updates on scibec are not supported yet

# def test_config_handler_reload_config_with_scibec(SciHubMock):
#     scibec_connector = SciBecMock
#     config_handler = scibec_connector.config_handler
#     msg = messages.DeviceConfigMessage(action="reload", config={}, metadata={})
#     with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
#         with mock.patch.object(scibec_connector, "scibec"):
#             with mock.patch.object(scibec_connector, "update_session") as update_session:
#                 with mock.patch.object(config_handler, "send_config") as send:
#                     config_handler.parse_config_request(msg)
#                     send.assert_called_once_with(msg)
#                     update_session.assert_called_once()


@pytest.mark.parametrize(
    "config, expected",
    [
        ({"samx": {"enabled": True}}, {"name": "samx", "enabled": True}),
        (
            {"samx": {"enabled": True, "deviceConfig": None}},
            {"name": "samx", "enabled": True, "deviceConfig": {}},
        ),
    ],
)
def test_config_handler_set_config(config_handler, config, expected):
    msg = messages.DeviceConfigMessage(action="set", config=config, metadata={"RID": "12345"})
    with mock.patch.object(config_handler.validator, "validate_device") as validator:
        with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
            with mock.patch.object(config_handler, "send_config") as send_config:
                config_handler._set_config(msg)
                req_reply.assert_called_once_with(
                    accepted=True, error_msg=None, metadata={"RID": "12345"}
                )
                validator.assert_called_once_with(expected)
                send_config.assert_called_once_with(
                    messages.DeviceConfigMessage(
                        action="reload", config={}, metadata={"RID": "12345"}
                    )
                )


def test_config_handler_set_invalid_config_raises(config_handler):
    msg = messages.DeviceConfigMessage(
        action="set", config={"samx": {"status": {"enabled": True}}}, metadata={"RID": "12345"}
    )
    with pytest.raises(JsonSchemaException):
        with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
            config_handler._set_config(msg)
            req_reply.assert_called_once_with(
                accepted=True, error_msg=None, metadata={"RID": "12345"}
            )


### Commented out as config updates on scibec are not supported yet

# def test_config_handler_set_config_with_scibec(SciHubMock):
#     scibec_connector = SciBecMock
#     config_handler = scibec_connector.config_handler
#     msg = messages.DeviceConfigMessage(
#         action="set", config={"samx": {"enabled": True}}, metadata={}
#     )
#     scibec_connector.scibec_info = {"beamline": {"info": [], "activeExperiment": "12345"}}
#     with mock.patch.object(scibec_connector, "scibec") as scibec:
#         with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
#             with mock.patch.object(scibec_connector, "update_session") as update_session:
#                 config_handler._set_config(msg)
#                 scibec.set_session_data.assert_called_once_with(
#                     "12345", {"samx": {"enabled": True}}
#                 )
#                 req_reply.assert_called_once_with(accepted=True, error_msg=None, metadata={})
#                 update_session.assert_called_once()


def test_config_handler_update_config(config_handler):
    dev = config_handler.device_manager.devices
    dev.samx = DeviceBase(name="samx", config={})
    msg = messages.DeviceConfigMessage(
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


def test_config_handler_update_config_not_updated(config_handler):
    dev = config_handler.device_manager.devices
    dev.samx = DeviceBase(name="samx", config={})
    msg = messages.DeviceConfigMessage(
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


def test_config_handler_update_device_config_enable(config_handler):
    dev = config_handler.device_manager.devices
    dev.samx = DeviceBase(name="samx", config={})
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


def test_config_handler_update_device_config_deviceConfig(config_handler):
    dev = config_handler.device_manager.devices
    dev.samx = DeviceBase(name="samx", config={"deviceConfig": {}})
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
                assert dev.samx._config == {"deviceConfig": {"something": "to_update"}}


def test_config_handler_update_device_config_misc(config_handler):
    dev = config_handler.device_manager.devices
    dev.samx = DeviceBase(name="samx", config={})
    with mock.patch.object(config_handler, "_validate_update") as validate_update:
        device = dev["samx"]
        config_handler._update_device_config(device, {"readOnly": True})
        validate_update.assert_called_once_with({"readOnly": True})


def test_config_handler_update_device_config_raise(config_handler):
    dev = config_handler.device_manager.devices
    dev.samx = DeviceBase(name="samx", config={})
    with mock.patch.object(config_handler, "_validate_update") as validate_update:
        device = dev["samx"]
        with pytest.raises(DeviceConfigError):
            config_handler._update_device_config(device, {"doesnt_exist": False})
