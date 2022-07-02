from __future__ import annotations

import inspect

import msgpack
from bec_utils import BECMessage, BECService, MessageEndpoints, bec_logger
from bec_utils.connector import ConnectorBase

import scan_server.scans as ScanServerScans

from .bkqueue import QueueManager
from .devicemanager import DeviceManagerScanServer
from .scan_assembler import ScanAssembler
from .scan_guard import ScanGuard
from .scan_worker import ScanWorker

logger = bec_logger.logger


class ScanServer(BECService):
    dm = None
    scan_guard = None
    scan_server = None
    scan_assembler = None

    def __init__(self, bootstrap_server: list, connector_cls: ConnectorBase, scibec_url: str):
        super().__init__(bootstrap_server, connector_cls)
        self.scan_number = 0
        self.scan_dict = {}
        self.scibec_url = scibec_url
        self.producer = self.connector.producer()
        self._update_available_scans()
        self._start_queue_manager()
        self._start_devicemanager()
        self._start_scan_guard()
        self._start_scan_assembler()
        self._start_scan_server()
        self._publish_available_scans()
        self._start_alarm_handler()

    def _start_devicemanager(self):
        self.dm = DeviceManagerScanServer(self.connector, self.scibec_url)
        self.dm.initialize([self.bootstrap_server])

    def _start_scan_server(self):
        self.scan_worker = ScanWorker(parent=self)
        self.scan_worker.start()

    def _start_queue_manager(self):
        self.qm = QueueManager(parent=self)

    def _start_scan_assembler(self):
        self.scan_assembler = ScanAssembler(parent=self)

    def _start_scan_guard(self):
        self.scan_guard = ScanGuard(parent=self)

    def _update_available_scans(self):
        for name, val in inspect.getmembers(ScanServerScans):
            try:
                if issubclass(val, ScanServerScans.RequestBase):
                    if val.scan_name == "":
                        logger.debug(f"Ignoring {name}")
                    self.scan_dict[val.scan_name] = {
                        "class": val.__name__,
                        "arg_input": val.arg_input,
                        "required_kwargs": val.required_kwargs,
                        "scan_report_hint": val.scan_report_hint,
                    }
                    doc = None
                    if val.__doc__ is not None:
                        doc = val.__doc__
                    elif val.__init__ is not None:
                        doc = val.__init__.__doc__
                    self.scan_dict[val.scan_name]["doc"] = doc
            except TypeError:
                logger.debug(f"Ignoring {name}")

    def _publish_available_scans(self):
        self.producer.set(MessageEndpoints.available_scans(), msgpack.dumps(self.scan_dict))

    def _start_alarm_handler(self):
        self._alarm_consumer = self.connector.consumer(
            MessageEndpoints.alarm(),
            cb=self._alarm_callback,
            parent=self,
        )
        self._alarm_consumer.start()

    @staticmethod
    def _alarm_callback(msg, parent: ScanServer, **_kwargs):
        msg = BECMessage.AlarmMessage.loads(msg.value)
        if "scanID" in msg.metadata:
            parent.qm._set_abort(scanID=msg.metadata["scanID"], queue=msg.metadata["stream"])

    def load_config_from_disk(self, file_path):
        self.dm.load_config_from_disk(file_path)

    def shutdown(self):
        self.dm.shutdown()
        self.qm.shutdown()
        self.scan_worker.signal_event.set()
        self.scan_worker.join()
