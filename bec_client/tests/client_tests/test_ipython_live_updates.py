from unittest import mock

import pytest
from bec_lib.core import BECMessage
from bec_lib.core.tests.utils import bec_client
from bec_lib.queue_items import QueueItem

from bec_client.callbacks.ipython_live_updates import IPythonLiveUpdates


@pytest.mark.timeout(20)
def test_live_updates_process_queue_pending(bec_client):
    client = bec_client
    client.start()
    live_updates = IPythonLiveUpdates(client)
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue = QueueItem(
        scan_manager=client.queue,
        queueID="queueID",
        request_blocks=[request_msg],
        status="PENDING",
        active_request_block={},
        scanID=["scanID"],
    )
    client.queue.queue_storage.current_scan_queue = {"primary": {"status": "RUNNING"}}
    with mock.patch.object(queue, "_update_with_buffer"):
        with mock.patch(
            "bec_lib.queue_items.QueueItem.queue_position", new_callable=mock.PropertyMock
        ) as queue_pos:
            queue_pos.return_value = 2
            with mock.patch.object(
                live_updates,
                "_available_req_blocks",
                return_value=[{"report_instructions": [], "content": {"scan_type": "grid_scan"}}],
            ):
                with mock.patch.object(live_updates, "_process_report_instructions") as process:
                    with mock.patch("builtins.print") as prt:
                        res = live_updates._process_queue(queue, request_msg, "req_id")
                        prt.assert_called_once()
                        process.assert_not_called()
                    assert res is False


@pytest.mark.timeout(20)
def test_live_updates_process_queue_running(bec_client):
    client = bec_client
    client.start()
    live_updates = IPythonLiveUpdates(client)
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue = QueueItem(
        scan_manager=client.queue,
        queueID="queueID",
        request_blocks=[request_msg],
        status="RUNNING",
        active_request_block={},
        scanID=["scanID"],
    )
    live_updates._active_request = request_msg
    client.queue.queue_storage.current_scan_queue = {"primary": {"status": "RUNNING"}}
    with mock.patch.object(queue, "_update_with_buffer"):
        with mock.patch(
            "bec_lib.queue_items.QueueItem.queue_position", new_callable=mock.PropertyMock
        ) as queue_pos:
            queue_pos.return_value = 2
            with mock.patch.object(
                live_updates,
                "_available_req_blocks",
                return_value=[
                    {
                        "report_instructions": [{"wait_table": 10}],
                        "content": {"scan_type": "grid_scan"},
                    }
                ],
            ):
                with mock.patch.object(live_updates, "_process_instruction") as process:
                    with mock.patch("builtins.print") as prt:
                        res = live_updates._process_queue(queue, request_msg, "req_id")
                        prt.assert_not_called()
                        process.assert_called_once_with({"wait_table": 10})
                    assert res is True


@pytest.mark.timeout(20)
def test_live_updates_process_queue_without_status(bec_client):
    client = bec_client
    client.start()
    live_updates = IPythonLiveUpdates(client)
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )
    queue = QueueItem(
        scan_manager=client.queue,
        queueID="queueID",
        request_blocks=[request_msg],
        status=None,
        active_request_block={},
        scanID=["scanID"],
    )
    with mock.patch.object(queue, "_update_with_buffer"):
        assert live_updates._process_queue(queue, request_msg, "req_id") is False


@pytest.mark.timeout(20)
def test_live_updates_process_queue_without_queue_number(bec_client):
    client = bec_client
    client.start()
    live_updates = IPythonLiveUpdates(client)
    request_msg = BECMessage.ScanQueueMessage(
        scan_type="grid_scan",
        parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
        queue="primary",
        metadata={"RID": "something"},
    )

    with mock.patch(
        "bec_lib.queue_items.QueueItem.queue_position", new_callable=mock.PropertyMock
    ) as queue_pos:
        queue = QueueItem(
            scan_manager=client.queue,
            queueID="queueID",
            request_blocks=[request_msg],
            status="PENDING",
            active_request_block={},
            scanID=["scanID"],
        )
        queue_pos.return_value = None
        with mock.patch.object(queue, "_update_with_buffer"):
            assert live_updates._process_queue(queue, request_msg, "req_id") is False


# @pytest.mark.timeout(20)
# @pytest.mark.asyncio
# def test_live_updates_process_instruction_readback(bec_client):
#     client = bec_client
#     client.start()
#     live_updates = IPythonLiveUpdates(client)
#     request_msg = BECMessage.ScanQueueMessage(
#         scan_type="grid_scan",
#         parameter={"args": {"samx": (-5, 5, 3)}, "kwargs": {}},
#         queue="primary",
#         metadata={"RID": "something"},
#     )
#     live_updates._active_request = request_msg
#     live_updates._user_callback = []
#     client.queue.queue_storage.current_scan_queue = {"primary": {"status": "RUNNING"}}
#     with mock.patch(
#         "bec_client.callbacks.ipython_live_updates.LiveUpdatesTable", new_callable=mock.Co
#     ) as table:
#         live_updates._process_instruction({"table_wait": 10})
#         table.assert_called_once_with(
#             client, report_instructions={"table_wait": 10}, request=request_msg, callbacks=[]
#         )
