import os
import contextlib
from unittest import mock

import numpy as np
import pytest
import yaml

import bec_lib
from bec_lib import DeviceManagerBase, MessageEndpoints, ServiceConfig, messages
from bec_lib.bec_errors import ServiceConfigError
from bec_lib.messages import BECStatus
from bec_lib.redis_connector import MessageObject
from bec_lib.tests.utils import ConnectorMock, create_session_from_config, get_device_info_mock
from file_writer import FileWriterManager
from file_writer.file_writer import FileWriter
from file_writer.file_writer_manager import ScanStorage

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_lib.__file__)


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

    # def shutdown(self):
    #  pass

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass


class DeviceManagerMock(DeviceManagerBase):
    def _get_device_info(self, device_name) -> messages.DeviceInfoMessage:
        return get_device_info_mock(device_name, self.get_device(device_name)["deviceClass"])

    def get_device(self, device_name):
        for dev in self._session["devices"]:
            if dev["name"] == device_name:
                return dev


def load_FileWriter():
    service_mock = mock.MagicMock()
    service_mock.connector = ConnectorMock("")
    device_manager = DeviceManagerMock(service_mock, "")
    device_manager.connector = service_mock.connector
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    return FileWriterManagerMock(device_manager, service_mock.connector)


@contextlib.contextmanager
def file_writer_manager_mock():
    writer = load_FileWriter()
    try:
        yield writer
    finally:
        writer.shutdown()


def test_scan_segment_callback():
    with file_writer_manager_mock() as file_manager:
        msg = messages.ScanMessage(
            point_id=1, scan_id="scan_id", data={"data": "data"}, metadata={"scan_number": 1}
        )
        msg_bundle = messages.BundleMessage()
        msg_bundle.append(msg)
        msg_raw = MessageObject(value=msg_bundle, topic="scan_segment")

        file_manager._scan_segment_callback(msg_raw, parent=file_manager)
        assert file_manager.scan_storage["scan_id"].scan_segments[1] == {"data": "data"}


def test_scan_status_callback():
    with file_writer_manager_mock() as file_manager:
        msg = messages.ScanStatusMessage(
            scan_id="scan_id",
            status="closed",
            info={
                "scan_number": 1,
                "DIID": "DIID",
                "stream": "stream",
                "scan_type": "step",
                "num_points": 1,
                "enforce_sync": True,
            },
        )
        msg_raw = MessageObject(value=msg, topic="scan_status")

        file_manager._scan_status_callback(msg_raw, parent=file_manager)
        assert file_manager.scan_storage["scan_id"].scan_finished is True


class MockWriter(FileWriter):
    def __init__(self, file_writer_manager):
        super().__init__(file_writer_manager)
        self.write_called = False

    def write(self, file_path: str, data):
        self.write_called = True


def test_write_file():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        with mock.patch.object(
            file_manager.writer_mixin, "compile_full_filename"
        ) as mock_create_file_path:
            mock_create_file_path.return_value = "path"
            # replace NexusFileWriter with MockWriter
            file_manager.file_writer = MockWriter(file_manager)
            file_manager.write_file("scan_id")
            assert file_manager.file_writer.write_called is True


def test_write_file_invalid_scan_id():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        with mock.patch.object(
            file_manager.writer_mixin, "compile_full_filename"
        ) as mock_create_file_path:
            file_manager.write_file("scan_id1")
            mock_create_file_path.assert_not_called()


def test_write_file_invalid_scan_number():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        file_manager.scan_storage["scan_id"].scan_number = None
        with mock.patch.object(
            file_manager.writer_mixin, "compile_full_filename"
        ) as mock_create_file_path:
            file_manager.write_file("scan_id")
            mock_create_file_path.assert_not_called()


def test_create_file_path():
    with file_writer_manager_mock() as file_manager:
        file_manager.file_writer_config["base_path"] = "./"
        file_path = file_manager.writer_mixin.compile_full_filename(
            10, "master.h5", create_dir=False
        )
        assert file_path == os.path.abspath("./data/S00000-00999/S00010/S00010_master.h5")


def test_write_file_raises_alarm_on_error():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        with mock.patch.object(
            file_manager.writer_mixin, "compile_full_filename"
        ) as mock_compile_filename:
            with mock.patch.object(file_manager, "connector") as mock_connector:
                mock_compile_filename.return_value = "path"
                # replace NexusFileWriter with MockWriter
                file_manager.file_writer = MockWriter(file_manager)
                file_manager.file_writer.write = mock.Mock(side_effect=Exception("error"))
                file_manager.write_file("scan_id")
                mock_connector.raise_alarm.assert_called_once()


def test_update_baseline_reading():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        with mock.patch.object(file_manager, "connector") as mock_connector:
            mock_connector.get.return_value = messages.ScanBaselineMessage(
                scan_id="scan_id", data={"data": "data"}
            )
            file_manager.update_baseline_reading("scan_id")
            assert file_manager.scan_storage["scan_id"].baseline == {"data": "data"}
            mock_connector.get.assert_called_once_with(
                MessageEndpoints.public_scan_baseline("scan_id")
            )


def test_scan_storage_append():
    storage = ScanStorage(10, "scan_id")
    storage.append(1, {"data": "data"})
    assert storage.scan_segments[1] == {"data": "data"}
    assert storage.scan_finished is False


def test_scan_storage_ready_to_write():
    storage = ScanStorage(10, "scan_id")
    storage.num_points = 1
    storage.scan_finished = True
    storage.append(1, {"data": "data"})
    assert storage.ready_to_write() is True


def test_update_file_references():
    with file_writer_manager_mock() as file_manager:
        with mock.patch.object(file_manager, "connector") as mock_connector:
            file_manager.update_file_references("scan_id")
            mock_connector.keys.assert_not_called()


def test_update_file_references_gets_keys():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        with mock.patch.object(file_manager, "connector") as mock_connector:
            file_manager.update_file_references("scan_id")
            mock_connector.keys.assert_called_once_with(
                MessageEndpoints.public_file("scan_id", "*")
            )


def test_update_async_data():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        with mock.patch.object(file_manager, "connector") as mock_connector:
            with mock.patch.object(file_manager, "_process_async_data") as mock_process:
                key = MessageEndpoints.device_async_readback("scan_id", "dev1").endpoint
                mock_connector.keys.return_value = [key.encode()]
                data = [(b"0-0", b'{"data": "data"}')]
                mock_connector.xrange.return_value = data
                file_manager.update_async_data("scan_id")
                mock_connector.xrange.assert_called_once_with(key, min="-", max="+")
                mock_process.assert_called_once_with(data, "scan_id", "dev1")


def test_process_async_data_single_entry():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        data = [{"data": messages.DeviceMessage(signals={"data": np.zeros((10, 10))})}]
        file_manager._process_async_data(data, "scan_id", "dev1")
        assert np.isclose(
            file_manager.scan_storage["scan_id"].async_data["dev1"]["data"], np.zeros((10, 10))
        ).all()


def test_process_async_data_extend():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        data = [
            {
                "data": messages.DeviceMessage(
                    signals={"data": {"value": np.zeros((10, 10))}},
                    metadata={"async_update": "extend"},
                )
            }
            for ii in range(10)
        ]
        file_manager._process_async_data(data, "scan_id", "dev1")
        assert file_manager.scan_storage["scan_id"].async_data["dev1"]["data"]["value"].shape == (
            100,
            10,
        )


def test_process_async_data_append():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        data = [
            {
                "data": messages.DeviceMessage(
                    signals={"data": {"value": np.zeros((10, 10))}},
                    metadata={"async_update": "append"},
                )
            }
            for ii in range(10)
        ]
        file_manager._process_async_data(data, "scan_id", "dev1")
        assert len(file_manager.scan_storage["scan_id"].async_data["dev1"]["data"]) == 10


def test_process_async_data_replace():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        data = [
            {
                "data": messages.DeviceMessage(
                    signals={"data": {"value": np.zeros((10, 10))}},
                    metadata={"async_update": "replace"},
                )
            }
            for ii in range(10)
        ]
        file_manager._process_async_data(data, "scan_id", "dev1")
        assert file_manager.scan_storage["scan_id"].async_data["dev1"]["data"]["value"].shape == (
            10,
            10,
        )


def test_update_scan_storage_with_status_ignores_none():
    with file_writer_manager_mock() as file_manager:
        file_manager.update_scan_storage_with_status(
            messages.ScanStatusMessage(scan_id=None, status="closed", info={})
        )
        assert file_manager.scan_storage == {}


def test_ready_to_write():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        file_manager.scan_storage["scan_id"].scan_finished = True
        file_manager.scan_storage["scan_id"].num_points = 1
        file_manager.scan_storage["scan_id"].scan_segments = {"0": {"data": np.zeros((10, 10))}}
        assert file_manager.scan_storage["scan_id"].ready_to_write() is True
        file_manager.scan_storage["scan_id1"] = ScanStorage(101, "scan_id1")
        file_manager.scan_storage["scan_id1"].scan_finished = True
        file_manager.scan_storage["scan_id1"].num_points = 2
        file_manager.scan_storage["scan_id1"].scan_segments = {"0": {"data": np.zeros((10, 10))}}
        assert file_manager.scan_storage["scan_id1"].ready_to_write() is False


def test_ready_to_write_forced():
    with file_writer_manager_mock() as file_manager:
        file_manager.scan_storage["scan_id"] = ScanStorage(10, "scan_id")
        file_manager.scan_storage["scan_id"].scan_finished = False
        file_manager.scan_storage["scan_id"].forced_finish = True
        assert file_manager.scan_storage["scan_id"].ready_to_write() is True
