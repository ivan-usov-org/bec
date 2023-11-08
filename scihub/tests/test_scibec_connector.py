from unittest import mock

import pytest

from bec_lib.core import DeviceManagerBase, ServiceConfig
from bec_lib.core.tests.utils import ConnectorMock
from scihub import SciHub
from scihub.scibec import SciBecConnector


class SciHubMocked(SciHub):
    def _start_metrics_emitter(self):
        pass


@pytest.fixture()
def SciHubMock():
    config = ServiceConfig(
        redis={"host": "dummy", "port": 6379},
        scibec={"host": "http://wrong_localhost", "port": 3030, "beamline": "TestBeamline"},
        config={"file_writer": {"plugin": "default_NeXus_format", "base_path": "./"}},
    )
    scihub_mocked = SciHubMocked(config, ConnectorMock)
    yield scihub_mocked
    scihub_mocked.shutdown()


def test_scibec_connector(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)


def test_get_current_session_with_SciBec(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    scibec_connector.scibec_info["beamline"] = {"activeExperiment": "12345"}
    with mock.patch.object(scibec_connector, "scibec") as scibec:
        scibec_connector.get_current_session()
        scibec.get_experiment_by_id.assert_called_once()
        scibec.get_session_by_id.assert_called_once()


def test_get_current_session_without_SciBec(SciHubMock):
    scibec_connector = SciBecConnector(SciHubMock, SciHubMock.connector)
    scibec_connector.scibec_info["beamline"] = {"activeSession": "12345"}
    assert scibec_connector.get_current_session() is None
