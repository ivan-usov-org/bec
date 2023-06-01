import os

import pytest
import yaml

import bec_client_lib.core
from bec_client_lib.core import DeviceManagerBase, ServiceConfig
from bec_client_lib.core.tests.utils import ConnectorMock, create_session_from_config
from file_writer import FileWriterManager

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_client_lib.core.__file__)


def load_FileWriter():
    connector = ConnectorMock("")
    device_manager = DeviceManagerBase(connector, "")
    device_manager.producer = connector.producer()
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    return FileWriterManagerMock(device_manager, connector)


class FileWriterManagerMock(FileWriterManager):
    def __init__(self, device_manager, connector) -> None:
        self.device_manager = device_manager
        config = ServiceConfig(
            redis={"host": "dummy", "port": 6379},
            config={"file_writer": {"plugin": "default_NeXus_format", "base_path": "./"}},
        )
        super().__init__(config=config, connector_cls=ConnectorMock)

    def _start_device_manager(self):
        pass

    def shutdown(self):
        pass


@pytest.mark.parametrize(
    "scan_number,bundle,lead,ref_path",
    [
        (10, 1000, None, "S0000-0999/S0010"),
        (2001, 1000, None, "S2000-2999/S2001"),
        (20, 50, 4, "S0000-0049/S0020"),
        (20, 50, 5, "S00000-00049/S00020"),
        (12000, 100, None, "S12000-12099/S12000"),
        (120, 100, None, "S100-199/S120"),
        (1200, 1000, 5, "S01000-01999/S01200"),
    ],
)
def test_get_scan_dir(scan_number, bundle, lead, ref_path):
    file_manager = load_FileWriter()
    dir_path = file_manager._get_scan_dir(
        scan_bundle=bundle, scan_number=scan_number, leading_zeros=lead
    )
    assert dir_path == ref_path
