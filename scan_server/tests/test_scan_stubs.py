from unittest import mock

import pytest

from bec_client_lib.core import BECMessage, MessageEndpoints
from bec_client_lib.core.tests.utils import ConnectorMock
from scan_server.scan_stubs import ScanAbortion, ScanStubs


@pytest.mark.parametrize(
    "device,parameter,metadata,reference_msg",
    [
        (
            "rtx",
            None,
            None,
            BECMessage.DeviceInstructionMessage(
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
            BECMessage.DeviceInstructionMessage(
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
            BECMessage.DeviceRPCMessage(device="samx", return_val="", out="", success=True),
            None,
        ),
        (
            BECMessage.DeviceRPCMessage(
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
            BECMessage.DeviceRPCMessage(
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
    msg = msg.dumps()
    with mock.patch.object(stubs.producer, "get", return_value=msg) as prod_get:
        if raised_error is None:
            stubs._get_from_rpc("rpc-id")
        else:
            with pytest.raises(ScanAbortion):
                stubs._get_from_rpc("rpc-id")

        prod_get.assert_called_with(MessageEndpoints.device_rpc("rpc-id"))
