from unittest import mock

import pytest

from bec_lib.core.tests.utils import bec_client
from bec_lib.scans import ScanObject


def test_scan_object_raises(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    with mock.patch.object(bec_client, "alarm_handler"):
        with pytest.raises(TypeError):
            obj._run()


def test_scan_object(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    dev = bec_client.device_manager.devices
    with mock.patch.object(bec_client, "alarm_handler"):
        with mock.patch("bec_lib.scan_manager.ScanReport.from_request") as report:
            obj._run(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.1, relative=False)
            report().wait.assert_not_called()


def test_scan_object_wo_live_updates(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    dev = bec_client.device_manager.devices
    bec_client.live_updates = None
    with mock.patch.object(bec_client, "alarm_handler"):
        with mock.patch("bec_lib.scan_manager.ScanReport.from_request") as report:
            obj._run(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.1, relative=False)
            report().wait.assert_not_called()


def test_scan_object_receives_sample_name(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    dev = bec_client.device_manager.devices
    with mock.patch.object(bec_client, "alarm_handler"):
        with mock.patch("bec_lib.scan_manager.ScanReport.from_request") as scan_report:
            with mock.patch.object(bec_client, "get_global_var", return_value="test_sample"):
                obj._run(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.1, relative=False)
                assert scan_report.call_args.args[0].metadata["sample_name"] == "test_sample"


def test_scan_object_receives_scan_group(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    bec_client.scans._scan_group = "group_id"
    dev = bec_client.device_manager.devices
    with mock.patch.object(bec_client, "alarm_handler"):
        with mock.patch("bec_lib.scan_manager.ScanReport.from_request") as scan_report:
            with mock.patch.object(bec_client, "get_global_var", return_value="test_sample"):
                obj._run(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.1, relative=False)
                assert scan_report.call_args.args[0].metadata["queue_group"] == "group_id"


def test_scan_object_receives_scan_def_id(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    bec_client.scans._scan_def_id = "scan_def_id"
    dev = bec_client.device_manager.devices
    with mock.patch.object(bec_client, "alarm_handler"):
        with mock.patch("bec_lib.scan_manager.ScanReport.from_request") as scan_report:
            with mock.patch.object(bec_client, "get_global_var", return_value="test_sample"):
                obj._run(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.1, relative=False)
                assert scan_report.call_args.args[0].metadata["scan_def_id"] == "scan_def_id"


def test_scan_object_receives_dataset_id_on_hold(bec_client):
    scan_info = {
        "class": "FermatSpiralScan",
        "arg_input": {
            "device": "device",
            "start": "float",
            "stop": "float",
        },
        "required_kwargs": ["step", "relative"],
        "arg_bundle_size": 3,
        "scan_report_hint": "table",
        "doc": "\n        A scan following Fermat's spiral.\n\n        Args:\n            *args: pairs of device / start position / end position / steps arguments\n            relative: Start from an absolute or relative position\n            burst: number of acquisition per point\n            optim_trajectory: routine used for the trajectory optimization, e.g. 'corridor'. Default: None\n\n        Returns:\n\n        Examples:\n            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True, optim_trajectory=\"corridor\")\n\n        ",
    }
    scan_name = "fermat_scan"
    obj = ScanObject(scan_name, scan_info, bec_client)
    bec_client.scans._dataset_id_on_hold = "dataset_id_on_hold"
    dev = bec_client.device_manager.devices
    with mock.patch.object(bec_client, "alarm_handler"):
        with mock.patch("bec_lib.scan_manager.ScanReport.from_request") as scan_report:
            with mock.patch.object(bec_client, "get_global_var", return_value="test_sample"):
                obj._run(dev.samx, -5, 5, dev.samy, -5, 5, step=0.5, exp_time=0.1, relative=False)
                assert (
                    scan_report.call_args.args[0].metadata["dataset_id_on_hold"]
                    == "dataset_id_on_hold"
                )
