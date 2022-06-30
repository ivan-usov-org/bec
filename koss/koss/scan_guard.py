import logging

import msgpack
from bec_utils import BECMessage, MessageEndpoints

logger = logging.getLogger(__name__)


class ScanRejection(Exception):
    pass


class ScanStatus:

    def __init__(self, decision: bool=True, message: str=""):
        self.decision = decision
        self.message = message


class ScanGuard:
    def __init__(self, *, parent):
        """
        Scan guard receives scan requests and checks their validity. If the scan is
        accepted, it enqueues a new scan message.
        """
        self.parent = parent
        self.device_manager = self.parent.device_manager
        self.connector = self.parent.connector
        self.producer = self.connector.producer()
        self._start_scan_queue_request_consumer()

    def _start_scan_queue_request_consumer(self):
        self._scan_queue_request_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_request(),
            cb=self._scan_queue_request_callback,
            parent=self,
        )

        self._scan_queue_modification_request_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_modification_request(),
            cb=self._scan_queue_modification_request_callback,
            parent=self,
        )

        self._scan_queue_request_consumer.start()
        self._scan_queue_modification_request_consumer.start()

    def _is_valid_scan_request(self, request) -> ScanStatus:
        try:
            self._check_valid_request(request)
            self._check_valid_scan(request)
            self._check_baton(request)
            self._check_motors_movable(request)
            self._check_soft_limits(request)
        except ScanRejection as e:
            return ScanStatus(False, str(e))
        else:
            return ScanStatus()

    def _check_valid_request(self, request) -> None:
            if request is None:
                raise ScanRejection("Invalid request.")

    def _check_valid_scan(self, request) -> None:
        avail_scans = msgpack.loads(self.producer.get(MessageEndpoints.available_scans()))
        scan_type = request.content.get("scan_type")
        if scan_type not in avail_scans:
            raise ScanRejection(f"Unknown scan type {scan_type}.")

        if scan_type == "device_rpc":
            # ensure that the requested rpc is allowed for this particular device
            params = request.content.get("parameter")
            if not self._device_rpc_is_valid(device=params.get("device"), func=params.get("func")):
                raise ScanRejection(f"Rejected rpc: {request.content}")

    def _device_rpc_is_valid(self, device: str, func: str) -> bool:
        # TODO: ?
        return True

    def _check_baton(self, request) -> None:
        # TODO: Implement baton handling
        pass

    def _check_motors_movable(self, request) -> None:
        # TODO: Make sure you are not trying to move protected motors
        if request.content["scan_type"] == "device_rpc":
            return
        motor_args = request.content["parameter"].get("args")
        if not motor_args:
            return
        for m in motor_args:
            if not self.device_manager.devices[m].enabled:
                raise ScanRejection(f"Device {m} is not enabled.")

    def _check_soft_limits(self, request) -> None:
        # TODO: Implement soft limit checks
        pass

    @staticmethod
    def _scan_queue_request_callback(msg, parent, **kwargs):
        content = BECMessage.ScanQueueMessage.loads(msg.value).content
        print("Receiving scan request:", content)
        # pylint: disable=protected-access
        parent._handle_scan_request(msg.value)

    @staticmethod
    def _scan_queue_modification_request_callback(msg, parent, **kwargs):
        content = BECMessage.ScanQueueModificationMessage.loads(msg.value).content
        print("Receiving scan modification request:", content)
        # pylint: disable=protected-access
        parent._handle_scan_modification_request(msg.value)

    def _send_scan_request_response(self, scan_status, metadata):
        sqrr = MessageEndpoints.scan_queue_request_response()
        rrm = BECMessage.RequestResponseMessage(
            decision=scan_status.decision, message=scan_status.message, metadata=metadata
        ).dumps()
        self.device_manager.producer.send(sqrr, rrm)

    def _handle_scan_request(self, msg):
        """
        Perform validity checks on the scan request and reply with a 'scan_request_response'.
        If the scan is accepted it will be enqueued.
        Args:
            msg: ConsumerRecord value

        Returns:

        """
        msg = BECMessage.ScanQueueMessage.loads(msg)
        scan_status = self._is_valid_scan_request(msg)

        # msg.metadata["scanID"] = str(uuid.uuid4()) if accepted else None #TODO: hmm?
        self._send_scan_request_response(scan_status, msg.metadata)

        if scan_status.decision:
            self._append_to_scan_queue(msg)
        else:
            logger.info(f"Request was rejected: {scan_status.message}")

    def _handle_scan_modification_request(self, msg):
        """
        Perform validity checks on the scan modification request and reply
        with a 'scan_queue_modification_request_response'.
        If the scan queue modification is accepted it will be forwarded.
        Args:
            msg: ConsumerRecord value

        Returns:

        """
        msg = BECMessage.ScanQueueModificationMessage.loads(msg).dumps()
        sqm = MessageEndpoints.scan_queue_modification()
        self.device_manager.producer.send(sqm, msg)

    def _append_to_scan_queue(self, msg):
        print("Appending new scan to queue")
        msg = msg.dumps()
        sqi = MessageEndpoints.scan_queue_insert()
        self.device_manager.producer.send(sqi, msg)
