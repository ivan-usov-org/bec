import os

from bluekafka_utils import (
    DeviceManagerBase,
    KafkaMessage,
    MessageEndpoints,
    RedisConnector,
)
from bluekafka_utils.connector import ConnectorBase

from file_writer.file_writer import NeXusFileWriter


class ScanStorage:
    def __init__(self, scan_number: str, scanID: str) -> None:
        self.scan_number = scan_number
        self.scanID = scanID
        self.scan_segments = dict()
        self.scan_finished = False
        self.num_points = None

    def append(self, pointID, data):
        self.scan_segments[pointID] = data

    def ready_to_write(self) -> bool:
        return self.scan_finished and (self.num_points + 1 == len(self.scan_segments))


class FileWriterManager:
    def __init__(self, bootstrap, Connector: ConnectorBase, scibec_url: str) -> None:
        self.connector = Connector(bootstrap)
        self.DM = DeviceManagerBase(self.connector, scibec_url)
        self.DM.initialize(bootstrap)
        self.producer = self.connector.producer()
        self._start_scan_segment_consumer()
        self._start_scan_status_consumer()
        self.scan_storage = dict()
        self.base_path = "./"  # should be configured
        self.file_writer = NeXusFileWriter()

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
        msg = KafkaMessage.ScanMessage.loads(msg.value)
        parent.insert_to_scan_storage(msg)

    @staticmethod
    def _scan_status_callback(msg, *, parent):
        msg = KafkaMessage.ScanStatusMessage.loads(msg.value)
        parent.update_scan_storage_with_status(msg)

    def update_scan_storage_with_status(self, msg: KafkaMessage.ScanStatusMessage):
        scanID = msg.content.get("scanID")
        if not self.scan_storage.get(scanID):
            self.scan_storage[scanID] = ScanStorage(
                scan_number=msg.content["info"].get("scan_number"), scanID=scanID
            )
        if msg.content.get("status") == "closed":
            self.scan_storage[scanID].scan_finished = True
            self.scan_storage[scanID].num_points = msg.content["info"]["points"]
            self.check_storage_status(scanID=scanID)

    def insert_to_scan_storage(self, msg: KafkaMessage.ScanMessage) -> None:
        scanID = msg.content.get("scanID")
        if scanID is not None:
            if not self.scan_storage.get(scanID):
                self.scan_storage[scanID] = ScanStorage(
                    scan_number=msg.metadata.get("scan_number"), scanID=scanID
                )
            self.scan_storage[scanID].append(
                pointID=msg.content.get("point_id"), data=msg.content.get("data")
            )
            print(msg.content.get("point_id"))
            self.check_storage_status(scanID=scanID)

    def check_storage_status(self, scanID: str):
        if self.scan_storage[scanID].ready_to_write():
            self.write_file(scanID)

    def write_file(self, scanID: str):
        storage = self.scan_storage[scanID]
        file_path = os.path.join(self.base_path, f"S{storage.scan_number:05d}.h5")
        self.file_writer.write(file_path=file_path, data=storage)
        self.scan_storage.pop(scanID)

    def shutdown(self):
        self.DM.shutdown()
