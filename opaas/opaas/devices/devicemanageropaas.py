import logging
import time

import bec_utils.BECMessage as BMessage
import msgpack
import ophyd
import ophyd.sim as ops
import ophyd_devices as opd
from bec_utils import Device, DeviceManagerBase, MessageEndpoints
from bec_utils.connector import ConnectorBase
from opaas.devices.device_serializer import get_device_info

logger = logging.getLogger(__name__)


class OPAASDevice(Device):
    def __init__(self, name, obj, enabled=False):
        super().__init__(name)
        self.obj = obj
        self.enabled = enabled
        self.metadata = {}

    def initialize_device_buffer(self, producer):
        dev_msg = BMessage.DeviceMessage(signals=self.obj.read(), metadata={}).dumps()
        pipe = producer.pipeline()
        producer.set_and_publish(MessageEndpoints.device_readback(self.name), dev_msg, pipe=pipe)
        producer.set(topic=MessageEndpoints.device_read(self.name), msg=dev_msg, pipe=pipe)
        pipe.execute()


class DeviceManagerOPAAS(DeviceManagerBase):
    def __init__(self, connector: ConnectorBase, scibec_url: str):
        super().__init__(connector, scibec_url)
        self._config_request_connector = None
        self._device_instructions_connector = None

    def _load_config_device(self):
        if self._is_config_valid():
            for name, dev in self._config.items():
                logger.info(
                    f"Adding device {name}: {'ENABLED' if dev['status']['enabled'] else 'DISABLED'}"
                )
                # BODGE:
                # TODO: remove this section
                if dev["type"] == "SynGauss":
                    obj = ops.det
                else:
                    _cls = self._get_device_class(dev["type"])
                    obj = _cls(**dev["config"])
                    obj.subscribe(self._obj_callback_readback, run=False)
                    obj.subscribe(self._obj_callback_acq_done, event_type="acq_done", run=False)
                    obj.motor_is_moving.subscribe(self._obj_callback_is_moving, run=False)
                self.devices._add_device(name, OPAASDevice(name, obj, dev["status"]["enabled"]))

        if self._is_config_valid():
            for dev in self._session["devices"]:
                obj = Device(dev.get("name"))
                obj.enabled = dev.get("enabled")
                self.devices._add_device(dev.get("name"), obj)

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

    def initialize_device(self, dev: dict) -> OPAASDevice:
        name = dev.get("name")
        enabled = dev.get("enabled")

        _cls = self._get_device_class(dev["deviceClass"])
        if len(dev["deviceConfig"].get("device_access", []))>0:
            obj = _cls(**dev["deviceConfig"], device_manager=self)
        else:
            obj = _cls(**dev["deviceConfig"])
        self.reset_device_data(obj)
        self.publish_device_info(obj)
        obj.subscribe(self._obj_callback_readback, run=enabled)
        if "acq_done" in obj.event_types:
            obj.subscribe(self._obj_callback_acq_done, event_type="acq_done", run=False)
        if "done_moving" in obj.event_types:
            obj.subscribe(self._obj_callback_done_moving, event_type="done_moving", run=False)

        if hasattr(obj, "motor_is_moving"):
            obj.motor_is_moving.subscribe(self._obj_callback_is_moving, run=enabled)
        opaas_obj = OPAASDevice(name, obj, enabled)
        self.devices._add_device(name, opaas_obj)
        if enabled:
            if not opaas_obj.obj.connected:
                opaas_obj.obj.stage()
            opaas_obj.initialize_device_buffer(self.producer)

        return opaas_obj

    def publish_device_info(self, obj) -> None:
        """


        Args:
            obj (_type_): _description_
        """

        interface = get_device_info(obj, {})
        self.producer.set(
            MessageEndpoints.device_info(obj.name),
            BMessage.DeviceInfoMessage(device=obj.name, info=interface).dumps(),
        )

    def reset_device_data(self, obj) -> None:
        self.producer.r.delete(MessageEndpoints.device_status(obj.name))
        self.producer.r.delete(MessageEndpoints.device_read(obj.name))
        self.producer.r.delete(MessageEndpoints.device_last_read(obj.name))
        self.producer.r.delete(MessageEndpoints.device_info(obj.name))

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

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        logger.info(f"Received request: {msg.value}")
        parent.parse_config_request(msg.value)
