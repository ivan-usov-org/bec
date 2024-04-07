from unittest import mock

import pytest
from utils import DMMock

from bec_server.scan_server.scan_plugins.flomni_fermat_scan import FlomniFermatScan


@pytest.fixture
def scan_request():
    device_manager = DMMock()
    device_manager.producer = mock.MagicMock()
    flomni_request = FlomniFermatScan(
        fovx=5,
        fovy=5,
        cenx=0.0,
        ceny=0.0,
        exp_time=0.1,
        step=1,
        zshift=0.0,
        angle=0.0,
        device_manager=device_manager,
        metadata={"RID": "1234"},
    )
    yield flomni_request


def test_flomni_fermat_scan(scan_request):
    assert scan_request.fovx == 5
    assert scan_request.fovy == 5


def test_flomni_rotation_no_rotation_required(scan_request):
    with mock.patch.object(scan_request.stubs, "_get_from_rpc") as get_from_rpc_mock:
        get_from_rpc_mock.return_value = 90
        with mock.patch.object(scan_request.stubs, "scan_report_instruction") as scan_report_mock:
            with mock.patch.object(scan_request.stubs, "set") as set_mock:
                list(scan_request.flomni_rotation(90))
                scan_report_mock.assert_not_called()
                assert not set_mock.called


def test_flomni_rotation_rotation_required(scan_request):
    with mock.patch.object(scan_request.stubs, "_get_from_rpc") as get_from_rpc_mock:
        get_from_rpc_mock.return_value = 0
        with mock.patch.object(scan_request.stubs, "scan_report_instruction") as scan_report_mock:
            with mock.patch.object(scan_request.stubs, "set") as set_mock:
                list(scan_request.flomni_rotation(90))
                scan_report_mock.assert_called_once_with(
                    {
                        "readback": {
                            "RID": scan_request.metadata["RID"],
                            "devices": ["fsamroy"],
                            "start": [0],
                            "end": [90],
                        }
                    }
                )
                set_mock.assert_called_once_with(
                    device="fsamroy", value=90, wait_group="flomni_rotation"
                )
