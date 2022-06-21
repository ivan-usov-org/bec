import logging

from bec_utils import Device, DeviceManagerBase
from bec_utils.connector import ConnectorBase

logger = logging.getLogger(__name__)


class DeviceManagerSB(DeviceManagerBase):
    def __init__(self, connector: ConnectorBase, scibec_url: str):
        super().__init__(connector, scibec_url=scibec_url)
        self._config_request_connector = None
        self._device_instructions_connector = None

    def _load_config_device(self):
        if self._is_config_valid():
            for name, dev in self._config.items():
                logger.info(
                    f"Adding device {name}: {'ENABLED' if dev['status']['enabled'] else 'DISABLED'}"
                )
                obj = Device(name)
                obj.enabled = dev["status"]["enabled"]
                self.devices._add_device(name, obj)
