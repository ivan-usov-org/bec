import pytest

from bec_client_lib.core import BECMessage, MessageEndpoints
from bec_client_lib.core.tests.utils import ConnectorMock
from bec_client_lib.scan_manager import ScanManager, ScanStorage

# pylint: disable=missing-function-docstring


@pytest.mark.parametrize(
    "queue_msg",
    [
        BECMessage.ScanQueueStatusMessage(
            queue={
                "primary": {
                    "info": [
                        {
                            "queueID": "7c15c9a2-71d4-4f2a-91a7-c4a63088fa38",
                            "scanID": ["bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5"],
                            "is_scan": [True],
                            "request_blocks": [
                                {
                                    "msg": b"\x84\xa8msg_type\xa4scan\xa7content\x83\xa9scan_type\xabfermat_scan\xa9parameter\x82\xa4args\x82\xa4samx\x92\xfe\x02\xa4samy\x92\xfe\x02\xa6kwargs\x83\xa4step\xcb?\xf8\x00\x00\x00\x00\x00\x00\xa8exp_time\xcb?\x94z\xe1G\xae\x14{\xa8relative\xc3\xa5queue\xa7primary\xa8metadata\x81\xa3RID\xd9$cd8fc68f-fe65-4031-9a37-e0e7ba9df542\xa7version\xcb?\xf0\x00\x00\x00\x00\x00\x00",
                                    "RID": "cd8fc68f-fe65-4031-9a37-e0e7ba9df542",
                                    "scan_motors": ["samx", "samy"],
                                    "is_scan": True,
                                    "scan_number": 25,
                                    "scanID": "bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5",
                                    "metadata": {"RID": "cd8fc68f-fe65-4031-9a37-e0e7ba9df542"},
                                    "content": {
                                        "scan_type": "fermat_scan",
                                        "parameter": {
                                            "args": {"samx": [-2, 2], "samy": [-2, 2]},
                                            "kwargs": {
                                                "step": 1.5,
                                                "exp_time": 0.02,
                                                "relative": True,
                                            },
                                        },
                                        "queue": "primary",
                                    },
                                }
                            ],
                            "scan_number": [25],
                            "status": "PENDING",
                            "active_request_block": None,
                        }
                    ],
                    "status": "RUNNING",
                }
            }
        ),
    ],
)
def test_update_with_queue_status(queue_msg):
    scan_manager = ScanManager(ConnectorMock(""))
    scan_manager.producer._get_buffer[MessageEndpoints.scan_queue_status()] = queue_msg.dumps()
    scan_manager.update_with_queue_status(queue_msg)
    assert (
        scan_manager.scan_storage.find_scan_by_ID("bfa582aa-f9cd-4258-ab5d-3e5d54d3dde5")
        is not None
    )
