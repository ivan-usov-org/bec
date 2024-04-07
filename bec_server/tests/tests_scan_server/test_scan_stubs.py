import threading
from unittest import mock

import pytest

from bec_lib import MessageEndpoints, messages
from bec_lib.tests.utils import ConnectorMock
from bec_server.scan_server.errors import DeviceMessageError
from bec_server.scan_server.scan_stubs import ScanAbortion, ScanStubs


@pytest.fixture
def stubs():
    connector = ConnectorMock("")
    shutdown_event = threading.Event()
    yield ScanStubs(connector, shutdown_event=shutdown_event)
    shutdown_event.set()


@pytest.mark.parametrize(
    "device,parameter,metadata,reference_msg",
    [
        (
            "rtx",
            None,
            None,
            messages.DeviceInstructionMessage(
                device="rtx",
                action="kickoff",
                parameter={"configure": {}, "wait_group": "kickoff"},
                metadata={},
            ),
        ),
        (
            "rtx",
            {"num_pos": 5, "positions": [1, 2, 3, 4, 5], "exp_time": 2},
            None,
            messages.DeviceInstructionMessage(
                device="rtx",
                action="kickoff",
                parameter={
                    "configure": {"num_pos": 5, "positions": [1, 2, 3, 4, 5], "exp_time": 2},
                    "wait_group": "kickoff",
                },
                metadata={},
            ),
        ),
    ],
)
def test_kickoff(stubs, device, parameter, metadata, reference_msg):
    connector = ConnectorMock("")
    stubs = ScanStubs(connector)
    msg = list(stubs.kickoff(device=device, parameter=parameter, metadata=metadata))
    assert msg[0] == reference_msg


@pytest.mark.parametrize(
    "msg,raised_error",
    [
        (messages.DeviceRPCMessage(device="samx", return_val="", out="", success=True), None),
        (
            messages.DeviceRPCMessage(
                device="samx",
                return_val="",
                out={"error": "TypeError", "msg": "some weird error", "traceback": "traceback"},
                success=False,
            ),
            ScanAbortion,
        ),
        (
            messages.DeviceRPCMessage(device="samx", return_val="", out="", success=False),
            ScanAbortion,
        ),
    ],
)
def test_rpc_raises_scan_abortion(stubs, msg, raised_error):
    with mock.patch.object(stubs.connector, "get", return_value=msg) as prod_get:
        if raised_error is None:
            stubs._get_from_rpc("rpc-id")
        else:
            with pytest.raises(raised_error):
                stubs._get_from_rpc("rpc-id")

        prod_get.assert_called_with(MessageEndpoints.device_rpc("rpc-id"))


def test_rpc_raises_scan_abortion_on_shutdown_event(stubs):
    stubs.shutdown_event.set()
    with pytest.raises(ScanAbortion):
        stubs._get_from_rpc("rpc-id")


@pytest.mark.parametrize(
    "msg, ret_value, raised_error",
    [
        (messages.ProgressMessage(value=10, max_value=100, done=False), None, False),
        (
            messages.ProgressMessage(
                value=10, max_value=100, done=False, metadata={"RID": "wrong"}
            ),
            None,
            False,
        ),
        (
            messages.ProgressMessage(value=10, max_value=100, done=False, metadata={"RID": "rid"}),
            10,
            False,
        ),
        (
            messages.DeviceStatusMessage(device="samx", status=0, metadata={"RID": "rid"}),
            None,
            True,
        ),
    ],
)
def test_device_progress(stubs, msg, ret_value, raised_error):
    if raised_error:
        with pytest.raises(DeviceMessageError):
            with mock.patch.object(stubs.connector, "get", return_value=msg):
                assert stubs.get_device_progress(device="samx", RID="rid") == ret_value
        return
    with mock.patch.object(stubs.connector, "get", return_value=msg):
        assert stubs.get_device_progress(device="samx", RID="rid") == ret_value
