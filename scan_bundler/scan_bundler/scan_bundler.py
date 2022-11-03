import collections
import threading
import time
import uuid
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import msgpack
import numpy as np
from bec_utils import BECMessage, BECService, MessageEndpoints, bec_logger
from bec_utils.connector import ConnectorBase

from .devicemanager_sb import DeviceManagerSB

logger = bec_logger.logger


class ScanBundler(BECService):
    def __init__(self, bootstrap_server, connector_cls: ConnectorBase, scibec_url: str) -> None:
        super().__init__(bootstrap_server, connector_cls, unique_service=True)

        self.device_manager = None
        self.scibec_url = scibec_url
        self._start_device_manager()
        self._start_device_read_consumer()
        self._start_scan_queue_consumer()
        self._start_scan_status_consumer()

        self.sync_storage = {}
        self.bluesky_metadata = {}
        self.primary_devices = {}
        self.monitor_devices = {}
        self.baseline_devices = {}
        self.device_storage = {}
        self.scan_motors = {}
        self.storage_initialized = set()
        self.current_queue = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.executor_tasks = collections.deque(maxlen=100)
        self._send_buffer = Queue()
        self._start_buffered_producer()
        self.scanID_history = collections.deque(maxlen=10)
        self._lock = threading.Lock()

    def _start_buffered_producer(self):
        self._buffered_producer_thread = threading.Thread(
            target=self._buffered_publish, daemon=True
        )
        self._buffered_producer_thread.start()

    def _start_device_manager(self):
        self.device_manager = DeviceManagerSB(self.connector, self.scibec_url)
        self.device_manager.initialize(self.bootstrap_server)

    def _start_device_read_consumer(self):
        self._device_read_consumer = self.connector.consumer(
            pattern=MessageEndpoints.device_read("*"),
            cb=self._device_read_callback,
            parent=self,
        )
        self._device_read_consumer.start()

    def _start_scan_queue_consumer(self):
        self._scan_queue_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_status(),
            cb=self._scan_queue_callback,
            group_id="scan_bundler",
            parent=self,
        )
        self._scan_queue_consumer.start()

    def _start_scan_status_consumer(self):
        self._scan_status_consumer = self.connector.consumer(
            MessageEndpoints.scan_status(),
            cb=self._scan_status_callback,
            group_id="scan_bundler",
            parent=self,
        )
        self._scan_status_consumer.start()

    @staticmethod
    def _device_read_callback(msg, parent, **_kwargs):
        # pylint: disable=protected-access
        dev = msg.topic.decode().split(MessageEndpoints._device_read + "/")[-1].split(":sub")[0]
        msgs = BECMessage.DeviceMessage.loads(msg.value)
        logger.debug(f"Received reading from device {dev}")
        if not isinstance(msgs, list):
            msgs = [msgs]
        task = parent.executor.submit(parent._add_device_to_storage, msgs, dev)
        parent.executor_tasks.append(task)

    @staticmethod
    def _scan_queue_callback(msg, parent, **_kwargs):
        msg = BECMessage.ScanQueueStatusMessage.loads(msg.value)
        logger.trace(msg)
        parent.current_queue = msg.content["queue"]["primary"].get("info")

    @staticmethod
    def _scan_status_callback(msg, parent, **_kwargs):
        msg = BECMessage.ScanStatusMessage.loads(msg.value)
        parent.handle_scan_status_message(msg)

    def handle_scan_status_message(self, msg: BECMessage.ScanStatusMessage) -> None:
        """handle scan status messages"""
        logger.info(f"Received new scan status: {msg}")
        scanID = msg.content["scanID"]
        self.cleanup_storage()
        if not scanID in self.sync_storage:
            self._initialize_scan_container(msg)
            if scanID not in self.scanID_history:
                self.scanID_history.append(scanID)
        if msg.content.get("status") != "open":
            self._scan_status_modification(msg)

    def _scan_status_modification(self, msg: BECMessage.ScanStatusMessage):
        status = msg.content.get("status")
        if status not in ["closed", "aborted"]:
            logger.error(f"Unknown scan status {status}")
            return

        scanID = msg.content.get("scanID")
        if not scanID:
            logger.error(f"Received scan status update without scanID: {msg}")
            return
        if self.sync_storage.get(scanID):
            self.sync_storage[scanID]["status"] = status
        else:
            self.sync_storage[scanID] = {"info": {}, "status": status, "sent": set()}
            self.storage_initialized.add(scanID)
            if scanID not in self.scanID_history:
                self.scanID_history.append(scanID)

        # doc = {
        #     "time": time.time(),
        #     "uid": str(uuid.uuid4()),
        #     "scanID": scanID,
        #     "run_start": self.bluesky_metadata[scanID]["start"]["uid"],
        #     "exit_status": "success" if status == "closed" else "aborted",
        #     "reason": "",
        #     "num_events": msg.content["info"].get("num_points"),
        # }
        # self.bluesky_metadata[scanID]["stop"] = doc
        # self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("stop", doc)))

    def _initialize_scan_container(self, scan_msg: BECMessage.ScanStatusMessage):
        if scan_msg.content.get("status") != "open":
            return

        scanID = scan_msg.content["scanID"]
        scan_info = scan_msg.content["info"]
        scan_motors = list(set(self.device_manager.devices[m] for m in scan_info["primary"]))

        self.scan_motors[scanID] = scan_motors
        if not scanID in self.storage_initialized:
            self.sync_storage[scanID] = {"info": scan_info, "status": "open", "sent": set()}
            self.bluesky_metadata[scanID] = {}
            # for now lets assume that all devices are primary devices:
            self.primary_devices[scanID] = {
                "devices": self.device_manager.devices.primary_devices(scan_motors),
                "pointID": {},
            }
            self.monitor_devices[scanID] = self.device_manager.devices.device_group("monitor")
            self.baseline_devices[scanID] = {
                "devices": self.device_manager.devices.baseline_devices(scan_motors),
                "done": {
                    dev.name: False
                    for dev in self.device_manager.devices.baseline_devices(scan_motors)
                },
            }
            self.storage_initialized.add(scanID)
            self.send_run_start_document(scanID)
            return

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

    def _step_scan_update(self, scanID, device, signal, metadata):
        if "pointID" not in metadata:
            return
        with self._lock:
            dev = {device: signal}
            pointID = metadata["pointID"]
            primary_devices = self.primary_devices[scanID]

            self.sync_storage[scanID][pointID] = {
                **self.sync_storage[scanID].get(pointID, {}),
                **dev,
            }

            if primary_devices["pointID"].get(pointID) is None:
                primary_devices["pointID"][pointID] = {
                    dev.name: False for dev in primary_devices["devices"]
                }
            primary_devices["pointID"][pointID][device] = True

            primary_devices_completed = [
                status for status in primary_devices["pointID"][pointID].values()
            ]

            all_primary_devices_completed = bool(
                all(primary_devices_completed)
                and (len(primary_devices_completed) == len(self.primary_devices[scanID]["devices"]))
            )

            if all_primary_devices_completed and self.sync_storage[scanID].get(pointID):
                self._update_monitor_signals(scanID, pointID)
                self._send_scan_point(scanID, pointID)

    def _fly_scan_update(self, scanID, device, signal, metadata):

        if "pointID" not in metadata:
            return
        with self._lock:
            dev = {}
            for sig_key, sig_val in signal.items():
                dev[sig_key] = {sig_key: sig_val}
            pointID = metadata["pointID"]

            self.sync_storage[scanID][pointID] = {
                **self.sync_storage[scanID].get(pointID, {}),
                **dev,
            }

            if self.sync_storage[scanID].get(pointID):
                self._update_monitor_signals(scanID, pointID)
                self._send_scan_point(scanID, pointID)

    def _add_device_to_storage(self, msgs, device):
        for msg in msgs:
            metadata = msg.metadata

            scanID = metadata.get("scanID")
            if not scanID:
                logger.error("Received device message without scanID")
                return

            signal = msg.content.get("signals")
            if not signal:
                logger.error("Received device message without signals")
                return

            timeout_time = 10
            elapsed_time = 0
            while not scanID in self.storage_initialized:
                msgs = [
                    BECMessage.ScanStatusMessage.loads(msg)
                    for msg in self.device_manager.producer.lrange(
                        MessageEndpoints.scan_status() + "_list", -5, -1
                    )
                ]
                for msg in msgs:
                    if msg.content["scanID"] == scanID:
                        self.handle_scan_status_message(msg)
                if scanID in self.sync_storage:
                    if self.sync_storage[scanID]["status"] in ["closed", "aborted"]:
                        logger.info(
                            f"Received reading for {self.sync_storage[scanID]['status']} scan {scanID}."
                        )
                        return
                time.sleep(0.1)
                elapsed_time += 0.1
                if elapsed_time > timeout_time:
                    logger.warning(
                        f"Failed to insert device data for {device} to sync_storage: Could not find a matching scanID {scanID} in sync_storage."
                    )
                    return
            if self.sync_storage[scanID]["status"] in ["aborted", "closed"]:
                # check if the sync_storage has been initialized properly.
                # In case of post-scan initialization, scan info is not available
                if not self.sync_storage[scanID]["info"].get("scan_type"):
                    return
            self.device_storage[device] = signal
            stream = metadata.get("stream")
            if stream == "primary":
                if self.sync_storage[scanID]["info"]["scan_type"] == "step":
                    self._step_scan_update(scanID, device, signal, metadata)
                elif self.sync_storage[scanID]["info"]["scan_type"] == "fly":
                    self._fly_scan_update(scanID, device, signal, metadata)
                else:
                    raise RuntimeError(
                        f"Unknown scan type {self.sync_storage[scanID]['scan_type']}"
                    )

            elif stream == "baseline":
                with self._lock:
                    dev = {device: signal}
                    baseline_devices_status = self.baseline_devices[scanID]["done"]
                    baseline_devices_status[device] = True

                    self.sync_storage[scanID]["baseline"] = {
                        **self.sync_storage[scanID].get("baseline", {}),
                        **dev,
                    }

                    if all(status for status in baseline_devices_status.values()):
                        logger.info(f"Sending baseline readings for scanID {scanID}.")
                        logger.debug("Baseline: ", self.sync_storage[scanID]["baseline"])
                        self._send_baseline(scanID=scanID)

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
        for data_point in self.sync_storage[scanID][pointID].values():
            for key, val in data_point.items():
                bls_event["data"][key] = val["value"]
                bls_event["timestamps"][key] = val["timestamp"]
        return bls_event

    def _update_monitor_signals(self, scanID, pointID) -> None:
        if self.sync_storage[scanID]["info"]["scan_type"] == "fly":
            # for fly scans, take all primary and monitor signals
            for dev in self.primary_devices[scanID]["devices"]:
                self.sync_storage[scanID][pointID][dev.name] = self.device_storage.get(dev.name)

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

    def shutdown(self):
        self.device_manager.shutdown()
