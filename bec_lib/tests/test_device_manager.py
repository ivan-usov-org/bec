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
from bec_lib.device import Device, Status
from bec_lib.devicemanager import DeviceConfigError, DeviceContainer, DeviceManagerBase, DeviceType
from bec_lib.tests.utils import (
    ConnectorMock,
    DMClientMock,
    create_session_from_config,
    dm,
    dm_with_devices,
)

dir_path = os.path.dirname(bec_lib.__file__)


def test_dm_initialize(dm):
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
def test_parse_config_request(dm, msg):
    dm.parse_config_message(msg)


def test_config_request_update(dm_with_devices):
    dm = dm_with_devices
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


def test_config_request_reload(dm_with_devices):
    dm = dm_with_devices

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
def test_check_request_validity(dm, msg, raised):
    if raised:
        with pytest.raises(DeviceConfigError):
            dm.check_request_validity(msg)
    else:
        dm.check_request_validity(msg)


def test_get_config_calls_load(dm):
    with mock.patch.object(
        dm, "_get_redis_device_config", return_value={"devices": [{}]}
    ) as get_redis_config:
        with mock.patch.object(dm, "_load_session") as load_session:
            with mock.patch.object(dm, "producer") as producer:
                dm._get_config()
                get_redis_config.assert_called_once()
                load_session.assert_called_once()


def test_get_devices_with_tags(dm):
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


def test_show_tags(dm):
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
def test_monitored_devices_are_unique(dm_with_devices, scan_motors_in, readout_priority_in):
    dm = dm_with_devices
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
def test_monitored_devices_with_readout_priority(
    dm_with_devices, scan_motors_in, readout_priority_in
):
    dm = dm_with_devices
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


@pytest.mark.parametrize(
    "scan_motors_in,readout_priority_in",
    [
        ([], {}),
        ([], {"monitored": ["samx"], "baseline": [], "on_request": []}),
        ([], {"monitored": [], "baseline": ["samx"], "on_request": []}),
        ([], {"monitored": ["samx", "samy"], "baseline": [], "on_request": ["bpm4i"]}),
        (
            [],
            {
                "monitored": ["samx", "samy"],
                "baseline": [],
                "on_request": ["bpm4i"],
                "async": ["bpm3i"],
            },
        ),
        (
            [],
            {
                "monitored": ["samx", "samy"],
                "baseline": [],
                "on_request": ["bpm4i"],
                "async": ["bpm3i"],
                "continuous": ["bpm2i"],
            },
        ),
    ],
)
def test_baseline_devices(dm_with_devices, scan_motors_in, readout_priority_in):
    dm = dm_with_devices
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
    assert len(set(readout_priority_in.get("async", [])) & primary_device_names) == 0
    assert len(set(readout_priority_in.get("continuous", [])) & primary_device_names) == 0


def test_device_config_update_callback(dm_with_devices):
    dm = dm_with_devices
    dev_config_msg = messages.DeviceConfigMessage(action="update", config={"samx": {}})
    msg = MessageObject(value=dev_config_msg.dumps(), topic="")

    with mock.patch.object(dm, "parse_config_message") as parse_config_message:
        dm._device_config_update_callback(msg, parent=dm)
        parse_config_message.assert_called_once_with(dev_config_msg)
