import pytest

from bec_lib.logger import bec_logger
from bec_lib.messages import BECStatus
from bec_lib.service_config import ServiceConfig
from bec_lib.tests.utils import ConnectorMock
from bec_server.scihub import SciHub

# overwrite threads_check fixture from bec_lib,
# to have it in autouse


@pytest.fixture(autouse=True)
def threads_check(threads_check):
    yield
    bec_logger.logger.remove()


class SciHubMocked(SciHub):
    def _start_metrics_emitter(self):
        pass

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass

    def _start_atlas_connector(self):
        pass

    def _start_scilog_connector(self):
        pass


@pytest.fixture()
def SciHubMock():
    config = ServiceConfig(
        redis={"host": "dummy", "port": 6379},
        service_config={
            "file_writer": {"plugin": "default_NeXus_format", "base_path": "./"},
            "log_writer": {"base_path": "./"},
        },
    )
    scihub_mocked = SciHubMocked(config, ConnectorMock)
    yield scihub_mocked
    scihub_mocked.shutdown()
