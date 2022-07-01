import inspect
import logging
import time
from email.message import Message

import bec_utils.BECMessage as BMessage
import msgpack
import ophyd
import ophyd.sim as ops
import ophyd_devices as opd
from bec_utils import Device, DeviceConfigError, DeviceManagerBase, MessageEndpoints
from bec_utils.connector import ConnectorBase
from device_server.devices.device_serializer import get_device_info

logger = logging.getLogger(__name__)


class DSDevice(Device):
    def __init__(self, name, obj, config):
        super().__init__(name, config)
        self.obj = obj
        self.metadata = {}

    def initialize_device_buffer(self, producer):
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

    def update_config(self, config) -> None:
        print(config)

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

    def _load_session(self, *args, **kwargs):
        if self._is_config_valid():
            for dev in self._session["devices"]:
                name = dev.get("name")
                enabled = dev.get("enabled")
                logger.info(f"Adding device {name}: {'ENABLED' if enabled else 'DISABLED'}")
                obj = self.initialize_device(dev)

    @staticmethod
    def update_config(obj, config) -> None:
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
        name = dev.get("name")
        enabled = dev.get("enabled")

        dev_cls = self._get_device_class(dev["deviceClass"])
        config = dev["deviceConfig"].copy()

        class_params = inspect.signature(dev_cls)._parameters
        class_params_and_config_keys = set(class_params) & config.keys()

        init_kwargs = {key: config.pop(key) for key in class_params_and_config_keys}
        if config.get("device_access"):
            init_kwargs["device_manager"] = self

        # initialize the device object
        obj = dev_cls(**init_kwargs)
        self.update_config(obj, config)

        # refresh the device info
        pipe = self.producer.pipeline()
        self.reset_device_data(obj, pipe)
        self.publish_device_info(obj, pipe)
        pipe.execute()

        # add subscriptions
        obj.subscribe(self._obj_callback_readback, run=enabled)
        if "acq_done" in obj.event_types:
            obj.subscribe(self._obj_callback_acq_done, event_type="acq_done", run=False)
        if "done_moving" in obj.event_types:
            obj.subscribe(self._obj_callback_done_moving, event_type="done_moving", run=False)
        if hasattr(obj, "motor_is_moving"):
            obj.motor_is_moving.subscribe(self._obj_callback_is_moving, run=enabled)

        # insert the created device obj into the device manager
        opaas_obj = DSDevice(name, obj, config=dev)
        self.devices._add_device(name, opaas_obj)

        # update device buffer
        if enabled:
            if not opaas_obj.obj.connected:
                opaas_obj.obj.stage()
            opaas_obj.initialize_device_buffer(self.producer)

        return opaas_obj

    def publish_device_info(self, obj, pipe=None) -> None:
        """


        Args:
            obj (_type_): _description_
        """

        interface = get_device_info(obj, {})
        self.producer.set(
            MessageEndpoints.device_info(obj.name),
            BMessage.DeviceInfoMessage(device=obj.name, info=interface).dumps(),
            pipe,
        )

    def reset_device_data(self, obj, pipe=None) -> None:
        self.producer.delete(MessageEndpoints.device_status(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_read(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_last_read(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_info(obj.name), pipe)

    def _obj_callback_readback(self, *args, **kwargs):
        # print(BMessage.DeviceMessage(signals=kwargs["obj"].read()).content)
        # start = time.time()
        obj = kwargs["obj"]
        if obj.connected:
            name = obj.root.name
            signals = obj.read()
            metadata = self.devices.get(obj.root.name).metadata
            dev_msg = BMessage.DeviceMessage(signals=signals, metadata=metadata).dumps()
            pipe = self.producer.pipeline()
            self.producer.set_and_publish(MessageEndpoints.device_readback(name), dev_msg, pipe)
            pipe.execute()
        # print(f"Elapsed time for readback of {kwargs['obj'].name}, pos {kwargs['obj'].read()}: {(time.time()-start)*1000} ms")

    def _obj_callback_acq_done(self, *_args, **kwargs):
        status_info = self.devices.get(kwargs["obj"].root.name).metadata
        status_info["status"] = 0
        self.producer.set(
            MessageEndpoints.device_status(kwargs["obj"].root.name),
            msgpack.dumps(status_info),
        )

    def _obj_callback_done_moving(self, *args, **kwargs):
        self._obj_callback_readback(*args, **kwargs)
        self._obj_callback_acq_done(*args, **kwargs)

    def _obj_callback_is_moving(self, *_args, **kwargs):
        status_info = self.devices.get(kwargs["obj"].root.name).metadata
        status_info["status"] = int(kwargs.get("value"))
        status_info["timestamp"] = time.time()
        self.producer.set(
            MessageEndpoints.device_status(kwargs["obj"].root.name),
            msgpack.dumps(status_info),
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
        # self._device_instructions_connector.signal_event.set()
        # self._device_instructions_connector.join()

    def send_config_request_reply(self, error_msg):
        pass

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        msg = BMessage.DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received request: {msg}")
        parent.parse_config_request(msg)

    def send_config(self, msg: BMessage.DeviceConfigMessage) -> None:
        self.producer.send(MessageEndpoints.device_config(), msg.dumps())

    def parse_config_request(self, msg: BMessage.DeviceConfigMessage) -> None:
        try:
            self._check_request_validity(msg)
            if msg.content["action"] == "update":
                updated = False
                for dev in msg.content["config"]:
                    dev_config = msg.content["config"][dev]
                    if "deviceConfig" in dev_config:
                        # store old config
                        old_config = self.devices[dev].config["deviceConfig"].copy()

                        # apply config
                        try:
                            self.update_config(self.devices[dev].obj, dev_config["deviceConfig"])
                        except Exception as e:
                            self.update_config(self.devices[dev].obj, old_config)
                            raise DeviceConfigError(f"Error during object update. {e}")

                        self.devices[dev].config["deviceConfig"].update(dev_config["deviceConfig"])

                        # update config in DB
                        print("updating in DB")
                        success = self._scibec.patch_device_config(
                            self.devices[dev].config["id"],
                            {"deviceConfig": self.devices[dev].config["deviceConfig"]},
                        )
                        if not success:
                            raise DeviceConfigError("Error during database update.")
                        updated = True

                    if "enabled" in dev_config:
                        self.devices[dev].config["enabled"] = dev_config["enabled"]
                        updated = True

                # send updates to services
                if updated:
                    self.send_config(msg)

        except DeviceConfigError as dev_conf_error:
            self.send_config_request_reply(dev_conf_error)
