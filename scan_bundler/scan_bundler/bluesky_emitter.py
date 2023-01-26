from __future__ import annotations

import time
import uuid
from collections.abc import Iterable
import blinker
import msgpack
import numpy as np
from typing import TYPE_CHECKING

from bec_utils import MessageEndpoints, bec_logger

logger = bec_logger.logger

if TYPE_CHECKING:
    from .scan_bundler import ScanBundler


class BlueskyEmitter:
    def __init__(self, scan_bundler: ScanBundler) -> None:

        self.scan_bundler = scan_bundler
        self.bluesky_metadata = {}
        self._connect_signals()

    def _connect_signals(self):
        sb = self.scan_bundler

        blinker.signal("scan_status_update").connect(self.send_run_start_document)
        blinker.signal("cleanup").connect(self.cleanup_storage)
        blinker.signal("scan_point").connect(self.send_bluesky_scan_point)

    def send_run_start_document(
        self, scanID
    ) -> None:  # comes here twice in tests and the second time sb.sync_storage[scanID] is empty...
        """Bluesky only: send run start documents."""
        print("run start doc")
        sb = self.scan_bundler
        self.bluesky_metadata[scanID] = {}
        doc = {
            "time": time.time(),
            "uid": str(uuid.uuid4()),
            "scanID": scanID,
            "queueID": sb.sync_storage[scanID]["info"]["queueID"],
            "scan_id": sb.sync_storage[scanID]["info"]["scan_number"],
            "motors": tuple(dev.name for dev in sb.scan_motors[scanID]),
        }
        self.bluesky_metadata[scanID]["start"] = doc
        sb.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("start", doc)))
        self.send_descriptor_document(scanID)

    def send_descriptor_document(self, scanID) -> None:
        """Bluesky only: send descriptor document"""
        sb = self.scan_bundler

        def _get_data_keys():
            signals = {}
            for dev in sb.primary_devices[scanID]["devices"]:
                # copied from bluesky/callbacks/stream.py:
                for key, val in dev.signals.items():
                    val = val["value"]
                    # String key
                    if isinstance(val, str):
                        key_desc = {"dtype": "string", "shape": []}
                    # Iterable
                    elif isinstance(val, Iterable):
                        key_desc = {"dtype": "array", "shape": np.shape(val)}
                    # Number
                    else:
                        key_desc = {"dtype": "number", "shape": []}
                    signals[key] = key_desc
            return signals

        doc = {
            "run_start": self.bluesky_metadata[scanID]["start"]["uid"],
            "time": time.time(),
            "data_keys": _get_data_keys(),
            "uid": str(uuid.uuid4()),
            "configuration": {},
            "name": "primary",
            "hints": {
                "samx": {"fields": ["samx"]},
                "samy": {"fields": ["samy"]},
            },
            "object_keys": {
                dev.name: list(dev.signals.keys()) for dev in sb.primary_devices[scanID]["devices"]
            },
        }
        self.bluesky_metadata[scanID]["descriptor"] = doc
        sb.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("descriptor", doc)))

    def cleanup_storage(self, scanID):
        """remove old scanIDs to free memory"""

        for storage in [
            "bluesky_metadata",
        ]:
            try:
                getattr(self, storage).pop(scanID)
            except KeyError:
                logger.warning(f"Failed to remove {scanID} from {storage}.")

    def send_bluesky_scan_point(self, scanID, pointID) -> None:

        self.producer.send(
            MessageEndpoints.bluesky_events(),
            msgpack.dumps(("event", self._prepare_bluesky_event_data(scanID, pointID))),
        )

    def _prepare_bluesky_event_data(self, scanID, pointID) -> dict:
        # event = {
        #     "descriptor": "5605e810-bb4e-4e40-b...d45279e3a4",
        #     "time": 1648468217.524021,
        #     "data": {
        #         "det": 1.0,
        #         "motor1": -10.0,
        #         "motor1_setpoint": -10.0,
        #         "motor2": -10.0,
        #         "motor2_setpoint": -10.0,
        #     },
        #     "timestamps": {
        #         "det": 1648468209.868633,
        #         "motor1": 1648468209.862141,
        #         "motor1_setpoint": 1648468209.8607192,
        #         "motor2": 1648468209.864479,
        #         "motor2_setpoint": 1648468209.8629901,
        #     },
        #     "seq_num": 1,
        #     "uid": "ea83a56e-6af2-4b94-9...44dcc36d4e",
        #     "filled": {},
        # }
        sb = self.scan_bundler
        metadata = self.bluesky_metadata[scanID]
        while not metadata.get("descriptor"):
            time.sleep(0.01)

        bls_event = {
            "descriptor": metadata["descriptor"].get("uid"),
            "time": time.time(),
            "seq_num": pointID,
            "uid": str(uuid.uuid4()),
            "filled": {},
            "data": {},
            "timestamps": {},
        }
        for data_point in sb.sync_storage[scanID][pointID].values():
            for key, val in data_point.items():
                bls_event["data"][key] = val["value"]
                bls_event["timestamps"][key] = val["timestamp"]
        return bls_event
