from unittest import mock

import pytest

from bec_lib.tests.utils import bec_client
from bec_lib.devicemanager_client import Device
from bec_lib.scans import DatasetIdOnHold, HideReport, Metadata, ScanDef, ScanGroup

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


def test_metadata_handler(bec_client):
    client = bec_client
    client.metadata = {"descr": "test", "uid": "12345"}
    with Metadata({"descr": "alignment", "pol": 1}):
        assert client.metadata == {"descr": "alignment", "uid": "12345", "pol": 1}

    assert client.metadata == {"descr": "test", "uid": "12345"}


def test_hide_report_cm(bec_client):
    client = bec_client
    client.scans._hide_report = None
    hrep = HideReport(client.scans)
    with hrep:
        assert client.scans._hide_report is True

    assert client.scans._hide_report is None


def test_dataset_id_on_hold_cm(bec_client):
    client = bec_client
    client.scans._dataset_id_on_hold = None
    dataset_id_on_hold = DatasetIdOnHold(client.scans)
    with mock.patch.object(client, "queue"):
        with dataset_id_on_hold:
            assert client.scans._dataset_id_on_hold is True

    assert client.scans._dataset_id_on_hold is None


def test_dataset_id_on_hold_cm_nested(bec_client):
    client = bec_client
    client.scans._dataset_id_on_hold = None
    dataset_id_on_hold = DatasetIdOnHold(client.scans)
    with mock.patch.object(client, "queue"):
        with dataset_id_on_hold:
            assert client.scans._dataset_id_on_hold is True
            with dataset_id_on_hold:
                assert client.scans._dataset_id_on_hold is True
            assert client.scans._dataset_id_on_hold is True
    assert client.scans._dataset_id_on_hold is None


def test_dataset_id_on_hold_cleanup_on_error(bec_client):
    client = bec_client
    client.scans._dataset_id_on_hold = None
    dataset_id_on_hold = DatasetIdOnHold(client.scans)
    with pytest.raises(AttributeError):
        with mock.patch.object(client, "queue"):
            with dataset_id_on_hold:
                assert client.scans._dataset_id_on_hold is True
                with dataset_id_on_hold:
                    assert client.scans._dataset_id_on_hold is True
                    raise AttributeError()
    assert client.scans._dataset_id_on_hold is None


def test_scan_def_cm(bec_client):
    client = bec_client
    client.scans._scan_def_id = None
    scan_def_id_cm = ScanDef(client.scans)
    with scan_def_id_cm:
        assert isinstance(client.scans._scan_def_id, str)

    assert client.scans._scan_def_id is None


def test_scan_group_cm(bec_client):
    client = bec_client
    client.scans._scan_group = None
    scan_group_cm = ScanGroup(client.scans)
    with scan_group_cm:
        assert isinstance(client.scans._scan_group, str)

    assert client.scans._scan_group is None


def test_parameter_bundler(bec_client):
    client = bec_client
    dev = client.device_manager.devices
    res = client.scans._parameter_bundler((dev.samx, -5, 5, dev.samy, -5, 5), 3)
    assert res == {"samx": [-5, 5], "samy": [-5, 5]}

    res = client.scans._parameter_bundler((dev.samx, -5, 5, 5), 4)
    assert res == {"samx": [-5, 5, 5]}

    res = client.scans._parameter_bundler((-5, 5, 5), 0)
    assert res == (-5, 5, 5)


@pytest.mark.parametrize(
    "in_type,out",
    [
        ("float", (float, int)),
        ("int", int),
        ("list", list),
        ("boolean", bool),
        ("str", str),
        ("dict", dict),
        ("device", Device),
    ],
)
def test_get_arg_type(bec_client, in_type, out):
    client = bec_client
    res = client.scans.get_arg_type(in_type)
    assert res == out


def test_get_arg_type_raises(bec_client):
    client = bec_client
    with pytest.raises(TypeError):
        client.scans.get_arg_type("not_existing")
