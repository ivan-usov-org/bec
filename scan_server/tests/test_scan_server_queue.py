import uuid
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
        self.queue = RequestBlockQueueMock(self, assembler)

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
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue_manager.queues = {"primary": ScanQueue(queue_manager, InstructionQueueMock)}
    queue_manager.add_to_queue(scan_queue="primary", msg=msg)
    queue_manager.set_abort(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.PAUSED
    assert len(queue_manager.producer.message_sent) == 2
    assert (
        queue_manager.producer.message_sent[0].get("queue") == MessageEndpoints.scan_queue_status()
    )


def test_set_abort_with_empty_queue():
    queue_manager = get_queuemanager()
    queue_manager.producer.message_sent = []
    queue_manager.set_abort(queue="primary")
    assert queue_manager.queues["primary"].status == ScanQueueStatus.RUNNING
    assert len(queue_manager.producer.message_sent) == 0


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
            with queue_manager._lock:
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


class RequestBlockMock(RequestBlock):
    def __init__(self, msg, scanID) -> None:
        self.scanID = scanID
        self.msg = msg
        self.scan = None


def test_request_block_queue_scanIDs():
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    rb1 = RequestBlockMock("", str(uuid.uuid4()))
    rb2 = RequestBlockMock("", str(uuid.uuid4()))
    req_block_queue.request_blocks.append(rb1)
    req_block_queue.request_blocks.append(rb2)
    assert req_block_queue.scanID == [rb1.scanID, rb2.scanID]


def test_request_block_queue_append():
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    msg = BECMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    with mock.patch("scan_server.scan_queue.RequestBlock") as rb:
        with mock.patch.object(req_block_queue, "_update_scan_def_id") as update_scan_def:
            with mock.patch.object(req_block_queue, "append_request_block") as update_rb:
                req_block_queue.append(msg)
                update_scan_def.assert_called_once_with(rb())
                update_rb.assert_called_once_with(rb())


@pytest.mark.parametrize(
    "scan_queue_msg,scanID",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            ),
            None,
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something", "scan_def_id": "something"},
            ),
            "scanID1",
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something", "scan_def_id": "existing_scan_def_id"},
            ),
            "scanID2",
        ),
    ],
)
def test_update_scan_def_id(scan_queue_msg, scanID):
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    req_block_queue.scan_def_ids["existing_scan_def_id"] = {"scanID": "existing_scanID"}
    rbl = RequestBlockMock(scan_queue_msg, scanID)
    if rbl.msg.metadata.get("scan_def_id") in req_block_queue.scan_def_ids:
        req_block_queue._update_scan_def_id(rbl)
        scan_def_id = scan_queue_msg.metadata.get("scan_def_id")
        assert rbl.scanID == req_block_queue.scan_def_ids[scan_def_id]["scanID"]
        return
    req_block_queue._update_scan_def_id(rbl)
    assert rbl.scanID == scanID


def test_append_request_block():
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    rbl = RequestBlockMock("", "")
    with mock.patch.object(req_block_queue, "request_blocks_queue") as request_blocks_queue:
        with mock.patch.object(req_block_queue, "request_blocks") as request_blocks:
            req_block_queue.append_request_block(rbl)
            request_blocks.append.assert_called_once_with(rbl)
            request_blocks_queue.append.assert_called_once_with(rbl)


@pytest.mark.parametrize(
    "scan_queue_msg,scanID",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something", "scan_def_id": "something"},
            ),
            "scanID1",
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something", "scan_def_id": "existing_scan_def_id"},
            ),
            "scanID2",
        ),
    ],
)
def test_update_point_id(scan_queue_msg, scanID):
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    req_block_queue.scan_def_ids["existing_scan_def_id"] = {
        "scanID": "existing_scanID",
        "pointID": 10,
    }
    rbl = RequestBlockMock(scan_queue_msg, scanID)
    rbl.scan = mock.MagicMock()
    scan_def_id = scan_queue_msg.metadata.get("scan_def_id")
    if rbl.msg.metadata.get("scan_def_id") in req_block_queue.scan_def_ids:
        req_block_queue._update_point_id(rbl)
        assert rbl.scan.pointID == req_block_queue.scan_def_ids[scan_def_id]["pointID"]
        return
    req_block_queue._update_point_id(rbl)
    assert rbl.scan.pointID != 10


@pytest.mark.parametrize(
    "scan_queue_msg,is_scan",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="mv",
                parameter={"args": {"samx": (1,)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            ),
            False,
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            ),
            True,
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something", "scan_def_id": "existing_scan_def_id"},
            ),
            True,
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something", "dataset_id_on_hold": True},
            ),
            True,
        ),
    ],
)
def test_increase_scan_number(scan_queue_msg, is_scan):
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    req_block_queue.scan_queue.queue_manager.parent.scan_number = 20
    req_block_queue.scan_queue.queue_manager.parent.dataset_number = 5
    rbl = RequestBlockMock(scan_queue_msg, "scanID")
    rbl.is_scan = is_scan
    dataset_id_on_hold = scan_queue_msg.metadata.get("dataset_id_on_hold")
    req_block_queue.active_rb = rbl
    req_block_queue.increase_scan_number()
    if is_scan and rbl.scan_def_id is None:
        assert req_block_queue.scan_queue.queue_manager.parent.scan_number == 21
        if dataset_id_on_hold:
            assert req_block_queue.scan_queue.queue_manager.parent.dataset_number == 5
        else:
            assert req_block_queue.scan_queue.queue_manager.parent.dataset_number == 6
    else:
        assert req_block_queue.scan_queue.queue_manager.parent.scan_number == 20


def test_pull_request_block_non_empyt_rb():
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    scan_queue_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    rbl = RequestBlockMock(scan_queue_msg, "scanID")
    req_block_queue.active_rb = rbl
    with mock.patch.object(req_block_queue, "request_blocks_queue") as rbqs:
        req_block_queue._pull_request_block()
        rbqs.assert_not_called()


def test_pull_request_block_empyt_rb():
    req_block_queue = RequestBlockQueue(mock.MagicMock(), mock.MagicMock())
    with mock.patch.object(req_block_queue, "request_blocks_queue") as rbqs:
        with pytest.raises(StopIteration):
            req_block_queue._pull_request_block()
            rbqs.assert_not_called()
