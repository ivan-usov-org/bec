from __future__ import annotations

import enum
import re
import time
import warnings
from typing import TYPE_CHECKING, List

import msgpack
from rich.console import Console
from rich.table import Table
from typeguard import typechecked

from bec_lib.bec_errors import DeviceConfigError
from bec_lib.config_helper import ConfigHelper
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.messages import (
    BECStatus,
    DeviceConfigMessage,
    DeviceInfoMessage,
    DeviceMessage,
    DeviceStatusMessage,
    LogMessage,
)

if TYPE_CHECKING:
    from bec_lib.connector import ConnectorBase
    from bec_lib.redis_connector import RedisProducer

logger = bec_logger.logger


class DeviceStatus(enum.Enum):
    """Device status"""

    IDLE = 0
    RUNNING = 1
    BUSY = 2


class OnFailure(str, enum.Enum):
    """On failure behaviour for devices"""

    RAISE = "raise"
    BUFFER = "buffer"
    RETRY = "retry"


class ReadoutPriority(str, enum.Enum):
    """Readout priority for devices"""

    ON_REQUEST = "on_request"
    BASELINE = "baseline"
    MONITORED = "monitored"
    ASYNC = "async"
    CONTINUOUS = "continuous"


class DeviceType(str, enum.Enum):
    """Device type"""

    POSITIONER = "positioner"
    DETECTOR = "detector"
    MONITOR = "monitor"
    CONTROLLER = "controller"
    MISC = "misc"


class Status:
    def __init__(self, producer: RedisProducer, RID: str) -> None:
        """
        Status object for RPC calls

        Args:
            producer (RedisProducer): Redis producer
            RID (str): Request ID
        """
        self._producer = producer
        self._RID = RID

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Status):
            return self._RID == __value._RID
        return False

    def wait(self, timeout=None):
        """wait until the request is completed"""
        sleep_time_step = 0.1
        sleep_count = 0

        def _sleep(sleep_time):
            nonlocal sleep_count
            nonlocal timeout
            time.sleep(sleep_time)
            sleep_count += sleep_time
            if timeout is not None and sleep_count > timeout:
                raise TimeoutError()

        while True:
            request_status = self._producer.lrange(
                MessageEndpoints.device_req_status(self._RID), 0, -1
            )
            if request_status:
                break
            _sleep(sleep_time_step)


class Device:
    def __init__(self, name, config, *args, parent=None):
        self.name = name
        self._config = config
        self._signals = []
        self._subdevices = []
        self._status = DeviceStatus.IDLE
        self.parent = parent

    def get_device_config(self):
        """get the device config for this device"""
        return self._config["deviceConfig"]

    @typechecked
    def set_device_config(self, val: dict):
        """set the device config for this device"""
        self._config["deviceConfig"].update(val)
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"deviceConfig": self._config["deviceConfig"]}}
        )

    def get_device_tags(self) -> List:
        """get the device tags for this device"""
        return self._config.get("deviceTags", [])

    @typechecked
    def set_device_tags(self, val: list):
        """set the device tags for this device"""
        self._config["deviceTags"] = val
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"deviceTags": self._config["deviceTags"]}}
        )

    @typechecked
    def add_device_tag(self, val: str):
        """add a device tag for this device"""
        if val in self._config["deviceTags"]:
            return None
        self._config["deviceTags"].append(val)
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"deviceTags": self._config["deviceTags"]}}
        )

    def remove_device_tag(self, val: str):
        """remove a device tag for this device"""
        if val not in self._config["deviceTags"]:
            return None
        self._config["deviceTags"].remove(val)
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"deviceTags": self._config["deviceTags"]}}
        )

    @property
    def wm(self) -> None:
        """get the current position of a device"""
        self.parent.devices.wm(self.name)

    @property
    def device_type(self) -> DeviceType:
        """get the device type for this device"""
        return DeviceType(self._config["deviceType"])

    @device_type.setter
    def device_type(self, val: DeviceType):
        """set the device type for this device"""
        if not isinstance(val, DeviceType):
            val = DeviceType(val)
        self._config["deviceType"] = val
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"deviceType": val}}
        )

    @property
    def readout_priority(self) -> ReadoutPriority:
        """get the readout priority for this device"""
        return ReadoutPriority(self._config["readoutPriority"])

    @readout_priority.setter
    def readout_priority(self, val: ReadoutPriority):
        """set the readout priority for this device"""
        if not isinstance(val, ReadoutPriority):
            val = ReadoutPriority(val)
        self._config["readoutPriority"] = val
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"readoutPriority": val}}
        )

    @property
    def on_failure(self) -> OnFailure:
        """get the failure behaviour for this device"""
        return OnFailure(self._config["onFailure"])

    @on_failure.setter
    def on_failure(self, val: OnFailure):
        """set the failure behaviour for this device"""
        if not isinstance(val, OnFailure):
            val = OnFailure(val)
        self._config["onFailure"] = val
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"onFailure": self._config["onFailure"]}}
        )

    @property
    def enabled(self):
        """Whether or not the device is enabled"""
        return self._config["enabled"]

    @enabled.setter
    def enabled(self, value):
        """Whether or not the device is enabled"""
        self._config["enabled"] = value
        self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"enabled": value}}
        )

    @property
    def read_only(self):
        """Whether or not the device can be set"""
        return self._config.get("readOnly", False)

    @read_only.setter
    def read_only(self, value):
        """Whether or not the device is read only"""
        self._config["readOnly"] = value
        self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"readOnly": value}}
        )

    def read(self, cached, filter_readback=True):
        """get the last reading from a device"""
        val = self.parent.producer.get(MessageEndpoints.device_read(self.name))
        if not val:
            return None
        if filter_readback:
            return DeviceMessage.loads(val).content["signals"].get(self.name)
        return DeviceMessage.loads(val).content["signals"]

    # def readback(self, filter_readback=True):
    #     """get the last readback value from a device"""
    #     val = self.parent.producer.get(MessageEndpoints.device_readback(self.name))
    #     if not val:
    #         return None
    #     if filter_readback:
    #         return DeviceMessage.loads(val).content["signals"].get(self.name)
    #     return DeviceMessage.loads(val).content["signals"]

    @property
    def device_status(self):
        """get the current status of the device"""
        val = self.parent.producer.get(MessageEndpoints.device_status(self.name))
        if val is None:
            return val
        val = DeviceStatusMessage.loads(val)
        return val.content.get("status")

    @property
    def signals(self):
        """get the last signals from a device"""
        val = self.parent.producer.get(MessageEndpoints.device_read(self.name))
        if val is None:
            return None
        self._signals = DeviceMessage.loads(val).content["signals"]
        return self._signals

    @property
    def user_parameter(self) -> dict:
        """get the user parameter for this device"""
        return self._config.get("userParameter")

    @typechecked
    def set_user_parameter(self, val: dict):
        """set the user parameter for this device"""
        self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"userParameter": val}}
        )

    @typechecked
    def update_user_parameter(self, val: dict):
        """update the user parameter for this device
        Args:
            val (dict): New user parameter
        """
        param = self.user_parameter
        if param is None:
            param = {}
        param.update(val)
        self.set_user_parameter(param)

    def __eq__(self, other):
        if isinstance(other, Device):
            return other.name == self.name
        return False

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        return f"{type(self).__name__}(name={self.name}, enabled={self.enabled})"

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name}, enabled={self.enabled})"


class DeviceContainer(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        if attr.startswith("__"):
            # if dunder attributes are would not be caught, they
            # would raise a DeviceConfigError and kill the
            # IPython completer
            return self.get(attr)
        dev = self.get(attr)
        if not dev:
            raise DeviceConfigError(f"Device {attr} does not exist.")
        return dev

    def __setattr__(self, key, value):
        if isinstance(value, Device):
            self.__setitem__(key, value)
        else:
            raise AttributeError("Unsupported device type.")

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]

    def flush(self) -> None:
        """
        Remove all devices from the device manager
        """
        self.clear()
        self.__dict__.clear()

    @property
    def enabled_devices(self) -> list:
        """get a list of enabled devices"""
        return [dev for _, dev in self.items() if dev.enabled]

    @property
    def disabled_devices(self) -> list:
        """get a list of disabled devices"""
        return [dev for _, dev in self.items() if not dev.enabled]

    def readout_priority(self, readout_priority: ReadoutPriority) -> list:
        """get all devices with the specified readout proprity

        Args:
            readout_priority (str): Readout priority (e.g.  on_request, baseline, monitored, async, continuous)

        Returns:
            list: List of devices that belong to the specified acquisition readoutPriority
        """
        val = ReadoutPriority(readout_priority)
        # pylint: disable=protected-access
        return [dev for _, dev in self.items() if dev._config["readoutPriority"] == val]

    def get_device_type_devices(self, device_type: DeviceType) -> list:
        """get all devices with the specified device type

        Args:
            device_type (str): device type (e.g. POSITIONER, DETECTOR, MONITOR, CONTROLLER, MISC)

        Returns:
            list: List of devices that belong to the specified acquisition readoutPriority
        """
        val = DeviceType(device_type)
        # pylint: disable=protected-access
        return [dev for _, dev in self.items() if dev._config["deviceType"] == val]

    def async_devices(self) -> list:
        """get a list of all synchronous devices"""
        # pylint: disable=protected-access
        return self.readout_priority(ReadoutPriority.ASYNC)

    @typechecked
    def monitored_devices(self, scan_motors: list = None, readout_priority: dict = None) -> list:
        """get a list of all enabled primary devices"""
        devices = self.readout_priority(ReadoutPriority.MONITORED)
        if scan_motors:
            if not isinstance(scan_motors, list):
                scan_motors = [scan_motors]
            for scan_motor in scan_motors:
                if not scan_motor in devices:
                    if isinstance(scan_motor, Device):
                        devices.append(scan_motor)
                    else:
                        devices.append(self.get(scan_motor))
        if not readout_priority:
            readout_priority = {}

        devices.extend([self.get(dev) for dev in readout_priority.get("monitored", [])])

        excluded_devices = self.async_devices()
        excluded_devices.extend(self.disabled_devices)
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("baseline", [])])
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("on_request", [])])
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("continuous", [])])
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("async", [])])

        return [dev for dev in set(devices) if dev not in excluded_devices]

    @typechecked
    def baseline_devices(self, scan_motors: list = None, readout_priority: dict = None) -> list:
        """
        Get a list of all enabled baseline devices
        Args:
            scan_motors(list): list of scan motors
            readout_priority(dict): readout priority

        Returns:
            list: list of baseline devices
        """
        devices = self.readout_priority(ReadoutPriority.BASELINE)
        if scan_motors:
            if not isinstance(scan_motors, list):
                scan_motors = [scan_motors]
            for scan_motor in scan_motors:
                if not scan_motor in devices:
                    if isinstance(scan_motor, Device):
                        devices.append(scan_motor)
                    else:
                        devices.append(self.get(scan_motor))
            excluded_devices = scan_motors
        else:
            excluded_devices = []
        if not readout_priority:
            readout_priority = {}

        devices.extend([self.get(dev) for dev in readout_priority.get("baseline", [])])
        excluded_devices.extend(self.disabled_devices)
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("monitored", [])])
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("on_request", [])])
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("continuous", [])])
        excluded_devices.extend([self.get(dev) for dev in readout_priority.get("async", [])])

        return [dev for dev in set(devices) if dev not in excluded_devices]

    def get_devices_with_tags(self, tags: List) -> List:
        """
        Get a list of all devices with the specified tags
        Args:
            tags (List): List of tags

        Returns:
            List: List of devices with the specified tags
        """
        # pylint: disable=protected-access
        if not isinstance(tags, list):
            tags = [tags]
        return [
            dev for _, dev in self.items() if set(tags) & set(dev._config.get("deviceTags", []))
        ]

    def show_tags(self) -> List:
        """returns a list of used tags in the current config"""
        tags = set()
        for _, dev in self.items():
            # pylint: disable=protected-access
            dev_tags = dev._config.get("deviceTags")
            if dev_tags:
                tags.update(dev_tags)
        return list(tags)

    @typechecked
    def detectors(self) -> list:
        """get a list of all enabled detectors"""
        return self.get_device_type_devices(DeviceType.DETECTOR)

    def wm(self, device_names: List[str]):
        """Get the current position of one or more devices.

        Args:
            device_names (List[str]): List of device names

        Examples:
            >>> dev.wm('samx')
            >>> dev.wm(['samx', 'samy'])
            >>> dev.wm(dev.monitored_devices())
            >>> dev.wm(dev.get_devices_with_tags('user motors'))

        """
        if not isinstance(device_names, list):
            device_names = [device_names]
        if len(device_names) == 0:
            return
        if not isinstance(device_names[0], Device):
            device_names = [self.__dict__[dev] for dev in device_names]
        console = Console()
        table = Table()
        table.add_column("", justify="center")
        table.add_column("readback", justify="center")
        table.add_column("setpoint", justify="center")
        table.add_column("limits", justify="center")
        dev_read = {dev.name: dev.read(cached=True) for dev in device_names}
        readbacks = {}
        setpoints = {}
        limits = {}
        for dev in device_names:
            # pylint: disable=protected-access
            if "limits" in dev._config.get("deviceConfig", {}):
                limits[dev.name] = str(dev._config["deviceConfig"]["limits"])
            else:
                limits[dev.name] = "[]"

        for dev, read in dev_read.items():
            if dev in read:
                val = read[dev]["value"]
                if not isinstance(val, str):
                    readbacks[dev] = f"{val:.4f}"
                else:
                    readbacks[dev] = val
            else:
                readbacks[dev] = "N/A"
            if f"{dev}_setpoint" in read:
                val = read[f"{dev}_setpoint"]["value"]
                if not isinstance(val, str):
                    setpoints[dev] = f"{val:.4f}"
                else:
                    setpoints[dev] = val
            elif f"{dev}_user_setpoint" in read:
                val = read[f"{dev}_user_setpoint"]["value"]
                if not isinstance(val, str):
                    setpoints[dev] = f"{val:.4f}"
                else:
                    setpoints[dev] = val
            else:
                setpoints[dev] = "N/A"
        for dev in device_names:
            table.add_row(dev.name, readbacks[dev.name], setpoints[dev.name], limits[dev.name])
        console.print(table)

    def _add_device(self, name, obj) -> None:
        """
        Add device a new device to the device manager
        Args:
            name: name of the device
            obj: instance of the device

        Returns:

        """
        self[name] = obj

    def describe(self) -> list:
        """
        Describe all devices associated with the DeviceManager
        Returns:

        """
        return [dev.describe() for name, dev in self.devices.items()]

    def show_all(self, console: Console = None) -> None:
        """print all devices"""

        if console is None:
            console = Console()
        table = Table()
        table.add_column("Device", justify="center")
        table.add_column("Description", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("ReadOnly", justify="center")
        table.add_column("Device class", justify="center")
        table.add_column("Readout priority", justify="center")
        table.add_column("Device tags", justify="center")

        # pylint: disable=protected-access
        for dev in self.values():
            table.add_row(
                dev.name,
                dev._config.get("description", dev.name),
                "enabled" if dev.enabled else "disabled",
                str(dev.read_only),
                dev._config.get("deviceClass"),
                dev._config.get("readoutPriority"),
                str(dev._config.get("deviceTags", [])),
            )
        console.print(table)

    def __repr__(self) -> str:
        return "Device container."


class DeviceManagerBase:
    devices = DeviceContainer()
    _config = {}  # valid config
    _session = {}
    _request = None  # requested config
    _request_config_parsed = None  # parsed config request
    _response = None  # response message

    _connector_base_consumer = {}
    producer = None
    config_helper = None
    _device_cls = Device
    _status_cb = []

    def __init__(self, connector: ConnectorBase, status_cb: list = None) -> None:
        self.connector = connector
        self.config_helper = ConfigHelper(self.connector)
        self._status_cb = status_cb if isinstance(status_cb, list) else [status_cb]

    def initialize(self, bootstrap_server) -> None:
        """
        Initialize the DeviceManager by starting all connectors.
        Args:
            bootstrap_server: Redis server address, e.g. 'localhost:6379'

        Returns:

        """
        self._start_connectors(bootstrap_server)
        self._get_config()

    def update_status(self, status: BECStatus):
        """Update the status of the device manager
        Args:
            status (BECStatus): New status
        """
        for cb in self._status_cb:
            if cb:
                cb(status)

    def parse_config_message(self, msg: DeviceConfigMessage) -> None:
        """
        Parse a config message and update the device config accordingly.

        Args:
            msg (DeviceConfigMessage): Config message

        """
        # pylint: disable=protected-access
        action = msg.content["action"]
        config = msg.content["config"]
        if action == "update":
            for dev in config:
                if "deviceConfig" in config[dev]:
                    logger.info(f"Updating device config for device {dev}.")
                    self.devices[dev]._config["deviceConfig"].update(config[dev]["deviceConfig"])
                    logger.debug(
                        f"New config for device {dev}: {self.devices[dev]._config['deviceConfig']}"
                    )
                if "enabled" in config[dev]:
                    self.devices[dev]._config["enabled"] = config[dev]["enabled"]
                    status = "enabled" if self.devices[dev].enabled else "disabled"
                    logger.info(f"Device {dev} has been {status}.")
                if "read_only" in config[dev]:
                    self.devices[dev]._config["read_only"] = config[dev]["read_only"]
                if "userParameter" in config[dev]:
                    self.devices[dev]._config["userParameter"] = config[dev]["userParameter"]
                if "onFailure" in config[dev]:
                    self.devices[dev]._config["onFailure"] = config[dev]["onFailure"]
                if "deviceTags" in config[dev]:
                    self.devices[dev]._config["deviceTags"] = config[dev]["deviceTags"]
                if "readoutPriority" in config[dev]:
                    self.devices[dev]._config["readoutPriority"] = config[dev]["readoutPriority"]
                if "deviceType" in config[dev]:
                    self.devices[dev]._config["deviceType"] = config[dev]["deviceType"]

        elif action == "add":
            self.update_status(BECStatus.BUSY)
            self._add_action(config)
            self.update_status(BECStatus.RUNNING)
        elif action == "reload":
            self.update_status(BECStatus.BUSY)
            logger.info("Reloading config.")
            self._reload_action()
            self.update_status(BECStatus.RUNNING)
        elif action == "remove":
            self.update_status(BECStatus.BUSY)
            self._remove_action(config)
            self.update_status(BECStatus.RUNNING)

    def _add_action(self, config) -> None:
        for dev in config:
            obj = self._create_device(dev)
            # pylint: disable=protected-access
            self.devices._add_device(dev.get("name"), obj)

    def _reload_action(self) -> None:
        self.devices.flush()
        self._get_config()

    def _remove_action(self, config) -> None:
        for dev in config:
            self._remove_device(dev)

    def _start_connectors(self, bootstrap_server) -> None:
        self._start_base_consumer()
        self.producer = self.connector.producer()
        self._start_custom_connectors(bootstrap_server)

    def _start_base_consumer(self) -> None:
        """
        Start consuming messages for all base topics. This method will be called upon startup.
        Returns:

        """
        self._connector_base_consumer["device_config_update"] = self.connector.consumer(
            MessageEndpoints.device_config_update(),
            cb=self._device_config_update_callback,
            parent=self,
        )

        # self._connector_base_consumer["log"].start()
        self._connector_base_consumer["device_config_update"].start()

    @staticmethod
    def _log_callback(msg, *, parent, **kwargs) -> None:
        """
        Consumer callback for handling log messages.
        Args:
            cls: Reference to the DeviceManager instance
            msg: log message of type LogMessage
            **kwargs: Additional keyword arguments for the callback function

        Returns:

        """
        msg = LogMessage.loads(msg.value)
        logger.info(f"Received log message: {str(msg)}")

    @staticmethod
    def _device_config_update_callback(msg, *, parent, **kwargs) -> None:
        """
        Consumer callback for handling new device configuration
        Args:
            cls: Reference to the DeviceManager instance
            msg: message of type DeviceConfigMessage

        Returns:

        """
        msg = DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received new config: {str(msg)}")
        parent.parse_config_message(msg)

    def _get_config(self):
        self._session["devices"] = self._get_redis_device_config()
        if not self._session["devices"]:
            logger.warning("No config available.")
        self._load_session()

    def _set_redis_device_config(self, devices: list) -> None:
        self.producer.set(MessageEndpoints.device_config(), msgpack.dumps(devices))

    def _get_redis_device_config(self) -> list:
        devices = self.producer.get(MessageEndpoints.device_config())
        if not devices:
            return []
        return msgpack.loads(devices)

    def _stop_base_consumer(self):
        """
        Stop all base consumers by setting the corresponding event
        Returns:

        """
        if self.connector is not None:
            for _, con in self._connector_base_consumer.items():
                con.signal_event.set()
                con.join()

    def _stop_consumer(self):
        """
        Stop all consumers
        Returns:

        """
        self._stop_base_consumer()
        self._stop_custom_consumer()

    def _start_custom_connectors(self, bootstrap_server) -> None:
        """
        Override this method in a derived class to start custom connectors upon initialization.
        Args:
            bootstrap_server: Kafka bootstrap server

        Returns:

        """

    def _stop_custom_consumer(self) -> None:
        """
        Stop all custom consumers. Override this method in a derived class.
        Returns:

        """

    def _create_device(self, dev: dict, *args) -> Device:
        obj = self._device_cls(dev.get("name"), *args, parent=self)
        # pylint: disable=protected-access
        obj._config = dev
        return obj

    def _remove_device(self, dev_name):
        if dev_name in self.devices:
            self.devices.pop(dev_name)

    def _load_session(self, *args, device_cls=Device):
        self._device_cls = device_cls
        if not self._is_config_valid():
            return
        for dev in self._session["devices"]:
            obj = self._create_device(dev, args)
            # pylint: disable=protected-access
            self.devices._add_device(dev.get("name"), obj)

    def _get_device_info(self, device_name) -> DeviceInfoMessage:
        msg = DeviceInfoMessage.loads(self.producer.get(MessageEndpoints.device_info(device_name)))
        return msg

    def check_request_validity(self, msg: DeviceConfigMessage) -> None:
        """
        Check if the config request is valid.

        Args:
            msg (DeviceConfigMessage): Config message

        """
        if msg.content["action"] not in ["update", "add", "remove", "reload", "set"]:
            raise DeviceConfigError("Action must be either add, remove, update, set or reload.")
        if msg.content["action"] in ["update", "add", "remove", "set"]:
            if not msg.content["config"]:
                raise DeviceConfigError(
                    "Config cannot be empty for an action of type add, remove, set or update."
                )
            if not isinstance(msg.content["config"], dict):
                raise DeviceConfigError("Config must be of type dict.")
        if msg.content["action"] in ["update", "remove"]:
            for dev in msg.content["config"].keys():
                if dev not in self.devices:
                    raise DeviceConfigError(
                        f"Device {dev} does not exist and cannot be updated / removed."
                    )
        if msg.content["action"] == "add":
            for dev in msg.content["config"].keys():
                if dev in self.devices:
                    raise DeviceConfigError(f"Device {dev} already exists and cannot be added.")

    def _is_config_valid(self) -> bool:
        if self._config is None:
            return False
        if not isinstance(self._config, dict):
            return False
        return True

    def shutdown(self):
        """
        Shutdown all connectors.
        """
        try:
            self.connector.shutdown()
        except RuntimeError as runtime_error:
            logger.error(f"Failed to shutdown connector. {runtime_error}")

    def __del__(self):
        self.shutdown()
