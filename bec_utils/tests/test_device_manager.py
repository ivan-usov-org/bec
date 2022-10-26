import os
from unittest import mock

import bec_utils
import pytest
import yaml
from bec_utils import BECMessage
from bec_utils.devicemanager import DeviceManagerBase
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
