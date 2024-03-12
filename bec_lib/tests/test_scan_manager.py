from unittest import mock

import pytest

from bec_lib import MessageEndpoints, messages
from bec_lib.scan_manager import ScanManager


@pytest.fixture
def scan_manager():
    connector = mock.MagicMock()
    manager = ScanManager(connector=connector)
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
