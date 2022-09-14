import datetime
import threading
import time
import traceback
from asyncio.log import logger
from typing import List

from bec_utils import (
    Alarms,
    BECMessage,
    Device,
    DeviceStatus,
    MessageEndpoints,
    bec_logger,
)

from .bkqueue import InstructionQueueItem, InstructionQueueStatus
from .errors import DeviceMessageError, ScanAbortion

logger = bec_logger.logger

DeviceMsg = BECMessage.DeviceInstructionMessage
ScanStatusMsg = BECMessage.ScanStatusMessage


class ScanWorker(threading.Thread):
    """
    Scan worker receives device instructions and pre-processes them before sending them to the device server
    """

    def __init__(self, *, parent):
        super().__init__()
        self.parent = parent
        self.device_manager = self.parent.device_manager
        self.connector = self.parent.connector
        self.status = InstructionQueueStatus.IDLE
        self.signal_event = threading.Event()
        self.scan_id = None
        self.scan_motors = []
        self.current_scanID = None
        self.current_scan_info = None
        self._staged_devices = set()
        self.max_point_id = 0
        self.reset()

    def _get_devices_from_instruction(self, instr: DeviceMsg) -> List[Device]:
        """Extract devices from instruction message

        Args:
            instr (DeviceMsg): DeviceInstructionMessage

        Returns:
            List[Device]: List of devices
        """
        devices = []
        if not instr.content.get("device"):
            group = instr.content["parameter"].get("group")
            if group == "primary":
                devices = self.device_manager.devices.primary_devices(self.scan_motors)
            elif group == "scan_motor":
                devices = self.scan_motors
        else:
            instr_devices = instr.content.get("device")
            if not isinstance(instr_devices, list):
                instr_devices = [instr_devices]
            devices = [self.device_manager.devices[dev] for dev in instr_devices]
        return devices

    def _add_wait_group(self, instr: DeviceMsg) -> None:
        """If needed, add a wait_group. This wait_group can later be used to
        wait for instructions to complete before continuing.

        Example:
            DeviceInstructionMessage(({'device': ['samx', 'samy'], 'action': 'read', 'parameter': {'group': 'scan_motor', 'wait_group': 'scan_motor'}}, {DIID': 0,...}))

            This instruction would create a new wait_group entry for the devices samx and samy, to finish DIID 0.

        Args:
            instr (DeviceMsg): DeviceInstructionMessage

        """
        wait_group = instr.content["parameter"].get("wait_group")
        action = instr.content["action"]
        if not wait_group or action == "wait":
            return

        devices = self._get_devices_from_instruction(instr)
        DIID = instr.metadata.get("DIID")
        if DIID is None:
            raise DeviceMessageError("Device message metadata does not contain a DIID entry.")

        if wait_group in self._groups:
            self._groups[wait_group].extend([(dev.name, DIID) for dev in devices])
        else:
            self._groups[wait_group] = [(dev.name, DIID) for dev in devices]

    def _wait_for_devices(self, instr: DeviceMsg) -> None:
        wait_type = instr.content["parameter"].get("type")

        if wait_type == "move":
            self._wait_for_idle(instr)
        elif wait_type == "read":
            self._wait_for_read(instr)
        elif wait_type == "trigger":
            self._wait_for_trigger(instr)
        else:
            logger.error("Unkown wait command")
            raise DeviceMessageError("Unkown wait command")

    def _get_device_status(self, devices: list) -> list:
        pipe = self.device_manager.producer.pipeline()
        for dev in devices:
            self.device_manager.producer.get(MessageEndpoints.device_req_status(dev), pipe)
        return pipe.execute()

    def _wait_for_idle(self, instr: DeviceMsg) -> None:
        """Wait for devices to become IDLE

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler
        """
        start = datetime.datetime.now()

        wait_group = instr.content["parameter"].get("wait_group")

        if not wait_group or wait_group not in self._groups:
            return

        group_devices = [dev.name for dev in self._get_devices_from_instruction(instr)]
        wait_group_devices = [dev for dev in self._groups[wait_group] if dev[0] in group_devices]

        logger.debug(f"Waiting for devices: {wait_group}")

        while True:
            device_status = self._get_device_status([dev for dev, _ in wait_group_devices])
            self._check_for_interruption()

            if None in device_status:
                continue

            device_status = [BECMessage.DeviceReqStatusMessage.loads(dev) for dev in device_status]
            devices_moved_successfully = all(dev.content["success"] for dev in device_status)
            matching_scanID = all(
                dev.metadata.get("scanID") == instr.metadata["scanID"] for dev in device_status
            )
            matching_requestID = all(
                dev.metadata.get("RID") == instr.metadata["RID"] for dev in device_status
            )
            matching_DIID = all(
                dev.metadata.get("DIID") == wait_group_devices[ii][1]
                for ii, dev in enumerate(device_status)
            )

            if (
                devices_moved_successfully
                and matching_scanID
                and matching_DIID
                and matching_requestID
            ):
                break

            if not devices_moved_successfully:
                ind = [dev.content["success"] for dev in device_status].index(False)
                failed_device = wait_group_devices[ind]

                # make sure that this is not an old message
                matching_DIID = (
                    device_status[ind].metadata.get("DIID") == wait_group_devices[ind][1]
                )
                matching_scanID = (
                    device_status[ind].metadata.get("scanID") == instr.metadata["scanID"]
                )
                if matching_DIID and matching_scanID:
                    last_pos = BECMessage.DeviceMessage.loads(
                        self.device_manager.producer.get(
                            MessageEndpoints.device_readback(failed_device[0])
                        )
                    ).content["signals"][failed_device[0]]["value"]
                    self.connector.raise_alarm(
                        severity=Alarms.MAJOR,
                        source=instr.content,
                        content=f"Movement of device {failed_device[0]} failed whilst trying to reach the target position. Last recorded position: {last_pos}",
                        alarm_type="MovementFailed",
                        metadata=instr.metadata,
                    )
                    raise ScanAbortion

        self._groups[wait_group] = [
            dev for dev in self._groups[wait_group] if dev not in wait_group_devices
        ]
        logger.debug("Finished waiting")
        logger.debug(datetime.datetime.now() - start)

    def _wait_for_read(self, instr: DeviceMsg) -> None:
        start = datetime.datetime.now()

        wait_group = instr.content["parameter"].get("wait_group")

        if not wait_group or wait_group not in self._groups:
            return

        group_devices = [dev.name for dev in self._get_devices_from_instruction(instr)]
        wait_group_devices = [dev for dev in self._groups[wait_group] if dev[0] in group_devices]

        logger.debug(f"Waiting for devices: {wait_group}")

        while True:
            pipe = self.device_manager.producer.pipeline()
            for dev, _ in wait_group_devices:
                self.device_manager.producer.get(MessageEndpoints.device_status(dev), pipe)
            device_status = pipe.execute()

            self._check_for_interruption()
            device_status = [BECMessage.DeviceStatusMessage.loads(dev) for dev in device_status]

            if None in device_status:
                continue
            devices_are_idle = all(
                DeviceStatus(dev.content.get("status")) == DeviceStatus.IDLE
                for dev in device_status
            )
            matching_scanID = all(
                dev.metadata.get("scanID") == instr.metadata["scanID"] for dev in device_status
            )
            matching_DIID = all(
                dev.metadata.get("DIID") == wait_group_devices[ii][1]
                for ii, dev in enumerate(device_status)
            )
            if devices_are_idle and matching_scanID and matching_DIID:
                break
            # time.sleep(1e-4)

        self._groups[wait_group] = [
            dev for dev in self._groups[wait_group] if dev not in wait_group_devices
        ]
        logger.debug("Finished waiting")
        logger.debug(datetime.datetime.now() - start)

    def _wait_for_trigger(self, instr: DeviceMsg) -> None:
        time.sleep(float(instr.content["parameter"]["time"]))

    def _set_devices(self, instr: DeviceMsg) -> None:
        """Send device instruction to set a device to a specific value

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler
        """

        # send instruction
        self.device_manager.producer.send(MessageEndpoints.device_instructions(), instr.dumps())

    def _trigger_devices(self, instr: DeviceMsg) -> None:
        devices = [dev.name for dev in self.device_manager.devices.detectors()]
        self.device_manager.producer.send(
            MessageEndpoints.device_instructions(),
            DeviceMsg(
                device=devices,
                action="trigger",
                parameter=instr.content["parameter"],
                metadata=instr.metadata,
            ).dumps(),
        )

    def _send_rpc(self, instr: DeviceMsg) -> None:
        self.device_manager.producer.send(MessageEndpoints.device_instructions(), instr.dumps())

    def _read_devices(self, instr: DeviceMsg) -> None:
        # devices = self.device_manager.devices.device_group("monitor")
        # devices.extend(self.scan_motors)
        devices = instr.content.get("device")
        if devices is None:
            devices = [
                dev.name for dev in self.device_manager.devices.primary_devices(self.scan_motors)
            ]
        self.device_manager.producer.send(
            MessageEndpoints.device_instructions(),
            DeviceMsg(
                device=devices,
                action="read",
                parameter=instr.content["parameter"],
                metadata=instr.metadata,
            ).dumps(),
        )

    def _kickoff_devices(self, instr: DeviceMsg) -> None:
        self.device_manager.producer.send(
            MessageEndpoints.device_instructions(),
            DeviceMsg(
                device=instr.content.get("device"),
                action="kickoff",
                parameter=instr.content["parameter"],
                metadata=instr.metadata,
            ).dumps(),
        )

    def _baseline_reading(self, instr: DeviceMsg) -> None:
        baseline_devices = [
            dev.name for dev in self.device_manager.devices.baseline_devices(self.scan_motors)
        ]
        self.device_manager.producer.send(
            MessageEndpoints.device_instructions(),
            DeviceMsg(
                device=baseline_devices,
                action="read",
                parameter=instr.content["parameter"],
                metadata=instr.metadata,
            ).dumps(),
        )

    def _check_for_interruption(self) -> None:
        while self.status == InstructionQueueStatus.PAUSED:
            time.sleep(0.1)
        if self.status == InstructionQueueStatus.STOPPED:
            raise ScanAbortion

    def _open_scan(self, instr: DeviceMsg) -> None:
        if not self.scan_id:
            self.scan_id = instr.metadata.get("scanID")
            if instr.content["parameter"].get("primary") is not None:
                self.scan_motors = [
                    self.device_manager.devices[dev]
                    for dev in instr.content["parameter"].get("primary")
                ]

        self.current_scan_info = {**instr.metadata, **instr.content["parameter"]}
        self.current_scan_info.update({"scan_number": self.parent.scan_number})
        self._send_scan_status("open")

    def _close_scan(self, instr: DeviceMsg, max_point_id: int) -> None:
        scan_id = instr.metadata.get("scanID")
        if self.scan_id == scan_id:
            self.scan_id = None
            self.current_scan_info["points"] = max_point_id
            self._send_scan_status("closed")

    def _stage_devices(self, instr: DeviceMsg) -> None:
        devices = [dev.name for dev in self.device_manager.devices.enabled_devices]
        self._staged_devices.update(devices)
        self.device_manager.producer.send(
            MessageEndpoints.device_instructions(),
            DeviceMsg(
                device=devices,
                action="stage",
                parameter=instr.content["parameter"],
                metadata=instr.metadata,
            ).dumps(),
        )

    def _unstage_devices(self, instr: DeviceMsg = None, devices: list = None) -> None:
        if not devices:
            devices = [dev.name for dev in self.device_manager.devices.enabled_devices]
        parameter = {} if not instr else instr.content["parameter"]
        metadata = {} if not instr else instr.metadata
        self._staged_devices.difference_update(devices)
        self.device_manager.producer.send(
            MessageEndpoints.device_instructions(),
            DeviceMsg(
                device=devices,
                action="unstage",
                parameter=parameter,
                metadata=metadata,
            ).dumps(),
        )

    def _send_scan_status(self, status: str):
        logger.info(f"New scan status: {self.current_scanID} / {status} / {self.current_scan_info}")
        msg = ScanStatusMsg(
            scanID=self.current_scanID,
            status=status,
            info=self.current_scan_info,
        ).dumps()
        expire = None if status == "open" else 1800
        pipe = self.device_manager.producer.pipeline()
        self.device_manager.producer.set(
            MessageEndpoints.public_scan_info(self.current_scanID), msg, pipe=pipe, expire=expire
        )
        self.device_manager.producer.set_and_publish(MessageEndpoints.scan_status(), msg, pipe=pipe)
        pipe.execute()

    def _process_instructions(self, queue: InstructionQueueItem) -> None:
        """
        Process scan instructions and send DeviceInstructions to OPAAS.
        For now this is an in-memory communication. In the future however,
        we might want to pass it through a dedicated Kafka topic.
        Args:
            queue: instruction queue

        Returns:

        """
        self.current_instruction_queue_item = queue

        start = time.time()
        self.max_point_id = 0

        queue.is_active = True
        try:
            for instr in queue:
                if instr is None:
                    continue
                self._check_for_interruption()
                self._instruction_step(instr)
        except ScanAbortion as exc:
            self._groups = {}
            if queue.stopped or not (queue.return_to_start and queue.active_request_block):
                raise ScanAbortion from exc
            queue.stopped = True
            cleanup = queue.active_request_block.scan.return_to_start()
            self.status = InstructionQueueStatus.RUNNING
            for instr in cleanup:
                self._check_for_interruption()
                instr.metadata["scanID"] = queue.queue.active_rb.scanID
                instr.metadata["queueID"] = queue.queue_id
                self._instruction_step(instr)
        queue.is_active = False
        queue.status = (
            InstructionQueueStatus.STOPPED if queue.stopped else InstructionQueueStatus.COMPLETED
        )
        self.current_instruction_queue_item = None

        logger.info(f"QUEUE ITEM finished after {time.time()-start:.2f} seconds")
        self.reset()

    def _instruction_step(self, instr: DeviceMsg):
        logger.debug(instr)
        action = instr.content.get("action")
        scan_def_id = instr.metadata.get("scan_def_id")
        if self.current_scanID != instr.metadata.get("scanID"):
            self.current_scanID = instr.metadata.get("scanID")

        if "pointID" in instr.metadata:
            self.max_point_id = instr.metadata["pointID"]

        self._add_wait_group(instr)

        logger.debug(f"Device instruction: {instr}")
        self._check_for_interruption()

        if action == "open_scan":
            self._open_scan(instr)
        elif action == "close_scan" and scan_def_id is None:
            self._close_scan(instr, self.max_point_id)
        elif action == "close_scan_def":
            self._close_scan(instr, self.max_point_id)
        elif action == "wait":
            self._wait_for_devices(instr)
        elif action == "trigger":
            self._trigger_devices(instr)
        elif action == "set":
            self._set_devices(instr)
        elif action == "read":
            self._read_devices(instr)
        elif action == "kickoff":
            self._kickoff_devices(instr)
        elif action == "baseline_reading":
            self._baseline_reading(instr)
        elif action == "rpc":
            self._send_rpc(instr)
        elif action == "stage":
            self._stage_devices(instr)
        elif action == "unstage":
            self._unstage_devices(instr)
        else:
            logger.warning(f"Unknown device instruction: {instr}")

    def reset(self):
        """reset the scan worker and its member variables"""
        self._groups = {}
        self.current_scanID = ""
        self.current_scan_info = {}
        self.scan_id = None
        self.interception_msg = None
        self.scan_motors = []

    def cleanup(self):
        """perform cleanup instructions"""
        self._unstage_devices(devices=list(self._staged_devices))

    def run(self):
        try:
            while not self.signal_event.is_set():
                try:
                    for queue in self.parent.queue_manager.queues["primary"]:
                        self._process_instructions(queue)
                        if not queue.stopped:
                            queue.append_to_queue_history()

                except ScanAbortion:
                    self._send_scan_status("aborted")
                    queue.status = InstructionQueueStatus.STOPPED
                    queue.append_to_queue_history()
                    self.cleanup()
                    self.parent.queue_manager.queues["primary"].abort()
                    self.reset()

        # pylint: disable=broad-except
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(content)
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source="ScanWorker",
                content=content,
                alarm_type=exc.__class__.__name__,
                metadata={},
            )
            self.parent.queue_manager.queues["primary"].abort()
            self.reset()
        finally:
            self.connector.shutdown()

    def shutdown(self):
        """shutdown the scan worker"""
        self.signal_event.set()
        self.join()
