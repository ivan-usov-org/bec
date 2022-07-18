import threading
import time
from collections import deque

from bec_utils import BECMessage, MessageEndpoints, bec_logger

logger = bec_logger.logger


class ScanRequest:
    def __init__(self) -> None:
        self.request_id = None
        self.request = None
        self.response = None
        self.accepted = None
        self.decision_pending = True
        self.status = "pending"
        self.scanID = None  # request.metadata.get("scanID")

    def update_with_response(self, response: BECMessage.RequestResponseMessage):
        self.response = response
        self.decision_pending = False
        self.request_id = response.metadata["RID"]
        self.accepted = [response.content["accepted"]]

    def update_with_request(self, request: BECMessage.ScanQueueMessage):
        self.request = request
        self.request_id = request.metadata["RID"]

    @classmethod
    def from_request(cls, request: BECMessage.ScanQueueMessage):
        scan_req = cls()
        scan_req.update_with_request(request=request)
        return scan_req

    @classmethod
    def from_response(cls, response: BECMessage.RequestResponseMessage):
        scan_req = cls()
        scan_req.update_with_response(response)
        return scan_req


class QueueInfo:
    def __init__(
        self,
        queueID: str,
        scanID: list,
        is_scan: list,
        request_blocks: list,
        scan_number: list,
        status: str,
        active_request_block: dict,
    ) -> None:
        self.scanID = scanID
        self.queueID = queueID
        self.is_scan = is_scan
        self.request_blocks = request_blocks
        self.scan_number = scan_number
        self.status = status
        self.active_request_block = active_request_block

    def get_block_id(self, RID) -> int:
        for ii, rb in enumerate(self.request_blocks):
            if rb.get("RID") == RID:
                return ii


class ScanReport:
    def __init__(self) -> None:
        self.data = dict()
        self.num_points = None
        self.status = {}
        self.completed = False
        self.accepted = False
        self.queue = {}
        self._client = None
        self.request = None

    @classmethod
    def from_request(cls, request, client=None):
        r = cls()
        r._client = client
        if r._client.queue.scan_queue_requests.get(request.metadata["RID"]) is None:
            r._client.queue.scan_queue_requests[request.metadata["RID"]] = ScanRequest.from_request(
                request
            )
        r.request = r._client.queue.scan_queue_requests.get(request.metadata["RID"])
        return r

    @property
    def scan(self):
        return self._client.queue.find_scan(RID=self.request.request_id)


class Scan:
    def __init__(self, queue_info: QueueInfo = None, client=None) -> None:
        self.queue_info = queue_info
        self.data = {}
        self.num_points = None
        self.start_time = None
        self.end_time = None
        self.status = {}
        self.open_scan_defs = []
        self._client = client

    def update_queue_info(self, queue_info: QueueInfo):
        self.queue_info = queue_info

    @property
    def scanID(self):
        return self.queue_info.scanID

    @property
    def scan_number(self):
        return self.queue_info.scan_number

    def abort(self):
        self._client.queue.request_scan_abortion(scanID=self.scanID)

    def pause(self):
        self._client.queue.request_scan_interruption(deferred_pause=False, scanID=self.scanID)

    def deferred_pause(self):
        self._client.queue.request_scan_interruption(deferred_pause=False, scanID=self.scanID)

    def continue_scan(self):
        self._client.queue.request_scan_continuation(scanID=self.scanID)

    def subscribe(self):
        pass

    def describe(self):
        pass


class ScanQueue:
    def __init__(self, parent):
        self.parent = parent
        self._current_scan_info = None
        self.connector = self.parent.connector
        self._lock = threading.Lock()

        self._scan_queue_consumer = self.connector.consumer(
            topics=MessageEndpoints.scan_queue_status(),
            auto_offset_reset="earliest",
            cb=self._scan_queue_status_callback,
            parent=self,
        )
        self._scan_queue_request_consumer = self.connector.consumer(
            topics=MessageEndpoints.scan_queue_request(),
            auto_offset_reset="earliest",
            cb=self._scan_queue_request_callback,
            parent=self,
        )
        self._scan_queue_request_response_consumer = self.connector.consumer(
            topics=MessageEndpoints.scan_queue_request_response(),
            auto_offset_reset="earliest",
            cb=self._scan_queue_request_response_callback,
            parent=self,
        )
        self._scan_status_consumer = self.connector.consumer(
            topics=MessageEndpoints.scan_status(),
            cb=self._scan_status_callback,
            parent=self,
        )

        self._scan_segment_consumer = self.connector.consumer(
            topics=MessageEndpoints.scan_segment(),
            cb=self._scan_segment_callback,
            parent=self,
        )

        self._scan_queue_consumer.start()
        self._scan_queue_request_consumer.start()
        self._scan_queue_request_response_consumer.start()
        self._scan_status_consumer.start()
        self._scan_segment_consumer.start()
        self.current_scan_queue = {}
        self.scan_queue_requests = {}
        self.scan_storage = deque(maxlen=10)
        self._last_scan_number = 0

    @property
    def last_scan_number(self):
        return self._last_scan_number

    @last_scan_number.setter
    def last_scan_number(self, val):
        self._last_scan_number = val
        # pylint: disable=protected-access
        self.parent._set_ipython_prompt_scan_number(val)

    @property
    def current_scan(self) -> Scan:
        if self.current_scanId is not None:
            return self.find_scan(scanID=self.current_scanId[0])
        return None

    @property
    def current_scanId(self):
        return self.current_scan_info.get("scanID") if self.current_scan_info is not None else None

    @property
    def current_scan_info(self):
        return self._current_scan_info

    @current_scan_info.setter
    def current_scan_info(self, val):
        self._current_scan_info = val

    def resume(self):
        self.request_scan_continuation()

    def request_scan_interruption(self, deferred_pause=True, scanID=None) -> None:
        if scanID is None:
            scanID = self.current_scanId
        if not any(scanID):
            return self.request_scan_abortion()

        action = "deferred_pause" if deferred_pause else "pause"
        return self.parent.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=scanID, action=action, parameter={}
            ).dumps(),
        )

    def request_scan_abortion(self, scanID=None):
        if scanID is None:
            scanID = self.current_scanId
        self.parent.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=scanID, action="abort", parameter={}
            ).dumps(),
        )

    def request_scan_continuation(self, scanID=None):
        if scanID is None:
            scanID = self.current_scanId
        self.parent.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=scanID, action="continue", parameter={}
            ).dumps(),
        )

    def add_scan_msg(self, scan_msg):
        inserted = False
        while not inserted:
            for scan_obj in self.scan_storage:
                if scan_obj.queue_info.scanID == scan_msg.metadata["scanID"]:
                    scan_obj.data[scan_msg.content["point_id"]] = scan_msg.content["data"]
                    inserted = True
            time.sleep(0.01)

    @staticmethod
    def _scan_segment_callback(msg, *, parent, **kwargs) -> None:
        scan_msg = BECMessage.ScanMessage.loads(msg.value)
        if scan_msg is not None:
            parent.add_scan_msg(scan_msg)

    @staticmethod
    def _scan_queue_status_callback(msg, *, parent, **kwargs) -> None:
        queue_status = BECMessage.ScanQueueStatusMessage.loads(msg.value)
        if queue_status is not None:
            parent._update_queue_status(queue_status.content["queue"])
        # if scan.metadata is not None:
        #     if "scanID" in scan.metadata:
        #         parent.scan_queue[scan.metadata["scanID"]] = Scan.from_ScanRequest(scan)

    def _update_scan_storage_queueinfo(self):
        with self._lock:
            for queue_item in self.current_scan_queue["primary"].get("info"):
                append = True
                for scan_obj in self.scan_storage:
                    if len(set(scan_obj.queue_info.scanID) & set(queue_item["scanID"])) > 0:
                        append = False
                        scan_obj.update_queue_info(queue_info=QueueInfo(**queue_item))
                if any(queue_item["is_scan"]) and append:
                    logger.debug(f"Appending new scan: {queue_item}")
                    self.scan_storage.append(Scan(QueueInfo(**queue_item), client=self.parent))

    def _update_queue_status(self, msg):
        self.current_scan_queue = msg
        logger.debug(f"New new scan queue: {self.current_scan_queue}")
        if len(self.current_scan_queue["primary"].get("info")) > 0:
            logger.debug(
                f"Updating current_scan_info: {self.current_scan_queue['primary'].get('info')[0]}"
            )
            self.current_scan_info = self.current_scan_queue["primary"].get("info")[0]
        else:
            self.current_scan_info = None
        self._update_scan_storage_queueinfo()

    def find_scan(self, RID=None, queueID=None, scanID=None, scan_number=None):
        """find scan object matching either the RID, queueID, scanID or scan_number"""
        with self._lock:
            if RID:
                for scan_obj in self.scan_storage:
                    for request_block in scan_obj.queue_info.request_blocks:
                        if request_block["RID"] == RID:
                            return scan_obj
            if queueID:
                for scan_obj in self.scan_storage:
                    if scan_obj.queue_info.queueID == queueID:
                        return scan_obj
            if scanID:
                for scan_obj in self.scan_storage:
                    for request_block in scan_obj.queue_info.request_blocks:
                        if request_block["scanID"] == scanID:
                            return scan_obj
            if scan_number:
                for scan_obj in self.scan_storage:
                    for request_block in scan_obj.queue_info.request_blocks:
                        if request_block["scan_number"] == scan_number:
                            return scan_obj
            return None

    def get_queue_position(self, scanID):
        """get the current queue position for a scan"""
        for queue_group in self.current_scan_queue.values():
            if isinstance(queue_group, dict):
                for queue_position, queue in enumerate(queue_group["info"]):
                    if queue["scanID"] == scanID:
                        return queue_position
        return None

    @staticmethod
    def _scan_queue_request_callback(msg, *, parent, **kwargs) -> None:
        request = BECMessage.ScanQueueMessage.loads(msg.value)
        if request.metadata is not None:
            if "RID" in request.metadata:
                if parent.scan_queue_requests.get(request.metadata["RID"]) is not None:
                    parent.scan_queue_requests[request.metadata["RID"]].update_with_request(request)
                else:
                    parent.scan_queue_requests[request.metadata["RID"]] = ScanRequest.from_request(
                        request
                    )

    @staticmethod
    def _scan_queue_request_response_callback(msg, *, parent, **kwargs) -> None:
        response = BECMessage.RequestResponseMessage.loads(msg.value)
        logger.debug(response)
        if parent.scan_queue_requests.get(response.metadata.get("RID")) is not None:
            parent.scan_queue_requests[response.metadata["RID"]].update_with_response(response)
            logger.debug("Scan queue request exists. Updating with response.")
        else:
            # it could be that the response arrived before the request
            parent.scan_queue_requests[response.metadata.get("RID")] = ScanRequest.from_response(
                response
            )
            logger.debug("Scan queue request does not exist. Creating from response.")
            # print(parent.scan_queue_requests.get(response.metadata.get("RID")))

    @staticmethod
    def _scan_status_callback(msg, *, parent, **kwargs) -> None:
        scan = BECMessage.ScanStatusMessage.loads(msg.value)
        scan_number = scan.content["info"].get("scan_number")
        if scan_number:
            parent.last_scan_number = scan_number

        while True:
            scan_obj = parent.find_scan(scanID=scan.content["scanID"])
            if scan_obj is not None:
                if scan.content.get("status") == "open":
                    scan_obj.start_time = scan.content.get("timestamp")
                elif scan.content.get("status") == "closed":
                    scan_obj.end_time = scan.content.get("timestamp")
                scan_obj.status[scan.content["scanID"]] = scan.content.get("status")
                if scan.content["info"].get("points"):
                    scan_obj.num_points = scan.content["info"].get("points") + 1
                break
            else:
                time.sleep(0.1)
