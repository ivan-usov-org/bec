import os
from unittest import mock

import msgpack
import pytest
import yaml

import bec_lib
from bec_lib import messages
from bec_lib.bec_errors import DeviceConfigError
from bec_lib.config_helper import ConfigHelper

dir_path = os.path.dirname(bec_lib.__file__)


def test_load_demo_config():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    with mock.patch.object(config_helper, "update_session_with_file") as mock_update:
        config_helper.load_demo_config()
        dirpath = os.path.dirname(bec_lib.__file__)
        fpath = os.path.join(dirpath, "configs/demo_config.yaml")
        mock_update.assert_called_once_with(fpath)


def test_config_helper_update_session_with_file():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    with mock.patch.object(config_helper, "send_config_request") as mock_send_config_request:
        with mock.patch.object(
            config_helper, "_load_config_from_file"
        ) as mock_load_config_from_file:
            mock_load_config_from_file.return_value = {"test": "test"}
            config_helper.update_session_with_file("test.yaml")
            mock_send_config_request.assert_called_once_with(action="set", config={"test": "test"})


def test_config_helper_load_config_from_file():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    config = config_helper._load_config_from_file(f"{dir_path}/tests/test_config.yaml")


def test_config_helper_save_current_session():
    connector = mock.MagicMock()

    config_helper = ConfigHelper(connector)
    connector.producer().get.return_value = msgpack.dumps(
        [
            {
                "id": "648c817f67d3c7cd6a354e8e",
                "createdAt": "2023-06-16T15:36:31.215Z",
                "createdBy": "unknown user",
                "name": "pinz",
                "sessionId": "648c817d67d3c7cd6a354df2",
                "enabled": True,
                "readOnly": False,
                "deviceClass": "SynAxisOPAAS",
                "deviceTags": ["user motors"],
                "deviceConfig": {
                    "delay": 1,
                    "labels": "pinz",
                    "limits": [-50, 50],
                    "name": "pinz",
                    "speed": 100,
                    "tolerance": 0.01,
                    "update_frequency": 400,
                },
                "readoutPriority": "baseline",
                "onFailure": "retry",
            },
            {
                "id": "648c817f67d3c7cd6a354ec5",
                "createdAt": "2023-06-16T15:36:31.764Z",
                "createdBy": "unknown user",
                "name": "transd",
                "sessionId": "648c817d67d3c7cd6a354df2",
                "enabled": True,
                "readOnly": False,
                "deviceClass": "SynAxisMonitor",
                "deviceTags": ["beamline"],
                "deviceConfig": {"labels": "transd", "name": "transd", "tolerance": 0.5},
                "readoutPriority": "monitored",
                "onFailure": "retry",
            },
        ]
    )
    with mock.patch("builtins.open", mock.mock_open()) as mock_open:
        config_helper.save_current_session("test.yaml")
        out_data = {
            "pinz": {
                "deviceClass": "SynAxisOPAAS",
                "deviceTags": ["user motors"],
                "enabled": True,
                "readOnly": False,
                "deviceConfig": {
                    "delay": 1,
                    "labels": "pinz",
                    "limits": [-50, 50],
                    "name": "pinz",
                    "speed": 100,
                    "tolerance": 0.01,
                    "update_frequency": 400,
                },
                "readoutPriority": "baseline",
                "onFailure": "retry",
            },
            "transd": {
                "deviceClass": "SynAxisMonitor",
                "deviceTags": ["beamline"],
                "enabled": True,
                "readOnly": False,
                "deviceConfig": {"labels": "transd", "name": "transd", "tolerance": 0.5},
                "readoutPriority": "monitored",
                "onFailure": "retry",
            },
        }
        mock_open().write.assert_called_once_with(yaml.dump(out_data))


def test_send_config_request_raises_with_empty_config():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    with mock.patch.object(config_helper, "wait_for_config_reply") as mock_wait_for_config_reply:
        with pytest.raises(DeviceConfigError):
            config_helper.send_config_request(action="update")
            mock_wait_for_config_reply.assert_called_once_with(mock.ANY)


def test_send_config_request():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    with mock.patch.object(config_helper, "wait_for_config_reply") as mock_wait_for_config_reply:
        config_helper.send_config_request(action="update", config={"test": "test"})
        mock_wait_for_config_reply.return_value = messages.RequestResponseMessage(
            accepted=True, message="test"
        )
        mock_wait_for_config_reply.assert_called_once_with(mock.ANY)


def test_send_config_request_raises_for_rejected_update():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    with mock.patch.object(config_helper, "wait_for_config_reply") as mock_wait_for_config_reply:
        mock_wait_for_config_reply.return_value = messages.RequestResponseMessage(
            accepted=False, message="test"
        )
        with pytest.raises(DeviceConfigError):
            config_helper.send_config_request(action="update", config={"test": "test"})
            mock_wait_for_config_reply.assert_called_once_with(mock.ANY)


def test_wait_for_config_reply():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    connector.producer().get.return_value = messages.RequestResponseMessage(
        accepted=True, message="test"
    ).dumps()

    res = config_helper.wait_for_config_reply("test")
    assert res == messages.RequestResponseMessage(accepted=True, message="test")


def test_wait_for_config_raises_timeout():
    connector = mock.MagicMock()
    config_helper = ConfigHelper(connector)
    connector.producer().get.return_value = None

    with pytest.raises(DeviceConfigError):
        config_helper.wait_for_config_reply("test", timeout=0.3)
