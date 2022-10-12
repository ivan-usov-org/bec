import threading
import time
from unittest import mock

import pytest
from bec_client.callbacks.live_table import (
    LiveUpdatesTable,
    ScanRequestMixin,
    sort_devices,
)
from bec_utils import BECMessage

from .utils import get_bec_client_mock


@pytest.mark.asyncio
async def test_scan_request_mixin():
    client = get_bec_client_mock()
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
    await request_mixin.wait()


def test_sort_devices():
    devices = sort_devices(["samx", "bpm4i", "samy", "bpm4s"], ["samx", "samy"])
    assert devices == ["samx", "samy", "bpm4i", "bpm4s"]


def test_get_devices_from_request():
    client = get_bec_client_mock()
    client.start()
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )

    live_update = LiveUpdatesTable(client, request_msg)
    devices = live_update.get_devices_from_request()
    assert devices[0] == "samx"


@pytest.mark.asyncio
async def test_wait_for_request_acceptance():
    client = get_bec_client_mock()
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
    live_update = LiveUpdatesTable(client, request_msg)
    await live_update.wait_for_request_acceptance()
