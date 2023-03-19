import os
from unittest import mock

import h5py
import numpy as np
import pytest
from test_file_writer_manager import load_FileWriter

import file_writer
from file_writer import NexusFileWriter, NeXusFileXMLWriter
from file_writer.file_writer import HDF5Storage
from file_writer.file_writer_manager import ScanStorage
from file_writer_plugins.cSAXS import NeXus_format as cSAXS_Nexus_format

dir_path = os.path.dirname(file_writer.__file__)


def test_nexus_file_xml_writer():
    file_manager = load_FileWriter()
    file_writer = NeXusFileXMLWriter(file_manager)
    file_writer.configure(
        layout_file=os.path.abspath(os.path.join(dir_path, "../layout_cSAXS_NXsas.xml"))
    )
    with mock.patch.object(
        file_writer, "_create_device_data_storage", return_value={"samx": [0, 1, 2]}
    ):
        file_writer.write("./test.h5", {})


def test_csaxs_nexus_format():
    file_manager = load_FileWriter()
    writer_storage = cSAXS_Nexus_format(
        HDF5Storage(), {"samx": [0, 1, 2]}, file_manager.device_manager
    )
    assert writer_storage._storage["entry"].attrs["definition"] == "NXsas"
    assert writer_storage._storage["entry"]._storage["sample"]._storage["x_translation"]._data == [
        0,
        1,
        2,
    ]


def test_nexus_file_writer():
    file_manager = load_FileWriter()
    file_writer = NexusFileWriter(file_manager)
    with mock.patch.object(
        file_writer, "_create_device_data_storage", return_value={"samx": [0, 1, 2]}
    ):
        file_writer.write("./test.h5", ScanStorage("2", "scanID-string"))
    with h5py.File("./test.h5", "r") as test_file:
        assert list(test_file) == ["entry"]
        assert list(test_file["entry"]) == ["collection", "control", "instrument", "sample"]
        assert list(test_file["entry"]["sample"]) == ["x_translation"]
        assert test_file["entry"]["sample"].attrs["NX_class"] == "NXsample"
        assert test_file["entry"]["sample"]["x_translation"].attrs["units"] == "mm"
        assert all(np.asarray(test_file["entry"]["sample"]["x_translation"]) == [0, 1, 2])


def test_create_device_data_storage():
    file_manager = load_FileWriter()
    file_writer = NexusFileWriter(file_manager)
    storage = ScanStorage("2", "scanID-string")
    storage.num_points = 2
    storage.scan_segments = {
        0: {"samx": {"samx": {"value": 0.1}}, "samy": {"samy": {"value": 1.1}}},
        1: {"samx": {"samx": {"value": 0.2}}, "samy": {"samy": {"value": 1.2}}},
    }
    storage.baseline = {}
    device_storage = file_writer._create_device_data_storage(storage)
    assert len(device_storage.keys()) == 2
    assert len(device_storage["samx"]) == 2
    assert device_storage["samx"][0]["samx"]["value"] == 0.1
    assert device_storage["samx"][1]["samx"]["value"] == 0.2


@pytest.mark.parametrize(
    "segments,baseline,metadata",
    [
        (
            {
                0: {
                    "samx": {"samx": {"value": 0.11}, "samx_setpoint": {"value": 0.1}},
                    "samy": {"samy": {"value": 1.1}},
                },
                1: {
                    "samx": {"samx": {"value": 0.21}, "samx_setpoint": {"value": 0.2}},
                    "samy": {"samy": {"value": 1.2}},
                },
            },
            {
                "eyefoc": {
                    "eyefoc": {"value": 0, "timestamp": 1679226971.564248},
                    "eyefoc_setpoint": {"value": 0, "timestamp": 1679226971.564235},
                    "eyefoc_motor_is_moving": {"value": 0, "timestamp": 1679226971.564249},
                },
                "field": {
                    "field_x": {"value": 0, "timestamp": 1679226971.579148},
                    "field_x_setpoint": {"value": 0, "timestamp": 1679226971.579145},
                    "field_x_motor_is_moving": {"value": 0, "timestamp": 1679226971.579148},
                    "field_y": {"value": 0, "timestamp": 1679226971.5799649},
                    "field_y_setpoint": {"value": 0, "timestamp": 1679226971.579962},
                    "field_y_motor_is_moving": {"value": 0, "timestamp": 1679226971.579966},
                    "field_z_zsub": {"value": 0, "timestamp": 1679226971.58087},
                    "field_z_zsub_setpoint": {"value": 0, "timestamp": 1679226971.580867},
                    "field_z_zsub_motor_is_moving": {"value": 0, "timestamp": 1679226971.58087},
                },
            },
            {
                "RID": "5ee455b8-d0ef-452d-b54a-e7cea5cea19e",
                "scanID": "a9fb36e4-3f38-486c-8434-c8eca19472ba",
                "queueID": "14463a5b-1c65-4888-8f87-4808c90a241f",
                "primary": ["samx"],
                "num_points": 2,
                "positions": [[-100], [100]],
                "scan_name": "monitor_scan",
                "scan_type": "fly",
                "scan_number": 88,
                "dataset_number": 88,
                "exp_time": 0.1,
                "scan_report_hint": "table",
                "scan_report_devices": ["samx"],
                "scan_msgs": [
                    "ScanQueueMessage(({'scan_type': 'monitor_scan', 'parameter': {'args': {'samx': [-100, 100]}, 'kwargs': {'relative': False}}, 'queue': 'primary'}, {'RID': '5ee455b8-d0ef-452d-b54a-e7cea5cea19e'})))"
                ],
            },
        )
    ],
)
def test_write_data_storage(segments, baseline, metadata):
    file_manager = load_FileWriter()
    file_writer = NexusFileWriter(file_manager)
    storage = ScanStorage("2", "scanID-string")
    storage.num_points = 2
    storage.scan_segments = segments
    storage.baseline = baseline
    storage.metadata = metadata
    file_writer.write("./test.h5", storage)
