from unittest import mock

from bec_lib import ServiceConfig
from bec_lib.client import BECClient

from data_processing.dap_server import DAPServer
from data_processing.dap_service import DAPServiceBase


def test_dap_server():
    config = ServiceConfig()
    server = DAPServer(
        config=config, connector_cls=mock.MagicMock(), provided_services=DAPServiceBase, forced=True
    )
    assert server._service_id == "DAPServiceBase"
