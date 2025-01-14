from __future__ import annotations

import datetime
import itertools
import threading
import time
import traceback
from typing import TYPE_CHECKING

import numpy
from blissdata.redis_engine.store import DataStore
from blissdata.streams.base import Stream

from bec_lib import messages
from bec_lib.alarm_handler import Alarms
from bec_lib.endpoints import MessageEndpoints
from bec_lib.file_utils import FileWriter
from bec_lib.logger import bec_logger

from .blissdata_utils import bec_scan_info_to_blissdata_scan_info
from .errors import ScanAbortion
from .scan_queue import InstructionQueueItem, InstructionQueueStatus, RequestBlock
from .scan_stubs import ScanStubStatus

logger = bec_logger.logger

if TYPE_CHECKING:
    from bec_server.scan_server.scan_server import ScanServer


class ScanWorker(threading.Thread):
    """
    Scan worker receives device instructions and pre-processes them before sending them to the device server
    """

    def __init__(self, *, parent: ScanServer, queue_name: str = "primary"):
        super().__init__(daemon=True)
        self._data_store = None
        self._blissdata_scan = {}
        self.queue_name = queue_name
        self.name = f"ScanWorker-{queue_name}"
        self.parent = parent
        self.device_manager = self.parent.device_manager
        self.connector = self.parent.connector
        self.status = InstructionQueueStatus.IDLE
        self.signal_event = threading.Event()
        self.scan_id = None
        self.scan_motors = []
        self.readout_priority = {}
        self.scan_type = None
        self.current_scan_id = None
        self.current_scan_info = None
        self.max_point_id = 0
        self._exposure_time = None
        self.current_instruction_queue_item = None
        self.interception_msg = None
        self.reset()

    def open_scan(self, instr: messages.DeviceInstructionMessage) -> None:
        """
        Open a new scan and emit a scan status message.

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler

        """
        if not self.scan_id:
            self.scan_id = instr.metadata.get("scan_id")
            if instr.content["parameter"].get("scan_motors") is not None:
                self.scan_motors = [
                    self.device_manager.devices[dev]
                    for dev in instr.content["parameter"].get("scan_motors")
                ]
                self.readout_priority = instr.content["parameter"].get("readout_priority", {})
            self.scan_type = instr.content["parameter"].get("scan_type")

        if not instr.metadata.get("scan_def_id"):
            self.max_point_id = 0
        instr_num_points = instr.content["parameter"].get("num_points", 0)
        if instr_num_points is None:
            instr_num_points = 0
        num_points = self.max_point_id + instr_num_points
        if self.max_point_id:
            num_points += 1

        active_rb = self.current_instruction_queue_item.active_request_block

        self._initialize_scan_info(active_rb, instr, num_points)

        # from here, self.current_scan_info is populated
        if self._data_store is None:
            # new scan
            service = self.device_manager._service
            redis_data_url = f"redis://{service._service_config.redis_data}"
            self._data_store = DataStore(redis_data_url)

        bliss_scan_id = {
            "name": self.current_scan_info["scan_name"],
            "number": self.current_scan_info["scan_number"],
            "data_policy": "no_policy",
            "session": "bec",
        }

        # read info about monitored devices ;
        # create blissdata scan_info structure
        devname_channels, scan_info = bec_scan_info_to_blissdata_scan_info(
            self.current_scan_info, self.connector
        )

        new_blissdata_scan = self._data_store.create_scan(bliss_scan_id, info=scan_info)

        data_streams = {}
        for dev_name, channel_info_list in devname_channels.items():
            data_streams[dev_name] = [
                new_blissdata_scan.create_stream(
                    Stream.recipe(
                        channel_info.name, channel_info.dtype, channel_info.shape, info={}
                    )
                )
                for channel_info in channel_info_list
            ]
        self._blissdata_scan[self.scan_id] = (new_blissdata_scan, data_streams)

        # after 'prepare', clients can connect to streams
        new_blissdata_scan.prepare()

        # now we can tell devices about their data streams
        for dev_name, streams in data_streams.items():
            if dev_name.startswith("axis:"):
                dev_name = dev_name[5:]
            msg = messages.DeviceStreamInfoMessage(
                scan_key=new_blissdata_scan.key,
                device_name=dev_name,
                stream_names=[stream.name for stream in streams],
            )
            self.connector.send(MessageEndpoints.device_blissdata_stream(dev_name), msg)

        # only append the scan_progress if the scan is not using device_progress
        if active_rb.scan.use_scan_progress_report:
            if not self.scan_report_instructions or not self.scan_report_instructions[-1].get(
                "device_progress"
            ):
                self.scan_report_instructions.append({"scan_progress": num_points})
        self.current_instruction_queue_item.parent.queue_manager.send_queue_status()

        new_blissdata_scan.start()
        self._send_scan_status("open")

    def close_scan(self, instr: messages.DeviceInstructionMessage, max_point_id: int) -> None:
        """
        Close a scan and emit a scan status message.

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler
            max_point_id (int): Maximum point ID of the scan
        """
        scan_id = instr.metadata.get("scan_id")

        if self.scan_id != scan_id:
            return

        try:
            bliss_scan, data_streams = self._blissdata_scan[self.scan_id]
        except KeyError:
            # are we in tests ?
            pass
        else:
            # close blissdata streams
            for stream in itertools.chain(*data_streams.values()):
                stream.seal()
            bliss_scan.stop()
            bliss_scan.info["end_reason"] = "SUCCESS"
            bliss_scan.info["end_time"] = datetime.datetime.now().astimezone().isoformat()
            bliss_scan.close()
            del self._blissdata_scan[self.scan_id]

        # reset the scan ID now that the scan will be closed
        self.scan_id = None

        scan_info = self.current_scan_info
        if scan_info.get("scan_type") == "fly":
            # flyers do not increase the point_id but instead set the num_points directly
            num_points = self.current_instruction_queue_item.active_request_block.scan.num_pos
            self.current_scan_info["num_points"] = num_points
        else:
            # point_id starts at 0
            scan_info["num_points"] = max_point_id + 1

        self._send_scan_status("closed")

    def publish_data_as_read(self, instr: messages.DeviceInstructionMessage):
        """
        Publish data as read by sending a DeviceMessage to the device_read endpoint.
        This instruction replicates the behaviour of the device server when it receives a read instruction.

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler
        """
        connector = self.device_manager.connector
        data = instr.content["parameter"]["data"]
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]
        if not isinstance(data, list):
            data = [data]
        for device, dev_data in zip(devices, data):
            msg = messages.DeviceMessage(signals=dev_data, metadata=instr.metadata)
            connector.set_and_publish(MessageEndpoints.device_read(device), msg)

    def process_scan_report_instruction(self, instr):
        """
        Process a scan report instruction by appending it to the scan_report_instructions list.

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler

        """
        self.scan_report_instructions.append(instr.content["parameter"])
        self.current_instruction_queue_item.parent.queue_manager.send_queue_status()

    def forward_instruction(self, instr: messages.DeviceInstructionMessage) -> None:
        """
        Forward an instruction to the device server.

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler

        """
        self.connector.send(MessageEndpoints.device_instructions(), instr)

    @property
    def scan_report_instructions(self):
        """
        List of scan report instructions
        """
        req_block = self.current_instruction_queue_item.active_request_block
        return req_block.scan_report_instructions

    def _wait_for_device_server(self) -> None:
        self.parent.wait_for_service("DeviceServer")

    def _check_for_interruption(self) -> None:
        if self.status == InstructionQueueStatus.PAUSED:
            self._send_scan_status("paused")
        while self.status == InstructionQueueStatus.PAUSED:
            time.sleep(0.1)
        if self.status == InstructionQueueStatus.STOPPED:
            raise ScanAbortion

    def _initialize_scan_info(
        self, active_rb: RequestBlock, instr: messages.DeviceInstructionMessage, num_points: int
    ):
        metadata = active_rb.metadata
        self.current_scan_info = {**instr.metadata, **instr.content["parameter"]}
        self.current_scan_info.update(metadata)
        self.current_scan_info.update(
            {
                "scan_number": self.parent.scan_number,
                "dataset_number": self.parent.dataset_number,
                "exp_time": self._exposure_time,
                "frames_per_trigger": active_rb.scan.frames_per_trigger,
                "settling_time": active_rb.scan.settling_time,
                "readout_time": active_rb.scan.readout_time,
                "acquisition_config": active_rb.scan.acquisition_config,
                "scan_report_devices": active_rb.scan.scan_report_devices,
                "monitor_sync": active_rb.scan.monitor_sync,
                "num_points": num_points,
            }
        )
        scan_args = active_rb.scan.parameter["args"]
        scan_kwargs = active_rb.scan.parameter["kwargs"]
        system_config = scan_kwargs.get("system_config", {"file_suffix": "", "file_directory": ""})
        user_suffix = system_config["file_suffix"]
        scan_dir = system_config["file_directory"]
        service_config = self.device_manager._service._service_config
        file_writer_service_config = service_config.service_config.get("file_writer")
        self.current_scan_info["scan_file_path"] = FileWriter(
            service_config=file_writer_service_config
        ).compile_full_filename(
            create_dir=False,
            scan_number=self.parent.scan_number,
            user_suffix=user_suffix,
            scan_dir=scan_dir,
        )

        self.current_scan_info["scan_msgs"] = [
            str(scan_msg) for scan_msg in self.current_instruction_queue_item.scan_msgs
        ]
        self.current_scan_info["args"] = scan_args
        self.current_scan_info["kwargs"] = scan_kwargs
        self.current_scan_info["readout_priority"] = {
            "monitored": [
                dev.full_name
                for dev in self.device_manager.devices.monitored_devices(
                    readout_priority=self.readout_priority
                )
            ],
            "baseline": [
                dev.full_name
                for dev in self.device_manager.devices.baseline_devices(
                    readout_priority=self.readout_priority
                )
            ],
            "async": [
                dev.full_name
                for dev in self.device_manager.devices.async_devices(
                    readout_priority=self.readout_priority
                )
            ],
            "continuous": [
                dev.full_name
                for dev in self.device_manager.devices.continuous_devices(
                    readout_priority=self.readout_priority
                )
            ],
            "on_request": [
                dev.full_name
                for dev in self.device_manager.devices.on_request_devices(
                    readout_priority=self.readout_priority
                )
            ],
        }

    def _send_scan_status(self, status: str):
        current_scan_info_print = self.current_scan_info.copy()
        if current_scan_info_print.get("positions", []):
            current_scan_info_print["positions"] = "..."
        logger.info(
            f"New scan status: {self.current_scan_id} / {status} / {current_scan_info_print}"
        )
        msg = messages.ScanStatusMessage(
            scan_id=self.current_scan_id, status=status, info=self.current_scan_info
        )
        expire = None if status in ["open", "paused"] else 1800
        pipe = self.device_manager.connector.pipeline()
        self.device_manager.connector.set(
            MessageEndpoints.public_scan_info(self.current_scan_id), msg, pipe=pipe, expire=expire
        )
        self.device_manager.connector.set_and_publish(
            MessageEndpoints.scan_status(), msg, pipe=pipe
        )
        pipe.execute()

    def update_instr_with_scan_report(self, instr: messages.DeviceInstructionMessage):
        if not self.scan_report_instructions:
            return
        for scan_report in self.scan_report_instructions:
            if "readback" not in scan_report:
                continue
            readback = scan_report["readback"]
            instr_device = (
                instr.content["device"]
                if isinstance(instr.content["device"], list)
                else [instr.content["device"]]
            )

            if set(readback.get("devices", [])) & set(instr_device):
                instr.metadata["response"] = True

    def _process_instructions(self, queue: InstructionQueueItem) -> None:
        """
        Process scan instructions and send DeviceInstructions to OPAAS.
        For now this is an in-memory communication. In the future however,
        we might want to pass it through a dedicated Kafka topic.
        Args:
            queue: instruction queue

        Returns:

        """
        if not queue:
            return None
        self.current_instruction_queue_item = queue

        start = time.time()
        self.max_point_id = 0

        # make sure the device server is ready to receive data
        self._wait_for_device_server()

        queue.is_active = True
        try:
            for instr in queue:
                self._check_for_interruption()
                if instr is None:
                    continue
                self._exposure_time = getattr(queue.active_request_block.scan, "exp_time", None)
                self._instruction_step(instr)
        except ScanAbortion as exc:
            if queue.stopped or not (queue.return_to_start and queue.active_request_block):
                raise ScanAbortion from exc
            queue.stopped = True
            try:
                cleanup = queue.active_request_block.scan.move_to_start()
                self.status = InstructionQueueStatus.RUNNING
                for instr in cleanup:
                    self._check_for_interruption()
                    instr.metadata["scan_id"] = queue.queue.active_rb.scan_id
                    instr.metadata["queue_id"] = queue.queue_id
                    self._instruction_step(instr)
            except Exception as exc_return_to_start:
                # if the return_to_start fails, raise the original exception
                content = traceback.format_exc()
                logger.error(content)
                self.connector.raise_alarm(
                    severity=Alarms.MAJOR,
                    source={"ScanWorker": "_process_instructions"},
                    msg=content,
                    alarm_type=exc_return_to_start.__class__.__name__,
                    metadata={},
                )
                raise ScanAbortion from exc
            raise ScanAbortion from exc
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(content)
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source={"ScanWorker": "_process_instructions"},
                msg=content,
                alarm_type=exc.__class__.__name__,
                metadata={},
            )
            raise ScanAbortion from exc
        queue.is_active = False
        queue.status = InstructionQueueStatus.COMPLETED
        self.current_instruction_queue_item = None

        logger.info(f"QUEUE ITEM finished after {time.time()-start:.2f} seconds")
        self.reset()

    def _instruction_step(self, instr: messages.DeviceInstructionMessage):
        logger.debug(instr)
        action = instr.content.get("action")
        scan_def_id = instr.metadata.get("scan_def_id")
        if self.current_scan_id != instr.metadata.get("scan_id"):
            self.current_scan_id = instr.metadata.get("scan_id")

        if "point_id" in instr.metadata:
            self.max_point_id = instr.metadata["point_id"]

        logger.debug(f"Device instruction: {instr}")
        self._check_for_interruption()

        if action == "open_scan":
            self.open_scan(instr)
        elif action == "close_scan" and scan_def_id is None:
            self.close_scan(instr, self.max_point_id)
        elif action == "close_scan" and scan_def_id is not None:
            pass
        elif action == "open_scan_def":
            pass
        elif action == "close_scan_def":
            self.close_scan(instr, self.max_point_id)
        elif action == "publish_data_as_read":
            self.publish_data_as_read(instr)
        elif action == "scan_report_instruction":
            self.process_scan_report_instruction(instr)
        elif action == "set":
            self.update_instr_with_scan_report(instr)
            self.forward_instruction(instr)
        elif action in [
            "trigger",
            "kickoff",
            "complete",
            "baseline_reading",
            "pre_scan",
            "rpc",
            "read",
            "stage",
            "unstage",
        ]:
            self.forward_instruction(instr)

        else:
            raise ValueError(f"Unknown device instruction: {instr}")

    def reset(self):
        """reset the scan worker and its member variables"""
        self.current_scan_id = ""
        self.current_scan_info = {}
        self.scan_id = None
        self.interception_msg = None
        self.scan_motors = []

    def cleanup(self):
        """perform cleanup instructions"""
        status = ScanStubStatus(self.parent.queue_manager.instruction_handler)
        staged_devices = [dev.root.name for dev in self.device_manager.devices.enabled_devices]
        msg = messages.DeviceInstructionMessage(
            device=staged_devices,
            action="unstage",
            parameter={},
            metadata={"device_instr_id": status._device_instr_id},
        )
        self.forward_instruction(msg)
        # status.wait()

    def run(self):
        try:
            while not self.signal_event.is_set():
                try:
                    for queue in self.parent.queue_manager.queues[self.queue_name]:
                        self._process_instructions(queue)
                        if self.signal_event.is_set():
                            break
                        if not queue.stopped:
                            queue.append_to_queue_history()

                except ScanAbortion:
                    content = traceback.format_exc()
                    logger.error(content)
                    queue.queue.increase_scan_number()
                    if queue.return_to_start:
                        self._send_scan_status("aborted")
                    else:
                        self._send_scan_status("halted")
                    logger.info(f"Scan aborted: {queue.queue_id}")
                    queue.status = InstructionQueueStatus.STOPPED
                    queue.append_to_queue_history()
                    self.cleanup()
                    self.parent.queue_manager.queues[self.queue_name].abort()
                    self.reset()
                    self.status = InstructionQueueStatus.RUNNING

        # pylint: disable=broad-except
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(content)
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source={"ScanWorker": "run"},
                msg=content,
                alarm_type=exc.__class__.__name__,
                metadata={},
            )
            if self.queue_name in self.parent.queue_manager.queues:
                self.parent.queue_manager.queues[self.queue_name].abort()
            self.reset()
            logger.error(f"Scan worker stopped: {exc}. Unrecoverable error.")

    def shutdown(self):
        """shutdown the scan worker"""
        self.signal_event.set()
        if self._started.is_set():
            self.join()
