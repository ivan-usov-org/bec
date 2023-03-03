from unittest import mock

import pytest
from bec_utils import DeviceManagerBase, ServiceConfig
from bec_utils.tests.utils import ConnectorMock

from scihub import SciHub
from scihub.scibec import SciBecConnector


@pytest.fixture()
def SciHubMock():
    config = ServiceConfig(
        redis={"host": "dummy", "port": 6379},
        scibec={"host": "http://localhost", "port": 3030, "beamline": "TestBeamline"},
        config={"file_writer": {"plugin": "default_NeXus_format", "base_path": "./"}},
    )
    return SciHub(config, ConnectorMock)


def test_scibec_connector(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)


def test_get_current_session(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    with mock.patch.object(scibec_connector.scibec, "get_session_by_id") as scibec_get_session:
        scibec_connector.get_current_session()
        scibec_get_session.assert_called_once()
