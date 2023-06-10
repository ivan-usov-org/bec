import os
from collections import defaultdict
from unittest import mock

import pytest
import yaml

import bec_client_lib
from bec_client_lib.core import BECMessage
from bec_client_lib.core.connector import MessageObject
from bec_client_lib.core.devicemanager import DeviceConfigError, DeviceManagerBase
from bec_client_lib.core.tests.utils import ConnectorMock, create_session_from_config

dir_path = os.path.dirname(bec_client_lib.__file__)


def test_dm_initialize():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with mock.patch.object(dm, "_get_config") as get_config:
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
    dm = DeviceManagerBase(connector)
    dm.parse_config_message(msg)


def test_config_request_update():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()
    msg = BECMessage.DeviceConfigMessage(action="update", config={})
    dm.parse_config_message(msg)

    msg = BECMessage.DeviceConfigMessage(
        action="update", config={"samx": {"deviceConfig": {"tolerance": 1}}}
    )
    dm.parse_config_message(msg)
    assert dm.devices.samx._config["deviceConfig"]["tolerance"] == 1

    msg = BECMessage.DeviceConfigMessage(action="update", config={"samx": {"enabled": False}})
    dm.parse_config_message(msg)
    assert dm.devices.samx._config["enabled"] is False


def test_config_request_reload():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()

    msg = BECMessage.DeviceConfigMessage(action="reload", config=None)
    with mock.patch.object(dm, "_get_config") as get_config:
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
        (BECMessage.DeviceConfigMessage(action="add", config={"new_device": {}}), False),
    ],
)
def test_check_request_validity(msg, raised):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)

    if raised:
        with pytest.raises(DeviceConfigError):
            dm.check_request_validity(msg)
    else:
        dm.check_request_validity(msg)


def test_get_config_calls_load():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with mock.patch.object(
        dm, "_get_redis_device_config", return_value={"devices": [{}]}
    ) as get_redis_config:
        with mock.patch.object(dm, "_load_session") as load_session:
            with mock.patch.object(dm, "producer") as producer:
                dm._get_config()
                get_redis_config.assert_called_once()
                load_session.assert_called_once()


def test_get_devices_with_tags():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    available_tags = defaultdict(lambda: [])
    for dev_name, dev in config_content.items():
        for tag in dev["deviceTags"]:
            available_tags[tag].append(dev_name)

    for tag, devices in available_tags.items():
        dev_list = dm.devices.get_devices_with_tags(tag)
        dev_names = {dev.name for dev in dev_list}
        assert dev_names == set(devices)

    assert len(dm.devices.get_devices_with_tags("someting")) == 0


def test_show_tags():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    available_tags = defaultdict(lambda: [])
    for dev_name, dev in config_content.items():
        for tag in dev["deviceTags"]:
            available_tags[tag].append(dev_name)

    assert set(dm.devices.show_tags()) == set(available_tags.keys())


@pytest.mark.parametrize(
    "scan_motors_in,readout_priority_in",
    [
        ([], {}),
        (["samx"], {}),
        ([], {"monitored": ["samx"]}),
        ([], {"baseline": ["samx"]}),
    ],
)
def test_primary_devices_are_unique(scan_motors_in, readout_priority_in):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    scan_motors = [dm.devices.get(dev) for dev in scan_motors_in]
    devices = dm.devices.primary_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    device_names = set(dev.name for dev in devices)
    assert len(device_names) == len(devices)


@pytest.mark.parametrize(
    "scan_motors_in,readout_priority_in",
    [
        ([], {}),
        ([], {"monitored": ["samx"], "baseline": [], "ignored": []}),
        ([], {"monitored": [], "baseline": ["samx"], "ignored": []}),
        ([], {"monitored": ["samx", "samy"], "baseline": [], "ignored": ["bpm4i"]}),
    ],
)
def test_primary_devices_with_readout_priority(scan_motors_in, readout_priority_in):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    scan_motors = [dm.devices.get(dev) for dev in scan_motors_in]
    primary_devices = dm.devices.primary_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    baseline_devices = dm.devices.baseline_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    primary_device_names = set(dev.name for dev in primary_devices)
    baseline_devices_names = set(dev.name for dev in baseline_devices)

    assert len(primary_device_names & baseline_devices_names) == 0

    assert len(set(readout_priority_in.get("ignored", [])) & baseline_devices_names) == 0
    assert len(set(readout_priority_in.get("ignored", [])) & primary_device_names) == 0


def test_device_config_update_callback():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    dev_config_msg = BECMessage.DeviceConfigMessage(action="update", config={"samx": {}})
    msg = MessageObject(value=dev_config_msg.dumps(), topic="")

    with mock.patch.object(dm, "parse_config_message") as parse_config_message:
        dm._device_config_update_callback(msg, parent=dm)
        parse_config_message.assert_called_once_with(dev_config_msg)
