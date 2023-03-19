import os
from unittest import mock

import h5py
import numpy as np
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
    assert len(device_storage["samx"]) == 2


def test_write_data_storage():
    file_manager = load_FileWriter()
    file_writer = NexusFileWriter(file_manager)
    storage = ScanStorage("2", "scanID-string")
    storage.num_points = 2
    storage.scan_segments = {
        0: {
            "samx": {"samx": {"value": 0.11}, "samx_setpoint": {"value": 0.1}},
            "samy": {"samy": {"value": 1.1}},
        },
        1: {
            "samx": {"samx": {"value": 0.21}, "samx_setpoint": {"value": 0.2}},
            "samy": {"samy": {"value": 1.2}},
        },
    }
    storage.baseline = {}
    file_writer.write("./test.h5", storage)
