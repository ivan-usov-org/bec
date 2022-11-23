from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from bec_utils import BECMessage as BMessage
from bec_utils import BECStatus, DeviceConfigError, MessageEndpoints, bec_logger

if TYPE_CHECKING:
    from devicemanager import DeviceManagerDS

logger = bec_logger.logger


class ConfigHandler:
    def __init__(self, device_manager: DeviceManagerDS) -> None:
        self.device_manager = device_manager

    def send_config(self, msg: BMessage.DeviceConfigMessage) -> None:
        """broadcast a new config"""
        self.device_manager.producer.send(MessageEndpoints.device_config(), msg.dumps())

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
        self.device_manager._get_config_from_DB()
        self.device_manager.update_status(BECStatus.RUNNING)

    def _update_config(self, msg: BMessage.DeviceConfigMessage):
        updated = False
        for dev in msg.content["config"]:
            dev_config = msg.content["config"][dev]
            device = self.device_manager.devices[dev]
            if "deviceConfig" in dev_config:
                # store old config
                old_config = device._config["deviceConfig"].copy()

                # apply config
                try:
                    self.device_manager.update_config(device.obj, dev_config["deviceConfig"])
                except Exception as exc:
                    self.device_manager.update_config(device.obj, old_config)
                    raise DeviceConfigError(f"Error during object update. {exc}") from exc

                device._config["deviceConfig"].update(dev_config["deviceConfig"])

                # update config in DB
                self.update_device_key_in_db(device_name=dev, key="deviceConfig")
                updated = True

            if "enabled" in dev_config:
                device._config["enabled"] = dev_config["enabled"]

                if device.enabled:
                    # pylint:disable=protected-access
                    if device.obj._destroyed:
                        self.device_manager.initialize_device(device._config)
                    else:
                        self.device_manager.initialize_enabled_device(device)
                else:
                    self.device_manager.disconnect_device(device.obj)

                # update device enabled status in DB
                self.update_device_key_in_db(device_name=dev, key="enabled")
                updated = True
            if "enabled_set" in dev_config:
                device._config["enabled_set"] = dev_config["enabled_set"]
                # update device enabled status in DB
                self.update_device_key_in_db(device_name=dev, key="enabled_set")
                updated = True

            if "userParameter" in dev_config:
                device._config["userParameter"] = dev_config["userParameter"]
                self.update_device_key_in_db(device_name=dev, key="userParameter")
                updated = True

            if "onFailure" in dev_config:
                device._config["onFailure"] = dev_config["onFailure"]
                self.update_device_key_in_db(device_name=dev, key="onFailure")
                updated = True

            if "deviceTags" in dev_config:
                device._config["deviceTags"] = dev_config["deviceTags"]
                self.update_device_key_in_db(device_name=dev, key="deviceTags")
                updated = True

        # send updates to services
        if updated:
            self.send_config(msg)
            self.device_manager.send_config_request_reply(
                accepted=True, error_msg=None, metadata=msg.metadata
            )

    def update_device_key_in_db(self, device_name: str, key: str) -> None:
        """Update a device key in the DB with the local version

        Args:
            device_name (str): Name of the device that should be updated
            key (str): Name of the config entry that should be updated

        Raises:
            DeviceConfigError: Raised if the db update fails.
        """
        logger.debug("updating in DB")
        success = self.device_manager.scibec.patch_device_config(
            self.device_manager.devices[device_name]._config["id"],
            {key: self.device_manager.devices[device_name]._config[key]},
        )
        if not success:
            raise DeviceConfigError("Error during database update.")
