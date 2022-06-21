import bec_utils.BECMessage as BMessage
import msgpack
from bec_utils import MessageEndpoints


class ScanAcceptance:
    """ScanAcceptance"""

    _accepted = True
    _message = ""

    def set(self, accepted: bool, message: str) -> None:
        """set scan acceptance
        Args:
            accepted (bool): true if scan was accepted
            message (str): non-empty message if scan was rejected
        """
        if self._accepted:
            self._accepted = accepted
            self._message = message

    def get(self) -> dict:
        return {"accepted": self._accepted, "message": self._message}


class ScanGuard:
    def __init__(self, *, parent):
        """
        Scan guard receives scan requests and checks their validity. If the scan is
        accepted, it enqueues a new scan message.
        """
        self.parent = parent
        self.dm = self.parent.dm
        self.connector = self.parent.connector
        self.producer = self.connector.producer()
        self._start_scan_queue_request_consumer()
        self.scan_acc = ScanAcceptance()

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

    def _is_valid_scan_request(self, request) -> dict:
        self.scan_acc = ScanAcceptance()
        self._check_valid_scan(request)
        self._check_baton(request)
        self._check_motors_movable(request)
        self._check_soft_limits(request)

        if request is None:
            self.scan_acc.set(False, "Invalid request.")

        return self.scan_acc.get()

    def _check_valid_scan(self, request) -> None:
        avail_scans = msgpack.loads(self.producer.get(MessageEndpoints.available_scans()))
        if request.content.get("scan_type") not in avail_scans:
            self.scan_acc.set(False, f"Unknown scan type {request.content.get('scan_type')}.")

        if request.content.get("scan_type") == "device_rpc":
            # ensure that the requested rpc is allowed for this particular device
            params = request.content.get("parameter")
            if not self._device_rpc_is_valid(device=params.get("device"), func=params.get("func")):
                self.scan_acc.set(False, f"Rejected rpc: {request.content}")

    def _device_rpc_is_valid(self, device: str, func: str) -> bool:

        return True

    def _check_baton(self, request) -> None:
        # TODO: Implement baton handling
        pass

    def _check_soft_limits(self, request) -> None:
        # TODO: Implement soft limit checks
        pass

    def _check_motors_movable(self, request) -> None:
        # TODO: Make sure you are not trying to move protected motors
        if request.content["scan_type"] != "device_rpc":
            motor_args = request.content["parameter"].get("args")
            if motor_args:
                motors = motor_args.keys()
                for m in motors:
                    if not self.dm.devices[m].enabled:
                        self.scan_acc.set(False, f"Device {m} is not enabled.")

    @staticmethod
    def _scan_queue_request_callback(msg, parent, **kwargs):
        print(
            "Receiving scan request:",
            BMessage.ScanQueueMessage.loads(msg.value).content,
        )
        # pylint: disable=protected-access
        parent._handle_scan_request(msg.value)

    @staticmethod
    def _scan_queue_modification_request_callback(msg, parent, **kwargs):
        print(
            "Receiving scan modification request:",
            BMessage.ScanQueueModificationMessage.loads(msg.value).content,
        )
        # pylint: disable=protected-access
        parent._handle_scan_modification_request(msg.value)

    def _send_scan_request_response(self, scan_request_decision, metadata):
        decision = "accepted" if scan_request_decision["accepted"] else "rejected"
        self.dm.producer.send(
            MessageEndpoints.scan_queue_request_response(),
            BMessage.RequestResponseMessage(
                decision=decision,
                message=scan_request_decision["message"],
                metadata=metadata,
            ).dumps(),
        )

    def _handle_scan_request(self, msg):
        """
        Perform validity checks on the scan request and reply with a 'scan_request_response'.
        If the scan is accepted it will be enqueued.
        Args:
            msg: ConsumerRecord value

        Returns:

        """
        msg = BMessage.ScanQueueMessage.loads(msg)
        scan_request_decision = self._is_valid_scan_request(msg)

        accepted = scan_request_decision.get("accepted")
        # msg.metadata["scanID"] = str(uuid.uuid4()) if accepted else None
        self._send_scan_request_response(scan_request_decision, msg.metadata)

        if accepted:
            self._append_to_scan_queue(msg)

    def _handle_scan_modification_request(self, msg):
        """
        Perform validity checks on the scan modification request and reply
        with a 'scan_queue_modification_request_response'.
        If the scan queue modification is accepted it will be forwarded.
        Args:
            msg: ConsumerRecord value

        Returns:

        """
        msg = BMessage.ScanQueueModificationMessage.loads(msg)
        self.dm.producer.send(MessageEndpoints.scan_queue_modification(), msg.dumps())

    def _append_to_scan_queue(self, msg):
        print("Appending new scan to queue")
        self.dm.producer.send(MessageEndpoints.scan_queue_insert(), msg.dumps())
