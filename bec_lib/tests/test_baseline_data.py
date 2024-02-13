import pytest
from _collections_abc import dict_items, dict_keys, dict_values

from bec_lib import messages
from bec_lib.baseline_data import BaselineData


@pytest.fixture
def baseline_data():
    baseline_data = BaselineData()
    msg = messages.ScanBaselineMessage(
        scanID="scanID",
        data={
            "slit0": {
                "setpoint": {"value": 0, "timestamp": 0},
                "slit0": {"value": 0, "timestamp": 0},
            }
        },
    )
    baseline_data.set(msg)

    yield baseline_data


def test_baseline_data_signals_single_val(baseline_data):
    assert baseline_data.slit0.setpoint.val[0] == 0
    assert baseline_data["slit0"]["setpoint"]["val"][0] == 0
    assert baseline_data["slit0"]["setpoint"]["timestamp"][0] == 0
    assert baseline_data["slit0"]["setpoint"].get("val")[0] == 0
    assert baseline_data["slit0"]["setpoint"].get("timestamp")[0] == 0
    assert baseline_data["slit0"].get("setpoint").get("val")[0] == 0
    assert baseline_data["slit0"].get("setpoint").get("timestamp")[0] == 0
    assert baseline_data.get("slit0").get("setpoint").get("val")[0] == 0


def test_baseline_data_dict_operations(baseline_data):
    assert baseline_data.keys() == {"slit0": 0}.keys()
    assert list(baseline_data.values()) == [
        {"setpoint": {"value": 0, "timestamp": 0}, "slit0": {"value": 0, "timestamp": 0}}
    ]
    assert dict(baseline_data.items()) == dict(
        {
            "slit0": {
                "setpoint": {"value": 0, "timestamp": 0},
                "slit0": {"value": 0, "timestamp": 0},
            }
        }.items()
    )

    assert "slit0" in baseline_data
    assert "not_a_device" not in baseline_data

    assert len(baseline_data) == 1


def test_baseline_data_signal_dict_operations(baseline_data):
    assert baseline_data.slit0.setpoint.keys() == {"value": 0, "timestamp": 0}.keys()
    assert list(baseline_data.slit0.setpoint.values()) == [0, 0]
    assert dict(baseline_data.slit0.setpoint.items()) == {"value": 0, "timestamp": 0}

    assert len(baseline_data.slit0.setpoint) == 2


def test_baseline_data_device_dict_operations(baseline_data):
    assert baseline_data.slit0.keys() == {"setpoint": 0, "slit0": 0}.keys()
    assert list(baseline_data.slit0.values()) == [
        {"value": 0, "timestamp": 0},
        {"value": 0, "timestamp": 0},
    ]
    assert dict(baseline_data.slit0.items()) == {
        "setpoint": {"value": 0, "timestamp": 0},
        "slit0": {"value": 0, "timestamp": 0},
    }
