import os
import time
import traceback
import uuid

import bec_utils
import msgpack
from bec_utils import BECMessage, Device, DeviceConfigError
from bec_utils import DeviceManagerBase as DeviceManager
from bec_utils import MessageEndpoints, ServiceConfig
from bec_utils.connector import ConnectorBase

from .scibec_validator import SciBecValidator

dir_path = os.path.abspath(os.path.join(os.path.dirname(bec_utils.__file__), "../../scibec/"))


class ConfigHandler:
    def __init__(self, config: ServiceConfig, connector: ConnectorBase) -> None:
        self.device_manager = DeviceManager(connector)
        self.device_manager.initialize(config.redis)
        self.producer = connector.producer()
        self.validator = SciBecValidator(os.path.join(dir_path, "openapi_schema.json"))

    def parse_config_request(self, msg: BECMessage.DeviceConfigMessage) -> None:
        """Processes a config request. If successful, it emits a config reply

        Args:
            msg (BMessage.DeviceConfigMessage): Config request

        """
        try:
            self.device_manager.check_request_validity(msg)
            if msg.content["action"] == "update":
                self._update_config(msg)
            if msg.content["action"] == "reload":
                self._reload_config(msg)

        except DeviceConfigError as dev_conf_error:
            content = traceback.format_exc()
            self.send_config_request_reply(accepted=False, error_msg=content, metadata=msg.metadata)

    def send_config(self, msg: BECMessage.DeviceConfigMessage) -> None:
        """broadcast a new config"""
        self.producer.send(MessageEndpoints.device_config_update(), msg.dumps())

    def send_config_request_reply(self, accepted, error_msg, metadata):
        """send a config request reply"""
        msg = BECMessage.RequestResponseMessage(
            accepted=accepted, message=error_msg, metadata=metadata
        )
        RID = metadata.get("RID")
        self.producer.set(
            MessageEndpoints.device_config_request_response(RID), msg.dumps(), expire=60
        )

    def _reload_config(self, msg: BECMessage.DeviceConfigMessage):
        self.send_config_request_reply(accepted=True, error_msg=None, metadata=msg.metadata)
        self.send_config(msg)
        # self.device_manager.update_status(BECStatus.BUSY)
        # self.device_manager.devices.flush()
        # self.device_manager._get_config()
        # self.device_manager.update_status(BECStatus.RUNNING)

    def _update_config(self, msg: BECMessage.DeviceConfigMessage):
        updated = False
        dev_configs = msg.content["config"]

        for dev, config in dev_configs.items():
            device = self.device_manager.devices[dev]
            updated = self._update_device_config(device, config.copy())
            if updated:
                self.update_scibec_config(device)

        # send updates to services
        if updated:
            self.send_config(msg)
            self.send_config_request_reply(accepted=True, error_msg=None, metadata=msg.metadata)

    def _update_device_server(self, RID: str, config: dict) -> None:
        msg = BECMessage.DeviceConfigMessage(action="update", config=config, metadata={"RID": RID})
        self.producer.send(MessageEndpoints.device_server_config_request(), msg.dumps())

    def _wait_for_device_server_update(self, RID: str) -> bool:
        timeout = 10
        time_step = 0.05
        elapsed_time = 0
        while True:
            raw_msg = self.producer.get(MessageEndpoints.device_server_config_request_response(RID))
            msg = BECMessage.RequestResponseMessage.loads(raw_msg)
            if msg:
                return msg.content["accepted"]

            if elapsed_time > timeout:
                raise TimeoutError(
                    "Reached timeout whilst waiting for a device server config reply."
                )

            time.sleep(time_step)
            elapsed_time += time_step

    def _update_device_config(self, device: Device, dev_config) -> bool:
        updated = False
        if "deviceConfig" in dev_config:
            RID = str(uuid.uuid4())
            self._update_device_server(RID, {device.name, dev_config})
            updated = self._wait_for_device_server_update(RID)

            # # store old config
            # old_config = device._config["deviceConfig"].copy()

            # # apply config
            # try:
            #     self.device_manager.update_config(device.obj, dev_config["deviceConfig"])
            # except Exception as exc:
            #     self.device_manager.update_config(device.obj, old_config)
            #     raise DeviceConfigError(f"Error during object update. {exc}") from exc

            # ref_config = device._config["deviceConfig"].copy()
            # ref_config.update(dev_config["deviceConfig"])
            # self._validate_update({"deviceConfig": ref_config})

            # device._config["deviceConfig"].update(dev_config["deviceConfig"])

            updated = True
            dev_config.pop("device_config")

        if "enabled" in dev_config:
            self._validate_update({"enabled": dev_config["enabled"]})
            device._config["enabled"] = dev_config["enabled"]
            RID = str(uuid.uuid4())
            self._update_device_server(RID, {device.name: dev_config})
            updated = self._wait_for_device_server_update(RID)
            # if device.enabled:
            #     # pylint:disable=protected-access
            #     if device.obj._destroyed:
            #         self.device_manager.initialize_device(device._config)
            #     else:
            #         self.device_manager.initialize_enabled_device(device)
            # else:
            #     self.device_manager.disconnect_device(device.obj)

            updated = True
            dev_config.pop("enabled")

        if not dev_config:
            return updated

        available_keys = [
            "enabled_set",
            "userParamter",
            "onFailure",
            "deviceTags",
            "acquisitionConfig",
        ]
        for key in dev_config:
            if key not in available_keys:
                raise DeviceConfigError(f"Unknown update key {key}.")

            self._validate_update({key: dev_config[key]})
            device._config[key] = dev_config[key]
            updated = True

        return updated

    def _validate_update(self, update):
        self.validator.validate_device_patch(update)

    def update_scibec_config(self, device):
        raw_msg = self.device_manager.producer.get(MessageEndpoints.device_config())
        config = msgpack.loads(raw_msg)
        index = next(
            index for index, dev_conf in enumerate(config) if dev_conf["name"] == device.name
        )
        config[index] = device._config
        self.device_manager.producer.set(MessageEndpoints.device_config(), msgpack.dumps(config))

    def update_config_in_redis(self, device):
        raw_msg = self.device_manager.producer.get(MessageEndpoints.device_config())
        config = msgpack.loads(raw_msg)
        index = next(
            index for index, dev_conf in enumerate(config) if dev_conf["name"] == device.name
        )
        config[index] = device._config
        self.device_manager.producer.set(MessageEndpoints.device_config(), msgpack.dumps(config))
