from bec_lib import BECService, RedisConnector
from bec_lib.service_config import ServiceConfig

from .worker_manager import DAPWorkerManager


class DAPServer(BECService):
    """Data processing server class."""

    def __init__(
        self, config: ServiceConfig, connector: RedisConnector, unique_service=False
    ) -> None:
        super().__init__(config, connector, unique_service)
        self._work_manager = None
        self._start_manager()

    def _start_manager(self):
        self._work_manager = DAPWorkerManager(self.connector)

    def shutdown(self):
        self._work_manager.shutdown()
        super().shutdown()
