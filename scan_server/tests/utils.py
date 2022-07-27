import os

import yaml
from bec_utils.connector import ConnectorBase
from scan_server.devicemanager import DeviceManagerScanServer
from scan_server.scan_assembler import ScanAssembler
from scan_server.scan_server import ScanServer
from scan_server.scan_worker import InstructionQueueStatus

dir_path = os.path.dirname(os.path.realpath(__file__))


def load_ScanServerMock():
    connector = ConnectorMock("")
    device_manager = DeviceManagerScanServer(connector, "")
    device_manager.producer = connector.producer()
    with open(f"{dir_path}/test_session.yaml", "r") as f:
        device_manager._session = yaml.safe_load(f)
    device_manager._load_session()
    return ScanServerMock(device_manager, connector)


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    message_sent = {}

    def set(self, topic, msg):
        pass

    def send(self, queue, msg):
        self.message_sent = {"queue": queue, "msg": msg}

    def set_and_publish(self, topic, msg):
        pass

    def lpush(self, queue, msg):
        pass

    def rpush(self, queue, msg):
        pass

    def lrange(self, queue, start, stop):
        return []

    def get(self, queue):
        return None


class ConnectorMock(ConnectorBase):
    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock()


class WorkerMock:
    def __init__(self) -> None:
        self.scan_id = None
        self.scan_motors = []
        self.current_scanID = None
        self.current_scan_info = None
        self.status = InstructionQueueStatus.IDLE


class ScanServerMock(ScanServer):
    def __init__(self, device_manager, connector) -> None:
        self.device_manager = device_manager
        super().__init__(bootstrap_server="dummy", connector_cls=ConnectorMock, scibec_url="dummy")
        self.scan_worker = WorkerMock()

    def _start_device_manager(self):
        pass

    def _start_scan_server(self):
        pass

    def shutdown(self):
        pass
