from __future__ import annotations

import collections
import threading
import time
import uuid
from enum import Enum
from typing import Union

from bec_utils import Alarms, BECMessage, MessageEndpoints, bec_logger
from prettytable import PrettyTable

from scan_server.scan_assembler import ScanAssembler
from scan_server.scan_worker import InstructionQueueStatus, ScanAbortion, ScanWorker
from scan_server.scans import LimitError

logger = bec_logger.logger


class ScanQueueStatus(Enum):
    PAUSED = 0
    RUNNING = 1


class QueueManager:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, parent) -> None:
        self.parent = parent
        self.connector = parent.connector
        self.producer = parent.producer
        self.num_queues = 1
        self.key = ""
        self.queues = {"primary": ScanQueue(self)}
        self._start_scan_queue_consumer()

    def add_to_queue(self, scan_queue: str, msg: BECMessage.ScanQueueMessage) -> None:
        try:
            self.queues[scan_queue].append(msg)
        except Exception as exc:
            if exc.__cause__:
                content = str(exc.__cause__)
            elif len(exc.args) > 0:
                content = exc.args[0]
            else:
                content = ""
            logger.error(content)
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=msg.content,
                content=content,
                alarm_type=exc.__class__.__name__,
                metadata=msg.metadata,
            )

    def _start_scan_queue_consumer(self) -> None:
        self._scan_queue_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_insert(),
            cb=self._scan_queue_callback,
            parent=self,
        )
        self._scan_queue_modification_consumer = self.connector.consumer(
            MessageEndpoints.scan_queue_modification(),
            cb=self._scan_queue_modification_callback,
            parent=self,
        )
        self._scan_queue_consumer.start()
        self._scan_queue_modification_consumer.start()

    @staticmethod
    def _scan_queue_callback(msg, parent, **_kwargs) -> None:
        scan_msg = BECMessage.ScanQueueMessage.loads(msg.value)
        logger.info("Receiving scan:", scan_msg.content, time.time())
        # instructions = parent.scan_assembler.assemble_device_instructions(scan_msg)
        parent.add_to_queue("primary", scan_msg)
        parent.send_queue_status()

    @staticmethod
    def _scan_queue_modification_callback(msg, parent, **_kwargs):
        scan_mod_msg = BECMessage.ScanQueueModificationMessage.loads(msg.value)
        logger.info("Receiving scan modification:", scan_mod_msg.content)
        if scan_mod_msg:
            parent.scan_interception(scan_mod_msg)
            parent.send_queue_status()

    def scan_interception(self, scan_mod_msg: BECMessage.ScanQueueModificationMessage) -> None:
        action = scan_mod_msg.content["action"]
        getattr(self, f"set_{action}")(scanID=scan_mod_msg.content["scanID"])

    def set_pause(self, scanID=None, queue="primary") -> None:
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.PAUSED

    def set_deferred_pause(self, scanID=None, queue="primary") -> None:
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.DEFERRED_PAUSE

    def set_continue(self, scanID=None, queue="primary") -> None:
        self.queues[queue].status = ScanQueueStatus.RUNNING
        self.queues[queue].worker_status = InstructionQueueStatus.RUNNING

    def set_abort(self, scanID=None, queue="primary") -> None:
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.STOPPED
        self.queues[queue].remove_queue_item(scanID=scanID)

    def set_clear(self, scanID=None, queue="primary") -> None:
        self.queues[queue].status = ScanQueueStatus.PAUSED
        self.queues[queue].worker_status = InstructionQueueStatus.PAUSED
        self.queues[queue].clear()

    def send_queue_status(self) -> None:
        queue_export = self.export_queue()
        logger.info("New scan queue:")
        for queue in self.describe_queue():
            logger.info(f"\n {queue}")
        self.producer.send(
            MessageEndpoints.scan_queue_status(),
            BECMessage.ScanQueueStatusMessage(queue=queue_export).dumps(),
        )

    def describe_queue(self) -> list:
        queue_tables = []
        for queue_name, scan_queue in self.queues.items():
            table = PrettyTable()
            table.title = f"{queue_name} queue"
            table.field_names = ["queueID", "scanID", "is_scan", "scan_number", "status"]
            for instruction_queue in scan_queue.queue:
                table.add_row(
                    [
                        instruction_queue.queue_id,
                        instruction_queue.scanID,
                        instruction_queue.is_scan,
                        instruction_queue.scan_number,
                        instruction_queue.status.name,
                    ]
                )
            queue_tables.append(table)
        return queue_tables

    def export_queue(self) -> dict:
        queue_export = {}
        for queue_name, scan_queue in self.queues.items():
            queue_info = []
            for instruction_queue in scan_queue.queue:
                request_blocks = [rb.describe() for rb in instruction_queue.queue.request_blocks]
                queue_info.append(
                    {
                        "queueID": instruction_queue.queue_id,
                        "scanID": instruction_queue.scanID,
                        "is_scan": instruction_queue.is_scan,
                        "request_blocks": request_blocks,
                        "scan_number": instruction_queue.scan_number,
                        "status": instruction_queue.status.name,
                        "active_request_block": instruction_queue.active_request_block.describe()
                        if instruction_queue.active_request_block
                        else None,
                    }
                )
            queue_export[queue_name] = {"info": queue_info, "status": scan_queue.status.name}
        return queue_export

    def shutdown(self):
        for queue in self.queues.values():
            queue.signal_event.set()


class ScanQueue:
    """The ScanQueue manages a queue of InstructionQueues.
    While for most scenarios a single ScanQueue is sufficient,
    multiple ScanQueues can be used to run experiments in parallel.
    The default ScanQueue is always "primary".

    Raises:
        StopIteration: _description_
        StopIteration: _description_

    Returns:
        _type_: _description_
    """

    MAX_HISTORY = 100
    DEFAULT_QUEUE_STATUS = ScanQueueStatus.RUNNING

    def __init__(
        self, queue_manager: QueueManager, instruction_queue_item_cls: InstructionQueueItem = None
    ) -> None:
        self.queue = collections.deque()
        self.history_queue = collections.deque(maxlen=self.MAX_HISTORY)
        self.active_instruction_queue = None
        self.queue_manager = queue_manager
        self._instruction_queue_item_cls = (
            instruction_queue_item_cls
            if instruction_queue_item_cls is not None
            else InstructionQueueItem
        )
        # self.open_instruction_queue = None
        self._status = self.DEFAULT_QUEUE_STATUS
        self.signal_event = threading.Event()

    @property
    def worker_status(self) -> Union[None, InstructionQueueStatus]:
        if len(self.queue) > 0:
            return self.queue[0].status
        return None

    @worker_status.setter
    def worker_status(self, val: InstructionQueueStatus):
        if len(self.queue) > 0:
            self.queue[0].status = val

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val: ScanQueueStatus):
        self._status = val
        self.queue_manager.send_queue_status()

    def remove_queue_item(self, scanID):
        remove = []
        for queue in self.queue:
            if len(set(scanID) & set(queue.scanID)) > 0:
                remove.append(queue)
        if remove:
            for rmv in remove:
                self.queue.remove(rmv)

    def clear(self):
        self.queue.clear()

    def __iter__(self):
        return self

    def __next__(self):
        while not self.signal_event.is_set():
            try:
                if self.active_instruction_queue is not None and len(self.queue) > 0:
                    self.queue.popleft()
                    self.queue_manager.send_queue_status()

                if self.status != ScanQueueStatus.PAUSED:
                    if len(self.queue) == 0:
                        self.active_instruction_queue = None
                        time.sleep(0.1)
                        continue

                    self.active_instruction_queue = self.queue[0]
                    self.history_queue.append(self.active_instruction_queue)
                    return self.active_instruction_queue

                while self.status == ScanQueueStatus.PAUSED:
                    if len(self.queue) == 0:
                        # we don't need to pause if there is no scan enqueued
                        self.status = ScanQueueStatus.RUNNING
                    time.sleep(1)
                    logger.info("Queue is paused")

                self.active_instruction_queue = self.queue.popleft()
                self.history_queue.append(self.active_instruction_queue)
                # self.active_instruction_queue
                return self.active_instruction_queue

            except IndexError:
                time.sleep(0.01)

    def append(self, msg, **_kwargs):
        target_group = msg.metadata.get("queue_group")
        scan_def_id = msg.metadata.get("scan_def_id")
        instruction_queue = None
        queue_exists = False
        if scan_def_id is not None:
            instruction_queue = self.get_queue_item(scan_def_id=scan_def_id)
            if instruction_queue is not None:
                queue_exists = True
        elif target_group is not None:
            instruction_queue = self.get_queue_item(group=target_group)
            if instruction_queue is not None:
                queue_exists = True
        if not queue_exists:
            # create new queue element (InstructionQueueItem)
            instruction_queue = self._instruction_queue_item_cls(
                parent=self,
                assembler=self.queue_manager.parent.scan_assembler,
                worker=self.queue_manager.parent.scan_worker,
            )
        instruction_queue.append_scan_request(msg)
        instruction_queue.queue.update_scan_number(request_block_index=-1)
        if not queue_exists:
            instruction_queue.queue_group = target_group
            self.queue.append(instruction_queue)

    def get_queue_item(self, group=None, scan_def_id=None):
        if scan_def_id is not None:
            for instruction_queue in self.queue:
                if scan_def_id in instruction_queue.queue.scan_def_ids:
                    return instruction_queue
        if group is not None:
            for instruction_queue in self.queue:
                if instruction_queue.queue_group == group:
                    return instruction_queue

        return None

    def abort(self) -> None:
        if self.active_instruction_queue is not None:
            self.active_instruction_queue.abort()

    def get_scan(self, scanID: str) -> Union[None, InstructionQueueItem]:
        queue_found = None
        for queue in self.history_queue + self.queue:
            if queue.scanID == scanID:
                queue_found = queue
                return queue_found
        return queue_found


class RequestBlock:
    def __init__(self, msg, assembler: ScanAssembler, parent=None) -> None:
        self.instructions = None
        self.scan = None
        self.scan_motors = []
        self.msg = msg
        self.RID = msg.metadata["RID"]
        self.scan_assembler = assembler
        self.is_scan = False
        self.scanID = None
        self.scan_number = None
        self.parent = parent
        self.scan_def_id = None
        self._assemble()

    def _assemble(self):
        self.scan = self.scan_assembler.assemble_device_instructions(self.msg)
        dev_msg_list = list(self.scan.run(simulate=True))
        self.is_scan = any(
            dev_msg.content.get("action")
            in [
                "open_scan",
                "open_scan_def",
                "close_scan_def",
            ]
            for dev_msg in dev_msg_list
        )
        self.scan_def_id = self.msg.metadata.get("scan_def_id")
        self.scan = self.scan_assembler.assemble_device_instructions(self.msg)
        self.instructions = self.scan.run()
        if self.is_scan and self.scanID is None:
            self.scanID = str(uuid.uuid4())
        if self.scan.caller_args:
            self.scan_motors = self.scan.scan_motors

    def update_scan_number(self, queue_manager):
        if self.is_scan:
            self.scan_number = queue_manager.parent.scan_number
            if self.scan_def_id is None or self.msg.content["scan_type"] == "close_scan_def":
                queue_manager.parent.scan_number += 1

    def describe(self):
        return {
            "msg": self.msg.dumps(),
            "RID": self.RID,
            "scan_motors": self.scan_motors,
            "is_scan": self.is_scan,
            "scan_number": self.scan_number,
            "scanID": self.scanID,
            "metadata": self.msg.metadata,
            "content": self.msg.content,
        }


class RequestBlockQueue:
    def __init__(self, parent, assembler) -> None:
        self.request_blocks_queue = collections.deque()
        self.request_blocks = []
        self.parent = parent
        self.assembler = assembler
        self.active_rb = None
        self.scan_def_ids = {}

    @property
    def scanID(self):
        return [rb.scanID for rb in self.request_blocks]

    @property
    def is_scan(self):
        return [rb.is_scan for rb in self.request_blocks]

    @property
    def scan_number(self):
        return [rb.scan_number for rb in self.request_blocks]

    def append(self, msg):
        request_block = RequestBlock(msg, self.assembler, parent=self)
        if "scan_def_id" in request_block.msg.metadata:
            scan_def_id = request_block.msg.metadata["scan_def_id"]
            if scan_def_id in self.scan_def_ids:
                request_block.scanID = self.scan_def_ids[scan_def_id]["scanID"]
            else:
                self.scan_def_ids[scan_def_id] = {"scanID": request_block.scanID, "pointID": 0}

        self.request_blocks_queue.append(request_block)
        self.request_blocks.append(request_block)

    def update_scan_number(self, request_block_index):
        self.request_blocks[request_block_index].update_scan_number(
            self.parent.parent.queue_manager
        )

    def _pull_request_block(self):
        if self.active_rb is None:
            if len(self.request_blocks_queue) > 0:
                self.active_rb = self.request_blocks_queue.popleft()
                if self.active_rb.scan_def_id in self.scan_def_ids:
                    if hasattr(self.active_rb.scan, "pointID"):
                        self.active_rb.scan.pointID = self.scan_def_ids[self.active_rb.scan_def_id][
                            "pointID"
                        ]

            else:
                raise StopIteration

    def __iter__(self):
        return self

    def __next__(self):
        self._pull_request_block()
        try:
            return next(self.active_rb.instructions)
        except StopIteration:
            if self.active_rb.scan_def_id in self.scan_def_ids:
                pointID = getattr(self.active_rb.scan, "pointID", None)
                if pointID is not None:
                    self.scan_def_ids[self.active_rb.scan_def_id]["pointID"] = pointID
            self.active_rb = None
            self._pull_request_block()
            return next(self.active_rb.instructions)
        except LimitError as limit_error:
            self.parent.parent.queue_manager.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=self.active_rb.msg.content,
                content=limit_error.args[0],
                alarm_type=limit_error.__class__.__name__,
            )
            raise ScanAbortion from limit_error


class InstructionQueueItem:
    """The InstructionQueueItem contains and manages the request blocks for a queue item.
    While an InstructionQueueItem can be comprised of multiple requests,
    it will always have at max one scan_number / scanID.

    Raises:
        StopIteration: _description_
        StopIteration: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, parent: ScanQueue, assembler: ScanAssembler, worker: ScanWorker) -> None:
        self.instructions = []
        self.queue = RequestBlockQueue(parent=self, assembler=assembler)
        self.parent = parent
        self.producer = self.parent.queue_manager.producer
        self._is_scan = False
        self.is_active = False  # set to true while a worker is processing the instructions
        self.completed = False
        self.deferred_pause = True
        self.queue_group = None
        self.queue_group_is_closed = False
        self.subqueue = iter([])
        self.queue_id = str(uuid.uuid4())
        self.scan_msgs = []
        self.scan_assembler = assembler
        self.worker = worker
        self._status = InstructionQueueStatus.PENDING

    @property
    def scan_number(self):
        return self.queue.scan_number

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val: ScanQueueStatus):
        self._status = val
        self.worker.status = val
        self.parent.queue_manager.send_queue_status()

    @property
    def active_request_block(self):
        return self.queue.active_rb

    @property
    def scan_macros_complete(self):
        return len(self.queue.scan_def_ids) == 0

    @property
    def scanID(self):
        return self.queue.scanID

    @property
    def is_scan(self):
        return self.queue.is_scan

    def abort(self):
        self.instructions = iter([])

    def append_scan_request(self, msg):
        self.scan_msgs.append(msg)
        self.queue.append(msg)

    def set_active(self):
        if self.status == InstructionQueueStatus.PENDING:
            self.status = InstructionQueueStatus.RUNNING

    def describe(self):
        return {
            "scanID": self.queue.active_rb.scanID,
            "is_active": self.is_active,
            "completed": self.completed,
            "deferred_pause": self.deferred_pause,
        }

    def __iter__(self):
        return self

    def _set_finished(self, raise_stopiteration=True):
        self.completed = True
        if raise_stopiteration:
            raise StopIteration

    def _get_next(self, queue="instructions", raise_stopiteration=True):
        try:
            instr = next(self.queue)
            # instr = next(self.__getattribute__(queue))
            if instr:
                if instr.content.get("action") == "close_scan_group":
                    self.queue_group_is_closed = True
                    raise StopIteration
                if instr.content.get("action") == "close_scan_def":
                    scan_def_id = instr.metadata.get("scan_def_id")
                    if scan_def_id in self.queue.scan_def_ids:
                        self.queue.scan_def_ids.pop(scan_def_id)

                instr.metadata["scanID"] = self.queue.active_rb.scanID
                instr.metadata["queueID"] = self.queue_id
                self.set_active()
                return instr

        except StopIteration:
            if not self.scan_macros_complete:
                logger.info(
                    f"Waiting for new instructions or scan macro to be closed (scan def ids: {self.queue.scan_def_ids})"
                )
                time.sleep(0.1)
            elif self.queue_group is not None and not self.queue_group_is_closed:
                logger.info(
                    f"Waiting for new instructions or queue group to be closed (group id: {self.queue_group})"
                )
                time.sleep(0.1)
            else:
                self._set_finished(raise_stopiteration=raise_stopiteration)

    def __next__(self):
        if self.status in [
            InstructionQueueStatus.RUNNING,
            InstructionQueueStatus.DEFERRED_PAUSE,
            InstructionQueueStatus.PENDING,
        ]:
            return self._get_next()

        while self.status == InstructionQueueStatus.PAUSED:
            return self._get_next(queue="subqueue", raise_stopiteration=False)

        return self._get_next()
