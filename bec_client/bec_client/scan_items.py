from __future__ import annotations

import threading
import time
from collections import deque
from typing import TYPE_CHECKING, Optional

from bec_utils import BECMessage, bec_logger

if TYPE_CHECKING:
    from bec_client.scan_manager import ScanManager
    from queue_items import QueueItem
    from request_items import RequestItem

logger = bec_logger.logger


class ScanItem:
    status: dict

    def __init__(
        self,
        scan_manager: ScanManager,
        queueID: str,
        scan_number: list,
        scanID: list,
        status: str,
        **kwargs,
    ) -> None:
        self.scan_manager = scan_manager
        self._queueID = queueID
        self.scan_number = scan_number
        self.scanID = scanID
        self.status = status
        self.data = {}
        self.open_scan_defs = []
        self.num_points = None
        self.start_time = None
        self.end_time = None

    @property
    def queue(self):
        return self.scan_manager.queue_storage.find_queue_item_by_ID(self._queueID)

    def __eq__(self, other):
        return self.scanID == other.scanID


class ScanStorage:
    """stores scan items"""

    def __init__(self, scan_manager: ScanManager, maxlen=50, init_scan_number=0) -> None:
        self.scan_manager = scan_manager
        self.storage = deque(maxlen=maxlen)
        self.last_scan_number = init_scan_number
        self._lock = threading.Lock()

    @property
    def current_scan_info(self) -> dict:
        """get the current scan info from the scan queue"""
        scan_queue = self.scan_manager.queue_storage.current_scan_queue
        if not scan_queue:
            return None
        return scan_queue["primary"].get("info")[0]

    @property
    def current_scan(self) -> Optional(ScanItem):
        """get the current scan item"""
        if not self.current_scanID:
            return None
        return self.find_scan_by_ID(scanID=self.current_scanID[0])

    @property
    def current_scanID(self) -> Optional(str):
        """get the current scanID"""
        return self.current_scan_info.get("scanID") if self.current_scan_info is not None else None

    def find_scan_by_ID(self, scanID: str) -> Optional(ScanItem):
        """find a scan item based on its scanID"""
        for scan in self.storage:
            if scanID == scan.scanID:
                return scan
        return None

    def update_with_scan_status(self, scan_status: BECMessage.ScanStatusMessage) -> None:
        """update scan item in storage with a new ScanStatusMessage"""

        scanID = scan_status.content["scanID"]
        if not scanID:
            return

        scan_number = scan_status.content["info"].get("scan_number")
        if scan_number:
            self.last_scan_number = scan_number

        while True:
            scan_item = self.find_scan_by_ID(scanID=scan_status.content["scanID"])
            if not scan_item:
                time.sleep(0.1)
                continue

            # update timestamps
            if scan_status.content.get("status") == "open":
                scan_item.start_time = scan_status.content.get("timestamp")
            elif scan_status.content.get("status") == "closed":
                scan_item.end_time = scan_status.content.get("timestamp")

            # update status message
            scan_item.status = scan_status.content.get("status")

            # update total number of points
            if scan_status.content["info"].get("num_points"):
                scan_item.num_points = scan_status.content["info"].get("num_points")
            break

    def add_scan_segment(self, scan_msg: BECMessage.ScanMessage) -> None:
        """update a scan item with a new scan segment"""
        while True:
            for scan_item in self.storage:
                if scan_item.scanID == scan_msg.metadata["scanID"]:
                    scan_item.data[scan_msg.content["point_id"]] = scan_msg
                    return
            time.sleep(0.01)

    def add_scan_item(self, queueID: str, scan_number: list, scanID: list, status: str):
        """append new scan item to scan storage"""
        self.storage.append(ScanItem(self.scan_manager, queueID, scan_number, scanID, status))

    def update_with_queue_status(self, queue_msg: BECMessage.ScanQueueStatusMessage):
        """create new scan items based on their existence in the queue info"""
        queue_info = queue_msg.content["queue"]["primary"].get("info")
        with self._lock:
            for queue_item in queue_info:
                # append = True
                # for scan_obj in self.storage:
                #     if len(set(scan_obj.scanID) & set(queue_item["scanID"])) > 0:
                #         append = False
                if not any(queue_item["is_scan"]):
                    continue

                for ii, scan in enumerate(queue_item["scanID"]):
                    if self.find_scan_by_ID(scan):
                        continue

                    logger.debug(f"Appending new scan: {queue_item}")
                    self.add_scan_item(
                        queueID=queue_item["queueID"],
                        scan_number=queue_item["scan_number"][ii],
                        scanID=queue_item["scanID"][ii],
                        status=queue_item["status"],
                    )
