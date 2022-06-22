from bec_utils.connector import ConnectorBase
from koss.koss import KOSS
from koss.scan_assembler import ScanAssembler
from koss.scan_worker import InstructionQueueStatus


def dummy_devices(enabled):
    devices = {"samx": {}}
    devices["samx"]["status"] = {}
    devices["samx"]["status"]["enabled"] = True
    devices["samx"]["type"] = "SynAxis"
    devices["samx"]["config"] = {}
    devices["samx"]["config"]["name"] = "motor"
    devices["samx"]["config"]["labels"] = "samx"
    devices["samx"]["config"]["delay"] = 5
    devices["samy"] = {}
    devices["samy"]["status"] = {}
    devices["samy"]["status"]["enabled"] = enabled
    devices["samy"]["type"] = "SynAxis"
    devices["samy"]["config"] = {}
    devices["samy"]["config"]["name"] = "motor"
    devices["samy"]["config"]["labels"] = "samy"
    return devices


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    message_sent = {}

    def set(self, topic, msg):
        pass

    def send(self, queue, msg):
        self.message_sent = {"queue": queue, "msg": msg}


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


class KossMock(KOSS):
    def __init__(self, dm, connector) -> None:
        self.dm = dm
        super().__init__(bootstrap_server="dummy", connector_cls=ConnectorMock, scibec_url="dummy")
        self.scan_worker = WorkerMock()

    def _start_devicemanager(self):
        pass

    def _start_scan_server(self):
        pass

    def shutdown(self):
        pass
