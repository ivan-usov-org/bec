import pytest

from bec_lib import ServiceConfig
from bec_lib.devicemanager import DeviceContainer
from bec_lib.logger import bec_logger
from bec_lib.messages import BECStatus
from bec_lib.tests.utils import ConnectorMock
from bec_server.scan_server.scan_server import ScanServer
from bec_server.scan_server.scan_worker import InstructionQueueStatus

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


@pytest.fixture
def scan_server_mock(dm_with_devices):
    server = ScanServerMock(dm_with_devices, dm_with_devices.connector)
    yield server
    bec_logger.logger.remove()


class WorkerMock:
    def __init__(self) -> None:
        self.scan_id = None
        self.scan_motors = []
        self.current_scan_id = None
        self.current_scan_info = None
        self.status = InstructionQueueStatus.IDLE
        self.current_instruction_queue_item = None


class ScanServerMock(ScanServer):
    def __init__(self, device_manager, connector) -> None:
        self.device_manager = device_manager
        super().__init__(
            ServiceConfig(redis={"host": "dummy", "port": 6379}), connector_cls=ConnectorMock
        )
        self.scan_worker = WorkerMock()

    def _start_metrics_emitter(self):
        pass

    def _start_update_service_info(self):
        pass

    def _start_device_manager(self):
        pass

    def shutdown(self):
        pass

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass

    @property
    def scan_number(self) -> int:
        """get the current scan number"""
        return 2

    @scan_number.setter
    def scan_number(self, val: int):
        pass

    @property
    def dataset_number(self) -> int:
        """get the current dataset number"""
        return 3

    @dataset_number.setter
    def dataset_number(self, val: int):
        pass


class DeviceMock:
    def __init__(self, name: str):
        self.name = name
        self.read_buffer = None
        self._config = {"deviceConfig": {"limits": [-50, 50]}, "userParameter": None}
        self._read_only = False
        self._enabled = True

    def read(self):
        return self.read_buffer

    def readback(self):
        return self.read_buffer

    @property
    def limits(self):
        return self._config["deviceConfig"]["limits"]

    @property
    def read_only(self) -> bool:
        return self._read_only

    @read_only.setter
    def read_only(self, val: bool):
        self._read_only = val

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, val: bool):
        self._enabled = val

    @property
    def user_parameter(self):
        return self._config["userParameter"]


class DMMock:
    devices = DeviceContainer()
    connector = ConnectorMock()

    def add_device(self, name):
        self.devices[name] = DeviceMock(name)
