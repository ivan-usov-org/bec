import logging
import time
import uuid
from collections.abc import Iterable

import bec_utils.BECMessage as BMessage
import msgpack
import numpy as np
from bec_utils import MessageEndpoints
from bec_utils.connector import ConnectorBase

from .devicemanager_sb import DeviceManagerSB

logger = logging.getLogger(__name__)


class ScanBundler:
    def __init__(self, bootstrap, Connector: ConnectorBase, scibec_url: str) -> None:
        self.connector = Connector(bootstrap)
        self.DM = DeviceManagerSB(self.connector, scibec_url)
        self.DM.initialize(bootstrap)
        self.producer = self.connector.producer()
        self._start_device_read_consumer()
        self._start_scan_queue_consumer()
        self._start_scan_status_consumer()
        self.sync_storage = dict()
        self.bluesky_metadata = dict()
        self.primary_devices = dict()
        self.monitor_devices = dict()
        self.baseline_devices = dict()
        self.scan_motors = dict()
        self.metadata = dict()

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
    def _device_read_callback(msg, parent, **kwargs):
        dev = msg.topic.decode().split(MessageEndpoints._device_read + "/")[-1].split(":sub")[0]
        msg = BMessage.DeviceMessage.loads(msg.value)
        if msg.content["signals"].get(dev) is not None:
            parent._add_device_to_storage(
                msg.metadata["scanID"], dev, msg.content["signals"], msg.metadata
            )
        else:
            logger.warning(f"Received reading from unknown device {dev}")

    @staticmethod
    def _scan_queue_callback(msg, parent, **kwargs):
        msg = BMessage.ScanQueueStatusMessage.loads(msg.value)
        print(msg)
        for q in msg.content["queue"]["primary"].get("info"):
            for rb in q.get("request_blocks"):
                if rb.get("is_scan"):
                    parent.metadata[rb["scanID"]] = q
                    parent._initialize_scan_container(rb)

    @staticmethod
    def _scan_status_callback(msg, parent, **kwargs):
        msg = BMessage.ScanStatusMessage.loads(msg.value)
        if msg.content.get("status") != "open":
            parent._scan_status_modification(msg)

    def _scan_status_modification(self, msg: BMessage.ScanStatusMessage):
        if msg.content.get("status") == "closed":
            scanID = msg.content.get("scanID")
            if scanID:
                doc = {
                    "time": time.time(),
                    "uid": str(uuid.uuid4()),
                    "scanID": scanID,
                    "run_start": self.bluesky_metadata[scanID]["start"]["uid"],
                    "exit_status": "success",
                    "reason": "",
                    "num_events": msg.content["info"].get("points") + 1,
                }
                self.bluesky_metadata[scanID]["stop"] = doc
                self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("stop", doc)))

    def _initialize_scan_container(self, queue):
        scanID = queue["scanID"]
        scan_motors = list(set([self.DM.devices[m] for m in queue["scan_motors"]]))
        self.scan_motors[scanID] = scan_motors
        if not scanID in self.sync_storage:
            self.sync_storage[scanID] = dict()
            self.bluesky_metadata[scanID] = dict()
            # for now lets assume that all devices are primary devices:
            self.primary_devices[scanID] = {
                "devices": self.DM.devices.primary_devices(scan_motors),
                "pointID": {},
            }
            self.monitor_devices[scanID] = dict()
            self.baseline_devices[scanID] = {
                "devices": self.DM.devices.baseline_devices(scan_motors),
                "done": {dev.name: False for dev in self.DM.devices.baseline_devices(scan_motors)},
            }
            self.send_run_start_document(scanID)

    def send_run_start_document(self, scanID) -> None:
        #  {'data_session': 'vist54321',
        # 'data_groups': ['bl42', 'proposal12345'],
        # 'detectors': ['random_walk:x'],
        # 'hints': {'dimensions': [(['random_walk:dt'], 'primary')]},
        # 'motors': ('random_walk:dt',),
        # 'num_intervals': 2,
        # 'num_points': 3,
        # 'plan_args': {'args': ["EpicsSignal(read_pv='random_walk:dt', " "name='random_walk:dt', " 'value=1.0, ' 'timestamp=1550070001.828528, ' 'auto_monitor=False, ' 'string=False, ' "write_pv='random_walk:dt', " 'limits=False, ' 'put_complete=False)', -1, 1],
        #             'detectors': ["EpicsSignal(read_pv='random_walk:x', " "name='random_walk:x', " 'value=1.61472277847348, ' 'timestamp=1550070000.807677, ' 'auto_monitor=False, ' 'string=False, ' "write_pv='random_walk:x', " 'limits=False, ' 'put_complete=False)'],
        #             'num': 3,
        #             'per_step': 'None'},
        # 'plan_name': 'scan',
        # 'plan_pattern': 'inner_product',
        # 'plan_pattern_args': {'args': ["EpicsSignal(read_pv='random_walk:dt', " "name='random_walk:dt', " 'value=1.0, ' 'timestamp=1550070001.828528, ' 'auto_monitor=False, ' 'string=False, ' "write_pv='random_walk:dt', " 'limits=False, ' 'put_complete=False)', -1, 1],
        #                     'num': 3},
        # 'plan_pattern_module': 'bluesky.plan_patterns',
        # 'plan_type': 'generator',
        # 'scan_id': 2,
        # 'time': 1550070004.9850419,
        # 'uid': 'ba1f9076-7925-4af8-916e-0e1eaa1b3c47'}

        doc = {
            "time": time.time(),
            "uid": str(uuid.uuid4()),
            "scanID": scanID,
            "queueID": self.metadata[scanID]["queueID"],
            "scan_id": self.metadata[scanID]["scan_number"],
            "request_blocks": self.metadata[scanID]["request_blocks"],
            "motors": tuple([dev.name for dev in self.scan_motors[scanID]]),
        }
        self.bluesky_metadata[scanID]["start"] = doc
        self.producer.send(MessageEndpoints.bluesky_events(), msgpack.dumps(("start", doc)))
        self.send_descriptor_document(scanID)

    def send_descriptor_document(self, scanID) -> None:
        def _get_data_keys():
            signals = {}
            for dev in self.primary_devices[scanID]["devices"]:
                # copied from bluesky/callbacks/stream.py:
                for k, v in dev.signals.items():
                    val = v["value"]
                    # String key
                    if isinstance(val, str):
                        key_desc = {"dtype": "string", "shape": []}
                    # Iterable
                    elif isinstance(val, Iterable):
                        key_desc = {"dtype": "array", "shape": np.shape(val)}
                    # Number
                    else:
                        key_desc = {"dtype": "number", "shape": []}
                    signals[k] = key_desc
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

    def _add_device_to_storage(self, scanID, device, signal, metadata):
        while not scanID in self.sync_storage:
            time.sleep(0.1)
        dev = {device: signal}
        if metadata["stream"] == "primary":
            if "pointID" in metadata:
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

                if all(status for status in primary_devices["pointID"][pointID].values()):
                    self._update_monitor_signals(scanID, pointID)
                    self._send_scan_point(scanID, pointID)

        elif metadata["stream"] == "baseline":
            baseline_devices_status = self.baseline_devices[scanID]["done"]
            baseline_devices_status[device] = True

            self.sync_storage[scanID]["baseline"] = {
                **self.sync_storage[scanID].get("baseline", {}),
                **dev,
            }

            if all(status for status in baseline_devices_status.values()):
                print("Baseline: ", self.sync_storage[scanID]["baseline"])

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
        pass

    def _send_scan_point(self, scanID, pointID) -> None:
        print(pointID, self.sync_storage[scanID][pointID])

        self.producer.send(
            MessageEndpoints.scan_segment(),
            BMessage.ScanMessage(
                point_id=pointID,
                scanID=scanID,
                data=self.sync_storage[scanID][pointID],
                metadata=self.metadata[scanID],
            ).dumps(),
        )
        self.producer.send(
            MessageEndpoints.bluesky_events(),
            msgpack.dumps(("event", self._prepare_bluesky_event_data(scanID, pointID))),
        )
        self.sync_storage[scanID].pop(pointID)

    def shutdown(self):
        self.DM.shutdown()
