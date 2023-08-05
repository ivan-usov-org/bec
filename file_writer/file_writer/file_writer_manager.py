from __future__ import annotations

import threading
import traceback

from bec_lib.core import (
    BECMessage,
    BECService,
    DeviceManagerBase,
    MessageEndpoints,
    ServiceConfig,
    bec_logger,
    threadlocked,
)
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
        self.file_references = {}
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
        self._lock = threading.RLock()
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

    def update_scan_storage_with_status(self, msg: BECMessage.ScanStatusMessage) -> None:
        """
        Update the scan storage with the scan status.

        Args:
            msg (BECMessage.ScanStatusMessage): Scan status message
        """
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
        """
        Insert scan data to the scan storage.

        Args:
            msg (BECMessage.ScanMessage): Scan message
        """
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
        """
        Update the baseline reading for the scan.

        Args:
            scanID (str): Scan ID
        """
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

    def update_file_references(self, scanID: str) -> None:
        """
        Update the file references for the scan.
        All external files ought to be announced to the endpoint public_file before the scan finishes. This function
        retrieves the file references and adds them to the scan storage.

        Args:
            scanID (str): Scan ID
        """
        if not self.scan_storage.get(scanID):
            return
        msgs = self.producer.keys(MessageEndpoints.public_file(scanID, "*"))
        if not msgs:
            return

        # extract name from 'public/<scanID>/file/<name>:val'
        names = [msg.decode().split(":val")[0].split("/")[-1] for msg in msgs]
        file_msgs = [self.producer.get(msg.decode()) for msg in msgs]
        if not file_msgs:
            return
        for name, msg in zip(names, file_msgs):
            file_msg = BECMessage.FileMessage.loads(msg)
            self.scan_storage[scanID].file_references[name] = {
                "path": file_msg.content["file_path"],
                "done": file_msg.content["done"],
                "successful": file_msg.content["successful"],
                "metadata": file_msg.metadata,
            }
        return

    @threadlocked
    def check_storage_status(self, scanID: str) -> None:
        """
        Check if the scan storage is ready to be written to file and write it if it is.

        Args:
            scanID (str): Scan ID
        """
        if not self.scan_storage.get(scanID):
            return
        self.update_baseline_reading(scanID)
        self.update_file_references(scanID)
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
        self.producer.set_and_publish(
            MessageEndpoints.public_file(scanID, "master"),
            BECMessage.FileMessage(file_path=file_path, done=False).dumps(),
        )
        successful = True
        try:
            logger.info(f"Starting writing to file {file_path}.")
            self.file_writer.write(file_path=file_path, data=storage)
        # pylint: disable=broad-except
        # pylint: disable=unused-variable
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
            MessageEndpoints.public_file(scanID, "master"),
            BECMessage.FileMessage(file_path=file_path, successful=successful).dumps(),
        )
        if successful:
            logger.success(f"Finished writing file {file_path}.")
            return
