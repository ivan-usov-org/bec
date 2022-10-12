from __future__ import annotations

import abc
import threading
import time
from typing import TYPE_CHECKING

from bec_utils import Alarms, BECMessage

if TYPE_CHECKING:
    from bec_client.bec_client import BKClient


class ScanRequestError(Exception):
    pass


def set_event_delayed(event: threading.Event, delay: int) -> None:
    """Set event with a delay

    Args:
        event (threading.Event): event that should be set
        delay (int): delay time in seconds

    """

    def call_set():
        time.sleep(delay)
        event.set()

    thread = threading.Thread(target=call_set, daemon=True)
    thread.start()


def check_alarms(bec):
    """check for alarms and raise them if needed"""
    for alarm in bec.alarms(severity=Alarms.MINOR):
        if alarm:
            raise alarm


class LiveUpdatesBase(abc.ABC):
    def __init__(self, bec: BKClient, request: BECMessage.ScanQueueMessage) -> None:
        self.bec = bec
        self.request = request

    @abc.abstractmethod
    def run(self):
        pass
