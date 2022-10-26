from unittest import mock

import pytest
from bec_utils import BECMessage
from bec_utils.tests.utils import ConnectorMock
from scan_server.scan_stubs import ScanStubs


@pytest.mark.parametrize(
    "device,parameter,metadata,reference_msg",
    [
        (
            "rtx",
            None,
            None,
            BECMessage.DeviceInstructionMessage(
                device="rtx", action="kickoff", parameter={}, metadata={}
            ),
        ),
        (
            "rtx",
            {"num_pos": 5, "positions": [1, 2, 3, 4, 5], "exp_time": 2},
            None,
            BECMessage.DeviceInstructionMessage(
                device="rtx",
                action="kickoff",
                parameter={"num_pos": 5, "positions": [1, 2, 3, 4, 5], "exp_time": 2},
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
