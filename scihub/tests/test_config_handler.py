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
            config_handler.parse_config_request(msg)
            req_reply.assert_called_once_with(accepted=False, error_msg=exc(), metadata={})
