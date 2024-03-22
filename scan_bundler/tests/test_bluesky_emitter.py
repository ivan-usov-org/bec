from unittest import mock

import msgpack
import pytest
from test_scan_bundler import load_ScanBundlerMock

from bec_lib import MessageEndpoints, messages
from scan_bundler.bluesky_emitter import BlueskyEmitter


@pytest.mark.parametrize("scan_id", ["alskdj"])
def test_run_start_document(scan_id):
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    with mock.patch.object(bls_emitter.connector, "raw_send") as send:
        with mock.patch.object(bls_emitter, "send_descriptor_document") as send_descr:
            with mock.patch.object(
                bls_emitter, "_get_run_start_document", return_value={}
            ) as get_doc:
                bls_emitter.send_run_start_document(scan_id)
                get_doc.assert_called_once_with(scan_id)
                send.assert_called_once_with(
                    MessageEndpoints.bluesky_events(), msgpack.dumps(("start", {}))
                )
                send_descr.assert_called_once_with(scan_id)


def test_get_run_start_document():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scan_id = "lkajsdl"
    sb.sync_storage[scan_id] = {"info": {"queueID": "jdklj", "scan_number": 5}}
    sb.scan_motors[scan_id] = [sb.device_manager.devices.samx, sb.device_manager.devices.samy]

    data = bls_emitter._get_run_start_document(scan_id)

    assert all(key in data for key in ["time", "uid", "scan_id", "queueID", "scan_id", "motors"])
    assert data["motors"] == ("samx", "samy")
    assert data["scan_id"] == 5


def test_send_descriptor_document():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scan_id = "lkajsdl"
    bls_emitter.bluesky_metadata[scan_id] = {}
    with mock.patch.object(bls_emitter.connector, "raw_send") as send:
        with mock.patch.object(
            bls_emitter, "_get_descriptor_document", return_value={}
        ) as get_descr:
            bls_emitter.send_descriptor_document(scan_id)
            get_descr.assert_called_once_with(scan_id)
            send.assert_called_once_with(
                MessageEndpoints.bluesky_events(), msgpack.dumps(("descriptor", {}))
            )


def test_bls_cleanup_storage():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scan_id = "lkajsdl"
    bls_emitter.bluesky_metadata[scan_id] = {}

    bls_emitter.cleanup_storage(scan_id)
    assert scan_id not in bls_emitter.bluesky_metadata


def test_bls_on_cleanup():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scan_id = "lkajsdl"
    with mock.patch.object(bls_emitter, "cleanup_storage") as cleanup:
        bls_emitter.on_cleanup(scan_id)
        cleanup.assert_called_once_with(scan_id)


def test_bls_on_init():
    sb = load_ScanBundlerMock()
    bls_emitter = BlueskyEmitter(sb)
    scan_id = "lkajsdl"
    with mock.patch.object(bls_emitter, "send_run_start_document") as start:
        bls_emitter.on_init(scan_id)
        start.assert_called_once_with(scan_id)
