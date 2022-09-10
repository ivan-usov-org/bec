from __future__ import annotations

import threading
from collections import deque
from typing import TYPE_CHECKING, Deque, List, Optional

from bec_utils import BECMessage, MessageEndpoints, threadlocked

if TYPE_CHECKING:
    from request_items import RequestItem
    from scan_items import ScanItem
    from scan_manager import ScanManager


class QueueItem:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        scan_manager: ScanManager,
        queueID: str,
        request_blocks: list,
        status: str,
        active_request_block: dict,
        scanID: List(str),
        **_kwargs,
    ) -> None:
        self.scan_manager = scan_manager
        self.queueID = queueID
        self.request_blocks = request_blocks
        self.status = status
        self.active_request_block = active_request_block
        self._requests = [request_block["RID"] for request_block in self.request_blocks]
        self._scans = scanID

    @property
    def scans(self) -> List[ScanItem]:
        """get the scans items assigned to the current queue item"""
        return [self.scan_manager.scan_storage.find_scan_by_ID(scanID) for scanID in self._scans]

    @property
    def requests(self) -> List[RequestItem]:
        """get the request items assigned to the current queue item"""
        return [
            self.scan_manager.request_storage.find_request_by_ID(requestID)
            for requestID in self._requests
        ]

    @property
    def queue_position(self) -> Optional(int):
        """get the current queue position"""
        current_queue = self.scan_manager.queue_storage.current_scan_queue
        for queue_group in current_queue.values():
            if not isinstance(queue_group, dict):
                continue
            for queue_position, queue in enumerate(queue_group["info"]):
                if self.queueID == queue["queueID"]:
                    return queue_position
        return None


class QueueStorage:
    """stores queue items"""

    def __init__(self, scan_manager: ScanManager, maxlen=50) -> None:
        self.storage: Deque[QueueItem] = deque(maxlen=maxlen)
        self._lock = threading.RLock()
        self.scan_manager = scan_manager
        self.current_scan_queue = None

    def queue_history(self, history=5):
        """get the queue history of length 'history'"""
        if not history:
            raise ValueError("History length cannot be 0.")
        if history < 0:
            history *= -1

        return [
            BECMessage.ScanQueueHistoryMessage.loads(msg)
            for msg in self.scan_manager.producer.lrange(
                MessageEndpoints.scan_queue_history(), history, -1
            )
        ]

    @threadlocked
    def update_with_status(self, queue_msg: BECMessage.ScanQueueStatusMessage) -> None:
        """update a queue item with a new ScanQueueStatusMessage / queue message"""
        self.current_scan_queue = queue_msg.content["queue"]
        queue_info = self.current_scan_queue["primary"].get("info")
        for queue_item in queue_info:
            if self.find_queue_item_by_ID(queueID=queue_item["queueID"]):
                continue
            self.storage.append(QueueItem(scan_manager=self.scan_manager, **queue_item))

    @threadlocked
    def find_queue_item_by_ID(self, queueID: str) -> Optional(QueueItem):
        """find a queue item based on its queueID"""
        for queue_item in self.storage:
            if queue_item.queueID == queueID:
                return queue_item
        return None

    @threadlocked
    def find_queue_item_by_requestID(self, requestID: str) -> Optional(QueueItem):
        """find a queue item based on its requestID"""
        for queue_item in self.storage:
            # pylint: disable=protected-access
            if requestID in queue_item._requests:
                return queue_item
        return None

    @threadlocked
    def find_queue_item_by_scanID(self, scanID: str) -> Optional(QueueItem):
        """find a queue item based on its scanID"""
        for queue_item in self.storage:
            # pylint: disable=protected-access
            if scanID in queue_item._scans:
                return queue_item
        return None
