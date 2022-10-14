from bec_utils import BECMessage as BMessage
from bec_utils import (
    DeviceConfigError,
    DeviceManagerBase,
    MessageEndpoints,
    ProducerConnector,
    bec_logger,
)

logger = bec_logger.logger


class ConfigHandler:
    def __init__(self, device_manager: DeviceManagerBase) -> None:
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
            if msg.content["action"] != "update":
                return
            updated = False
            for dev in msg.content["config"]:
                dev_config = msg.content["config"][dev]
                device = self.device_manager.devices[dev]
                if "deviceConfig" in dev_config:
                    # store old config
                    old_config = device.config["deviceConfig"].copy()

                    # apply config
                    try:
                        self.device_manager.update_config(device.obj, dev_config["deviceConfig"])
                    except Exception as exc:
                        self.device_manager.update_config(device.obj, old_config)
                        raise DeviceConfigError(f"Error during object update. {exc}") from exc

                    device.config["deviceConfig"].update(dev_config["deviceConfig"])

                    # update config in DB
                    self.update_device_config_in_db(device_name=dev)
                    updated = True

                if "enabled" in dev_config:
                    device.config["enabled"] = dev_config["enabled"]
                    # update device enabled status in DB
                    self.update_device_enabled_in_db(device_name=dev)
                    updated = True
                if "enabled_set" in dev_config:
                    device.config["enabled_set"] = dev_config["enabled_set"]
                    # update device enabled status in DB
                    self.update_device_enabled_set_in_db(device_name=dev)
                    updated = True

            # send updates to services
            if updated:
                self.send_config(msg)

        except DeviceConfigError as dev_conf_error:
            self.device_manager.send_config_request_rejection(dev_conf_error)

    def update_device_enabled_in_db(self, device_name: str) -> None:
        """Update a device enabled setting in the DB with the local version

        Args:
            device_name (str): Name of the device that should be updated

        Raises:
            DeviceConfigError: Raised if the db update fails.
        """
        logger.debug("updating in DB")
        success = self.device_manager.scibec.patch_device_config(
            self.device_manager.devices[device_name].config["id"],
            {"enabled": self.device_manager.devices[device_name].enabled},
        )
        if not success:
            raise DeviceConfigError("Error during database update.")

    def update_device_enabled_set_in_db(self, device_name: str) -> None:
        """Update a device enabled setting in the DB with the local version

        Args:
            device_name (str): Name of the device that should be updated

        Raises:
            DeviceConfigError: Raised if the db update fails.
        """
        logger.debug("updating in DB")
        success = self.device_manager.scibec.patch_device_config(
            self.device_manager.devices[device_name].config["id"],
            {"enabled_set": self.device_manager.devices[device_name].enabled_set},
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
        success = self.device_manager.scibec.patch_device_config(
            self.device_manager.devices[device_name].config["id"],
            {"deviceConfig": self.device_manager.devices[device_name].config["deviceConfig"]},
        )
        if not success:
            raise DeviceConfigError("Error during database update.")
