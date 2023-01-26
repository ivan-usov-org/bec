from .scan_bundler import ScanBundler
import time
import uuid
from collections.abc import Iterable

import msgpack
import numpy as np

from bec_utils import MessageEndpoints, bec_logger

logger = bec_logger.logger


class BlueskyEmitter:
    def __init__(self, scan_bundler: ScanBundler) -> None:

        self.scan_bundler = scan_bundler
        self.bluesky_metadata = {}

    def send_run_start_document(self, scanID) -> None:
        """Bluesky only: send run start documents."""
        doc = {
            "time": time.time(),
            "uid": str(uuid.uuid4()),
            "scanID": scanID,
            "queueID": self.sync_storage[scanID]["info"]["queueID"],
            "scan_id": self.sync_storage[scanID]["info"]["scan_number"],
            "motors": tuple(dev.name for dev in self.scan_motors[scanID]),
        }
        self.bluesky_metadata[scanID]["start"] = doc
        self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("start", doc)))
        self.send_descriptor_document(scanID)

    def send_descriptor_document(self, scanID) -> None:
        """Bluesky only: send descriptor document"""

        def _get_data_keys():
            signals = {}
            for dev in self.primary_devices[scanID]["devices"]:
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
                dev.name: list(dev.signals.keys())
                for dev in self.primary_devices[scanID]["devices"]
            },
        }
        self.bluesky_metadata[scanID]["descriptor"] = doc
        self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("descriptor", doc)))

    def cleanup_storage(self):
        """remove old scanIDs to free memory"""
        remove_scanIDs = []
        for scanID, entry in self.sync_storage.items():
            if entry.get("status") not in ["closed", "aborted"]:
                continue
            if scanID in self.scanID_history:
                continue
            remove_scanIDs.append(scanID)

        for scanID in remove_scanIDs:
            for storage in [
                "sync_storage",
                "bluesky_metadata",
                "primary_devices",
                "monitor_devices",
                "baseline_devices",
                "scan_motors",
            ]:
                try:
                    getattr(self, storage).pop(scanID)
                except KeyError:
                    logger.warning(f"Failed to remove {scanID} from {storage}.")
            self.storage_initialized.remove(scanID)
