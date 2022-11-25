from unittest import mock

import pytest
from bec_utils import BECMessage, MessageEndpoints
from utils import load_ScanServerMock

from scan_server.scan_assembler import ScanAssembler
from scan_server.scan_queue import (
    InstructionQueueItem,
    InstructionQueueStatus,
    QueueManager,
    RequestBlock,
    RequestBlockQueue,
    ScanQueue,
    ScanQueueStatus,
)
from scan_server.scan_worker import ScanWorker

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access


def get_queuemanager() -> QueueManager:
    k = load_ScanServerMock()
    return QueueManager(parent=k)


class RequestBlockQueueMock(RequestBlockQueue):
    request_blocks = []
    _scanID = []

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
    queue_manager.producer.message_sent = []
    queue_manager.set_pause(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert len(queue_manager.producer.message_sent) == 1
    assert (
        queue_manager.producer.message_sent[0].get("queue") == MessageEndpoints.scan_queue_status()
    )


def test_set_deferred_pause():
    queue_manager = get_queuemanager()
    queue_manager.producer.message_sent = []
    queue_manager.set_deferred_pause(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert len(queue_manager.producer.message_sent) == 1
    assert (
        queue_manager.producer.message_sent[0].get("queue") == MessageEndpoints.scan_queue_status()
    )


def test_set_continue():
    queue_manager = get_queuemanager()
    queue_manager.producer.message_sent = []
    queue_manager.set_continue(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.RUNNING
    assert len(queue_manager.producer.message_sent) == 1
    assert (
        queue_manager.producer.message_sent[0].get("queue") == MessageEndpoints.scan_queue_status()
    )


def test_set_abort():
    queue_manager = get_queuemanager()
    queue_manager.producer.message_sent = []
    queue_manager.set_abort(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert len(queue_manager.producer.message_sent) == 1
    assert (
        queue_manager.producer.message_sent[0].get("queue") == MessageEndpoints.scan_queue_status()
    )


def test_set_clear_sends_message():
    queue_manager = get_queuemanager()
    queue_manager.producer.message_sent = []
    setter_mock = mock.Mock(wraps=ScanQueue.worker_status.fset)
    # pylint: disable=assignment-from-no-return
    # pylint: disable=too-many-function-args
    mock_property = ScanQueue.worker_status.setter(setter_mock)
    with mock.patch.object(ScanQueue, "worker_status", mock_property):
        queue_manager.set_clear(queue="primary")

        assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
        mock_property.fset.assert_called_once_with(
            queue_manager.queues["primary"], InstructionQueueStatus.STOPPED
        )
        assert len(queue_manager.producer.message_sent) == 1
        assert (
            queue_manager.producer.message_sent[0].get("queue")
            == MessageEndpoints.scan_queue_status()
        )


def test_set_restart():
    queue_manager = get_queuemanager()
    queue_manager.queues = {"primary": ScanQueue(queue_manager, InstructionQueueMock)}
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue_manager.add_to_queue(scan_queue="primary", msg=msg)
    with mock.patch.object(queue_manager, "_get_active_scanID", return_value="new_scanID"):
        with mock.patch.object(
            queue_manager, "_wait_for_queue_to_appear_in_history"
        ) as scan_msg_wait:
            queue_manager.set_restart(queue="primary", parameter={"RID": "something_new"})
            scan_msg_wait.assert_called_once_with("new_scanID", "primary")


def test_request_block():
    scan_server = load_ScanServerMock()
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    request_block = RequestBlock(msg, assembler=ScanAssembler(parent=scan_server))


@pytest.mark.parametrize(
    "scan_queue_msg",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            )
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            )
        ),
    ],
)
def test_request_block_scan_number(scan_queue_msg):
    scan_server = load_ScanServerMock()
    request_block = RequestBlock(scan_queue_msg, assembler=ScanAssembler(parent=scan_server))
    if not request_block.is_scan:
        assert request_block.scan_number is None
        return
    with mock.patch.object(
        RequestBlock, "_scan_server_scan_number", new_callable=mock.PropertyMock, return_value=5
    ):
        with mock.patch.object(RequestBlock, "scanIDs_head", return_value=0):
            assert request_block.scan_number == 5


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
    queue_manager.set_clear(queue="primary")
    assert len(queue_manager.queues["primary"].queue) == 0
