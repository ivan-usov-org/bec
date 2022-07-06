from __future__ import annotations

from bec_utils import BECMessage, BECService, MessageEndpoints, bec_logger
from bec_utils.connector import ConnectorBase

from .bkqueue import QueueManager
from .devicemanager import DeviceManagerScanServer
from .scan_assembler import ScanAssembler
from .scan_guard import ScanGuard
from .scan_manager import ScanManager
from .scan_worker import ScanWorker

logger = bec_logger.logger


class ScanServer(BECService):
    device_manager = None
    queue_manager = None
    scan_guard = None
    scan_server = None
    scan_assembler = None
    scan_manager = None

    def __init__(self, bootstrap_server: list, connector_cls: ConnectorBase, scibec_url: str):
        super().__init__(bootstrap_server, connector_cls)
        self.scan_number = 0
        self.scibec_url = scibec_url
        self.producer = self.connector.producer()
        self._start_scan_manager()
        self._start_queue_manager()
        self._start_device_manager()
        self._start_scan_guard()
        self._start_scan_assembler()
        self._start_scan_server()
        self._start_alarm_handler()

    def _start_device_manager(self):
        self.device_manager = DeviceManagerScanServer(self.connector, self.scibec_url)
        self.device_manager.initialize([self.bootstrap_server])

    def _start_scan_server(self):
        self.scan_worker = ScanWorker(parent=self)
        self.scan_worker.start()

    def _start_scan_manager(self):
        self.scan_manager = ScanManager(parent=self)

    def _start_queue_manager(self):
        self.queue_manager = QueueManager(parent=self)

    def _start_scan_assembler(self):
        self.scan_assembler = ScanAssembler(parent=self)

    def _start_scan_guard(self):
        self.scan_guard = ScanGuard(parent=self)

    def _start_alarm_handler(self):
        self._alarm_consumer = self.connector.consumer(
            MessageEndpoints.alarm(),
            cb=self._alarm_callback,
            parent=self,
        )
        self._alarm_consumer.start()

    @staticmethod
    def _alarm_callback(msg, parent: ScanServer, **_kwargs):
        metadata = BECMessage.AlarmMessage.loads(msg.value).metadata
        scanID = metadata.get("scanID")
        queue = metadata.get("stream")
        if scanID and queue:
            parent.queue_manager.set_abort(scanID=scanID, queue=queue)

    def load_config_from_disk(self, file_path: str) -> None:
        """load a config file from disk"""
        self.device_manager.load_config_from_disk(file_path)

    def shutdown(self) -> None:
        """shutdown the scan server"""

        self.device_manager.shutdown()
        self.queue_manager.shutdown()
        self.scan_worker.shutdown()
