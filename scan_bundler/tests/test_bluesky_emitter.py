from unittest import mock
from bec_lib import messages

import msgpack
import pytest
from test_scan_bundler import load_ScanBundlerMock

from bec_lib import MessageEndpoints
from scan_bundler.bluesky_emitter import BlueskyEmitter


@pytest.mark.parametrize("scanID", ["alskdj"])
def test_run_start_document(scanID):
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    with mock.patch.object(bls_emitter.producer, "send") as send:
        with mock.patch.object(bls_emitter, "send_descriptor_document") as send_descr:
            with mock.patch.object(
                bls_emitter, "_get_run_start_document", return_value={}
            ) as get_doc:
                bls_emitter.send_run_start_document(scanID)
                get_doc.assert_called_once_with(scanID)
                send.assert_called_once_with(
                    MessageEndpoints.bluesky_events(), msgpack.dumps(("start", {}))
                )
                send_descr.assert_called_once_with(scanID)


def test_get_run_start_document():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scanID = "lkajsdl"
    sb.sync_storage[scanID] = {"info": {"queueID": "jdklj", "scan_number": 5}}
    sb.scan_motors[scanID] = [sb.device_manager.devices.samx, sb.device_manager.devices.samy]

    data = bls_emitter._get_run_start_document(scanID)

    assert all(key in data for key in ["time", "uid", "scanID", "queueID", "scan_id", "motors"])
    assert data["motors"] == ("samx", "samy")
    assert data["scan_id"] == 5


def test_send_descriptor_document():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scanID = "lkajsdl"
    bls_emitter.bluesky_metadata[scanID] = {}
    with mock.patch.object(bls_emitter.producer, "send") as send:
        with mock.patch.object(
            bls_emitter, "_get_descriptor_document", return_value={}
        ) as get_descr:
            bls_emitter.send_descriptor_document(scanID)
            get_descr.assert_called_once_with(scanID)
            send.assert_called_once_with(
                MessageEndpoints.bluesky_events(), msgpack.dumps(("descriptor", {}))
            )


def test_bls_cleanup_storage():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scanID = "lkajsdl"
    bls_emitter.bluesky_metadata[scanID] = {}

    bls_emitter.cleanup_storage(scanID)
    assert scanID not in bls_emitter.bluesky_metadata


def test_bls_on_cleanup():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scanID = "lkajsdl"
    with mock.patch.object(bls_emitter, "cleanup_storage") as cleanup:
        bls_emitter.on_cleanup(scanID)
        cleanup.assert_called_once_with(scanID)


def test_bls_on_init():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scanID = "lkajsdl"
    with mock.patch.object(bls_emitter, "send_run_start_document") as start:
        bls_emitter.on_init(scanID)
        start.assert_called_once_with(scanID)
