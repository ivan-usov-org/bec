import inspect
import traceback

import bec_utils.BECMessage as BMessage
import ophyd
import ophyd.sim as ops
import ophyd_devices as opd
from bec_utils import (
    Device,
    DeviceConfigError,
    DeviceManagerBase,
    MessageEndpoints,
    bec_logger,
)
from bec_utils.connector import ConnectorBase
from device_server.devices.device_serializer import get_device_info
from ophyd.ophydobj import OphydObject

logger = bec_logger.logger


class DSDevice(Device):
    def __init__(self, name, obj, config, parent=None):
        super().__init__(name, config, parent=parent)
        self.obj = obj
        self.metadata = {}

    def initialize_device_buffer(self, producer):
        """initialize the device read and readback buffer on redis with a new reading"""
        dev_msg = BMessage.DeviceMessage(signals=self.obj.read(), metadata={}).dumps()
        pipe = producer.pipeline()
        producer.set_and_publish(MessageEndpoints.device_readback(self.name), dev_msg, pipe=pipe)
        producer.set(topic=MessageEndpoints.device_read(self.name), msg=dev_msg, pipe=pipe)
        pipe.execute()


class DeviceManagerDS(DeviceManagerBase):
    def __init__(self, connector: ConnectorBase, scibec_url: str):
        super().__init__(connector, scibec_url)
        self._config_request_connector = None
        self._device_instructions_connector = None

    def _get_device_class(self, dev_type):
        module = None
        if hasattr(ophyd, dev_type):
            module = ophyd
        elif hasattr(opd, dev_type):
            module = opd
        elif hasattr(ops, dev_type):
            module = ops
        else:
            TypeError(f"Unknown device class {dev_type}")
        return getattr(module, dev_type)

    def _load_session(self, *_args, **_kwargs):
        if self._is_config_valid():
            for dev in self._session["devices"]:
                name = dev.get("name")
                enabled = dev.get("enabled")
                logger.info(f"Adding device {name}: {'ENABLED' if enabled else 'DISABLED'}")
                self.initialize_device(dev)

    @staticmethod
    def update_config(obj: OphydObject, config: dict) -> None:
        """Update an ophyd device's config

        Args:
            obj (Ophydobj): Ophyd object that should be updated
            config (dict): Config dictionary

        """
        if hasattr(obj, "update_config"):
            obj.update_config(config)
        else:
            for config_key, config_value in config.items():
                # first handle the ophyd exceptions...
                if config_key == "limits":
                    if hasattr(obj, "low_limit_travel") and hasattr(obj, "high_limit_travel"):
                        obj.low_limit_travel.set(config_value[0])
                        obj.high_limit_travel.set(config_value[1])
                        continue
                if config_key == "labels":
                    if not config_value:
                        config_value = set()
                    # pylint: disable=protected-access
                    obj._ophyd_labels_ = set(config_value)
                    continue
                if not hasattr(obj, config_key):
                    raise DeviceConfigError(
                        f"Unknown config parameter {config_key} for device of type {obj.__class__.__name__}."
                    )

                config_attr = getattr(obj, config_key)
                if isinstance(config_attr, ophyd.Signal):
                    config_attr.set(config_value)
                elif callable(config_attr):
                    config_attr(config_value)
                else:
                    setattr(obj, config_key, config_value)

    def initialize_device(self, dev: dict) -> DSDevice:
        """
        Prepares a device for later usage.
        This includes inspecting the device class signature,
        initializing the object, refreshing the device info and buffer,
        as well as adding subscriptions.
        """
        name = dev.get("name")
        enabled = dev.get("enabled")

        dev_cls = self._get_device_class(dev["deviceClass"])
        config = dev["deviceConfig"].copy()

        # pylint: disable=protected-access
        class_params = inspect.signature(dev_cls)._parameters
        class_params_and_config_keys = set(class_params) & config.keys()

        init_kwargs = {key: config.pop(key) for key in class_params_and_config_keys}
        device_access = config.pop("device_access", None)
        if device_access or (device_access is None and config.get("device_mapping")):
            init_kwargs["device_manager"] = self

        # initialize the device object
        obj = dev_cls(**init_kwargs, **config)
        self.update_config(obj, config)

        # refresh the device info
        pipe = self.producer.pipeline()
        self.reset_device_data(obj, pipe)
        self.publish_device_info(obj, pipe)
        pipe.execute()

        # add subscriptions
        if "readback" in obj.event_types:
            obj.subscribe(self._obj_callback_readback, run=enabled)
        if "done_moving" in obj.event_types:
            obj.subscribe(self._obj_callback_done_moving, event_type="done_moving", run=False)
        if hasattr(obj, "motor_is_moving"):
            obj.motor_is_moving.subscribe(self._obj_callback_is_moving, run=enabled)

        # insert the created device obj into the device manager
        opaas_obj = DSDevice(name, obj, config=dev, parent=self)

        # pylint:disable=protected-access # this function is shared with clients and it is currently not foreseen that clients add new devices
        self.devices._add_device(name, opaas_obj)

        if not enabled:
            return opaas_obj

        # update device buffer for enabled devices
        try:
            if not opaas_obj.obj.connected:
                if hasattr(opaas_obj.obj, "controler"):
                    opaas_obj.obj.controller.on()
                else:
                    logger.error(
                        f"Device {opaas_obj.obj.name} does not implement the socket controller interface and cannot be turned on."
                    )
            opaas_obj.initialize_device_buffer(self.producer)
        # pylint:disable=broad-except
        except Exception:
            error_traceback = traceback.format_exc()
            logger.error(
                f"{error_traceback}. Failed to stage {opaas_obj.name}. The device will be disabled."
            )
            opaas_obj.enabled = False

        return opaas_obj

    def publish_device_info(self, obj: OphydObject, pipe=None) -> None:
        """
        Publish the device info to redis. The device info contains
        inter alia the class name, user functions and signals.

        Args:
            obj (_type_): _description_
        """

        interface = get_device_info(obj, {})
        self.producer.set(
            MessageEndpoints.device_info(obj.name),
            BMessage.DeviceInfoMessage(device=obj.name, info=interface).dumps(),
            pipe,
        )

    def reset_device_data(self, obj: OphydObject, pipe=None) -> None:
        """delete all device data and device info"""
        self.producer.delete(MessageEndpoints.device_status(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_read(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_last_read(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_info(obj.name), pipe)

    def _obj_callback_readback(self, *_args, **kwargs):
        obj = kwargs["obj"]
        if obj.connected:
            name = obj.root.name
            signals = obj.read()
            metadata = self.devices.get(obj.root.name).metadata
            dev_msg = BMessage.DeviceMessage(signals=signals, metadata=metadata).dumps()
            pipe = self.producer.pipeline()
            self.producer.set_and_publish(MessageEndpoints.device_readback(name), dev_msg, pipe)
            pipe.execute()

    def _obj_callback_acq_done(self, *_args, **kwargs):
        device = kwargs["obj"].root.name
        status = 0
        metadata = self.devices[device].metadata
        self.producer.send(
            MessageEndpoints.device_status(device),
            BMessage.DeviceStatusMessage(device=device, status=status, metadata=metadata).dumps(),
        )

    def _obj_callback_done_moving(self, *args, **kwargs):
        self._obj_callback_readback(*args, **kwargs)
        # self._obj_callback_acq_done(*args, **kwargs)

    def _obj_callback_is_moving(self, *_args, **kwargs):
        device = kwargs["obj"].root.name
        status = int(kwargs.get("value"))
        metadata = self.devices[device].metadata
        self.producer.set(
            MessageEndpoints.device_status(kwargs["obj"].root.name),
            BMessage.DeviceStatusMessage(device=device, status=status, metadata=metadata).dumps(),
        )

    def _start_custom_connectors(self, bootstrap_server):
        self._config_request_connector = self.connector.consumer(
            MessageEndpoints.device_config_request(),
            cb=self._device_config_request_callback,
            parent=self,
        )
        self._config_request_connector.start()

    def _stop_custom_consumer(self) -> None:
        self._config_request_connector.signal_event.set()
        self._config_request_connector.join()

    def send_config_request_rejection(self, error_msg):
        """send a reply back if the config request was rejected"""

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        msg = BMessage.DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received request: {msg}")
        parent.parse_config_request(msg)

    def send_config(self, msg: BMessage.DeviceConfigMessage) -> None:
        """broadcast a new config"""
        self.producer.send(MessageEndpoints.device_config(), msg.dumps())

    def parse_config_request(self, msg: BMessage.DeviceConfigMessage) -> None:
        """Processes a config request. If successful, it emits a config reply

        Args:
            msg (BMessage.DeviceConfigMessage): Config request

        """
        try:
            self._check_request_validity(msg)
            if msg.content["action"] != "update":
                return
            updated = False
            for dev in msg.content["config"]:
                dev_config = msg.content["config"][dev]
                if "deviceConfig" in dev_config:
                    # store old config
                    old_config = self.devices[dev].config["deviceConfig"].copy()

                    # apply config
                    try:
                        self.update_config(self.devices[dev].obj, dev_config["deviceConfig"])
                    except Exception as exc:
                        self.update_config(self.devices[dev].obj, old_config)
                        raise DeviceConfigError(f"Error during object update. {exc}") from exc

                    self.devices[dev].config["deviceConfig"].update(dev_config["deviceConfig"])

                    # update config in DB
                    self.update_device_config_in_db(device_name=dev)
                    updated = True

                if "enabled" in dev_config:
                    self.devices[dev].config["enabled"] = dev_config["enabled"]
                    # update device enabled status in DB
                    self.update_device_enabled_in_db(device_name=dev)
                    updated = True

            # send updates to services
            if updated:
                self.send_config(msg)

        except DeviceConfigError as dev_conf_error:
            self.send_config_request_rejection(dev_conf_error)

    def update_device_enabled_in_db(self, device_name: str) -> None:
        """Update a device enabled setting in the DB with the local version

        Args:
            device_name (str): Name of the device that should be updated

        Raises:
            DeviceConfigError: Raised if the db update fails.
        """
        logger.debug("updating in DB")
        success = self._scibec.patch_device_config(
            self.devices[device_name].config["id"],
            {"enabled": self.devices[device_name].enabled},
        )
        if not success:
            raise DeviceConfigError("Error during database update.")

    def update_device_config_in_db(self, device_name: str) -> None:
        """Update a device config in the DB with the local version

        Args:
            device_name (str): Name of the device that should be updated

        Raises:
            DeviceConfigError: Raised if the db update fails.
        """
        logger.debug("updating in DB")
        success = self._scibec.patch_device_config(
            self.devices[device_name].config["id"],
            {"deviceConfig": self.devices[device_name].config["deviceConfig"]},
        )
        if not success:
            raise DeviceConfigError("Error during database update.")
