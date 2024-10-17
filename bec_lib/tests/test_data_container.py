from unittest import mock

import h5py
import numpy as np
import pytest

from bec_lib.scan_data_container import FileReference, ScanDataContainer, _file_cache


@pytest.fixture
def mock_file(tmpdir):
    """
    Create a mock hdf5 file.
    """
    file_path = tmpdir / "test.h5"
    readout_groups = {
        "baseline": ["samy", "samz"],
        "monitored": ["samx", "bpm4i"],
        "async": ["waveform"],
    }
    with h5py.File(file_path, "w") as f:
        for group, devices in readout_groups.items():
            readout_group = f.create_group(f"entry/collection/readout_groups/{group}")

            for device in devices:
                dev_group = f.create_group(f"entry/collection/devices/{device}/{device}")
                for signal in ["value", "timestamp"]:
                    dev_group.create_dataset(signal, data=[1, 2, 3])
                # create a link from the readout group to the device
                readout_group[device] = h5py.SoftLink(f"/entry/collection/devices/{device}")

    return file_path


@pytest.fixture
def file_cache():
    _file_cache.clear_cache()
    yield _file_cache
    _file_cache.clear_cache()


def test_file_cache(mock_file, file_cache):
    """
    Test that the file access is cached and repeated access does not trigger a reload.
    """
    reference = FileReference(file_path=mock_file)
    entry_path = "entry/collection/devices/samx/samx/value"
    reference.read(entry_path=entry_path)
    assert file_cache._cache[0][0] == f"{reference.file_path}::{entry_path}"

    with mock.patch.object(file_cache, "add_item") as add_item:
        reference.read(entry_path=entry_path)
        add_item.assert_not_called()


def test_file_read_groups(mock_file):
    """
    Test that the file reference can read groups.
    """
    reference = FileReference(file_path=mock_file)
    groups = reference.get_hdf5_structure()
    assert groups["entry"]["collection"]["devices"]["samx"]["samx"]["value"] == {
        "type": "dataset",
        "shape": (3,),
        "dtype": int,
        "mem_size": 24,
    }


def test_data_container(mock_file):

    container = ScanDataContainer(file_path=mock_file)
    assert "samx" in container.devices.keys()
    assert "samx" in dir(container.devices)

    assert all(container.devices.samx.read()["samx"]["value"] == np.array([1, 2, 3]))
    assert all(container.devices.samx["samx"].read()["timestamp"] == np.array([1, 2, 3]))


def test_data_container_raises_without_file():
    with pytest.raises(RuntimeError):
        container = ScanDataContainer(file_path="does_not_exist.h5")
        container._load_devices(timeout_time=0.3)


def test_data_container_readout_group_access(mock_file):
    container = ScanDataContainer(file_path=mock_file)

    assert all(
        container.readout_groups.baseline_devices.samz.read()["samz"]["value"]
        == np.array([1, 2, 3])
    )
    assert all(
        container.readout_groups.baseline_devices.samz["samz"].read()["timestamp"]
        == np.array([1, 2, 3])
    )
