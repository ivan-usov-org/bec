from unittest import mock

import pytest

from bec_lib import messages
from bec_server.scan_server.scan_assembler import ScanAssembler
from bec_server.scan_server.scans import FermatSpiralScan, LineScan


@pytest.fixture
def scan_assembler():
    return ScanAssembler(parent=mock.MagicMock())


@pytest.mark.parametrize(
    "msg, request_inputs_expected",
    [
        (
            # Fermat scan with args and kwargs, matching the FermatSpiralScan signature
            messages.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"steps": 3}},
                queue="primary",
            ),
            {
                "arg_bundle": [],
                "inputs": {
                    "motor1": "samx",
                    "start_motor1": -5,
                    "stop_motor1": 5,
                    "motor2": "samy",
                    "start_motor2": -5,
                    "stop_motor2": 5,
                },
                "kwargs": {"steps": 3},
            },
        ),
        (
            # Fermat scan with no args; everything is in kwargs
            messages.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={
                    "args": [],
                    "kwargs": {
                        "motor1": "samx",
                        "start_motor1": -5,
                        "stop_motor1": 5,
                        "motor2": "samy",
                        "start_motor2": -5,
                        "stop_motor2": 5,
                        "steps": 3,
                    },
                },
                queue="primary",
            ),
            {
                "arg_bundle": [],
                "inputs": {
                    "motor1": "samx",
                    "start_motor1": -5,
                    "stop_motor1": 5,
                    "motor2": "samy",
                    "start_motor2": -5,
                    "stop_motor2": 5,
                },
                "kwargs": {"steps": 3},
            },
        ),
        (
            # Fermat scan with mixed args and kwargs
            messages.ScanQueueMessage(
                scan_type="fermat_scan",
                parameter={
                    "args": ["samx"],
                    "kwargs": {
                        "start_motor1": -5,
                        "stop_motor1": 5,
                        "motor2": "samy",
                        "start_motor2": -5,
                        "stop_motor2": 5,
                        "steps": 3,
                    },
                },
                queue="primary",
            ),
            {
                "arg_bundle": [],
                "inputs": {
                    "motor1": "samx",
                    "start_motor1": -5,
                    "stop_motor1": 5,
                    "motor2": "samy",
                    "start_motor2": -5,
                    "stop_motor2": 5,
                },
                "kwargs": {"steps": 3},
            },
        ),
        (
            # Line scan with arg bundle
            messages.ScanQueueMessage(
                scan_type="line_scan",
                parameter={"args": {"samx": (-5, 5), "samy": (-5, 5)}, "kwargs": {"steps": 3}},
                queue="primary",
            ),
            {"arg_bundle": ["samx", -5, 5, "samy", -5, 5], "inputs": {}, "kwargs": {"steps": 3}},
        ),
    ],
)
def test_scan_assembler_request_inputs(msg, request_inputs_expected, scan_assembler):

    class MockScanManager:
        available_scans = {
            "fermat_scan": {"class": "FermatSpiralScan"},
            "line_scan": {"class": "LineScan"},
        }
        scan_dict = {"FermatSpiralScan": FermatSpiralScan, "LineScan": LineScan}

    with mock.patch.object(scan_assembler, "scan_manager", MockScanManager()):
        request = scan_assembler.assemble_device_instructions(msg, "scan_id")
        assert request.request_inputs == request_inputs_expected
