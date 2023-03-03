from bec_utils import BECMessage, MessageEndpoints, ServiceConfig, bec_logger
from bec_utils.connector import ConnectorBase

from .scibec.config_handler import ConfigHandler

logger = bec_logger.logger


class SciBecConnector:
    def __init__(self, config: ServiceConfig, connector: ConnectorBase) -> None:
        self.config = config
        self.connector = connector
        self.producer = connector.producer()
        self.config_handler = ConfigHandler(config, connector)

        self._config_request_handler = None
        self._start_config_request_handler()

    def _start_config_request_handler(self) -> None:
        self._config_request_handler = self.connector.consumer(
            MessageEndpoints.device_config_request(),
            cb=self._device_config_request_callback,
            parent=self,
        )
        self._config_request_handler.start()

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received request: {msg}")
        parent.config_handler.parse_config_request(msg)
