from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from typeguard import TypeCheckError

from bec_lib import messages
from bec_lib.endpoints import MessageEndpoints
from bec_lib.scan_manager import ScanManager

if TYPE_CHECKING:
    from bec_lib.redis_connector import RedisConnector


@pytest.fixture
def scan_manager():
    connector = mock.MagicMock()
    manager = ScanManager(connector=connector)
    yield manager
    manager.shutdown()


@pytest.fixture
def scan_manager_with_fakeredis(connected_connector: RedisConnector):
    manager = ScanManager(connector=connected_connector)
    yield manager
    manager.shutdown()


def test_scan_manager_next_scan_number(scan_manager):
    scan_manager.connector.get.return_value = messages.VariableMessage(value=3)
    assert scan_manager.next_scan_number == 3


def test_scan_manager_next_scan_number_failed(scan_manager):
    scan_manager.connector.get.return_value = None
    assert scan_manager.next_scan_number == -1


def test_scan_manager_next_scan_number_with_int(scan_manager):
    scan_manager.connector.get.return_value = 3
    assert scan_manager.next_scan_number == 3


def test_scan_manager_next_scan_number_setter(scan_manager):
    scan_manager.next_scan_number = 3
    scan_manager.connector.set.assert_called_once_with(
        MessageEndpoints.scan_number(), messages.VariableMessage(value=3)
    )


def test_scan_manager_next_dataset_number(scan_manager):
    scan_manager.connector.get.return_value = messages.VariableMessage(value=3)
    assert scan_manager.next_dataset_number == 3


def test_scan_manager_next_dataset_number_failed(scan_manager):
    scan_manager.connector.get.return_value = None
    assert scan_manager.next_dataset_number == -1


def test_scan_manager_next_dataset_number_with_int(scan_manager):
    scan_manager.connector.get.return_value = 3
    assert scan_manager.next_dataset_number == 3


def test_scan_manager_next_dataset_number_setter(scan_manager):
    scan_manager.next_dataset_number = 3
    scan_manager.connector.set.assert_called_once_with(
        MessageEndpoints.dataset_number(), messages.VariableMessage(value=3)
    )


def test_scan_manager_request_scan_abortion(scan_manager):
    scan_manager.request_scan_abortion("scan_id")
    scan_manager.connector.send.assert_called_once_with(
        MessageEndpoints.scan_queue_modification_request(),
        messages.ScanQueueModificationMessage(scan_id="scan_id", action="abort", parameter={}),
    )


@pytest.mark.parametrize("scan_id", [None, "scan_id", ["scan_id"], [None]])
def test_scan_manager_request_scan_abortion_scan_id(scan_manager, scan_id):

    class ScanStorage:
        current_scan_info = {"scan_id": scan_id}

        @property
        def current_scan_id(self):
            return self.current_scan_info["scan_id"]

    scan_manager.scan_storage = ScanStorage()
    scan_manager.request_scan_abortion()
    scan_manager.connector.send.assert_called_once_with(
        MessageEndpoints.scan_queue_modification_request(),
        messages.ScanQueueModificationMessage(scan_id=scan_id, action="abort", parameter={}),
    )


def test_scan_manager_request_scan_halt(scan_manager):
    scan_manager.request_scan_halt("scan_id")
    scan_manager.connector.send.assert_called_once_with(
        MessageEndpoints.scan_queue_modification_request(),
        messages.ScanQueueModificationMessage(scan_id="scan_id", action="halt", parameter={}),
    )


@pytest.mark.parametrize("scan_id", [None, "scan_id", ["scan_id"], [None]])
def test_scan_manager_request_scan_halt_scan_id(scan_manager, scan_id):

    class ScanStorage:
        current_scan_info = {"scan_id": scan_id}

        @property
        def current_scan_id(self):
            return self.current_scan_info["scan_id"]

    scan_manager.scan_storage = ScanStorage()
    scan_manager.request_scan_halt()
    scan_manager.connector.send.assert_called_once_with(
        MessageEndpoints.scan_queue_modification_request(),
        messages.ScanQueueModificationMessage(scan_id=scan_id, action="halt", parameter={}),
    )


def test_scan_manager_request_scan_continuation(scan_manager):
    scan_manager.request_scan_continuation("scan_id")
    scan_manager.connector.send.assert_called_once_with(
        MessageEndpoints.scan_queue_modification_request(),
        messages.ScanQueueModificationMessage(scan_id="scan_id", action="continue", parameter={}),
    )


@pytest.mark.parametrize("scan_id", [None, "scan_id", ["scan_id"], [None]])
def test_scan_manager_request_scan_continuation_scan_id(scan_manager, scan_id):

    class ScanStorage:
        current_scan_info = {"scan_id": scan_id}

        @property
        def current_scan_id(self):
            return self.current_scan_info["scan_id"]

    scan_manager.scan_storage = ScanStorage()
    scan_manager.request_scan_continuation()
    scan_manager.connector.send.assert_called_once_with(
        MessageEndpoints.scan_queue_modification_request(),
        messages.ScanQueueModificationMessage(scan_id=scan_id, action="continue", parameter={}),
    )


def test_scan_manager_add_scan_to_queue_schedule(scan_manager_with_fakeredis):
    """
    Test the interaction with queue schedules

    Args:
        scan_manager_with_fakeredis: The scan manager fixture with a fakeredis connection
    """
    manager: ScanManager = scan_manager_with_fakeredis
    msg = messages.ScanQueueMessage(scan_type="mv", parameter={"args": {"samx": [5], "samy": [5]}})
    manager.add_scan_to_queue_schedule("new_schedule", msg)

    with pytest.raises(TypeCheckError):
        manager.add_scan_to_queue_schedule("new_schedule", {})

    assert manager.get_scan_queue_schedule("new_schedule") == [msg]

    msg2 = messages.ScanQueueMessage(scan_type="mv", parameter={"args": {"samx": [6], "samy": [6]}})
    manager.add_scan_to_queue_schedule("new_schedule", msg2)

    assert manager.get_scan_queue_schedule("new_schedule") == [msg, msg2]

    manager.add_scan_to_queue_schedule("new_schedule2", msg)

    assert manager.get_scan_queue_schedule("new_schedule2") == [msg]

    assert manager.get_scan_queue_schedule_names() == ["new_schedule", "new_schedule2"]

    manager.clear_scan_queue_schedule("new_schedule2")

    assert manager.get_scan_queue_schedule_names() == ["new_schedule"]

    assert manager.get_scan_queue_schedule("new_schedule2") == []

    assert manager.get_scan_queue_schedule("new_schedule") == [msg, msg2]

    manager.clear_all_scan_queue_schedules()

    assert manager.get_scan_queue_schedule_names() == []
