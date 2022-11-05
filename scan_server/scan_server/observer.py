from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, List

from bec_utils import BECMessage, MessageEndpoints, bec_logger
from bec_utils.observer import Observer, ObserverManagerBase

from scan_server.devicemanager import DeviceManagerScanServer

logger = bec_logger.logger

if TYPE_CHECKING:
    from scan_server.scan_server import ScanServer


class ObserverThread(threading.Thread, Observer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        super(threading.Thread, self).__init__(**kwargs)
        self.signal = threading.Event()
        self._triggered = False
        self.producer = self.parent.device_manager.producer

    def run(self) -> None:
        while not self.signal.is_set():
            if not self._is_condition_met():
                if self._triggered:
                    self._send_command(trigger="on_resume")
                    self._triggered = False
                time.sleep(0.01)
                continue
            if not self._triggered:
                self._send_command(trigger="on_trigger")
                self._triggered = True
                continue
            time.sleep(1)
            logger.debug(f"Running observer {self.name}.")

    def _send_command(self, trigger):
        action = getattr(self, trigger)
        if action == "halt":
            return self._send_halt()
        if action == "abort":
            return self._send_abort()
        if action == "deferred_pause":
            return self._send_deferred_pause()
        if action == "pause":
            return self._send_pause()
        if action == "continue":
            return self._send_continuation()
        if action == "restart":
            return self._send_scan_restart()
        if action == "reset":
            return self._send_queue_reset()
        return None

    def _send_abort(self):
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="abort", parameter={}
            ).dumps(),
        )

    def _send_halt(self):
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="halt", parameter={}
            ).dumps(),
        )

    def _send_deferred_pause(self) -> None:
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="deferred_pause", parameter={}
            ).dumps(),
        )

    def _send_pause(self) -> None:
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="pause", parameter={}
            ).dumps(),
        )

    def _send_continuation(self):
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="continue", parameter={}
            ).dumps(),
        )

    def _send_queue_reset(self):
        """request a scan queue reset"""
        logger.info("Requesting a queue reset")
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="clear", parameter={}
            ).dumps(),
        )

    def _send_scan_restart(self):
        self.producer.send(
            MessageEndpoints.scan_queue_modification_request(),
            BECMessage.ScanQueueModificationMessage(
                scanID=None, action="restart", parameter={"position": "replace"}
            ).dumps(),
        )

    def _is_condition_met(self):
        dev = self.parent.device_manager.devices[self.device]
        val = dev.readback()
        if self.low_limit is not None:
            if val["value"] < self.low_limit:
                return True
        if self.high_limit is not None:
            if val["value"] > self.high_limit:
                return True
        if self.target_value is not None:
            if val["value"] == self.target_value:
                return True
        return False


class ObserverManager(ObserverManagerBase):
    def __init__(self, device_manager: DeviceManagerScanServer, parent: ScanServer):
        super().__init__(device_manager)
        self.parent = parent
        self._observer_consumer = None

    def _dict_to_observer(self, observer: List[dict]):
        obs_container = []
        for obs in observer:
            obs.update({"parent": self})
            obs_container.append(ObserverThread.from_dict(obs))
        return obs_container

    def start(self):
        self._observer_consumer = self.parent.connector.consumer(
            MessageEndpoints.observer(),
            cb=self._observer_update,
            parent=self,
        )
        self._observer_consumer.start()
        self._start_all_observer()

    def _stop_all_observer(self):
        for obs in self.observer:
            obs.signal.set()
        for obs in self.observer:
            obs.join()

    def handle_observer_update(self, msg: BECMessage.ObserverMessage):
        self._stop_all_observer()
        self._observer = self._dict_to_observer(msg.content["observer"])
        self._start_all_observer()

    @staticmethod
    def _observer_update(msg, parent: ObserverManager, **kwargs):
        msg = BECMessage.ObserverMessage.loads(msg.value)
        logger.debug("Receiving observer update")
        parent.handle_observer_update(msg)

    def _start_all_observer(self):
        for obs in self.observer:
            obs.start()
