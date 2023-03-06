from unittest import mock

from bec_utils import BECMessage
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
        action="set", config={"samx": {"enabled": True}}, metadata={}
    )
    with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
        config_handler._set_config(msg)
        req_reply.assert_called_once_with(accepted=True, error_msg=None, metadata={})


def test_config_handler_set_config_with_scibec(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    config_handler = scibec_connector.config_handler
    msg = BECMessage.DeviceConfigMessage(
        action="set", config={"samx": {"enabled": True}}, metadata={}
    )
    scibec_connector.scibec_info = {"beamline": {"info": []}}
    with mock.patch.object(scibec_connector, "scibec") as scibec:
        with mock.patch.object(config_handler, "send_config_request_reply") as req_reply:
            with mock.patch.object(scibec_connector, "update_session") as update_session:
                config_handler._set_config(msg)
                scibec.set_session_data.assert_called_once_with(
                    {"info": []}, {"samx": {"enabled": True}}
                )
                req_reply.assert_called_once_with(accepted=True, error_msg=None, metadata={})
                update_session.assert_called_once()
