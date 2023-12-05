# pylint: skip-file
import os
from collections import defaultdict
from unittest import mock

import pytest
import yaml
from rich.console import Console
from rich.table import Table

import bec_lib
from bec_lib import messages
from bec_lib.connector import MessageObject
from bec_lib.devicemanager import (
    Device,
    DeviceConfigError,
    DeviceContainer,
    DeviceManagerBase,
    Status,
)
from bec_lib.tests.utils import ConnectorMock, create_session_from_config

dir_path = os.path.dirname(bec_lib.__file__)


def test_dm_initialize():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with mock.patch.object(dm, "_get_config") as get_config:
        dm.initialize("")
        get_config.assert_called_once()


@pytest.mark.parametrize(
    "msg",
    [
        (messages.DeviceConfigMessage(action="update", config={})),
        (messages.DeviceConfigMessage(action="add", config={})),
        (messages.DeviceConfigMessage(action="remove", config={})),
    ],
)
def test_parse_config_request(msg):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    dm.parse_config_message(msg)


def test_config_request_update():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()
    msg = messages.DeviceConfigMessage(action="update", config={})
    dm.parse_config_message(msg)

    msg = messages.DeviceConfigMessage(
        action="update", config={"samx": {"deviceConfig": {"tolerance": 1}}}
    )
    dm.parse_config_message(msg)
    assert dm.devices.samx._config["deviceConfig"]["tolerance"] == 1

    msg = messages.DeviceConfigMessage(action="update", config={"samx": {"enabled": False}})
    dm.parse_config_message(msg)
    assert dm.devices.samx._config["enabled"] is False


def test_config_request_reload():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()

    msg = messages.DeviceConfigMessage(action="reload", config=None)
    with mock.patch.object(dm, "_get_config") as get_config:
        dm.parse_config_message(msg)
        assert len(dm.devices) == 0
        get_config.assert_called_once()


@pytest.mark.parametrize(
    "msg,raised",
    [
        (messages.DeviceConfigMessage(action="wrong_action", config={}), True),
        (messages.DeviceConfigMessage(action="add", config={}), True),
        (messages.DeviceConfigMessage(action="remove", config={}), True),
        (messages.DeviceConfigMessage(action="reload", config={}), False),
        (messages.DeviceConfigMessage(action="add", config={"new_device": {}}), False),
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
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    available_tags = defaultdict(lambda: [])
    for dev_name, dev in config_content.items():
        tags = dev.get("deviceTags")
        if tags is None:
            continue
        for tag in tags:
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
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    available_tags = defaultdict(lambda: [])
    for dev_name, dev in config_content.items():
        tags = dev.get("deviceTags")
        if tags is None:
            continue
        for tag in tags:
            available_tags[tag].append(dev_name)

    assert set(dm.devices.show_tags()) == set(available_tags.keys())


@pytest.mark.parametrize(
    "scan_motors_in,readout_priority_in",
    [([], {}), (["samx"], {}), ([], {"monitored": ["samx"]}), ([], {"baseline": ["samx"]})],
)
def test_monitored_devices_are_unique(scan_motors_in, readout_priority_in):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    scan_motors = [dm.devices.get(dev) for dev in scan_motors_in]
    devices = dm.devices.monitored_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    device_names = set(dev.name for dev in devices)
    assert len(device_names) == len(devices)


@pytest.mark.parametrize(
    "scan_motors_in,readout_priority_in",
    [
        ([], {}),
        ([], {"monitored": ["samx"], "baseline": [], "on_request": []}),
        ([], {"monitored": [], "baseline": ["samx"], "on_request": []}),
        ([], {"monitored": ["samx", "samy"], "baseline": [], "on_request": ["bpm4i"]}),
    ],
)
def test_monitored_devices_with_readout_priority(scan_motors_in, readout_priority_in):
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    scan_motors = [dm.devices.get(dev) for dev in scan_motors_in]
    monitored_devices = dm.devices.monitored_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    baseline_devices = dm.devices.baseline_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    primary_device_names = set(dev.name for dev in monitored_devices)
    baseline_devices_names = set(dev.name for dev in baseline_devices)

    assert len(primary_device_names & baseline_devices_names) == 0

    assert len(set(readout_priority_in.get("on_request", [])) & baseline_devices_names) == 0
    assert len(set(readout_priority_in.get("on_request", [])) & primary_device_names) == 0


def test_device_config_update_callback():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector)
    config_content = None
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    dev_config_msg = messages.DeviceConfigMessage(action="update", config={"samx": {}})
    msg = MessageObject(value=dev_config_msg.dumps(), topic="")

    with mock.patch.object(dm, "parse_config_message") as parse_config_message:
        dm._device_config_update_callback(msg, parent=dm)
        parse_config_message.assert_called_once_with(dev_config_msg)


def test_status_wait():
    producer = mock.MagicMock()

    def lrange_mock(*args, **kwargs):
        yield False
        yield True

    def get_lrange(*args, **kwargs):
        return next(lmock)

    lmock = lrange_mock()
    producer.lrange = get_lrange
    status = Status(producer, "test")
    status.wait()


def test_device_get_device_config():
    device = Device("test", {"deviceConfig": {"tolerance": 1}})
    assert device.get_device_config() == {"tolerance": 1}


def test_device_set_device_config():
    parent = mock.MagicMock()
    device = Device("test", {"deviceConfig": {"tolerance": 1}}, parent=parent)
    device.set_device_config({"tolerance": 2})
    assert device.get_device_config() == {"tolerance": 2}
    parent.config_helper.send_config_request.assert_called_once()


def test_get_device_tags():
    device = Device("test", {"deviceTags": ["tag1", "tag2"]})
    assert device.get_device_tags() == ["tag1", "tag2"]

    device = Device("test", {})
    assert device.get_device_tags() == []


def test_set_device_tags():
    parent = mock.MagicMock()
    device = Device("test", {"deviceTags": ["tag1", "tag2"]}, parent=parent)
    device.set_device_tags(["tag3", "tag4"])
    assert device.get_device_tags() == ["tag3", "tag4"]
    parent.config_helper.send_config_request.assert_called_once()


def test_add_device_tag():
    parent = mock.MagicMock()
    device = Device("test", {"deviceTags": ["tag1", "tag2"]}, parent=parent)
    device.add_device_tag("tag3")
    assert device.get_device_tags() == ["tag1", "tag2", "tag3"]
    parent.config_helper.send_config_request.assert_called_once()


def test_add_device_tags_duplicate():
    parent = mock.MagicMock()
    device = Device("test", {"deviceTags": ["tag1", "tag2"]}, parent=parent)
    device.add_device_tag("tag1")
    assert device.get_device_tags() == ["tag1", "tag2"]
    parent.config_helper.send_config_request.assert_not_called()


def test_remove_device_tag():
    parent = mock.MagicMock()
    device = Device("test", {"deviceTags": ["tag1", "tag2"]}, parent=parent)
    device.remove_device_tag("tag1")
    assert device.get_device_tags() == ["tag2"]
    parent.config_helper.send_config_request.assert_called_once()


def test_device_wm():
    parent = mock.MagicMock()
    device = Device("test", {"deviceTags": ["tag1", "tag2"]}, parent=parent)
    with mock.patch.object(parent.devices, "wm", new_callable=mock.PropertyMock) as wm:
        res = device.wm
        parent.devices.wm.assert_called_once()


def test_readout_priority():
    parent = mock.MagicMock()
    device = Device("test", {"readoutPriority": "baseline"}, parent=parent)
    assert device.readout_priority == "baseline"


def test_set_readout_priority():
    parent = mock.MagicMock()
    device = Device("test", {"readoutPriority": "baseline"}, parent=parent)
    device.readout_priority = "monitored"
    assert device.readout_priority == "monitored"
    parent.config_helper.send_config_request.assert_called_once()


def test_on_failure():
    parent = mock.MagicMock()
    device = Device("test", {"onFailure": "buffer"}, parent=parent)
    assert device.on_failure == "buffer"


def test_set_on_failure():
    parent = mock.MagicMock()
    device = Device("test", {"onFailure": "buffer"}, parent=parent)
    device.on_failure = "retry"
    assert device.on_failure == "retry"
    parent.config_helper.send_config_request.assert_called_once()


def test_read_only():
    parent = mock.MagicMock()
    device = Device("test", {"read_only": False}, parent=parent)
    assert device.read_only is False


def test_set_read_only():
    parent = mock.MagicMock()
    device = Device("test", {"read_only": False}, parent=parent)
    device.read_only = True
    assert device.read_only is True
    parent.config_helper.send_config_request.assert_called_once()


def test_device_container_wm():
    devs = DeviceContainer()
    devs["test"] = Device("test", {})
    with mock.patch.object(devs.test, "read", return_value={"test": {"value": 1}}) as read:
        devs.wm("test")


def test_device_container_wm_with_setpoint():
    devs = DeviceContainer()
    devs["test"] = Device("test", {})
    with mock.patch.object(
        devs.test, "read", return_value={"test": {"value": 1}, "test_setpoint": {"value": 1}}
    ) as read:
        devs.wm("test")


def test_device_container_wm_with_user_setpoint():
    devs = DeviceContainer()
    devs["test"] = Device("test", {})
    with mock.patch.object(
        devs.test, "read", return_value={"test": {"value": 1}, "test_user_setpoint": {"value": 1}}
    ) as read:
        devs.wm("test")


def test_show_all():
    # Create a mock Console object
    console = mock.MagicMock()

    # Create a DeviceContainer with some mock Devices
    devs = DeviceContainer()
    devs["dev1"] = Device(
        "dev1",
        {
            "description": "Device 1",
            "enabled": True,
            "readOnly": False,
            "deviceClass": "Class1",
            "readoutPriority": "high",
            "deviceTags": ["tag1", "tag2"],
        },
    )
    devs["dev2"] = Device(
        "dev2",
        {
            "description": "Device 2",
            "enabled": False,
            "readOnly": True,
            "deviceClass": "Class2",
            "readoutPriority": "low",
            "deviceTags": ["tag3", "tag4"],
        },
    )

    # Call show_all with the mock Console
    devs.show_all(console)

    # check that the device names were printed
    table = console.print.call_args[0][0]
    assert len(table.rows) == 2
    assert list(table.columns[0].cells) == ["dev1", "dev2"]
    # Check that Console.print was called with a Table containing the correct data
    console.print.assert_called_once()
