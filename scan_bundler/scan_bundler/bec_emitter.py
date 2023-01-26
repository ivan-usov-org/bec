import time

from bec_utils import BECMessage, MessageEndpoints, bec_logger

from .scan_bundler import ScanBundler

logger = bec_logger.logger


class BECEmitter:
    def __init__(self, scan_bundler: ScanBundler) -> None:
        self.scan_bundler = scan_bundler

    def _send_scan_point(self, scanID, pointID) -> None:
        logger.info(f"Sending point {pointID} for scanID {scanID}.")
        logger.debug(f"{pointID}, {self.sync_storage[scanID][pointID]}")
        self._send_buffer.put(
            BECMessage.ScanMessage(
                point_id=pointID,
                scanID=scanID,
                data=self.sync_storage[scanID][pointID],
                metadata=self.sync_storage[scanID]["info"],
            )
        )

        # self.producer.send(
        #     MessageEndpoints.bluesky_events(),
        #     msgpack.dumps(("event", self._prepare_bluesky_event_data(scanID, pointID))),
        # )
        # self.sync_storage[scanID].pop(pointID)
        if not pointID in self.sync_storage[scanID]["sent"]:
            self.sync_storage[scanID]["sent"].add(pointID)
        else:
            logger.warning(f"Resubmitting existing pointID {pointID} for scanID {scanID}")

    def _send_baseline(self, scanID: str) -> None:
        pipe = self.producer.pipeline()
        msg = BECMessage.ScanBaselineMessage(
            scanID=scanID, data=self.sync_storage[scanID]["baseline"]
        ).dumps()
        self.producer.set(
            MessageEndpoints.public_scan_baseline(scanID=scanID),
            msg,
            pipe=pipe,
            expire=1800,
        )
        pipe.execute()

    def _buffered_publish(self):
        while True:
            msgs_to_send = []
            while not self._send_buffer.empty():
                msgs_to_send.append(self._send_buffer.get())
            if len(msgs_to_send) > 0:
                pipe = self.producer.pipeline()
                msgs = BECMessage.BundleMessage()
                for msg in msgs_to_send:
                    scanID = msg.content["scanID"]
                    pointID = msg.content["point_id"]
                    msg_dump = msg.dumps()
                    msgs.append(msg_dump)
                    self.producer.set(
                        MessageEndpoints.public_scan_segment(scanID=scanID, pointID=pointID),
                        msg_dump,
                        pipe=pipe,
                        expire=1800,
                    )
                self.producer.send(MessageEndpoints.scan_segment(), msgs.dumps(), pipe=pipe)
                pipe.execute()
                continue
            time.sleep(0.1)
