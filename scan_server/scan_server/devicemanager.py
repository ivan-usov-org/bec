from bec_utils import DeviceManagerBase
from bec_utils.connector import ConnectorBase


class DeviceManagerScanServer(DeviceManagerBase):
    def __init__(self, connector: ConnectorBase, scibec_url: str):
        super().__init__(connector, scibec_url=scibec_url)
        self._device_groups = {}

    def _update_config(self, config) -> None:
        pass

    # def _load_config_device(self):
    #     if self._is_config_valid():
    #         for name, dev in self._config.items():
    #             obj = Device(name)
    #             obj.enabled = dev["status"]["enabled"]
    #             self.devices._add_device(name, obj)
