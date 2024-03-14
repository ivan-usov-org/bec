from unittest import mock

import pytest
from test_scan_bundler import scan_bundler, threads_check

from bec_lib import MessageEndpoints, messages
from scan_bundler.bec_emitter import BECEmitter


@pytest.fixture
def bec_emitter(scan_bundler):
    emitter = BECEmitter(scan_bundler)
    yield emitter
    emitter.shutdown()


def test_on_scan_point_emit_BEC(bec_emitter):
    with mock.patch.object(bec_emitter, "_send_bec_scan_point") as send:
        bec_emitter.on_scan_point_emit("scan_id", 2)
        send.assert_called_once_with("scan_id", 2)


def test_on_baseline_emit_BEC(bec_emitter):
    with mock.patch.object(bec_emitter, "_send_baseline") as send:
        bec_emitter.on_baseline_emit("scan_id")
        send.assert_called_once_with("scan_id")


def test_send_bec_scan_point(bec_emitter):
    sb = bec_emitter.scan_bundler
    scan_id = "lkajsdlkj"
    pointID = 2
    sb.sync_storage[scan_id] = {"info": {}, "status": "open", "sent": set()}
    sb.sync_storage[scan_id][pointID] = {}
    msg = messages.ScanMessage(
        point_id=pointID,
        scan_id=scan_id,
        data=sb.sync_storage[scan_id][pointID],
        metadata={"scan_id": "lkajsdlkj", "scan_type": None, "scan_report_devices": None},
    )
    with mock.patch.object(bec_emitter, "add_message") as send:
        bec_emitter._send_bec_scan_point(scan_id, pointID)
        send.assert_called_once_with(
            msg,
            MessageEndpoints.scan_segment(),
            MessageEndpoints.public_scan_segment(scan_id, pointID),
        )


def test_send_baseline_BEC(bec_emitter):
    sb = bec_emitter.scan_bundler
    scan_id = "lkajsdlkj"
    sb.sync_storage[scan_id] = {"info": {}, "status": "open", "sent": set()}
    sb.sync_storage[scan_id]["baseline"] = {}
    msg = messages.ScanBaselineMessage(scan_id=scan_id, data=sb.sync_storage[scan_id]["baseline"])
    with mock.patch.object(sb, "connector") as connector:
        bec_emitter._send_baseline(scan_id)
        pipe = connector.pipeline()
        connector.set.assert_called_once_with(
            MessageEndpoints.public_scan_baseline(scan_id), msg, expire=1800, pipe=pipe
        )
        connector.set_and_publish.assert_called_once_with(
            MessageEndpoints.scan_baseline(), msg, pipe=pipe
        )
