from __future__ import annotations

import threading
from collections import deque
from typing import TYPE_CHECKING, Deque, Optional

from bec_utils import BECMessage, bec_logger

logger = bec_logger.logger


if TYPE_CHECKING:
    from queue_items import QueueItem
    from scan_items import ScanItem
    from scan_manager import ScanManager


class RequestItem:
    def __init__(
        self,
        scan_manager: ScanManager,
        requestID: str,
        decision_pending: bool = True,
        scanID: str = None,
        request=None,
        response=None,
        accepted: bool = None,
        **kwargs,
    ) -> None:
        self.scan_manager = scan_manager
        self.requestID = requestID
        self.request = request
        self.response = response
        self.accepted = accepted
        self.decision_pending = decision_pending
        self.status = "PENDING"  # needed?
        self._scanID = scanID

    def update_with_response(self, response: BECMessage.RequestResponseMessage):
        self.response = response
        self.decision_pending = False
        self.requestID = response.metadata["RID"]
        self.accepted = [response.content["accepted"]]

    def update_with_request(self, request: BECMessage.ScanQueueMessage):
        self.request = request
        self.requestID = request.metadata["RID"]

    @classmethod
    def from_response(cls, scan_manager: ScanManager, response: BECMessage.RequestResponseMessage):
        scan_req = cls(
            scan_manager=scan_manager,
            requestID=response.metadata["RID"],
            response=response,
            decision_pending=False,
            accepted=[response.content["accepted"]],
        )
        return scan_req

    @classmethod
    def from_request(cls, scan_manager: ScanManager, request: BECMessage.ScanQueueMessage):
        scan_req = cls(
            scan_manager=scan_manager, requestID=request.metadata["RID"], request=request
        )
        return scan_req

    @property
    def scan(self) -> ScanItem:
        queue_item = self.scan_manager.queue_storage.find_queue_item_by_requestID(self.requestID)
        if not queue_item:
            return None
        # pylint: disable=protected-access
        request_index = queue_item._requests.index(self.requestID)
        return queue_item.scans[request_index]

    @property
    def queue(self) -> QueueItem:
        return self.scan_manager.queue_storage.find_queue_item_by_requestID(self.requestID)


class RequestStorage:
    """stores request items"""

    def __init__(self, scan_manager: ScanManager, maxlen=50) -> None:
        self.storage: Deque[RequestItem] = deque(maxlen=maxlen)
        self._lock = threading.Lock()
        self.scan_manager = scan_manager

    def find_request_by_ID(self, requestID: str) -> Optional(RequestItem):
        """find a request item based on its requestID"""
        for request in self.storage:
            if request.requestID == requestID:
                return request
        return None

    def update_with_response(self, response_msg: BECMessage.RequestResponseMessage) -> None:
        """create or update request item based on a new RequestResponseMessage"""
        request_item = self.find_request_by_ID(response_msg.metadata.get("RID"))
        if request_item:
            request_item.update_with_response(response_msg)
            logger.debug("Scan queue request exists. Updating with response.")
            return

        # it could be that the response arrived before the request
        self.storage.append(RequestItem.from_response(self.scan_manager, response_msg))
        logger.debug("Scan queue request does not exist. Creating from response.")

    def update_with_request(self, request_msg: BECMessage.ScanQueueMessage) -> None:
        """create or update request item based on a new ScanQueueMessage (i.e. request message)"""
        if not request_msg.metadata:
            return

        if not request_msg.metadata.get("RID"):
            return

        request_item = self.find_request_by_ID(request_msg.metadata.get("RID"))
        if request_item:
            request_item.update_with_request(request_msg)
            return

        self.storage.append(RequestItem.from_request(self.scan_manager, request_msg))
