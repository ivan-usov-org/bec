import os
from pathlib import Path

import numpy as np
from bec_utils import (
    BECMessage,
    BECService,
    DeviceManagerBase,
    MessageEndpoints,
    bec_logger,
)
from bec_utils.connector import ConnectorBase

from .file_writer import NexusFileWriter

logger = bec_logger.logger


class ScanStorage:
    def __init__(self, scan_number: str, scanID: str) -> None:
        self.scan_number = scan_number
        self.scanID = scanID
        self.scan_segments = {}
        self.scan_finished = False
        self.num_points = None
        self.baseline = None
        self.metadata = {}

    def append(self, pointID, data):
        self.scan_segments[pointID] = data

    def ready_to_write(self) -> bool:
        return self.scan_finished and (self.num_points == len(self.scan_segments))


class FileWriterManager(BECService):
    def __init__(self, bootstrap_server, connector_cls: ConnectorBase, scibec_url: str) -> None:
        super().__init__(bootstrap_server, connector_cls, unique_service=True)
        self.scibec_url = scibec_url
        self.producer = self.connector.producer()
        self._start_device_manager()
        self._start_scan_segment_consumer()
        self._start_scan_status_consumer()
        self.scan_storage = {}
        self.base_path = "./"  # should be configured
        self.file_writer = NexusFileWriter()

    def _start_device_manager(self):
        self.device_manager = DeviceManagerBase(self.connector, self.scibec_url)
        self.device_manager.initialize([self.bootstrap_server])

    def _start_scan_segment_consumer(self):
        self._scan_segment_consumer = self.connector.consumer(
            pattern=MessageEndpoints.scan_segment(),
            cb=self._scan_segment_callback,
            parent=self,
        )
        self._scan_segment_consumer.start()

    def _start_scan_status_consumer(self):
        self._scan_status_consumer = self.connector.consumer(
            MessageEndpoints.scan_status(),
            cb=self._scan_status_callback,
            parent=self,
        )
        self._scan_status_consumer.start()

    @staticmethod
    def _scan_segment_callback(msg, *, parent):
        msgs = BECMessage.ScanMessage.loads(msg.value)
        for scan_msg in msgs:
            parent.insert_to_scan_storage(scan_msg)

    @staticmethod
    def _scan_status_callback(msg, *, parent):
        msg = BECMessage.ScanStatusMessage.loads(msg.value)
        parent.update_scan_storage_with_status(msg)

    def update_scan_storage_with_status(self, msg: BECMessage.ScanStatusMessage):
        scanID = msg.content.get("scanID")
        if not self.scan_storage.get(scanID):
            self.scan_storage[scanID] = ScanStorage(
                scan_number=msg.content["info"].get("scan_number"), scanID=scanID
            )
        metadata = msg.content.get("info").copy()
        metadata.pop("DIID", None)
        metadata.pop("stream", None)
        self.scan_storage[scanID].metadata.update(metadata)
        if msg.content.get("status") == "closed":
            self.scan_storage[scanID].scan_finished = True
            self.scan_storage[scanID].num_points = msg.content["info"]["num_points"]
            self.check_storage_status(scanID=scanID)

    def insert_to_scan_storage(self, msg: BECMessage.ScanMessage) -> None:
        scanID = msg.content.get("scanID")
        if scanID is not None:
            if not self.scan_storage.get(scanID):
                self.scan_storage[scanID] = ScanStorage(
                    scan_number=msg.metadata.get("scan_number"), scanID=scanID
                )
            self.scan_storage[scanID].append(
                pointID=msg.content.get("point_id"), data=msg.content.get("data")
            )
            logger.debug(msg.content.get("point_id"))
            self.check_storage_status(scanID=scanID)

    def update_baseline_reading(self, scanID: str) -> None:
        if not self.scan_storage.get(scanID):
            return
        if self.scan_storage[scanID].baseline:
            return
        msg = self.producer.get(MessageEndpoints.public_scan_baseline(scanID))
        baseline = BECMessage.ScanBaselineMessage.loads(msg)
        if not baseline:
            return
        self.scan_storage[scanID].baseline = baseline.content["data"]
        return

    def check_storage_status(self, scanID: str):
        self.update_baseline_reading(scanID)
        if self.scan_storage[scanID].ready_to_write():
            self.write_file(scanID)

    def write_file(self, scanID: str):
        storage = self.scan_storage[scanID]
        scan = storage.scan_number
        scan_bundle = 1000
        scan_dir = f"S{scan//scan_bundle:04d}-{scan//scan_bundle+scan_bundle-1:04d}/S{scan:04d}"
        data_dir = Path(os.path.join(self.base_path, "data", scan_dir))
        data_dir.mkdir(parents=True, exist_ok=True)
        file_path = os.path.abspath(os.path.join(data_dir, f"S{storage.scan_number:04d}.h5"))
        successful = True
        try:
            logger.info(f"Writing file {file_path}")
            self.file_writer.write(file_path=file_path, data=storage)
        except:
            successful = False
        self.scan_storage.pop(scanID)
        self.producer.set_and_publish(
            MessageEndpoints.public_file(scanID),
            BECMessage.FileMessage(file_path=file_path, successful=successful).dumps(),
        )
