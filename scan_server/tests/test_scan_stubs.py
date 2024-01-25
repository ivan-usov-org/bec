from unittest import mock
from bec_lib import messages

import pytest

from bec_lib import MessageEndpoints
from bec_lib.tests.utils import ConnectorMock
from scan_server.scan_stubs import ScanAbortion, ScanStubs


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
def test_kickoff(device, parameter, metadata, reference_msg):
    connector = ConnectorMock("")
    stubs = ScanStubs(connector.producer())
    msg = list(stubs.kickoff(device=device, parameter=parameter, metadata=metadata))
    assert msg[0] == reference_msg


@pytest.mark.parametrize(
    "msg,raised_error",
    [
        (
            messages.DeviceRPCMessage(device="samx", return_val="", out="", success=True),
            None,
        ),
        (
            messages.DeviceRPCMessage(
                device="samx",
                return_val="",
                out={
                    "error": "TypeError",
                    "msg": "some weird error",
                    "traceback": "traceback",
                },
                success=False,
            ),
            ScanAbortion,
        ),
        (
            messages.DeviceRPCMessage(
                device="samx",
                return_val="",
                out="",
                success=False,
            ),
            ScanAbortion,
        ),
    ],
)
def test_rpc_raises_scan_abortion(msg, raised_error):
    connector = ConnectorMock("")
    stubs = ScanStubs(connector.producer())
    msg = msg
    with mock.patch.object(stubs.producer, "get", return_value=msg) as prod_get:
        if raised_error is None:
            stubs._get_from_rpc("rpc-id")
        else:
            with pytest.raises(ScanAbortion):
                stubs._get_from_rpc("rpc-id")

        prod_get.assert_called_with(MessageEndpoints.device_rpc("rpc-id"))
