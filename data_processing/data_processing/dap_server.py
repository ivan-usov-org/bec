from bec_lib import BECClient, bec_logger
from bec_lib.connector import ConnectorBase
from bec_lib.service_config import ServiceConfig

from .dap_service_manager import DAPServiceManager
from .worker_manager import DAPWorkerManager

logger = bec_logger.logger


class DAPServer(BECClient):
    """Data processing server class."""

    def __init__(self) -> None:
        super().__init__()
        # self._work_manager = None
        self._dap_server = None
        # self._start_manager()

    # def _start_manager(self):
    #     self._work_manager = DAPWorkerManager(self.connector)

    def start(self):
        super().start()
        self._start_dap_serivce()
        bec_logger.level = bec_logger.LOGLEVEL.INFO
        return

    def _start_dap_serivce(self):
        self._dap_server = DAPServiceManager()
        self._dap_server.start(self)

    def shutdown(self):
        # self._work_manager.shutdown()
        super().shutdown()
