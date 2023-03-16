import enum
import functools
import time
import uuid
from typing import List

import msgpack
from rich.console import Console
from rich.table import Table
from typeguard import typechecked

from bec_utils import ConfigHelper
from bec_utils.connector import ConnectorBase

from .bec_errors import DeviceConfigError, RPCError, ScanRequestError
from .BECMessage import (
    BECStatus,
    DeviceConfigMessage,
    DeviceInfoMessage,
    DeviceMessage,
    DeviceRPCMessage,
    LogMessage,
    ScanQueueMessage,
)
from .endpoints import MessageEndpoints
from .logger import bec_logger

logger = bec_logger.logger


def rgetattr(obj, attr, *args):
    """See https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects"""

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


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

    def _get_full_obj_name(self) -> str:
        """Return the full object name"""
        names = []
        obj = self
        while not isinstance(obj.parent, DeviceManagerBase):
            names.append(obj.name)
            obj = obj.parent
        dotted_name = ".".join(names[::-1])
        if not dotted_name:
            return obj.root.name
        return f"{obj.root.name}.{dotted_name}"

    @typechecked
    def set_device_config(self, val: dict):
        """set the device config for this device"""
        self._config["deviceConfig"].update(val)
        return self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"deviceConfig": self._config["deviceConfig"]}}
        )

    def get_device_tags(self) -> List:
        """get the device tags for this device"""
        return self._config["deviceTags"]

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

    @property
    def readout_priority(self) -> ReadoutPriority:
        """get the readout priority for this device"""
        return ReadoutPriority(self._config["acquisitionConfig"]["readoutPriority"])

    @readout_priority.setter
    def readout_priority(self, val: ReadoutPriority):
        """set the readout priority for this device"""
        if not isinstance(val, ReadoutPriority):
            val = ReadoutPriority(val)
        self._config["acquisitionConfig"]["readoutPriority"] = val
        return self.parent.config_helper.send_config_request(
            action="update",
            config={self.name: {"acquisitionConfig": self._config["acquisitionConfig"]}},
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
    def enabled_set(self):
        """Whether or not the device can be set"""
        return self._config.get("enabled_set", True)

    @enabled_set.setter
    def enabled_set(self, value):
        """Whether or not the device can be set"""
        self._config["enabled_set"] = value
        self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"enabled_set": value}}
        )

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
    def device_status(self):
        """get the current status of the device"""
        val = self.parent.producer.get(MessageEndpoints.device_status(self.name))
        if val is None:
            return val
        val = msgpack.loads(val)
        return val.get("status")

    @property
    def signals(self):
        """get the last signals from a device"""
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
        self.parent.config_helper.send_config_request(
            action="update", config={self.name: {"userParameter": val}}
        )

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

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        if "." in key:
            return rgetattr(self, key)
        return self.__dict__[key]

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
        """Get the current position of one or more devices.

        Args:
            device_names (List[str]): List of device names

        Examples:
            >>> dev.wm('samx')
            >>> dev.wm(['samx', 'samy'])
            >>> dev.wm(dev.primary_devices())
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
        dev_read = {dev.name: dev.read(cached=True, filter_signal=False) for dev in device_names}
        readbacks = {}
        setpoints = {}
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

    def show_all(self) -> None:
        """print all devices"""
        print(
            [
                (name, dev._config["acquisitionConfig"]["acquisitionGroup"])
                for name, dev in self.items()
            ]
        )

    def __repr__(self) -> str:
        return f"Device container."


def rpc(fcn):
    """Decorator to perform rpc calls."""

    @functools.wraps(fcn)
    def wrapper(self, *args, **kwargs):
        # pylint: disable=protected-access
        device, func_call = self._get_rpc_func_name(fcn=fcn)

        if kwargs.get("cached", False):
            return fcn(self, *args, **kwargs)
        return self._run_rpc_call(device, func_call, *args, **kwargs)

    return wrapper


class RPCBase:
    def __init__(self, name: str, info: dict = None, config: dict = None, parent=None) -> None:
        self.name = name
        if info is None:
            info = {}
        self._info = info.get("device_info")
        self.parent = parent
        self._config = config if config else self.root._config
        self._custom_rpc_methods = {}
        if self._info:
            self._parse_info()

        self.run = lambda *args, **kwargs: self._run(*args, **kwargs)

    def _run(self, *args, **kwargs):
        device, func_call = self._get_rpc_func_name(fcn_name=self.name, use_parent=True)
        return self._run_rpc_call(device, func_call, *args, **kwargs)

    @property
    def root(self):
        parent = self
        while not isinstance(parent.parent, DeviceManagerBase):
            parent = parent.parent
        return parent

    def _run_rpc_call(self, device, func_call, *args, **kwargs):
        rpc_id = str(uuid.uuid4())
        requestID = str(uuid.uuid4())  # TODO: move this to the API server
        params = {
            "device": device,
            "rpc_id": rpc_id,
            "func": func_call,
            "args": args,
            "kwargs": kwargs,
        }
        msg = ScanQueueMessage(
            scan_type="device_rpc",
            parameter=params,
            queue="primary",
            metadata={"RID": requestID},
        )
        self.root.parent.producer.send(MessageEndpoints.scan_queue_request(), msg.dumps())
        queue = self.root.parent.parent.queue
        while queue.request_storage.find_request_by_ID(requestID) is None:
            time.sleep(0.1)
        scan_queue_request = queue.request_storage.find_request_by_ID(requestID)
        while scan_queue_request.decision_pending:
            time.sleep(0.1)
        if not all(scan_queue_request.accepted):
            raise ScanRequestError(
                f"Function call was rejected by the server: {scan_queue_request.response.content['message']}"
            )
        while True:
            msg = self.root.parent.producer.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.01)
        msg = DeviceRPCMessage.loads(msg)
        if not msg.content["success"]:
            error = msg.content["out"]
            raise RPCError(
                f"During an RPC, the following error occured:\n{error['error']}: {error['msg']}.\nTraceback: {error['traceback']}\n The scan will be aborted."
            )
        print(msg.content.get("out"))
        return msg.content.get("return_val")

    def _get_rpc_func_name(self, fcn_name=None, fcn=None, use_parent=False):
        if not fcn_name:
            fcn_name = fcn.__name__
        full_func_call = ".".join([self._compile_function_path(use_parent=use_parent), fcn_name])
        device = full_func_call.split(".", maxsplit=1)[0]
        func_call = ".".join(full_func_call.split(".")[1:])
        return (device, func_call)

    def _compile_function_path(self, use_parent=False) -> str:
        if use_parent:
            parent = self.parent
        else:
            parent = self
        func_call = []
        while not isinstance(parent, DeviceManagerBase):
            func_call.append(parent.name)
            parent = parent.parent
        return ".".join(func_call[::-1])

    def _parse_info(self):
        if self._info.get("signals"):
            for signal_name in self._info.get("signals"):
                setattr(self, signal_name, Signal(signal_name, parent=self))
        if self._info.get("sub_devices"):
            for dev in self._info.get("sub_devices"):
                base_class = dev["device_info"].get("device_base_class")
                if base_class == "positioner":
                    setattr(
                        self,
                        dev.get("device_attr_name"),
                        Positioner(dev.get("device_attr_name"), parent=self),
                    )
                elif base_class == "device":
                    setattr(
                        self,
                        dev.get("device_attr_name"),
                        DeviceBase(dev.get("device_attr_name"), config=None, parent=self),
                    )

        for user_access_name, descr in self._info.get("custom_user_access", {}).items():
            if "type" in descr:
                self._custom_rpc_methods[user_access_name] = RPCBase(
                    name=user_access_name, info=descr, parent=self
                )
                setattr(
                    self,
                    user_access_name,
                    self._custom_rpc_methods[user_access_name].run,
                )
                setattr(getattr(self, user_access_name), "__doc__", descr.get("doc"))
            else:
                self._custom_rpc_methods[user_access_name] = RPCBase(
                    name=user_access_name,
                    info={"device_info": {"custom_user_access": descr}},
                    parent=self,
                )
                setattr(
                    self,
                    user_access_name,
                    self._custom_rpc_methods[user_access_name],
                )

    def update_config(self, update):
        self.root.parent.config_helper.send_config_request(
            action="update", config={self.name: update}
        )


class DeviceBase(RPCBase, Device):
    """
    Device (bluesky interface):
    * trigger
    * read
    * describe
    * stage
    * unstage
    * pause
    * resume
    """

    @property
    def enabled(self):
        return self.root._config["enabled"]

    @enabled.setter
    def enabled(self, val):
        self.update_config({"enabled": val})
        self.root._config["enabled"] = val

    @rpc
    def trigger(self, rpc_id: str):
        pass

    @rpc
    def read(self, cached=False, use_readback=True, filter_signal=True):
        full_name = self._get_full_obj_name()
        if use_readback:
            val = self.root.parent.producer.get(MessageEndpoints.device_readback(full_name))
        else:
            val = self.root.parent.producer.get(MessageEndpoints.device_read(full_name))

        if not val:
            return None
        signals = DeviceMessage.loads(val).content["signals"]
        signal_name = full_name.replace(".", "_")
        if filter_signal and signals.get(signal_name):
            return signals.get(signal_name)
        return signals

    @rpc
    def read_configuration(self):
        pass

    @rpc
    def describe(self):
        pass

    @rpc
    def stage(self):
        pass

    @rpc
    def unstage(self):
        pass

    @rpc
    def summary(self):
        pass


class Signal(DeviceBase):
    """
    Signal:
    * trigger
    * get
    * put
    * set
    * value
    * read
    * describe
    * limits
    * low limit
    * high limit
    """

    @rpc
    def get(self):
        pass

    @rpc
    def put(self, val):
        pass

    @rpc
    def set(self, val):
        pass

    @rpc
    def value(self):
        pass

    @rpc
    def limits(self):
        pass

    def low_limit(self):
        pass

    @rpc
    def high_limit(self):
        pass


class Positioner(DeviceBase):
    """
    Positioner:
    * trigger
    * read
    * set
    * stop
    * settle_time
    * timeout
    * egu
    * limits
    * low_limit
    * high_limit
    * move
    * position
    * moving
    """

    @rpc
    def set(self, val):
        pass

    @rpc
    def stop(self):
        pass

    @rpc
    def settle_time(self):
        pass

    @rpc
    def timeout(self):
        pass

    @rpc
    def egu(self):
        pass

    @property
    def limits(self):
        return self._config["deviceConfig"]["limits"]

    @limits.setter
    def limits(self, val: list):
        self.update_config({"deviceConfig": {"limits": val}})

    @property
    def low_limit(self):
        return self.limits[0]

    @low_limit.setter
    def low_limit(self, val: float):
        limits = [val, self.high_limit]
        self.update_config({"deviceConfig": {"limits": limits}})

    @property
    def high_limit(self):
        return self.limits[1]

    @high_limit.setter
    def high_limit(self, val: float):
        limits = [self.low_limit, val]
        self.update_config({"deviceConfig": {"limits": limits}})

    def move(self, val: float, relative=False):
        return self.parent.parent.scans.mv(self, val, relative=relative)

    @rpc
    def position(self):
        pass

    @rpc
    def moving(self):
        pass


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
            bootstrap_server: Kafka's bootstrap server

        Returns:

        """
        self._start_connectors(bootstrap_server)
        self._get_config()

    def update_status(self, status: BECStatus):
        for cb in self._status_cb:
            if cb:
                cb(status)

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
                if "onFailure" in config[dev]:
                    self.devices[dev]._config["onFailure"] = config[dev]["onFailure"]
                if "deviceTags" in config[dev]:
                    self.devices[dev]._config["deviceTags"] = config[dev]["deviceTags"]
                if "acquisitionConfig" in config[dev]:
                    self.devices[dev]._config["acquisitionConfig"] = config[dev][
                        "acquisitionConfig"
                    ]

        elif action == "add":
            self.update_status(BECStatus.BUSY)
            for dev in config:
                obj = self._create_device(dev)
                self.devices._add_device(dev.get("name"), obj)
            self.update_status(BECStatus.RUNNING)
        elif action == "reload":
            self.update_status(BECStatus.BUSY)
            logger.info("Reloading config.")
            self.devices.flush()
            self._get_config()
            self.update_status(BECStatus.RUNNING)
        elif action == "remove":
            self.update_status(BECStatus.BUSY)
            for dev in config:
                self._remove_device(dev)
            self.update_status(BECStatus.RUNNING)

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
        pass

    def _stop_custom_consumer(self) -> None:
        """
        Stop all custom consumers. Override this method in a derived class.
        Returns:

        """
        pass

    def _get_device_info(self, device_name) -> DeviceInfoMessage:
        msg = DeviceInfoMessage.loads(self.producer.get(MessageEndpoints.device_info(device_name)))
        return msg

    def _create_device(self, dev: dict, *args) -> Device:
        msg = self._get_device_info(dev.get("name"))
        name = msg.content["device"]
        info = msg.content["info"]

        base_class = info["device_info"]["device_base_class"]

        if base_class == "device":
            logger.info(f"Adding new device {name}")
            obj = DeviceBase(name, info, config=dev, parent=self)
        elif base_class == "positioner":
            logger.info(f"Adding new positioner {name}")
            obj = Positioner(name, info, config=dev, parent=self)
        elif base_class == "signal":
            logger.info(f"Adding new signal {name}")
            obj = Signal(name, info, config=dev, parent=self)
        else:
            logger.error(f"Trying to add new device {name} of type {base_class}")

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

    def check_request_validity(self, msg: DeviceConfigMessage) -> None:
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
        Returns:

        """
        try:
            self.connector.shutdown()
        except RuntimeError as runtime_error:
            logger.error(f"Failed to shutdown connector. {runtime_error}")

    def __del__(self):
        self.shutdown()
