import collections
from unittest import mock

import pytest

from bec_client.callbacks.move_device import LiveUpdatesReadbackProgressbar, ReadbackDataMixin
from bec_lib import messages
from bec_lib.tests.utils import bec_client


@pytest.mark.asyncio
async def test_move_callback(bec_client):
    client = bec_client
    request = messages.ScanQueueMessage(
        scan_type="umv",
        parameter={"args": {"samx": [10]}, "kwargs": {"relative": True}},
        metadata={"RID": "something"},
    )
    readback = collections.deque()
    readback.extend([[-10], [0], [10]])

    def mock_readback(*args):
        if len(readback) > 1:
            return readback.popleft()
        return readback[0]

    req_done = collections.deque()
    msg_acc = messages.DeviceReqStatusMessage(
        device="samx", success=True, metadata={"RID": "something"}
    ).dumps()
    req_done.extend([[None], [None], [None], [msg_acc]])

    def mock_req_msg(*args):
        if len(req_done) > 1:
            return req_done.popleft()
        return req_done[0]

    with mock.patch("bec_client.callbacks.move_device.check_alarms") as check_alarms_mock:
        with mock.patch.object(ReadbackDataMixin, "wait_for_RID"):
            with mock.patch.object(LiveUpdatesReadbackProgressbar, "wait_for_request_acceptance"):
                with mock.patch.object(ReadbackDataMixin, "get_device_values", mock_readback):
                    with mock.patch.object(
                        ReadbackDataMixin, "get_request_done_msgs", mock_req_msg
                    ):
                        await LiveUpdatesReadbackProgressbar(bec=client, request=request).run()


@pytest.mark.asyncio
async def test_move_callback_with_report_instruction(bec_client):
    client = bec_client
    request = messages.ScanQueueMessage(
        scan_type="umv",
        parameter={"args": {"samx": [10]}, "kwargs": {"relative": True}},
        metadata={"RID": "something"},
    )
    readback = collections.deque()
    readback.extend([[-10], [0], [10]])
    report_instruction = {
        "readback": {
            "RID": "something",
            "devices": ["samx"],
            "start": [0],
            "end": [10],
        }
    }

    def mock_readback(*args):
        if len(readback) > 1:
            return readback.popleft()
        return readback[0]

    req_done = collections.deque()
    msg_acc = messages.DeviceReqStatusMessage(
        device="samx", success=True, metadata={"RID": "something"}
    ).dumps()
    req_done.extend([[None], [None], [None], [msg_acc]])

    def mock_req_msg(*args):
        if len(req_done) > 1:
            return req_done.popleft()
        return req_done[0]

    with mock.patch("bec_client.callbacks.move_device.check_alarms") as check_alarms_mock:
        with mock.patch.object(ReadbackDataMixin, "wait_for_RID"):
            with mock.patch.object(LiveUpdatesReadbackProgressbar, "wait_for_request_acceptance"):
                with mock.patch.object(ReadbackDataMixin, "get_device_values", mock_readback):
                    with mock.patch.object(
                        ReadbackDataMixin, "get_request_done_msgs", mock_req_msg
                    ):
                        await LiveUpdatesReadbackProgressbar(
                            bec=client, report_instruction=report_instruction, request=request
                        ).run()
