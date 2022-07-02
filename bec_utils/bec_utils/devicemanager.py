import enum
import json
import logging

import msgpack
import yaml
from typeguard import typechecked

from bec_utils.connector import ConnectorBase

from .BECMessage import DeviceConfigMessage, DeviceStatusMessage, LogMessage
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


class Device:
    def __init__(self, name, config, *args, parent=None):
        self.name = name
        self.config = config
        self._signals = []
        self._subdevices = []
        self._status = DeviceStatus.IDLE
        self.DIID = None
        self.scanID = None
        self.parent = parent

    @property
    def enabled(self):
        return self.config["enabled"]

    @enabled.setter
    def enabled(self, value):
        self.config["enabled"] = value

    def read(self):
        val = self.parent.producer.get(MessageEndpoints.device_read(self.name))
        if val:
            return msgpack.loads(val)["content"]["signals"].get(self.name)
        else:
            return None

    def readback(self):
        val = self.parent.producer.get(MessageEndpoints.device_readback(self.name))
        if val:
            return msgpack.loads(val)["content"]["signals"].get(self.name)
        else:
            return None

    @property
    def status(self):
        val = self.parent.producer.get(MessageEndpoints.device_status(self.name))
        if val is None:
            return val
        val = msgpack.loads(val)
        return val.get("status")

    @property
    def signals(self):
        if not self._signals:
            val = self.parent.producer.get(MessageEndpoints.device_read(self.name))
            if val is None:
                return None
            self._signals = msgpack.loads(val)["content"]["signals"]
        return self._signals

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
        return [dev for _, dev in self.items() if dev.enabled]

    @property
    def disabled_devices(self) -> list:
        """

        Returns: list of disabled devices

        """
        return [dev for _, dev in self.items() if not dev.enabled]

    def device_group(self, device_group) -> list:
        return [dev for _, dev in self.items() if dev.config["deviceGroup"] == device_group]

    @typechecked
    def primary_devices(self, scan_motors: list) -> list:
        devices = self.device_group("monitor")
        devices.extend(scan_motors)
        return [dev for dev in self.enabled_devices if dev in devices]

    @typechecked
    def baseline_devices(self, scan_motors: list) -> list:
        excluded_devices = self.device_group("monitor")
        excluded_devices.extend(scan_motors)
        return [dev for dev in self.enabled_devices if dev not in excluded_devices]

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

    def __init__(self, connector: ConnectorBase, scibec_url: str = None) -> None:
        self.connector = connector
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

    def load_config_from_disk(self, config_path) -> dict:
        """
        load config from disk and send request
        Args:
            config_path: path to config file

        Returns:

        """
        data = {}
        if config_path.endswith(".yaml"):
            with open(config_path, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                    logger.info(
                        f"Loaded new config from disk: {json.dumps(data, sort_keys=True, indent=4)}"
                    )
                except yaml.YAMLError as er:
                    logger.error(f"Error while loading config from disk: {repr(er)}")
        elif config_path.endswith(".json"):
            with open(config_path) as stream:
                try:
                    data = json.load(stream)
                    logger.info(
                        f"Loaded new config from disk: {json.dumps(data, sort_keys=True, indent=4)}"
                    )
                except json.JSONDecodeError as er:
                    logger.error(f"Error while loading config from disk: {repr(er)}")
        else:
            raise NotImplementedError

        return data

    def send_config_request(self, action: str = "update", config=None) -> None:
        """
        send request to update config
        Returns:

        """
        if action in ["update", "add"] and not config:
            raise DeviceConfigError(f"Config cannot be empty for an {action} request.")

        self.producer.send(
            MessageEndpoints.device_config_request(),
            DeviceConfigMessage(action="update", config=config).dumps(),
        )

    def parse_config_message(self, msg: DeviceConfigMessage):
        action = msg.content["action"]
        config = msg.content["config"]
        if action == "update":
            for dev in config:
                if "deviceConfig" in config[dev]:
                    logger.info(f"Updating device config for device {dev}.")
                    self.devices[dev].config["deviceConfig"].update(config[dev]["deviceConfig"])
                    logger.debug(
                        f"New config for device {dev}: {self.devices[dev].config['deviceConfig']}"
                    )
                if "enabled" in config[dev]:
                    self.devices[dev].config["enabled"] = config[dev]["enabled"]
                    status = "enabled" if self.devices[dev].enabled else "disabled"
                    logger.info(f"Device {dev} has been {status}.")
        elif action == "add":
            for dev in config:
                obj = self._create_device(dev)
                self.devices._add_device(dev.get("name"), obj)
        elif action == "reload":
            self.devices.flush()
            self._load_session()
        elif action == "remove":
            for dev in config:
                self._remove_device(dev)

    def update_device_status(self, msg):
        msg = DeviceStatusMessage.loads(msg.value)
        device = self.devices.get(msg.content["device"])
        if device:
            device.status = DeviceStatus(msg.content["status"])
            if device.DIID is not None:
                if device.DIID > msg.metadata["DIID"]:
                    if device.scanID != msg.metadata["scanID"]:
                        device.DIID = msg.metadata["DIID"]
                elif device.DIID < msg.metadata["DIID"]:
                    device.DIID = msg.metadata["DIID"]
            else:
                device.DIID = msg.metadata["DIID"]
            device.scanID = msg.metadata["scanID"]

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

    @staticmethod
    def _device_status_callback(msg, *, parent, **kwargs) -> None:
        """
        Consumer callback for handling device status updates
        Args:
            cls: Reference to the DeviceManager instance
            msg: message of type DeviceConfigMessage

        Returns:

        """
        parent.update_device_status(msg)

    def _get_config_from_DB(self):
        self._session = self._scibec.get_current_session()[0]
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
            for key, con in self._connector_base_consumer.items():
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
        obj.config = dev
        return obj

    def _remove_device(self, dev_name):
        if dev_name in self.devices:
            self.devices.pop(dev_name)

    def _load_session(self, device_cls=Device, *args):
        self._device_cls = device_cls
        if self._is_config_valid():
            for dev in self._session["devices"]:
                obj = self._create_device(dev, args)
                self.devices._add_device(dev.get("name"), obj)

    def _check_request_validity(self, msg: DeviceConfigMessage) -> None:
        if msg.content["action"] not in ["update", "add", "remove", "reload"]:
            raise DeviceConfigError("Action must be either add, remove, update, or reload.")
        if msg.content["action"] in ["update", "add", "remove"] and not msg.content["config"]:
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
        elif not isinstance(self._config, dict):
            return False
        else:
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
