from __future__ import annotations

import os
import traceback
from typing import TYPE_CHECKING

import bec_utils
import msgpack
from bec_utils import BECMessage as BMessage
from bec_utils import BECStatus, DeviceConfigError, MessageEndpoints, bec_logger

from .scibec_validator import SciBecValidator

if TYPE_CHECKING:
    from devicemanager import DeviceManagerDS

logger = bec_logger.logger

dir_path = os.path.abspath(os.path.join(os.path.dirname(bec_utils.__file__), "../../scibec/"))


class ConfigHandler:
    def __init__(self, device_manager: DeviceManagerDS) -> None:
        self.device_manager = device_manager
        self.validator = SciBecValidator(os.path.join(dir_path, "openapi_schema.json"))

    def send_config(self, msg: BMessage.DeviceConfigMessage) -> None:
        """broadcast a new config"""
        self.device_manager.producer.send(MessageEndpoints.device_config_update(), msg.dumps())

    def parse_config_request(self, msg: BMessage.DeviceConfigMessage) -> None:
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
            self.device_manager.send_config_request_reply(
                accepted=False, error_msg=content, metadata=msg.metadata
            )

    def _reload_config(self, msg: BMessage.DeviceConfigMessage):
        self.device_manager.send_config_request_reply(
            accepted=True, error_msg=None, metadata=msg.metadata
        )
        self.send_config(msg)
        self.device_manager.update_status(BECStatus.BUSY)
        self.device_manager.devices.flush()
        self.device_manager._get_config()
        self.device_manager.update_status(BECStatus.RUNNING)

    def _update_config(self, msg: BMessage.DeviceConfigMessage):
        updated = False
        for dev in msg.content["config"]:
            dev_config = msg.content["config"][dev]
            device = self.device_manager.devices[dev]
            updated = self._update_device_config(device, dev_config.copy())
            if updated:
                self.update_config_in_redis(device)

        # send updates to services
        if updated:
            self.send_config(msg)
            self.device_manager.send_config_request_reply(
                accepted=True, error_msg=None, metadata=msg.metadata
            )

    def _update_device_config(self, device, dev_config) -> bool:
        if "deviceConfig" in dev_config:
            # store old config
            old_config = device._config["deviceConfig"].copy()

            # apply config
            try:
                self.device_manager.update_config(device.obj, dev_config["deviceConfig"])
            except Exception as exc:
                self.device_manager.update_config(device.obj, old_config)
                raise DeviceConfigError(f"Error during object update. {exc}") from exc

            ref_config = device._config["deviceConfig"].copy()
            ref_config.update(dev_config["deviceConfig"])
            self._validate_update({"deviceConfig": ref_config})

            device._config["deviceConfig"].update(dev_config["deviceConfig"])

            updated = True
            dev_config.pop("device_config")

        if "enabled" in dev_config:
            self._validate_update({"enabled": dev_config["enabled"]})
            device._config["enabled"] = dev_config["enabled"]

            if device.enabled:
                # pylint:disable=protected-access
                if device.obj._destroyed:
                    self.device_manager.initialize_device(device._config)
                else:
                    self.device_manager.initialize_enabled_device(device)
            else:
                self.device_manager.disconnect_device(device.obj)

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
        for key in available_keys:
            if key not in dev_config:
                raise DeviceConfigError(f"Unknown update key {key}.")

            self._validate_update({key: dev_config[key]})
            device._config[key] = dev_config[key]
            updated = True

        return updated

    def _validate_update(self, update):
        self.validator.validate_device_patch(update)

    def update_config_in_redis(self, device):
        raw_msg = self.device_manager.producer.get(MessageEndpoints.device_config())
        config = msgpack.loads(raw_msg)
        index = next(
            index for index, dev_conf in enumerate(config) if dev_conf["name"] == device.name
        )
        config[index] = device._config
        self.device_manager.producer.set(MessageEndpoints.device_config(), msgpack.dumps(config))
