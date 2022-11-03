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

    def run(self) -> None:
        while not self.signal.is_set():
            logger.debug(f"Running observer {self.name}.")
            time.sleep(1)


class ObserverManager(ObserverManagerBase):
    def __init__(self, device_manager: DeviceManagerScanServer, parent: ScanServer):
        super().__init__(device_manager)
        self.parent = parent
        self._observer_consumer = None

    def _dict_to_observer(self, observer: List[dict]):
        return [ObserverThread.from_dict(obs) for obs in observer]

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
