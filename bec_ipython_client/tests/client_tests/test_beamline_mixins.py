import io
from unittest import mock

import pytest
from rich.console import Console

from bec_ipython_client.beamline_mixin import BeamlineMixin
from bec_ipython_client.plugins.cSAXS.beamline_info import BeamlineInfo
from bec_ipython_client.plugins.SLS.sls_info import OperatorInfo, SLSInfo


def _get_operator_messages(num: int):
    info = {f"sls_operator_messages_message{i}": {"value": f"message{i}"} for i in range(1, num)}
    info.update({f"sls_operator_date_message{i}": {"value": f"message{i}"} for i in range(1, num)})

    for i in range(num, 6):
        info.update({f"sls_operator_messages_message{i}": {"value": ""}})
        info.update({f"sls_operator_date_message{i}": {"value": ""}})

    return info


@pytest.mark.parametrize(
    "info,out",
    (
        [
            (
                _get_operator_messages(6),
                " SLS Operator messages \n┌──────────┬──────────┐\n│ Message  │ Time     │\n├──────────┼──────────┤\n│ message1 │ message1 │\n│ message2 │ message2 │\n│ message3 │ message3 │\n│ message4 │ message4 │\n│ message5 │ message5 │\n└──────────┴──────────┘\n",
            ),
            (
                _get_operator_messages(3),
                " SLS Operator messages \n┌──────────┬──────────┐\n│ Message  │ Time     │\n├──────────┼──────────┤\n│ message1 │ message1 │\n│ message2 │ message2 │\n└──────────┴──────────┘\n",
            ),
        ]
    ),
)
def test_operator_messages(info, out):
    mixin = BeamlineMixin()
    mixin._bl_info_register(OperatorInfo)
    bl_call = mixin._bl_calls[-1]
    with mock.patch.object(bl_call, "_get_operator_messages", return_value=info) as get_op_msgs:
        console = Console(file=io.StringIO(), width=120)
        with mock.patch.object(bl_call, "_get_console", return_value=console):
            mixin.bl_show_all()
            get_op_msgs.assert_called_once()
            # pylint: disable=no-member
            output = console.file.getvalue()
            assert output == out


@pytest.mark.parametrize(
    "info,out",
    (
        [
            (
                {
                    "sls_info_machine_status": {"value": "Light Available"},
                    "sls_info_injection_mode": {"value": "TOP-UP"},
                    "sls_info_current_threshold": {"value": 400.8},
                    "sls_info_current_deadband": {"value": 1.8},
                    "sls_info_filling_pattern": {"value": "Default"},
                    "sls_info_filling_life_time": {"value": 10.2},
                    "sls_info_orbit_feedback_mode": {"value": "on"},
                    "sls_info_fast_orbit_feedback": {"value": "running"},
                    "sls_info_ring_current": {"value": 401.2},
                    "sls_info_crane_usage": {"value": "OFF"},
                },
                "                 SLS Info                 \n┌──────────────────────┬─────────────────┐\n│ Key                  │ Value           │\n├──────────────────────┼─────────────────┤\n│ Machine status       │ Light Available │\n│ Injection mode       │ TOP-UP          │\n│ Ring current         │ 401.200 mA      │\n│ Current threshold    │ 400.8           │\n│ Current deadband     │ 1.8             │\n│ Filling pattern      │ Default         │\n│ SLS filling lifetime │ 10.20 h         │\n│ Orbit feedback mode  │ on              │\n│ Fast orbit feedback  │ running         │\n│ SLS crane usage      │ OFF             │\n└──────────────────────┴─────────────────┘\n",
            ),
        ]
    ),
)
def test_sls_info(info, out):
    mixin = BeamlineMixin()
    mixin._bl_info_register(SLSInfo)
    bl_call = mixin._bl_calls[-1]
    with mock.patch.object(bl_call, "_get_sls_info", return_value=info) as get_sls_info:
        console = Console(file=io.StringIO(), width=120)
        with mock.patch.object(bl_call, "_get_console", return_value=console):
            mixin.bl_show_all()
            get_sls_info.assert_called_once()
            # pylint: disable=no-member
            output = console.file.getvalue()
            assert output == out


def test_bl_show_all():
    mixin = BeamlineMixin()
    mixin._bl_info_register(SLSInfo)
    mixin._bl_info_register(OperatorInfo)
    mixin._bl_info_register(BeamlineInfo)
    calls = mixin._bl_calls
    with mock.patch.object(calls[0], "show") as sls_info:
        with mock.patch.object(calls[1], "show") as op_msgs:
            with mock.patch.object(calls[2], "show") as bl_info:
                mixin.bl_show_all()
                bl_info.assert_called_once()
                op_msgs.assert_called_once()
                sls_info.assert_called_once()


@pytest.mark.parametrize(
    "info,out",
    (
        [
            (
                {
                    "x12sa_op_status": {"value": "attended"},
                    "x12sa_id_gap": {"value": 4.2},
                    "x12sa_storage_ring_vac": {"value": "OK"},
                    "x12sa_es1_shutter_status": {"value": "OPEN"},
                    "x12sa_mokev": {"value": 6.2002},
                    "x12sa_fe_status": {"value": "Open enabled"},
                    "x12sa_es1_valve": {"value": "open"},
                    "x12sa_exposure_box1_pressure": {"value": 7.975205787427068e-09},
                    "x12sa_exposure_box2_pressure": {"value": 7.975205787427068e-09},
                },
                "                X12SA Info                \n┌─────────────────────────┬──────────────┐\n│ Key                     │ Value        │\n├─────────────────────────┼──────────────┤\n│ Beamline operation      │ attended     │\n│ ID gap                  │ 4.200 mm     │\n│ Storage ring vacuum     │ OK           │\n│ Shutter                 │ OPEN         │\n│ Selected energy (mokev) │ 6.200 keV    │\n│ Front end shutter       │ Open enabled │\n│ ES1 valve               │ open         │\n│ Exposure box 1 pressure │ 8.0e-09 mbar │\n│ Exposure box 2 pressure │ 8.0e-09 mbar │\n└─────────────────────────┴──────────────┘\n",
            ),
        ]
    ),
)
def test_bl_info(info, out):
    mixin = BeamlineMixin()
    mixin._bl_info_register(BeamlineInfo)
    bl_call = mixin._bl_calls[-1]
    with mock.patch.object(
        bl_call, "_get_beamline_info_messages", return_value=info
    ) as get_bl_info:
        console = Console(file=io.StringIO(), width=120)
        with mock.patch.object(bl_call, "_get_console", return_value=console):
            mixin.bl_show_all()
            get_bl_info.assert_called_once()
            # pylint: disable=no-member
            output = console.file.getvalue()
            assert output == out
