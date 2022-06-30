from __future__ import annotations

import inspect
import logging

import msgpack
from bec_utils import BECMessage, MessageEndpoints
from bec_utils.connector import ConnectorBase

import koss.scans as koss_scans

from .bkqueue import QueueManager
from .devicemanager import DeviceManager
from .scan_assembler import ScanAssembler
from .scan_guard import ScanGuard
from .scan_worker import ScanWorker

logger = logging.getLogger(__name__)


class KOSS:
    device_manager = None
    queue_manager = None
    scan_guard = None
    scan_server = None
    scan_assembler = None

    def __init__(self, bootstrap_server: list, connector_cls: ConnectorBase, scibec_url: str):
        self.bootstrap_server = bootstrap_server
        self.scan_number = 0
        self.scan_dict = {}
        self.connector = connector_cls(bootstrap_server)
        self.scibec_url = scibec_url
        self.producer = self.connector.producer()
        self._update_available_scans()
        self._start_queue_manager()
        self._start_device_manager()
        self._start_scan_guard()
        self._start_scan_assembler()
        self._start_scan_server()
        self._publish_available_scans()
        self._start_alarm_handler()

    def _start_device_manager(self):
        self.device_manager = DeviceManager(self.connector, self.scibec_url)
        self.device_manager.initialize([self.bootstrap_server])

    def _start_scan_server(self):
        self.scan_worker = ScanWorker(parent=self)
        self.scan_worker.start()

    def _start_queue_manager(self):
        self.queue_manager = QueueManager(parent=self)

    def _start_scan_assembler(self):
        self.scan_assembler = ScanAssembler(parent=self)

    def _start_scan_guard(self):
        self.scan_guard = ScanGuard(parent=self)

    def _update_available_scans(self):
        for name, val in inspect.getmembers(koss_scans):  # TODO: use vars() ?
            try:
                is_scan = issubclass(val, koss_scans.RequestBase)
            except TypeError:
                is_scan = False

            if not is_scan or not val.scan_name:
                logger.debug(f"Ignoring {name}")
                continue

            self.scan_dict[val.scan_name] = {
                "class": val.__name__,
                "arg_input": val.arg_input,
                "required_kwargs": val.required_kwargs,
                "scan_report_hint": val.scan_report_hint,
                "doc": val.__doc__ or val.__init__.__doc__,
            }

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
    def _alarm_callback(msg, parent: KOSS, **_kwargs):
        md = BECMessage.AlarmMessage.loads(msg.value).metadata
        scanID = md.get("scanID")
        queue = md.get("stream")
        if scanID and queue:
            parent.queue_manager._set_abort(scanID=scanID, queue=queue)

    def load_config_from_disk(self, file_path):
        self.device_manager.load_config_from_disk(file_path)

    def shutdown(self):
        self.device_manager.shutdown()
        self.queue_manager.shutdown()
        self.scan_worker.signal_event.set()  # TODO: this should be a shutdown method, too
        self.scan_worker.join()
