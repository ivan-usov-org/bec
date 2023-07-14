from __future__ import annotations

import os
import traceback
from pathlib import Path

from bec_lib.core import (
    BECMessage,
    BECService,
    DeviceManagerBase,
    MessageEndpoints,
    ServiceConfig,
    bec_logger,
)
from bec_lib.core.bec_errors import ServiceConfigError
from bec_lib.core.file_utils import FileWriterMixin
from bec_lib.core.redis_connector import Alarms, MessageObject, RedisConnector

from file_writer.file_writer import NexusFileWriter

logger = bec_logger.logger


class ScanStorage:
    def __init__(self, scan_number: int, scanID: str) -> None:
        """
        Helper class to store scan data until it is ready to be written to file.

        Args:
            scan_number (int): Scan number
            scanID (str): Scan ID
        """
        self.scan_number = scan_number
        self.scanID = scanID
        self.scan_segments = {}
        self.scan_finished = False
        self.num_points = None
        self.baseline = None
        self.metadata = {}
        self.start_time = None
        self.end_time = None

    def append(self, pointID, data):
        """
        Append data to the scan storage.

        Args:
            pointID (int): Point ID
            data (dict): Data to be stored
        """
        self.scan_segments[pointID] = data

    def ready_to_write(self) -> bool:
        """
        Check if the scan is ready to be written to file.
        """
        return self.scan_finished and (self.num_points == len(self.scan_segments))


class FileWriterManager(BECService):
    def __init__(self, config: ServiceConfig, connector_cls: RedisConnector) -> None:
        """
        Service to write scan data to file.

        Args:
            config (ServiceConfig): Service config
            connector_cls (RedisConnector): Connector class
        """
        super().__init__(config, connector_cls, unique_service=True)
        self.file_writer_config = self._service_config.service_config.get("file_writer")
        self.writer_mixin = FileWriterMixin(self.file_writer_config)
        self.producer = self.connector.producer()
        self._start_device_manager()
        self._start_scan_segment_consumer()
        self._start_scan_status_consumer()
        self.scan_storage = {}
        self.file_writer = NexusFileWriter(self)

    def _start_device_manager(self):
        self.device_manager = DeviceManagerBase(self.connector)
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
    def _scan_segment_callback(msg: MessageObject, *, parent: FileWriterManager):
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

        scan_storage = self.scan_storage[scanID]
        scan_storage.metadata.update(metadata)
        if msg.content.get("status") == "open" and not scan_storage.start_time:
            scan_storage.start_time = msg.content.get("timestamp")

        if msg.content.get("status") == "closed":
            if not scan_storage.end_time:
                scan_storage.end_time = msg.content.get("timestamp")
            scan_storage.scan_finished = True
            scan_storage.num_points = msg.content["info"]["num_points"]
            self.check_storage_status(scanID=scanID)

    def insert_to_scan_storage(self, msg: BECMessage.ScanMessage) -> None:
        scanID = msg.content.get("scanID")
        if scanID is None:
            return
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

    def write_file(self, scanID: str) -> None:
        """
        Write scan data to file.

        Args:
            scanID (str): Scan ID
        """
        storage = self.scan_storage[scanID]
        scan = storage.scan_number
        file_path = self.writer_mixin.compile_full_filename(scan, "master.h5")
        successful = True
        try:
            logger.info(f"Starting writing to file {file_path}.")
            self.file_writer.write(file_path=file_path, data=storage)
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(f"Failed to write to file {file_path}. Error: {content}")
            self.connector.raise_alarm(
                severity=Alarms.MINOR,
                alarm_type="FileWriterError",
                source="file_writer_manager",
                content=f"Failed to write to file {file_path}. Error: {content}",
                metadata=self.scan_storage[scanID].metadata,
            )
            successful = False
        self.scan_storage.pop(scanID)
        self.producer.set_and_publish(
            MessageEndpoints.public_file(scanID),
            BECMessage.FileMessage(file_path=file_path, successful=successful).dumps(),
        )
        if successful:
            logger.success(f"Finished writing file {file_path}.")
            return
