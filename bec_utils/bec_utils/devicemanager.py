import enum
import json
import time
import uuid
from typing import List

import msgpack
from rich.console import Console
from rich.table import Table
from typeguard import typechecked

from bec_utils.connector import ConnectorBase

from .BECMessage import BECStatus, DeviceConfigMessage, LogMessage, RequestResponseMessage
from .endpoints import MessageEndpoints
from .logger import bec_logger
from .scibec import SciBec

logger = bec_logger.logger


class DeviceConfigError(Exception):
    pass


class DeviceStatus(enum.Enum):
    IDLE = 0
    RUNNING = 1
    BUSY = 2


class OnFailure(str, enum.Enum):
    RAISE = "raise"
    BUFFER = "buffer"
    RETRY = "retry"


class ReadoutPriority(str, enum.Enum):
    MONITORED = "monitored"
    BASELINE = "baseline"
    IGNORED = "ignored"


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
        return self.parent.send_config_request(
            action="update", config={self.name: {"deviceConfig": self._config["deviceConfig"]}}
        )

    def get_device_tags(self) -> List:
        """get the device tags for this device"""
        return self._config["deviceTags"]

    @typechecked
    def set_device_tags(self, val: list):
        """set the device tags for this device"""
        self._config["deviceTags"] = val
        return self.parent.send_config_request(
            action="update", config={self.name: {"deviceTags": self._config["deviceTags"]}}
        )

    @typechecked
    def add_device_tag(self, val: str):
        """add a device tag for this device"""
        if val in self._config["deviceTags"]:
            return None
        self._config["deviceTags"].append(val)
        return self.parent.send_config_request(
            action="update", config={self.name: {"deviceTags": self._config["deviceTags"]}}
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
        return self.parent.send_config_request(
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
        self.parent.send_config_request(action="update", config={self.name: {"enabled": value}})

    @property
    def enabled_set(self):
        """Whether or not the device can be set"""
        return self._config.get("enabled_set", True)

    @enabled_set.setter
    def enabled_set(self, value):
        """Whether or not the device can be set"""
        self._config["enabled_set"] = value
        self.parent.send_config_request(action="update", config={self.name: {"enabled_set": value}})

    def read(self, cached):
        """get the last reading from a device"""
        val = self.parent.producer.get(MessageEndpoints.device_read(self.name))
        if val:
            return msgpack.loads(val)["content"]["signals"].get(self.name)
        return None

    def readback(self):
        """get the last readback value from a device"""
        val = self.parent.producer.get(MessageEndpoints.device_readback(self.name))
        if val:
            return msgpack.loads(val)["content"]["signals"].get(self.name)
        return None

    @property
    def status(self):
        """get the current status of the device"""
        val = self.parent.producer.get(MessageEndpoints.device_status(self.name))
        if val is None:
            return val
        val = msgpack.loads(val)
        return val.get("status")

    @property
    def signals(self):
        """get the last signals from a device"""
        if not self._signals:
            val = self.parent.producer.get(MessageEndpoints.device_read(self.name))
            if val is None:
                return None
            self._signals = msgpack.loads(val)["content"]["signals"]
        return self._signals

    @property
    def user_parameter(self) -> dict:
        """get the user parameter for this device"""
        return self._config.get("userParameter")

    @typechecked
    def set_user_parameter(self, val: dict):
        self.parent.send_config_request(action="update", config={self.name: {"userParameter": val}})

    @typechecked
    def update_user_parameter(self, val: dict):
        param = self.user_parameter
        param.update(val)
        self.set_user_parameter(param)

    def __repr__(self):
        if isinstance(self.parent, DeviceManagerBase):
            config = "".join(
                [f"\t{key}: {val}\n" for key, val in self._config.get("deviceConfig").items()]
            )
            separator = "--" * 10
            return (
                f"{type(self).__name__}(name={self.name}, enabled={self.enabled}):\n"
                f"{separator}\n"
                "Details:\n"
                f"\tStatus: {'enabled' if self.enabled else 'disabled'}\n"
                f"\tLast recorded value: {self.read(cached=True)}\n"
                f"\tDevice class: {self._config.get('deviceClass')}\n"
                f"\tAcquisition group: {self._config['acquisitionConfig'].get('acquisitionGroup')}\n"
                f"\tAcquisition readoutPriority: {self._config['acquisitionConfig'].get('readoutPriority')}\n"
                f"\tDevice tags: {self._config.get('deviceTags', [])}\n"
                f"\tUser parameter: {self._config.get('userParameter')}\n"
                f"{separator}\n"
                "Config:\n"
                f"{config}"
            )
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
        return self.get(attr)

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
        self.clear()

    @property
    def enabled_devices(self) -> list:
        """get a list of enabled devices"""
        return [dev for _, dev in self.items() if dev.enabled]

    @property
    def disabled_devices(self) -> list:
        """get a list of disabled devices"""
        return [dev for _, dev in self.items() if not dev.enabled]

    def acquisition_group(self, acquisition_group: str) -> list:
        """get all devices that belong to the specified acquisition group

        Args:
            acquisition_group (str): Acquisition group (e.g. monitor, detector, motor, status)

        Returns:
            list: List of devices that belong to the specified device group
        """
        return [
            dev
            for _, dev in self.items()
            if dev._config["acquisitionConfig"]["acquisitionGroup"] == acquisition_group
        ]

    def readout_priority(self, readout_priority: ReadoutPriority) -> list:
        """get all devices with the specified readout proprity

        Args:
            readout_priority (str): Readout priority (e.g. monitored, baseline, ignored)

        Returns:
            list: List of devices that belong to the specified acquisition readoutPriority
        """
        val = ReadoutPriority(readout_priority)
        return [
            dev
            for _, dev in self.items()
            if dev._config["acquisitionConfig"]["readoutPriority"] == str(readout_priority)
        ]

    def async_devices(self) -> list:
        """get a list of all synchronous devices"""
        return [
            dev for _, dev in self.items() if dev._config["acquisitionConfig"]["schedule"] != "sync"
        ]

    @typechecked
    def primary_devices(self, scan_motors: list = None) -> list:
        """get a list of all enabled primary devices"""
        devices = self.readout_priority("monitored")
        if scan_motors:
            devices.extend(scan_motors)

        return [
            dev
            for dev in self.enabled_devices
            if dev in devices and dev not in self.acquisition_group("detector")
        ]

    @typechecked
    def baseline_devices(self, scan_motors: list) -> list:
        """get a list of all enabled baseline devices"""
        excluded_devices = self.primary_devices(scan_motors)
        excluded_devices.extend(self.async_devices())
        excluded_devices.extend(self.detectors())
        excluded_devices.extend(self.readout_priority("ignored"))
        return [dev for dev in self.enabled_devices if dev not in excluded_devices]

    def get_devices_with_tags(self, tags: List) -> List:
        """get a list of all devices that have the specified tags"""
        if not isinstance(tags, list):
            tags = [tags]
        return [dev for _, dev in self.items() if set(tags) & set(dev._config["deviceTags"])]

    def show_tags(self) -> List:
        """returns a list of used tags in the current config"""
        tags = set()
        for _, dev in self.items():
            tags.update(dev._config["deviceTags"])
        return list(tags)

    @typechecked
    def detectors(self) -> list:
        """get a list of all enabled detectors"""
        return [dev for dev in self.enabled_devices if dev in self.acquisition_group("detector")]

    def wm(self, device_names: List[str]):
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
        dev_read = {dev.name: dev.read(cached=True, filter_signal=False) for dev in device_names}
        readbacks = {}
        setpoints = {}
        for dev, read in dev_read.items():
            if dev in read:
                readbacks[dev] = f"{read[dev]['value']:.4f}"
            else:
                readbacks[dev] = "N/A"
            if f"{dev}_setpoint" in read:
                setpoints[dev] = f"{read[dev]['value']:.4f}"
            else:
                setpoints[dev] = "N/A"
        for dev in device_names:
            table.add_row(dev.name, readbacks[dev.name], setpoints[dev.name])
        console.print(table)

    def _add_device(self, name, obj) -> None:
        """
        Add device a new device to the device manager
        Args:
            name: name of the device
            obj: instance of the device

        Returns:

        """
        self.__setattr__(name, obj)

    def describe(self) -> list:
        """
        Describe all devices associated with the DeviceManager
        Returns:

        """
        return [dev.describe() for name, dev in self.devices.items()]


class DeviceManagerBase:
    devices = DeviceContainer()
    _config = {}  # valid config
    _session = {}
    _request = None  # requested config
    _request_config_parsed = None  # parsed config request
    _response = None  # response message

    _connector_base_consumer = {}
    producer = None
    _scibec = SciBec()
    _device_cls = Device
    _status_cb = []

    def __init__(
        self, connector: ConnectorBase, scibec_url: str = None, status_cb: list = None
    ) -> None:
        self.connector = connector
        self._status_cb = status_cb if isinstance(status_cb, list) else [status_cb]
        if scibec_url is not None:
            self._scibec.url = scibec_url

    def initialize(self, bootstrap_server) -> None:
        """
        Initialize the DeviceManager by starting all connectors.
        Args:
            bootstrap_server: Kafka's bootstrap server

        Returns:

        """
        self._start_connectors(bootstrap_server)
        self._get_config_from_DB()

    def update_status(self, status: BECStatus):
        for cb in self._status_cb:
            cb(status)

    @property
    def scibec(self):
        """SciBec instance"""
        return self._scibec

    def send_config_request(self, action: str = "update", config=None) -> None:
        """
        send request to update config
        Returns:

        """
        if action in ["update", "add"] and not config:
            raise DeviceConfigError(f"Config cannot be empty for an {action} request.")
        RID = str(uuid.uuid4())
        self.producer.send(
            MessageEndpoints.device_config_request(),
            DeviceConfigMessage(action=action, config=config, metadata={"RID": RID}).dumps(),
        )

        reply = self.wait_for_config_reply(RID)

        if not reply.content["accepted"]:
            raise DeviceConfigError(f"Failed to update the config: {reply.content['message']}.")

    def wait_for_config_reply(self, RID: str) -> RequestResponseMessage:
        start = 0
        timeout = 10
        while True:
            msg = self.producer.get(MessageEndpoints.device_config_request_response(RID))
            if msg is None:
                time.sleep(0.1)
                start += 0.1

                if start > timeout:
                    raise DeviceConfigError("Timeout reached whilst waiting for config reply.")
                continue
            return RequestResponseMessage.loads(msg)

    def parse_config_message(self, msg: DeviceConfigMessage):
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
                if "enabled_set" in config[dev]:
                    self.devices[dev]._config["enabled_set"] = config[dev]["enabled_set"]
                if "userParameter" in config[dev]:
                    self.devices[dev]._config["userParameter"] = config[dev]["userParameter"]

        elif action == "add":
            for dev in config:
                obj = self._create_device(dev)
                self.devices._add_device(dev.get("name"), obj)
        elif action == "reload":
            logger.info("Reloading config.")
            self.devices.flush()
            self._get_config_from_DB()
        elif action == "remove":
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
        # self._connector_base_consumer["log"] = self.connector.consumer(
        #     MessageEndpoints.log(), cb=self._log_callback, parent=self
        # )
        self._connector_base_consumer["device_config"] = self.connector.consumer(
            MessageEndpoints.device_config(),
            cb=self._device_config_callback,
            parent=self,
        )

        # self._connector_base_consumer["log"].start()
        self._connector_base_consumer["device_config"].start()

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
    def _device_config_callback(msg, *, parent, **kwargs) -> None:
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

    def _get_config_from_DB(self):
        beamlines = self._scibec.get_beamlines()
        if not beamlines:
            logger.warning("No config available.")
            return
        if len(beamlines) > 1:
            logger.warning("More than one beamline available.")
        beamline = beamlines[0]

        session = self._scibec.get_current_session(beamline["name"], include_devices=True)
        if not session:
            logger.warning(f"No config available for beamline {beamline['name']}.")
            return
        if not session.get("devices"):
            logger.warning(f"The currently active config has no devices specified.")
            return
        self._session = session
        logger.debug(
            f"Loaded session from DB: {json.dumps(self._session, sort_keys=True, indent=4)}"
        )
        self._load_session()

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
        pass

    def _stop_custom_consumer(self) -> None:
        """
        Stop all custom consumers. Override this method in a derived class.
        Returns:

        """
        pass

    def _create_device(self, dev: dict, *args) -> Device:
        obj = self._device_cls(dev.get("name"), *args, parent=self)
        obj._config = dev
        return obj

    def _remove_device(self, dev_name):
        if dev_name in self.devices:
            self.devices.pop(dev_name)

    def _load_session(self, *args, device_cls=Device):
        self._device_cls = device_cls
        if self._is_config_valid():
            for dev in self._session["devices"]:
                obj = self._create_device(dev, args)
                # pylint: disable=protected-access
                self.devices._add_device(dev.get("name"), obj)

    def check_request_validity(self, msg: DeviceConfigMessage) -> None:
        if msg.content["action"] not in ["update", "add", "remove", "reload"]:
            raise DeviceConfigError("Action must be either add, remove, update, or reload.")
        if msg.content["action"] in ["update", "add", "remove"]:
            if not msg.content["config"]:
                raise DeviceConfigError(
                    "Config cannot be empty for an action of type add, remove or update."
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
        Returns:

        """
        try:
            self.connector.shutdown()
        except RuntimeError as runtime_error:
            logger.error(f"Failed to shutdown connector. {runtime_error}")

    def __del__(self):
        self.shutdown()
