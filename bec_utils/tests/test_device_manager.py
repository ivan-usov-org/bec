import os
from unittest import mock

import bec_utils
import pytest
import yaml
from bec_utils import BECMessage
from bec_utils.devicemanager import DeviceConfigError, DeviceManagerBase
from bec_utils.tests.utils import ConnectorMock, create_session_from_config

dir_path = os.path.dirname(bec_utils.__file__)


def test_dm_initialize():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with mock.patch.object(dm, "_get_config_from_DB") as get_config:
        dm.initialize("")
        get_config.assert_called_once()


@pytest.mark.parametrize(
    "msg",
    [
        (BECMessage.DeviceConfigMessage(action="update", config={})),
        (BECMessage.DeviceConfigMessage(action="add", config={})),
        (BECMessage.DeviceConfigMessage(action="remove", config={})),
    ],
)
def test_parse_config_request(msg):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    dm.parse_config_message(msg)


def test_config_request_update():

    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()
    msg = BECMessage.DeviceConfigMessage(action="update", config={})
    dm.parse_config_message(msg)

    msg = BECMessage.DeviceConfigMessage(
        action="update", config={"samx": {"deviceConfig": {"tolerance": 1}}}
    )
    dm.parse_config_message(msg)
    assert dm.devices.samx.config["deviceConfig"]["tolerance"] == 1

    msg = BECMessage.DeviceConfigMessage(action="update", config={"samx": {"enabled": False}})
    dm.parse_config_message(msg)
    assert dm.devices.samx.config["enabled"] is False


def test_config_request_reload():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()

    msg = BECMessage.DeviceConfigMessage(action="reload", config=None)
    with mock.patch.object(dm, "_get_config_from_DB") as get_config:
        dm.parse_config_message(msg)
        assert len(dm.devices) == 0
        get_config.assert_called_once()


@pytest.mark.parametrize(
    "msg,raised",
    [
        (BECMessage.DeviceConfigMessage(action="wrong_action", config={}), True),
        (BECMessage.DeviceConfigMessage(action="add", config={}), True),
        (BECMessage.DeviceConfigMessage(action="remove", config={}), True),
        (BECMessage.DeviceConfigMessage(action="reload", config={}), False),
    ],
)
def test_check_request_validity(msg, raised):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")

    if raised:
        with pytest.raises(DeviceConfigError):
            dm.check_request_validity(msg)
    else:
        dm.check_request_validity(msg)


def test_get_config_from_DB_no_beamline():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with mock.patch.object(dm._scibec, "get_beamlines", return_value=[]):
        with mock.patch.object(dm, "_load_session") as load_session:
            dm._get_config_from_DB()
            load_session.assert_not_called()


def test_get_config_from_DB_no_active_session():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with mock.patch.object(dm._scibec, "get_beamlines", return_value=[{"name": "test"}]):
        with mock.patch.object(
            dm._scibec, "get_current_session", return_value=None
        ) as current_session:
            with mock.patch.object(dm, "_load_session") as load_session:
                dm._get_config_from_DB()
                current_session.assert_called_once_with("test", include_devices=True)
                load_session.assert_not_called()


def test_get_config_from_DB_no_devices():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with mock.patch.object(dm._scibec, "get_beamlines", return_value=[{"name": "test"}]):
        with mock.patch.object(
            dm._scibec, "get_current_session", return_value={"devices": []}
        ) as current_session:
            with mock.patch.object(dm, "_load_session") as load_session:
                dm._get_config_from_DB()
                current_session.assert_called_once_with("test", include_devices=True)
                load_session.assert_not_called()


def test_get_config_from_DB_calls_load():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with mock.patch.object(dm._scibec, "get_beamlines", return_value=[{"name": "test"}]):
        with mock.patch.object(
            dm._scibec, "get_current_session", return_value={"devices": [{}]}
        ) as current_session:
            with mock.patch.object(dm, "_load_session") as load_session:
                dm._get_config_from_DB()
                current_session.assert_called_once_with("test", include_devices=True)
                load_session.assert_called_once()
