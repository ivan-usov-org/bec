import csv
import os
from unittest import mock

import pytest

from bec_lib import messages
from bec_lib.scan_items import ScanItem
from bec_lib.scan_report import ScanReport
from bec_lib.utils import _write_csv, scan_to_dict, scan_to_csv, user_access


class class_mock:
    USER_ACCESS = []

    @user_access
    def _func_decorated_not_in_user_access(self, *args, **kwargs):
        return None

    @user_access
    def _func_decorated_in_user_access(self, *args, **kwargs):
        return None

    def _func_not_decorated_not_in_user_access(self, *args, **kwargs):
        return None


@pytest.fixture(scope="class")
def class_factory():
    yield class_mock()


def test_user_access(class_factory):
    """Test user_access function."""
    assert class_factory.USER_ACCESS == [
        "_func_decorated_not_in_user_access",
        "_func_decorated_in_user_access",
    ]


def test__write_csv():
    """Test _write_csv function."""

    output = [["#samx", "bpm4i"], ["2.056", "100.1234"], ["0.0", "-0.12345"]]

    _write_csv(output_name="test.csv", delimiter=",", dialect=None, output=output)
    with open("test.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row, row_value in zip(csvreader, output):
            assert row == row_value

    os.remove("test.csv")


def test_scan_to_dict():
    """Test scan_to_dict function."""

    # input_dict = input_dict = create_scan_report()
    scan_manager_mock = mock.MagicMock()
    scan_item = ScanItem(
        scan_manager=scan_manager_mock, queueID="test", scan_number=[1], scanID=["tmp"], status="OK"
    )
    for scan_msg in create_scan_messages().values():
        scan_item.data.set(scan_msg.content["point_id"], scan_msg)

    output_dict = {
        "timestamp": {
            "bpm4i": [1689340694.3702202, 1689340694.3702202, 1689340694.3702202],
            "samx": [1689957983.5892477, 1689957983.6680737, 1689957983.747301],
            "samx_setpoint": [1689957983.5038617, 1689957983.607795, 1689957983.6842027],
            "samx_motor_is_moving": [1689957983.5894659, 1689957983.6683168, 1689957983.7475493],
        },
        "value": {
            "bpm4i": [0.8140756084557457, 0.980531184880259, 0.8360317021600272],
            "samx": [-2.997623536163973, 2.0203129364662855, 7.01317320459588],
            "samx_setpoint": [-2.9878629905097327, 2.0121370094902673, 7.012137009490267],
            "samx_motor_is_moving": [0, 0, 0],
        },
    }
    return_dict = scan_to_dict(scan_item, flat=True)
    assert return_dict == output_dict


def test_scan_to_csv():
    """Test scan_to_csv function."""
    scanreport_mock = mock.MagicMock(spec=ScanReport)
    with pytest.raises(Exception):
        scan_to_csv(
            scan_report=scanreport_mock,
            output_name=1234,
            delimiter=",",
            dialect=None,
            header=None,
            write_metadata=True,
        )
    with pytest.raises(Exception):
        scan_to_csv(
            scan_report=[scanreport_mock, scanreport_mock, scanreport_mock],
            output_name="test.csv",
            delimiter=",",
            dialect=None,
            header=None,
            write_metadata=True,
        )
    with pytest.raises(Exception):
        scan_to_csv(
            scan_report=[scanreport_mock, scanreport_mock, scanreport_mock],
            output_name="test.csv",
            delimiter=123,
            dialect=None,
            header=None,
            write_metadata=True,
        )


def create_scan_messages():
    return {
        0: messages.ScanMessage(
            **{
                "point_id": 0,
                "scanID": "661efd43-49e5-4cc8-946e-d1c0e826f262",
                "data": {
                    "bpm4i": {
                        "bpm4i": {"value": 0.8140756084557457, "timestamp": 1689340694.3702202}
                    },
                    "samx": {
                        "samx": {"value": -2.997623536163973, "timestamp": 1689957983.5892477},
                        "samx_setpoint": {
                            "value": -2.9878629905097327,
                            "timestamp": 1689957983.5038617,
                        },
                        "samx_motor_is_moving": {"value": 0, "timestamp": 1689957983.5894659},
                    },
                },
            },
            metadata={
                "stream": "primary",
                "DIID": 3,
                "sample_name": "temp",
                "exp_time": 0.001,
                "RID": "b4d74aa3-62f7-4444-abea-67dc33e75f34",
                "scanID": "661efd43-49e5-4cc8-946e-d1c0e826f262",
                "queueID": "82c6cfd2-62d6-4303-be7a-5d6ca875d6f3",
                "scan_motors": ["samx"],
                "readout_priority": {"monitored": ["samx"], "baseline": [], "ignored": []},
                "num_points": 3,
                "positions": "...",
                "scan_name": "line_scan",
                "scan_type": "step",
                "scan_number": 260,
                "dataset_number": 260,
                "scan_report_hint": "table",
                "scan_report_devices": ["samx"],
                "scan_msgs": [
                    "messages.ScanQueueMessage(**{'scan_type': 'line_scan', 'parameter': {'args':"
                    " {'samx': [-5, 5]}, 'kwargs': {'steps': 3, 'exp_time': 0.001, 'relative':"
                    " True}}, 'queue': 'primary'}, metadata={'sample_name': 'temp', 'exp_time':"
                    " 0.02, 'RID': 'b4d74aa3-62f7-4444-abea-67dc33e75f34'})"
                ],
            }
        ),
        1: messages.ScanMessage(
            **{
                "point_id": 1,
                "scanID": "661efd43-49e5-4cc8-946e-d1c0e826f262",
                "data": {
                    "bpm4i": {
                        "bpm4i": {"value": 0.980531184880259, "timestamp": 1689340694.3702202}
                    },
                    "samx": {
                        "samx": {"value": 2.0203129364662855, "timestamp": 1689957983.6680737},
                        "samx_setpoint": {
                            "value": 2.0121370094902673,
                            "timestamp": 1689957983.607795,
                        },
                        "samx_motor_is_moving": {"value": 0, "timestamp": 1689957983.6683168},
                    },
                },
            },
            metadata={
                "stream": "primary",
                "DIID": 3,
                "sample_name": "temp",
                "exp_time": 0.001,
                "RID": "b4d74aa3-62f7-4444-abea-67dc33e75f34",
                "scanID": "661efd43-49e5-4cc8-946e-d1c0e826f262",
                "queueID": "82c6cfd2-62d6-4303-be7a-5d6ca875d6f3",
                "scan_motors": ["samx"],
                "readout_priority": {"monitored": ["samx"], "baseline": [], "ignored": []},
                "num_points": 3,
                "positions": "...",
                "scan_name": "line_scan",
                "scan_type": "step",
                "scan_number": 260,
                "dataset_number": 260,
                "scan_report_hint": "table",
                "scan_report_devices": ["samx"],
                "scan_msgs": [
                    "messages.ScanQueueMessage(**{'scan_type': 'line_scan', 'parameter': {'args':"
                    " {'samx': [-5, 5]}, 'kwargs': {'steps': 3, 'exp_time': 0.001, 'relative':"
                    " True}}, 'queue': 'primary'}, metadata={'sample_name': 'temp', 'exp_time':"
                    " 0.02, 'RID': 'b4d74aa3-62f7-4444-abea-67dc33e75f34'})"
                ],
            }
        ),
        2: messages.ScanMessage(
            **{
                "point_id": 2,
                "scanID": "661efd43-49e5-4cc8-946e-d1c0e826f262",
                "data": {
                    "bpm4i": {
                        "bpm4i": {"value": 0.8360317021600272, "timestamp": 1689340694.3702202}
                    },
                    "samx": {
                        "samx": {"value": 7.01317320459588, "timestamp": 1689957983.747301},
                        "samx_setpoint": {
                            "value": 7.012137009490267,
                            "timestamp": 1689957983.6842027,
                        },
                        "samx_motor_is_moving": {"value": 0, "timestamp": 1689957983.7475493},
                    },
                },
            },
            metadata={
                "stream": "primary",
                "DIID": 3,
                "sample_name": "temp",
                "exp_time": 0.001,
                "RID": "b4d74aa3-62f7-4444-abea-67dc33e75f34",
                "scanID": "661efd43-49e5-4cc8-946e-d1c0e826f262",
                "queueID": "82c6cfd2-62d6-4303-be7a-5d6ca875d6f3",
                "scan_motors": ["samx"],
                "readout_priority": {"monitored": ["samx"], "baseline": [], "ignored": []},
                "num_points": 3,
                "positions": "...",
                "scan_name": "line_scan",
                "scan_type": "step",
                "scan_number": 260,
                "dataset_number": 260,
                "scan_report_hint": "table",
                "scan_report_devices": ["samx"],
                "scan_msgs": [
                    "messages.ScanQueueMessage(**{'scan_type': 'line_scan', 'parameter': {'args':"
                    " {'samx': [-5, 5]}, 'kwargs': {'steps': 3, 'exp_time': 0.001, 'relative':"
                    " True}}, 'queue': 'primary'}, metadata={'sample_name': 'temp', 'exp_time':"
                    " 0.02, 'RID': 'b4d74aa3-62f7-4444-abea-67dc33e75f34'})"
                ],
            }
        ),
    }
