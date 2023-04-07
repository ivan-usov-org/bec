from bec_utils import BECService, ServiceConfig
from bec_utils.connector import ConnectorBase

from scihub.scibec import SciBecConnector
from scihub.scilog import SciLogConnector


class SciHub(BECService):
    def __init__(self, config: ServiceConfig, connector_cls: ConnectorBase) -> None:
        super().__init__(config, connector_cls, unique_service=True)
        self.config = config
        self.scibec_connector = None
        self.scilog_connector = None
        self._start_scibec_connector()
        self._start_scilog_connector()

    def _start_scibec_connector(self):
        self.scibec_connector = SciBecConnector(self, self.connector)

    def _start_scilog_connector(self):
        self.scibec_connector = SciLogConnector(self.connector)
