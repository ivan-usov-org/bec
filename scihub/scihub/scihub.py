from bec_utils import BECService, ServiceConfig
from bec_utils.connector import ConnectorBase

from scihub.scibec import SciBecConnector


class SciHub(BECService):
    def __init__(self, config: ServiceConfig, connector_cls: ConnectorBase) -> None:
        super().__init__(config, connector_cls, unique_service=True)
        self.config = config
        self._start_scibec_connector()
        self.scibec_connector = None

    def _start_scibec_connector(self):
        self.scibec_connector = SciBecConnector(self, self.connector)
