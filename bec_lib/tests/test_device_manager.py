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
from bec_lib.devicemanager import DeviceConfigError, DeviceContainer, DeviceManagerBase
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
            dm._get_config()
            get_redis_config.assert_called_once()
            load_session.assert_called_once()


def test_get_redis_device_config(dm):
    with mock.patch.object(dm, "connector") as connector:
        connector.get.return_value = messages.AvailableResourceMessage(resource={"devices": [{}]})
        assert dm._get_redis_device_config() == {"devices": [{}]}


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


def test_get_software_triggered_devices(dm):
    config_content = None
    with open(f"{dir_path}/tests/test_config.yaml", "r") as f:
        config_content = yaml.safe_load(f)
        dm._session = create_session_from_config(config_content)
    dm._load_session()
    # Only eiger has softwareTrigger set to True in test_config.yaml
    software_triggered_devices = []
    for dev_name, dev_cfg in config_content.items():
        if dev_cfg.get("softwareTrigger", None):
            software_triggered_devices.append(dm.devices.get(dev_name))

    dev_list = dm.devices.get_software_triggered_devices()
    assert software_triggered_devices == dev_list


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
    "readout_priority_in",
    [
        {"monitored": ["samx"], "async": ["samx"]},
        {"monitored": ["samx"], "continuous": ["samx", "samy"]},
    ],
)
def test_readoutpriority_raises_with_conflicting_input(dm_with_devices, readout_priority_in):
    dm = dm_with_devices
    with pytest.raises(ValueError):
        dm.devices.monitored_devices(readout_priority=readout_priority_in)


@pytest.mark.parametrize(
    "readout_priority_in, priority_out",
    [
        ({"monitored": ["samx"], "baseline": ["samx"]}, {"monitored": ["samx"]}),
        (
            {"monitored": ["samx"], "continuous": ["samx", "samy"]},
            {"monitored": ["samx"], "continuous": ["samy"]},
        ),
        (
            {"monitored": ["samx"], "on_request": ["samx", "samy"]},
            {"monitored": ["samx"], "on_request": ["samy"]},
        ),
        (
            {"baseline": ["samx"], "on_request": ["samx", "samy"]},
            {"baseline": ["samx"], "on_request": ["samy"]},
        ),
    ],
)
def test_readoutpriority_highest_priority_wins(dm_with_devices, readout_priority_in, priority_out):
    dm = dm_with_devices
    monitored_devices = dm.devices.monitored_devices(readout_priority=readout_priority_in)
    baseline_devices = dm.devices.baseline_devices(readout_priority=readout_priority_in)
    async_devices = dm.devices.async_devices(readout_priority=readout_priority_in)
    continuous_devices = dm.devices.continuous_devices(readout_priority=readout_priority_in)
    on_request_devices = dm.devices.on_request_devices(readout_priority=readout_priority_in)

    monitored_device_names = set(dev.name for dev in monitored_devices)
    baseline_device_names = set(dev.name for dev in baseline_devices)
    async_device_names = set(dev.name for dev in async_devices)
    continuous_device_names = set(dev.name for dev in continuous_devices)
    on_request_device_names = set(dev.name for dev in on_request_devices)

    assert (
        monitored_device_names.intersection(
            baseline_device_names,
            async_device_names,
            continuous_device_names,
            on_request_device_names,
        )
        == set()
    )
    assert set(priority_out.get("monitored", [])).intersection(monitored_device_names) == set(
        priority_out.get("monitored", [])
    )
    assert set(priority_out.get("baseline", [])).intersection(baseline_device_names) == set(
        priority_out.get("baseline", [])
    )
    assert set(priority_out.get("async", [])).intersection(async_device_names) == set(
        priority_out.get("async", [])
    )
    assert set(priority_out.get("continuous", [])).intersection(continuous_device_names) == set(
        priority_out.get("continuous", [])
    )
    assert set(priority_out.get("on_request", [])).intersection(on_request_device_names) == set(
        priority_out.get("on_request", [])
    )


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
                "continuous": ["bpm6i"],
            },
        ),
        (
            [],
            {
                "monitored": ["samx"],
                "baseline": ["samy"],
                "on_request": ["bpm4i"],
                "async": ["bpm3i"],
                "continuous": ["bpm6i"],
            },
        ),
        (
            [],
            {
                "monitored": ["hexapod.x"],
                "baseline": ["samy"],
                "on_request": ["bpm4i"],
                "async": ["bpm3i"],
                "continuous": ["bpm6i"],
            },
        ),
    ],
)
def test_readout_priority(dm_with_devices, scan_motors_in, readout_priority_in):
    dm = dm_with_devices
    scan_motors = [dm.devices.get(dev) for dev in scan_motors_in]
    monitored_devices = dm.devices.monitored_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    baseline_devices = dm.devices.baseline_devices(
        scan_motors=scan_motors, readout_priority=readout_priority_in
    )
    async_devices = dm.devices.async_devices(readout_priority=readout_priority_in)
    continuous_devices = dm.devices.continuous_devices(readout_priority=readout_priority_in)
    on_request_devices = dm.devices.on_request_devices(readout_priority=readout_priority_in)

    primary_device_names = set(dev.name for dev in monitored_devices)
    baseline_devices_names = set(dev.name for dev in baseline_devices)
    async_devices_names = set(dev.name for dev in async_devices)
    continuous_devices_names = set(dev.name for dev in continuous_devices)
    on_request_devices_names = set(dev.name for dev in on_request_devices)

    primary_device_names.intersection(readout_priority_in.get("monitored", [])) == set(
        readout_priority_in.get("monitored", [])
    )
    baseline_devices_names.intersection(readout_priority_in.get("baseline", [])) == set(
        readout_priority_in.get("baseline", [])
    )
    async_devices_names.intersection(readout_priority_in.get("async", [])) == set(
        readout_priority_in.get("async", [])
    )
    continuous_devices_names.intersection(readout_priority_in.get("continuous", [])) == set(
        readout_priority_in.get("continuous", [])
    )
    on_request_devices_names.intersection(readout_priority_in.get("on_request", [])) == set(
        readout_priority_in.get("on_request", [])
    )

    assert len(primary_device_names & baseline_devices_names) == 0

    assert len(set(readout_priority_in.get("on_request", [])) & baseline_devices_names) == 0
    assert len(set(readout_priority_in.get("on_request", [])) & primary_device_names) == 0
    assert len(set(readout_priority_in.get("async", [])) & primary_device_names) == 0
    assert len(set(readout_priority_in.get("continuous", [])) & primary_device_names) == 0

    assert (
        set(primary_device_names).intersection(
            set(baseline_devices_names),
            set(async_devices_names),
            set(continuous_devices_names),
            set(on_request_devices_names),
        )
    ) == set()

    assert (
        set(baseline_devices_names).intersection(
            set(async_devices_names),
            set(continuous_devices_names),
            set(on_request_devices_names),
            set(primary_device_names),
        )
        == set()
    )

    assert (
        set(async_devices_names).intersection(
            set(continuous_devices_names),
            set(on_request_devices_names),
            set(primary_device_names),
            set(baseline_devices_names),
        )
        == set()
    )


def test_device_config_update_callback(dm_with_devices):
    dm = dm_with_devices
    dev_config_msg = messages.DeviceConfigMessage(action="update", config={"samx": {}})
    msg = MessageObject(value=dev_config_msg, topic="")

    with mock.patch.object(dm, "parse_config_message") as parse_config_message:
        dm._device_config_update_callback(msg, parent=dm)
        parse_config_message.assert_called_once_with(dev_config_msg)


def test_disabled_device_not_in_monitored(dm_with_devices):
    assert "motor1_disabled" in dm_with_devices.devices
    monitored_devices = dm_with_devices.devices.monitored_devices()
    assert "motor1_disabled" not in [dev.name for dev in monitored_devices]
