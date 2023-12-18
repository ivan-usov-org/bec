from unittest import mock

import pytest

from bec_lib import messages
from bec_lib.redis_connector import MessageObject
from bec_lib.scan_manager import ScanManager


@pytest.fixture
def scan_manager():
    manager = ScanManager(connector=mock.MagicMock())
    yield manager


def test_scan_baseline_callback(scan_manager):
    msg_orig = messages.ScanBaselineMessage(
        scanID="test_scanID", data={"samx": {"samx": {"value": 0, "timestamp": 12345}}}
    )
    msg = MessageObject(topic="test", value=msg_orig.dumps())
    with mock.patch.object(scan_manager.scan_storage, "add_baseline") as add_baseline:
        scan_manager._scan_baseline_callback(msg, parent=scan_manager)
        add_baseline.assert_called_once_with(msg_orig)


def test_scan_segment_callback(scan_manager):
    msg_orig = messages.ScanMessage(
        point_id=0, scanID="test_scanID", data={"samx": {"samx": {"value": 0, "timestamp": 12345}}}
    )
    msg = MessageObject(topic="test", value=msg_orig.dumps())
    with mock.patch.object(scan_manager.scan_storage, "add_scan_segment") as add_scan_segment:
        scan_manager._scan_segment_callback(msg, parent=scan_manager)
        add_scan_segment.assert_called_once_with(msg_orig)


def test_scan_status_callback(scan_manager):
    msg_orig = messages.ScanStatusMessage(scanID="test_scanID", status={"status": "open"}, info={})
    msg = MessageObject(topic="test", value=msg_orig.dumps())
    with mock.patch.object(
        scan_manager.scan_storage, "update_with_scan_status"
    ) as update_with_scan_status:
        scan_manager._scan_status_callback(msg, parent=scan_manager)
        update_with_scan_status.assert_called_once_with(msg_orig)
