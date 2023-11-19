import threading
import time
from unittest import mock

import pytest
from bec_lib import messages
from bec_lib.scan_items import ScanItem
from bec_lib.tests.utils import bec_client

from bec_client.callbacks.live_table import LiveUpdatesTable, sort_devices
from bec_client.callbacks.utils import ScanRequestMixin


@pytest.mark.timeout(20)
@pytest.mark.asyncio
async def test_scan_request_mixin(bec_client):
    client = bec_client
    client.start()
    request_msg = messages.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = messages.RequestResponseMessage(
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
            messages.ScanQueueMessage(
                scan_type="grid_scan",
                parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
                queue="primary",
                metadata={"RID": "something"},
            ),
            ["samx"],
        ),
        (
            messages.ScanQueueMessage(
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
    data = messages.ScanMessage(
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
    request_msg = messages.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = messages.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    client.queue.request_storage.update_with_request(request_msg)
    client.queue.request_storage.update_with_response(response_msg)
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    with mock.patch.object(client.queue.queue_storage, "find_queue_item_by_requestID"):
        await live_update.wait_for_request_acceptance()


class ScanItemMock:
    def __init__(self, data):
        self.data = data
        self.metadata = {}


def test_print_table_data(bec_client):
    client = bec_client
    client.start()
    request_msg = messages.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = messages.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    client.queue.request_storage.update_with_request(request_msg)
    client.queue.request_storage.update_with_response(response_msg)
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    live_update.point_data = messages.ScanMessage(
        point_id=0,
        scanID="",
        data={"samx": {"samx": {"value": 0}}},
        metadata={"scan_report_devices": ["samx"], "scan_type": "step"},
    )
    live_update.scan_item = ScanItemMock(data=[live_update.point_data])

    live_update.print_table_data()


def test_print_table_data_lamni_flyer(bec_client):
    client = bec_client
    client.start()
    request_msg = messages.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = messages.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    client.queue.request_storage.update_with_request(request_msg)
    client.queue.request_storage.update_with_response(response_msg)
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    live_update.point_data = messages.ScanMessage(
        point_id=0,
        scanID="",
        data={"lamni_flyer_1": {"value": 0}},
        metadata={"scan_report_devices": ["samx"], "scan_type": "fly"},
    )
    live_update.scan_item = ScanItemMock(data=[live_update.point_data])

    live_update.print_table_data()


def test_print_table_data_hinted_value(bec_client):
    client = bec_client
    client.start()
    request_msg = messages.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = messages.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    client.queue.request_storage.update_with_request(request_msg)
    client.queue.request_storage.update_with_response(response_msg)
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    client.device_manager.devices["samx"]._info["hints"] = {"fields": ["samx_hint"]}
    client.device_manager.devices["samx"].precision = 3
    live_update.point_data = messages.ScanMessage(
        point_id=0,
        scanID="",
        data={"samx": {"samx_hint": {"value": 0}}},
        metadata={"scan_report_devices": ["samx"], "scan_type": "fly"},
    )
    live_update.scan_item = ScanItemMock(data=[live_update.point_data])

    with mock.patch.object(live_update, "table") as mocked_table:
        live_update.dev_values = (len(live_update._get_header()) - 1) * [0]
        live_update.print_table_data()
        mocked_table.get_row.assert_called_with("0", "0.000")


def test_print_table_data_hinted_value_with_precision(bec_client):
    client = bec_client
    client.start()
    request_msg = messages.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    response_msg = messages.RequestResponseMessage(
        accepted=True, message="", metadata={"RID": "something"}
    )
    client.queue.request_storage.update_with_request(request_msg)
    client.queue.request_storage.update_with_response(response_msg)
    live_update = LiveUpdatesTable(client, {"table_wait": 10}, request_msg)
    client.device_manager.devices["samx"]._info["hints"] = {"fields": ["samx_hint"]}
    client.device_manager.devices["samx"].precision = 2
    live_update.point_data = messages.ScanMessage(
        point_id=0,
        scanID="",
        data={"samx": {"samx_hint": {"value": 0}}},
        metadata={"scan_report_devices": ["samx"], "scan_type": "fly"},
    )
    live_update.scan_item = ScanItemMock(data=[live_update.point_data])

    with mock.patch.object(live_update, "table") as mocked_table:
        live_update.dev_values = (len(live_update._get_header()) - 1) * [0]
        live_update.print_table_data()
        mocked_table.get_row.assert_called_with("0", f"{0:.2f}")
