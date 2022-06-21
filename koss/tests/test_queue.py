import collections

import pytest
from bluekafka_utils import KafkaMessage, MessageEndpoints
from koss.bkqueue import QueueManager, ScanQueueStatus
from koss.devicemanager import DeviceManagerKOSS

from utils import ConnectorMock, KossMock, dummy_devices


def get_queuemanager() -> QueueManager:
    devices = dummy_devices(True)
    connector = ConnectorMock("")
    device_manager = DeviceManagerKOSS(connector, "")
    device_manager._config = devices
    device_manager._load_config_device()
    k = KossMock(device_manager, connector)
    return QueueManager(parent=k)


def test_queuemanager_queue_contains_primary():
    queue_manager = get_queuemanager()
    assert "primary" in queue_manager.queues


class ScanQueueMock:
    def __init__(self, queue_manager: QueueManager) -> None:
        self.queue_manager = queue_manager
        self.queue = collections.deque()

    def append(self, msg):
        self.queue.append(msg)

    def clear(self):
        self.queue.clear()


@pytest.mark.parametrize("queue", [("primary",), ("alignment",)])
def test_queuemanager_add_to_queue(queue):
    queue_manager = get_queuemanager()
    msg = KafkaMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue=queue,
        metadata={"RID": "something"},
    )
    queue_manager.queues = {queue: ScanQueueMock(queue_manager)}
    queue_manager.add_to_queue(scan_queue=queue, msg=msg)
    assert queue_manager.queues[queue].queue.popleft() == msg


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


def test_set_clear():
    queue_manager = get_queuemanager()
    queue_manager.queues = {"primary": ScanQueueMock(queue_manager)}
    msg = KafkaMessage.ScanQueueMessage(
        scan_type="mv",
        parameter={"args": {"samx": (1,)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue_manager.add_to_queue(scan_queue="primary", msg=msg)
    queue_manager._set_clear(queue="primary")
    assert len(queue_manager.queues["primary"].queue) == 0
