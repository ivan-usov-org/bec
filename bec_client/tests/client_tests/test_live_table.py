import threading
import time
from unittest import mock

import pytest
from bec_utils import BECMessage

from bec_client.callbacks.live_table import LiveUpdatesTable, sort_devices
from bec_client.callbacks.utils import ScanRequestMixin

from .utils import bec_client


@pytest.mark.timeout(20)
@pytest.mark.asyncio
async def test_scan_request_mixin(bec_client):
    client = bec_client
    client.start()
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = BECMessage.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    request_mixin = ScanRequestMixin(client, "something")

    def update_with_response(request_msg):
        time.sleep(1)
        client.queue.request_storage.update_with_response(response_msg)

    client.queue.request_storage.update_with_request(request_msg)
    threading.Thread(target=update_with_response, args=(response_msg,)).start()
    with mock.patch.object(client.queue.queue_storage, "find_queue_item_by_requestID"):
        await request_mixin.wait()


def test_sort_devices():
    devices = sort_devices(["samx", "bpm4i", "samy", "bpm4s"], ["samx", "samy"])
    assert devices == ["samx", "samy", "bpm4i", "bpm4s"]


@pytest.mark.parametrize(
    "request_msg,scan_report_devices",
    [
        (
            BECMessage.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            ),
            ["samx"],
        ),
        (
            BECMessage.ScanQueueMessage(
                scan_type="round_scan",
                parameter={"args": {"samx": ["samy", 0, 25, 5, 3]}},
                queue="primary",
                metadata={"RID": "something"},
            ),
            ["samx", "samy"],
        ),
    ],
)
def test_get_devices_from_scan_data(bec_client, request_msg, scan_report_devices):
    client = bec_client
    client.start()
    data = BECMessage.ScanMessage(
        point_id=0, scanID="", data={}, metadata={"scan_report_devices": scan_report_devices}
    )
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    devices = live_update.get_devices_from_scan_data(data)
    assert devices[0 : len(scan_report_devices)] == scan_report_devices


@pytest.mark.timeout(20)
@pytest.mark.asyncio
async def test_wait_for_request_acceptance(bec_client):
    client = bec_client
    client.start()
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = BECMessage.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    client.queue.request_storage.update_with_request(request_msg)
    client.queue.request_storage.update_with_response(response_msg)
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    with mock.patch.object(client.queue.queue_storage, "find_queue_item_by_requestID"):
        await live_update.wait_for_request_acceptance()
