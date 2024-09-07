import pytest

from bec_lib import messages
from bec_lib.endpoints import MessageEndpoints
from bec_server.scan_server.scan_server import ScanServer


def test_start_scan_server(scan_server):
    assert isinstance(scan_server, ScanServer)


@pytest.mark.parametrize(
    "scan_msg",
    [
        messages.ScanQueueMessage(
            scan_type="fermat_scan",
            parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"step": 3}},
            queue="primary",
            metadata={"RID": "1234"},
        )
    ],
)
def test_scan_server_scan_request(scan_server, scan_msg):
    scan_server.connector.send(MessageEndpoints.scan_queue_request(), scan_msg)
    while True:
        msgs = scan_server.connector.lrange(MessageEndpoints.scan_queue_history(), 0, -1)
        if not msgs:
            continue
        if msgs[0].info["request_blocks"][0]["msg"] == scan_msg:
            break
    print(msgs)
