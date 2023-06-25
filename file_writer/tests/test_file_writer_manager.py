import os
from unittest import mock

import bec_client_lib.core
import pytest
import yaml
from bec_client_lib.core import (
    BECMessage,
    DeviceManagerBase,
    MessageEndpoints,
    ServiceConfig,
)
from bec_client_lib.core.bec_errors import ServiceConfigError
from bec_client_lib.core.redis_connector import MessageObject
from bec_client_lib.core.tests.utils import ConnectorMock, create_session_from_config

from file_writer import FileWriterManager
from file_writer.file_writer import FileWriter
from file_writer.file_writer_manager import ScanStorage

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


def test_scan_segment_callback():
    file_manager = load_FileWriter()
    msg = BECMessage.ScanMessage(
        point_id=1, scanID="scanID", data={"data": "data"}, metadata={"scan_number": 1}
    )
    msg_bundle = BECMessage.BundleMessage()
    msg_bundle.append(msg.dumps())
    msg_raw = MessageObject(value=msg_bundle.dumps(), topic="scan_segment")

    file_manager._scan_segment_callback(msg_raw, parent=file_manager)
    assert file_manager.scan_storage["scanID"].scan_segments[1] == {"data": "data"}


def test_scan_status_callback():
    file_manager = load_FileWriter()
    msg = BECMessage.ScanStatusMessage(
        scanID="scanID",
        status="closed",
        info={"scan_number": 1, "DIID": "DIID", "stream": "stream", "num_points": 1},
    )
    msg_raw = MessageObject(value=msg.dumps(), topic="scan_status")

    file_manager._scan_status_callback(msg_raw, parent=file_manager)
    assert file_manager.scan_storage["scanID"].scan_finished is True


def test_get_base_path():
    file_manager = load_FileWriter()
    assert file_manager._get_base_path() == os.path.expanduser("./")


def test_get_base_path_no_base_path():
    file_manager = load_FileWriter()
    file_manager.file_writer_config.pop("base_path")
    with pytest.raises(ServiceConfigError):
        file_manager._get_base_path()


def test_get_base_path_no_file_writer_config():
    file_manager = load_FileWriter()
    file_manager.file_writer_config = None
    with pytest.raises(ServiceConfigError):
        file_manager._get_base_path()


class MockWriter(FileWriter):
    def __init__(self, file_writer_manager):
        super().__init__(file_writer_manager)
        self.write_called = False

    def write(self, file_path: str, data):
        self.write_called = True


def test_write_file():
    file_manager = load_FileWriter()
    file_manager.scan_storage["scanID"] = ScanStorage(10, "scanID")
    with mock.patch.object(file_manager, "_create_file_path") as mock_create_file_path:
        mock_create_file_path.return_value = "path"
        # replace NexusFileWriter with MockWriter
        file_manager.file_writer = MockWriter(file_manager)
        file_manager.write_file("scanID")
        assert file_manager.file_writer.write_called is True


def test_create_file_path():
    file_manager = load_FileWriter()
    file_manager.file_writer_config["base_path"] = "./"
    # mock Path to avoid creating directories
    with mock.patch("file_writer.file_writer_manager.Path") as mock_path:
        with mock.patch("file_writer.file_writer_manager.os") as mock_os:
            mock_os.path.abspath.return_value = os.path.abspath("./bec/data/scan_dir/S00010.h5")
            mock_path.return_value = mock_path
            mock_path.join.return_value = os.path.abspath("./bec/data/scan_dir/S00010.h5")
            file_path = file_manager._create_file_path("scan_dir", 10)
            assert file_path == os.path.abspath("./bec/data/scan_dir/S00010.h5")


def test_write_file_raises_alarm_on_error():
    file_manager = load_FileWriter()
    file_manager.scan_storage["scanID"] = ScanStorage(10, "scanID")
    with mock.patch.object(file_manager, "_create_file_path") as mock_create_file_path:
        with mock.patch.object(file_manager, "connector") as mock_connector:
            mock_create_file_path.return_value = "path"
            # replace NexusFileWriter with MockWriter
            file_manager.file_writer = MockWriter(file_manager)
            file_manager.file_writer.write = mock.Mock(side_effect=Exception("error"))
            file_manager.write_file("scanID")
            mock_connector.raise_alarm.assert_called_once()


def test_update_baseline_reading():
    file_manager = load_FileWriter()
    file_manager.scan_storage["scanID"] = ScanStorage(10, "scanID")
    with mock.patch.object(file_manager, "producer") as mock_producer:
        mock_producer.get.return_value = BECMessage.ScanBaselineMessage(
            scanID="scanID", data={"data": "data"}
        ).dumps()
        file_manager.update_baseline_reading("scanID")
        assert file_manager.scan_storage["scanID"].baseline == {"data": "data"}
        mock_producer.get.assert_called_once_with(MessageEndpoints.public_scan_baseline("scanID"))


def test_scan_storage_append():
    storage = ScanStorage(10, "scanID")
    storage.append(1, {"data": "data"})
    assert storage.scan_segments[1] == {"data": "data"}
    assert storage.scan_finished is False


def test_scan_storage_ready_to_write():
    storage = ScanStorage(10, "scanID")
    storage.num_points = 1
    storage.scan_finished = True
    storage.append(1, {"data": "data"})
    assert storage.ready_to_write() is True
