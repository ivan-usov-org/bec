import datetime
import threading
import time
from asyncio.log import logger
from enum import Enum

import msgpack
from bec_utils import Alarms, BECMessage, DeviceStatus, MessageEndpoints, bec_logger

logger = bec_logger.logger

DeviceMsg = BECMessage.DeviceInstructionMessage
ScanStatusMsg = BECMessage.ScanStatusMessage


class InstructionQueueStatus(Enum):
    STOPPED = -1
    PENDING = 0
    IDLE = 1
    PAUSED = 2
    DEFERRED_PAUSE = 3
    RUNNING = 4
    COMPLETED = 5


class ScanAbortion(Exception):
    pass


class ScanWorker(threading.Thread):
    """
    Scan worker receives device instructions and pre-processes them before sending them to OPAAS
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
        self.reset()

    def _get_devices_from_instruction(self, instr) -> list:
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

    def _add_wait_group(self, instr) -> None:
        wait_group = instr.content["parameter"].get("wait_group")
        action = instr.content["action"]
        if wait_group and action != "wait":

            devices = self._get_devices_from_instruction(instr)
            DIID = instr.metadata["DIID"]
            if wait_group in self._groups:
                self._groups[wait_group].extend([(dev.name, DIID) for dev in devices])
            else:
                self._groups[wait_group] = [(dev.name, DIID) for dev in devices]

    def _wait_for_devices(self, instr) -> None:
        wait_type = instr.content["parameter"].get("type")

        if wait_type == "move":
            self._wait_for_idle(instr)
        elif wait_type == "read":
            self._wait_for_read(instr)
        elif wait_type == "trigger":
            self._wait_for_trigger(instr)
        else:
            logger.error("Unkown wait command")

    def _wait_for_idle(self, instr) -> None:
        """Wait for devices to become IDLE

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler
        """
        start = datetime.datetime.now()

        wait_group = instr.content["parameter"].get("wait_group")
        logger.debug("Waiting for devices:", wait_group)
        if wait_group is not None:
            if wait_group in self._groups:
                group_devices = [dev.name for dev in self._get_devices_from_instruction(instr)]
                wait_group_devices = [
                    dev for dev in self._groups[wait_group] if dev[0] in group_devices
                ]
                while True:
                    pipe = self.device_manager.producer.pipeline()
                    for dev, _ in wait_group_devices:
                        self.device_manager.producer.get(
                            MessageEndpoints.device_req_status(dev), pipe
                        )
                    device_status = pipe.execute()
                    self._check_for_interruption()
                    if None in device_status:
                        continue
                    device_status = [
                        BECMessage.DeviceReqStatusMessage.loads(dev) for dev in device_status
                    ]
                    devices_moved_successfully = all(
                        dev.content["success"] for dev in device_status
                    )
                    matching_scanID = all(
                        dev.metadata.get("scanID") == instr.metadata["scanID"]
                        for dev in device_status
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

                    elif not devices_moved_successfully:
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

    def _wait_for_read(self, instr) -> None:
        start = datetime.datetime.now()

        wait_group = instr.content["parameter"].get("wait_group")
        logger.debug("Waiting for devices:", wait_group)
        if wait_group is not None:
            if wait_group in self._groups:
                group_devices = [dev.name for dev in self._get_devices_from_instruction(instr)]
                wait_group_devices = [
                    dev for dev in self._groups[wait_group] if dev[0] in group_devices
                ]
                while True:
                    pipe = self.device_manager.producer.pipeline()
                    for dev, _ in wait_group_devices:
                        self.device_manager.producer.get(MessageEndpoints.device_status(dev), pipe)
                    device_status = pipe.execute()
                    self._check_for_interruption()
                    if None in device_status:
                        continue
                    device_status = [msgpack.loads(dev) for dev in device_status]
                    devices_are_idle = all(
                        DeviceStatus(dev.get("status")) == DeviceStatus.IDLE
                        for dev in device_status
                    )
                    matching_scanID = all(
                        dev.get("scanID") == instr.metadata["scanID"] for dev in device_status
                    )
                    matching_DIID = all(
                        dev.get("DIID") == wait_group_devices[ii][1]
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

    def _wait_for_trigger(self, instr) -> None:
        time.sleep(float(instr.content["parameter"]["time"]))

    def _set_devices(self, instr) -> None:
        """Send device instruction to set a device to a specific value

        Args:
            instr (DeviceInstructionMessage): Device instruction received from the scan assembler
        """

        # send instruction
        self.device_manager.producer.send(MessageEndpoints.device_instructions(), instr.dumps())

    def _trigger_devices(self, instr) -> None:
        # self._get_triggerable_devices()
        pass

    def _send_rpc(self, instr) -> None:
        self.device_manager.producer.send(MessageEndpoints.device_instructions(), instr.dumps())

    def _read_devices(self, instr) -> None:
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

    def _baseline_reading(self, instr) -> None:
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

    def _open_scan(self, instr) -> None:
        if not self.scan_id:
            self.scan_id = instr.metadata.get("scanID")
            if instr.content["parameter"].get("primary") is not None:
                self.scan_motors = [
                    self.device_manager.devices[dev]
                    for dev in instr.content["parameter"].get("primary")
                ]
            # self.parent.scan_number += 1
        if instr.content["parameter"].get("num_points"):
            self.current_scan_info["points"] = instr.content["parameter"].get("num_points")
            self._send_scan_status("open")

    def _close_scan(self, instr, max_point_id) -> None:
        scan_id = instr.metadata.get("scanID")
        if self.scan_id == scan_id:
            self.scan_id = None
            self.current_scan_info["points"] = max_point_id
            self.device_manager.producer.send(
                MessageEndpoints.scan_status(),
                ScanStatusMsg(
                    scanID=self.current_scanID, status="closed", info=self.current_scan_info
                ).dumps(),
            )

    def _send_scan_status(self, status: str):
        self.device_manager.producer.send(
            MessageEndpoints.scan_status(),
            ScanStatusMsg(
                scanID=self.current_scanID,
                status=status,
                info=self.current_scan_info,
            ).dumps(),
        )

    def _process_instructions(self, queue) -> None:
        """
        Process scan instructions and send DeviceInstructions to OPAAS.
        For now this is an in-memory communication. In the future however,
        we might want to pass it through a dedicated Kafka topic.
        Args:
            queue: instruction queue

        Returns:

        """
        start = time.time()
        max_point_id = 0

        def _instruction_step(instr):
            action = instr.content.get("action")
            scan_def_id = instr.metadata.get("scan_def_id")
            if "pointID" in instr.metadata:
                nonlocal max_point_id
                max_point_id = instr.metadata["pointID"]
            if action == "open_scan":
                self._open_scan(instr)
            elif action == "close_scan" and scan_def_id is None:
                self._close_scan(instr, max_point_id)
            elif action == "close_scan_def":
                self._close_scan(instr, max_point_id)

            if self.current_scanID != instr.metadata.get("scanID"):
                self.current_scanID = instr.metadata.get("scanID")
                self.current_scan_info = instr.metadata
                self.current_scan_info.update({"scan_number": self.parent.scan_number})
                if self.current_scanID:
                    self._send_scan_status("open")

            logger.debug("Device instruction: ", instr)

            self._add_wait_group(instr)

            # TODO: for interception:
            self._check_for_interruption()
            if action == "wait":
                self._wait_for_devices(instr)
            elif action == "trigger":
                self._trigger_devices(instr)
            elif action == "set":
                self._set_devices(instr)
            elif action == "read":
                self._read_devices(instr)
            elif action == "baseline_reading":
                self._baseline_reading(instr)
            elif action == "rpc":
                self._send_rpc(instr)

        queue.is_active = True
        for instr in queue:
            if instr is not None:
                self._check_for_interruption()
                _instruction_step(instr)
        queue.is_active = False

        logger.info(f"QUEUE ITEM finished after {time.time()-start:.2f} seconds")
        self.reset()

    def reset(self):
        self._groups = dict()
        self.current_scanID = ""
        self.current_scan_info = dict()
        self.scan_id = None
        self.interception_msg = None
        self.scan_motors = []

    def run(self):
        try:
            while not self.signal_event.is_set():
                try:
                    for queue in self.parent.queue_manager.queues["primary"]:
                        self._process_instructions(queue)
                except ScanAbortion:
                    self.parent.queue_manager.queues["primary"].abort()
                    self.reset()
        except AttributeError as exc:
            if exc.__cause__:
                content = str(exc.__cause__)
            elif len(exc.args) > 0:
                content = exc.args[0]
            else:
                content = ""
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
