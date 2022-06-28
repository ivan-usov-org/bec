from bec_utils import Device, DeviceManagerBase
from bec_utils.connector import ConnectorBase


class DeviceManagerKOSS(DeviceManagerBase):
    def __init__(self, connector: ConnectorBase, scibec_url: str):
        super().__init__(connector, scibec_url=scibec_url)
        self._device_groups = {}

    def _update_config(self, config) -> None:
        pass
