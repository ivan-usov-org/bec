import pytest
from bec_client_lib.core import BECMessage
from bec_client_lib.core.tests.utils import bec_client
from bec_client_lib.queue_items import QueueItem

from bec_client.callbacks.ipython_live_updates import IPythonLiveUpdates


@pytest.mark.timeout(20)
def test_live_updates_process_queue(bec_client):
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
        request_blocks=[],
        status="PENDING",
        active_request_block={},
        scanID=["scanID"],
    )
    res = live_updates._process_queue(queue, request_msg, "req_id")
    assert res is False
