from unittest import mock

from bec_lib import MessageEndpoints, messages
from test_scan_bundler import load_ScanBundlerMock

from scan_bundler.bec_emitter import BECEmitter


def test_on_scan_point_emit_BEC():
    sb = load_ScanBundlerMock()
    bec_emitter = BECEmitter(sb)

    with mock.patch.object(bec_emitter, "_send_bec_scan_point") as send:
        bec_emitter.on_scan_point_emit("scanID", 2)
        send.assert_called_once_with("scanID", 2)


def test_on_baseline_emit_BEC():
    sb = load_ScanBundlerMock()
    bec_emitter = BECEmitter(sb)

    with mock.patch.object(bec_emitter, "_send_baseline") as send:
        bec_emitter.on_baseline_emit("scanID")
        send.assert_called_once_with("scanID")


def test_send_bec_scan_point():
    sb = load_ScanBundlerMock()
    bec_emitter = BECEmitter(sb)

    scanID = "lkajsdlkj"
    pointID = 2
    sb.sync_storage[scanID] = {"info": {}, "status": "open", "sent": set()}
    sb.sync_storage[scanID][pointID] = {}
    msg = messages.ScanMessage(
        point_id=pointID,
        scanID=scanID,
        data=sb.sync_storage[scanID][pointID],
        metadata={"scanID": "lkajsdlkj", "scan_type": None, "scan_report_devices": None},
    )
    with mock.patch.object(bec_emitter, "add_message") as send:
        bec_emitter._send_bec_scan_point(scanID, pointID)
        send.assert_called_once_with(
            msg,
            MessageEndpoints.scan_segment(),
            MessageEndpoints.public_scan_segment(scanID, pointID),
        )


def test_send_baseline_BEC():
    sb = load_ScanBundlerMock()
    bec_emitter = BECEmitter(sb)

    scanID = "lkajsdlkj"
    sb.sync_storage[scanID] = {"info": {}, "status": "open", "sent": set()}
    sb.sync_storage[scanID]["baseline"] = {}
    msg = messages.ScanBaselineMessage(scanID=scanID, data=sb.sync_storage[scanID]["baseline"])
    with mock.patch.object(sb, "connector") as connector:
        bec_emitter._send_baseline(scanID)
        pipe = connector.pipeline()
        connector.set.assert_called_once_with(
            MessageEndpoints.public_scan_baseline(scanID), msg, expire=1800, pipe=pipe
        )
        connector.set_and_publish.assert_called_once_with(
            MessageEndpoints.scan_baseline(), msg, pipe=pipe
        )
