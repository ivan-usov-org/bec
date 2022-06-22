import pytest
from bec_utils import BECMessage, MessageEndpoints
from koss.bkqueue import (
    InstructionQueueItem,
    QueueManager,
    RequestBlockQueue,
    ScanQueue,
    ScanQueueStatus,
)
from koss.devicemanager import DeviceManagerKOSS
from koss.scan_assembler import ScanAssembler
from koss.scan_worker import ScanWorker

from utils import ConnectorMock, KossMock, dummy_devices


def get_queuemanager() -> QueueManager:
    devices = dummy_devices(True)
    connector = ConnectorMock("")
    device_manager = DeviceManagerKOSS(connector, "")
    device_manager._config = devices
    device_manager._load_config_device()
    k = KossMock(device_manager, connector)
    return QueueManager(parent=k)


class RequestBlockQueueMock(RequestBlockQueue):
    request_blocks = []
    _scanID = None

    @property
    def scanID(self):
        return self._scanID

    def update_scan_number(self, request_block_index):
        pass

    def append(self, msg):
        pass


class InstructionQueueMock(InstructionQueueItem):
    def __init__(self, parent: ScanQueue, assembler: ScanAssembler, worker: ScanWorker) -> None:
        super().__init__(parent, assembler, worker)
        self.queue = RequestBlockQueueMock(self.parent, assembler)

    def append_scan_request(self, msg):
        self.scan_msgs.append(msg)
        self.queue.append(msg)


def test_queuemanager_queue_contains_primary():
    queue_manager = get_queuemanager()
    assert "primary" in queue_manager.queues


@pytest.mark.parametrize("queue", [("primary",), ("alignment",)])
def test_queuemanager_add_to_queue(queue):
    queue_manager = get_queuemanager()
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue=queue,
        metadata={"RID": "something"},
    )
    queue_manager.queues = {queue: ScanQueue(queue_manager, InstructionQueueMock)}
    queue_manager.add_to_queue(scan_queue=queue, msg=msg)
    assert queue_manager.queues[queue].queue.popleft().scan_msgs[0] == msg


def test_set_pause():
    queue_manager = get_queuemanager()
    queue_manager._set_pause(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert queue_manager.producer.message_sent.get("queue") == MessageEndpoints.scan_queue_status()


def test_set_deferred_pause():
    queue_manager = get_queuemanager()
    queue_manager._set_deferred_pause(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert queue_manager.producer.message_sent.get("queue") == MessageEndpoints.scan_queue_status()


def test_set_continue():
    queue_manager = get_queuemanager()
    queue_manager._set_continue(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.RUNNING
    assert queue_manager.producer.message_sent.get("queue") == MessageEndpoints.scan_queue_status()


def test_set_abort():
    queue_manager = get_queuemanager()
    queue_manager._set_abort(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert queue_manager.producer.message_sent.get("queue") == MessageEndpoints.scan_queue_status()


def test_set_clear_sends_message():
    queue_manager = get_queuemanager()
    queue_manager._set_clear(queue="primary")

    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert queue_manager.producer.message_sent.get("queue") == MessageEndpoints.scan_queue_status()


def test_remove_queue_item():
    queue_manager = get_queuemanager()
    # queue_manager.queues = {"primary": ScanQueueMock(queue_manager)}
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue_manager.queues = {"primary": ScanQueue(queue_manager, InstructionQueueMock)}
    queue_manager.add_to_queue(scan_queue="primary", msg=msg)
    queue_manager.queues["primary"].queue[0].queue._scanID = "random"
    queue_manager.queues["primary"].remove_queue_item(scanID="random")
    assert len(queue_manager.queues["primary"].queue) == 0


def test_set_clear():
    queue_manager = get_queuemanager()
    queue_manager.queues = {"primary": ScanQueue(queue_manager, InstructionQueueMock)}
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue_manager.add_to_queue(scan_queue="primary", msg=msg)
    queue_manager._set_clear(queue="primary")
    assert len(queue_manager.queues["primary"].queue) == 0
