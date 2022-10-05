import os
from unittest import mock

import file_writer
import h5py
import numpy as np
from file_writer import NexusFileWriter, NeXusFileXMLWriter
from file_writer.file_writer import HDF5Storage, cSAXS_NeXus_format

dir_path = os.path.dirname(file_writer.__file__)


def test_nexus_file_xml_writer():
    file_writer = NeXusFileXMLWriter()
    file_writer.configure(
        layout_file=os.path.abspath(os.path.join(dir_path, "../layout_cSAXS_NXsas.xml"))
    )
    with mock.patch.object(
        file_writer, "_create_device_data_storage", return_value={"samx": [0, 1, 2]}
    ):
        file_writer.write("./test.h5", {})


def test_csaxs_nexus_format():
    writer_storage = cSAXS_NeXus_format(HDF5Storage(), {"samx": [0, 1, 2]})
    assert writer_storage._storage["entry"].attrs["definition"] == "NXsas"
    assert writer_storage._storage["entry"]._storage["sample"]._storage["x_translation"]._data == [
        0,
        1,
        2,
    ]


def test_nexus_file_writer():
    file_writer = NexusFileWriter()
    with mock.patch.object(
        file_writer, "_create_device_data_storage", return_value={"samx": [0, 1, 2]}
    ):
        file_writer.write("./test.h5", {})
    with h5py.File("./test.h5", "r") as test_file:
        assert list(test_file) == ["entry"]
        assert list(test_file["entry"]) == ["collection", "control", "instrument", "sample"]
        assert list(test_file["entry"]["sample"]) == ["x_translation"]
        assert test_file["entry"]["sample"].attrs["NX_class"] == "NXsample"
        assert test_file["entry"]["sample"]["x_translation"].attrs["units"] == "mm"
        assert all(np.asarray(test_file["entry"]["sample"]["x_translation"]) == [0, 1, 2])
