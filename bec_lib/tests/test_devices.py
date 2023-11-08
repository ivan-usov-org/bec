from unittest import mock

import pytest

from bec_lib.core.devicemanager import DeviceManagerBase
from bec_lib.core.tests.utils import ConnectorMock


@pytest.fixture
def device_config():
    return {
        "id": "1c6518b2-b779-4b28-b8b1-31295f8fbf26",
        "accessGroups": "customer",
        "name": "eiger",
        "sessionId": "569ea788-09d7-44fc-a140-b0b34a2b7f6f",
        "enabled": True,
        "enabled_set": True,
        "acquisitionConfig": {
            "acquisitionGroup": "detectors",
            "schedule": "sync",
            "readoutPriority": "monitored",
        },
        "deviceClass": "SynSLSDetector",
        "deviceConfig": {"device_access": True, "labels": "eiger", "name": "eiger"},
        "deviceTags": ["detector"],
    }


def test_create_device_saves_config(device_config):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    obj = dm._create_device(device_config, ())
    assert obj._config == device_config


def test_device_enabled(device_config):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    obj = dm._create_device(device_config, ())
    assert obj.enabled == device_config["enabled"]
    device_config["enabled"] = False
    assert obj.enabled == device_config["enabled"]


def test_device_enable(device_config):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    obj = dm._create_device(device_config, ())
    with mock.patch.object(obj.parent.config_helper, "send_config_request") as config_req:
        obj.enabled = True
        config_req.assert_called_once_with(action="update", config={obj.name: {"enabled": True}})


def test_device_enable_set(device_config):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    obj = dm._create_device(device_config, ())
    with mock.patch.object(obj.parent.config_helper, "send_config_request") as config_req:
        obj.enabled_set = True
        config_req.assert_called_once_with(
            action="update", config={obj.name: {"enabled_set": True}}
        )


@pytest.mark.parametrize(
    "val,raised_error", [({"in": 5}, None), ({"in": 5, "out": 10}, None), ({"5", "4"}, TypeError)]
)
def test_device_set_user_parameter(device_config, val, raised_error):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    obj = dm._create_device(device_config, ())
    with mock.patch.object(obj.parent.config_helper, "send_config_request") as config_req:
        if raised_error is None:
            obj.set_user_parameter(val)
            config_req.assert_called_once_with(
                action="update", config={obj.name: {"userParameter": val}}
            )
        else:
            with pytest.raises(raised_error):
                obj.set_user_parameter(val)


@pytest.mark.parametrize(
    "val,raised_error", [({"in": 5}, None), ({"in": 5, "out": 10}, None), ({"5", "4"}, TypeError)]
)
def test_device_update_user_parameter(device_config, val, raised_error):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    obj = dm._create_device(device_config, ())
    obj._config["userParameter"] = {"in": 2, "out": 5}
    with mock.patch.object(obj.parent.config_helper, "send_config_request") as config_req:
        if raised_error is None:
            obj.update_user_parameter(val)
            config_req.assert_called_once_with(
                action="update", config={obj.name: {"userParameter": obj._config["userParameter"]}}
            )
        else:
            with pytest.raises(raised_error):
                obj.update_user_parameter(val)
