from __future__ import annotations

import time
from queue import Queue

from typing import TYPE_CHECKING

from bec_utils import BECMessage, MessageEndpoints, bec_logger

logger = bec_logger.logger

if TYPE_CHECKING:
    from .scan_bundler import ScanBundler


class BECEmitter:
    def __init__(self, scan_bundler: ScanBundler) -> None:
        self.scan_bundler = scan_bundler
        self._send_buffer = Queue()

    def _send_bec_scan_point(self, scanID, pointID) -> None:
        sb = self.scan_bundler

        self._send_buffer.put(
            BECMessage.ScanMessage(
                point_id=pointID,
                scanID=scanID,
                data=sb.sync_storage[scanID][pointID],
                metadata=sb.sync_storage[scanID]["info"],
            )
        )

    def _send_baseline(self, scanID: str) -> None:
        sb = self.scan_bundler

        pipe = sb.producer.pipeline()
        msg = BECMessage.ScanBaselineMessage(
            scanID=scanID, data=sb.sync_storage[scanID]["baseline"]
        ).dumps()
        sb.producer.set(
            MessageEndpoints.public_scan_baseline(scanID=scanID),
            msg,
            pipe=pipe,
            expire=1800,
        )
        pipe.execute()

    def _buffered_publish(self):
        sb = self.scan_bundler

        while True:
            msgs_to_send = []
            while not self._send_buffer.empty():
                msgs_to_send.append(self._send_buffer.get())
            if len(msgs_to_send) > 0:
                pipe = sb.producer.pipeline()
                msgs = BECMessage.BundleMessage()
                for msg in msgs_to_send:
                    scanID = msg.content["scanID"]
                    pointID = msg.content["point_id"]
                    msg_dump = msg.dumps()
                    msgs.append(msg_dump)
                    sb.producer.set(
                        MessageEndpoints.public_scan_segment(scanID=scanID, pointID=pointID),
                        msg_dump,
                        pipe=pipe,
                        expire=1800,
                    )
                sb.producer.send(MessageEndpoints.scan_segment(), msgs.dumps(), pipe=pipe)
                pipe.execute()
                continue
            time.sleep(0.1)
