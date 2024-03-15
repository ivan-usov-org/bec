import os
import pytest
import yaml
from unittest import mock

import bec_lib
from bec_lib import bec_logger
from bec_lib import DeviceManagerBase, ServiceConfig, messages
from bec_lib.messages import BECStatus
from bec_lib.tests.utils import (
    ConnectorMock,
    create_session_from_config,
    get_device_info_mock,
)
from scan_bundler import ScanBundler


# overwrite threads_check fixture from bec_lib,
# to have it in autouse


@pytest.fixture(autouse=True)
def threads_check(threads_check):
    yield
    bec_logger.logger.remove()


class ScanBundlerDeviceManagerMock(DeviceManagerBase):
    def _get_device_info(self, device_name) -> messages.DeviceInfoMessage:
        return get_device_info_mock(device_name, self.get_device(device_name)["deviceClass"])

    def get_device(self, device_name):
        for dev in self._session["devices"]:
            if dev["name"] == device_name:
                return dev


class ScanBundlerMock(ScanBundler):
    def __init__(self, device_manager, connector_cls) -> None:
        super().__init__(
            ServiceConfig(redis={"host": "dummy", "port": 6379}), connector_cls=ConnectorMock
        )
        self.device_manager = device_manager

    def _start_device_manager(self):
        pass

    def _start_metrics_emitter(self):
        pass

    def _start_update_service_info(self):
        pass

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass


dir_path = os.path.dirname(bec_lib.__file__)


@pytest.fixture
def scan_bundler_mock():
    service_mock = mock.MagicMock()
    service_mock.connector = ConnectorMock("")
    device_manager = ScanBundlerDeviceManagerMock(service_mock, "")
    device_manager.connector = service_mock.connector
    with open(f"{dir_path}/tests/test_config.yaml", "r") as session_file:
        device_manager._session = create_session_from_config(yaml.safe_load(session_file))
    device_manager._load_session()
    scan_bundler_mock = ScanBundlerMock(device_manager, service_mock.connector)
    yield scan_bundler_mock
    scan_bundler_mock.shutdown()
