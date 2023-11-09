from unittest import mock

import pytest

from bec_lib import messages
from bec_lib.bec_errors import ScanAbortion
from bec_lib.scan_manager import ScanReport


def test_scan_report_wait_mv():
    report = ScanReport()
    report.request = mock.MagicMock()
    report.request.request = messages.ScanQueueMessage(scan_type="mv", parameter={})
    with mock.patch.object(report, "_wait_move") as wait_move:
        report.wait()
        wait_move.assert_called_once_with(None, 0.1)


def test_scan_report_wait_mv_timeout():
    report = ScanReport()
    report.request = mock.MagicMock()
    report.request.request = messages.ScanQueueMessage(scan_type="mv", parameter={})
    with mock.patch.object(report, "_wait_move") as wait_move:
        report.wait(10)
        wait_move.assert_called_once_with(10, 0.1)


def test_scan_report_wait_scan():
    report = ScanReport()
    report.request = mock.MagicMock()
    report.request.request = messages.ScanQueueMessage(scan_type="line_scan", parameter={})
    with mock.patch.object(report, "_wait_scan") as wait_scan:
        report.wait()
        wait_scan.assert_called_once_with(None, 0.1)


@pytest.mark.parametrize("timeout, elapsed_time", [(10, 0.1), (None, 0.1), (0.1, 10)])
def test_scan_report_check_timeout(timeout, elapsed_time):
    report = ScanReport()
    if timeout is None or timeout > elapsed_time:
        report._check_timeout(timeout, elapsed_time)
    else:
        with pytest.raises(TimeoutError):
            report._check_timeout(timeout, elapsed_time)


def test_scan_report_wait_move():
    report = ScanReport()
    report.request = mock.MagicMock()
    report._client = mock.MagicMock()
    report.request.request = messages.ScanQueueMessage(scan_type="mv", parameter={})
    with mock.patch.object(report, "_get_mv_status") as get_mv_status:
        get_mv_status.side_effect = [False, False, True]
        report._wait_move(None, 0.1)
        assert get_mv_status.call_count == 3
        assert report._client.alarm_handler.raise_alarms.call_count == 2


def test_scan_report_wait_for_scan():
    report = ScanReport()
    report.request = mock.MagicMock()
    report._client = mock.MagicMock()
    report._queue_item = mock.MagicMock()
    report.request.request = messages.ScanQueueMessage(scan_type="mv", parameter={})
    with mock.patch.object(report, "_get_mv_status") as get_mv_status:
        get_mv_status.side_effect = [False, False, True]
        report.queue_item.status = "COMPLETED"
        report._wait_scan(None, 0.1)


def test_scan_report_wait_for_scan_raises():
    report = ScanReport()
    report.request = mock.MagicMock()
    report._client = mock.MagicMock()
    report._queue_item = mock.MagicMock()
    report.request.request = messages.ScanQueueMessage(scan_type="mv", parameter={})
    with mock.patch.object(report, "_get_mv_status") as get_mv_status:
        get_mv_status.side_effect = [False, False, True]
        report.queue_item.status = "STOPPED"
        with pytest.raises(ScanAbortion):
            report._wait_scan(None, 0.1)
