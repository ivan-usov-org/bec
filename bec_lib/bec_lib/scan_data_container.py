from __future__ import annotations

import copy
import time
from collections import deque
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Dict, Literal, Tuple

import h5py

from bec_lib.logger import bec_logger

logger = bec_logger.logger

if TYPE_CHECKING:
    from bec_lib.scan_items import ScanItem


class DataCache:
    """
    Data cache for repeated file reads, implementing a least-recently-used cache.
    This class is a singleton and stores the estimated memory usage of the
    data cache by reading the HDF5 file and group sizes. The cache is cleared
    when the memory usage exceeds a certain threshold.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(DataCache, cls).__new__(cls)
        return cls._instance

    def __init__(self, max_memory: int = 1e9) -> None:
        self._cache = deque()
        self._memory_usage = 0
        self._max_memory = max_memory

    def add_item(self, key: str, value: Any, memory_usage: int) -> None:
        """
        Add an item to the cache.

        Args:
            key (str): The key to store the item under.
            value (Any): The value to store.
            memory_usage (int): The memory usage of the item.
        """
        self._cache.appendleft((key, value, memory_usage))
        self._memory_usage += memory_usage
        if self._memory_usage > self._max_memory:
            self.run_cleanup()

    def get_item(self, key: str) -> Any:
        """
        Get an item from the cache and move it to the front of the cache.

        Args:
            key (str): The key to get the item from.

        Returns:
            Any: The item.
        """
        for i, (item_key, item_value, _) in enumerate(self._cache):
            if item_key == key:
                self._cache.rotate(-i)
                return copy.deepcopy(item_value)
        return None

    def run_cleanup(self) -> None:
        """
        Run the cache cleanup and remove the least-recently-used items.
        """
        while self._memory_usage > self._max_memory:
            _, _, memory_usage = self._cache.pop()
            self._memory_usage -= memory_usage


_file_cache = DataCache()


class FileReference:
    """
    This class is a wrapper around an HDF5 file reference, adding convenience methods for accessing the
    data in the file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the FileReference object.

        Args:
            file_path (str): The path to the HDF5 file.
        """
        self.file_path = file_path

    def read(self, entry_path: str, cached=True) -> Any:
        """
        Recurisively read the data from the HDF5 file and return it as a dictionary.

        Args:
            entry_path (str): The path to the entry in the HDF5 file, e.g. "entry/collection/devices/samx".
            cached (bool): Whether to use the cache for reading the data.

        Returns:
            dict: The data from the HDF5 file.
        """
        if cached:
            out = _file_cache.get_item(f"{self.file_path}::{entry_path}")
            if out is not None:
                return out
        out = {}
        print(f"Reading {entry_path} from {self.file_path}")
        with h5py.File(self.file_path, "r") as f:
            entry = f[entry_path]
            if isinstance(entry, h5py.Group):
                out, size = self._read_group(entry)
            elif isinstance(entry, h5py.Dataset):
                # TODO: Add here a safeguard for large datasets to avoid loading them into memory all at once
                out = entry[()]
                size = entry.size * entry.dtype.itemsize
            else:
                raise ValueError(f"Entry at {entry_path} is not a group or dataset.")

        _file_cache.add_item(f"{self.file_path}::{entry_path}", out, size)
        return copy.deepcopy(out)

    def _read_group(self, group: h5py.Group) -> Tuple[Dict[str, Any], int]:
        """
        Recursively read the data from a group in the HDF5 file and return it as a dictionary.
        It also returns the memory usage of the group as specified by the HDF5 file.

        Args:
            group (h5py.Group): The group to read the data from.

        Returns:
            Tuple[Dict[str, Any], int]: The data from the group and the memory usage of the group.
        """
        out = {}
        size = 0
        for key, value in group.items():
            if value is None:
                continue
            if isinstance(value, h5py.Group):
                out[key], group_size = self._read_group(value)
                size += group_size
            else:
                out[key] = value[()]
                size += value.size * value.dtype.itemsize
        return out, size

    def get_group_names(self, entry_path: str) -> list:
        """
        Get the names of all groups in the HDF5 file at the given entry path.

        Args:
            entry_path (str): The path to the entry in the HDF5 file, e.g. "entry/collection/devices/samx".

        Returns:
            list: The names of all groups in the HDF5 file.
        """
        with h5py.File(self.file_path, "r") as f:
            entry = f[entry_path]
            if isinstance(entry, h5py.Group):
                return list(entry.keys())
            return []

    def get_hdf5_structure(self) -> dict:
        """
        Get the structure of the HDF5 file.

        Returns:
            dict: The structure of the HDF5 file.
        """
        with h5py.File(self.file_path, "r") as f:
            return self._get_hdf5_structure(f)

    def _get_hdf5_structure(self, group: h5py.Group) -> dict:
        """
        Recursively get the structure of the HDF5 file.

        Args:
            group (h5py.Group): The group to get the structure from.

        Returns:
            dict: The structure of the HDF5 file.
        """
        out = {}
        for key, value in group.items():
            if value is None:
                continue
            if isinstance(value, h5py.Group):
                out[key] = self._get_hdf5_structure(value)
            else:
                out[key] = {"type": "dataset", "shape": value.shape, "dtype": value.dtype}
        return out


class AttributeDict(dict):
    """
    This class is a Pydantic model for the DeviceContainer class.
    """

    def __dir__(self) -> Iterable[str]:
        return list(self.keys())

    def __getattr__(self, name: str) -> Any:
        if name in self:
            return self[name]
        raise AttributeError(f"Attribute '{name}' not found in data or instance attributes.")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        del self[name]


class SignalDataReference:

    def __init__(self, file_path: str, entry_path: str, dict_entry: str | list[str] = None):
        self._file_reference = FileReference(file_path)
        self._entry_path = entry_path
        if dict_entry is None:
            self._dict_entry = None
        else:
            self._dict_entry = dict_entry if isinstance(dict_entry, list) else [dict_entry]

    def read(self) -> dict:
        return self._get_entry()

    def _get_entry(self) -> dict:
        data = self._file_reference.read(self._entry_path)
        if self._dict_entry is not None:
            for entry in self._dict_entry:
                data = data[entry]
        return data

    def __str__(self) -> str:
        return f"{self._file_reference.file_path}::{self._entry_path}::{self._dict_entry}"


class DeviceDataReference(AttributeDict, SignalDataReference):

    def __init__(
        self, content: dict, file_path: str, entry_path: str, dict_entry: str | list[str] = None
    ):
        super().__init__(content)
        SignalDataReference.__init__(self, file_path, entry_path, dict_entry)


class LazyAttributeDict(AttributeDict):
    """
    This class is a lazy attribute dictionary that loads the data using a load function when the data is accessed.
    """

    def __init__(self, load_function: callable = None):
        self._load_function = load_function
        self._loaded = False

    def _load(self) -> None:
        if not super().__getitem__("_loaded"):
            super().__getitem__("_load_function")()
            super().__setitem__("_loaded", True)

    def __dir__(self) -> Iterable[str]:
        object.__getattribute__(self, "_load")()
        return list(self.keys())

    def __getattr__(self, name: str) -> Any:
        object.__getattribute__(self, "_load")()
        return super().__getattr__(name)

    def __getitem__(self, key: Any) -> Any:
        object.__getattribute__(self, "_load")()
        return super().__getitem__(key)


class ScanDataContainer:

    def __init__(self, parent: ScanItem = None, file_path: str = None):
        self.parent = parent
        self._file_reference = None
        self.devices = LazyAttributeDict(self._load_devices)
        self._baseline_devices = None
        self._monitored_devices = None
        self._async_devices = None
        self._loaded = False
        if file_path is not None:
            self.set_file(file_path)

    def set_file(self, file_path: str):
        self._file_reference = FileReference(file_path)

    def _load_devices(self) -> None:
        _start = time.time()

        if self._loaded:
            return

        if self._file_reference is None:
            return

        # self.devices = AttributeDict()
        info = self._file_reference.get_hdf5_structure()
        self._load_device_group("baseline", info)
        self._load_device_group("monitored", info)
        self._load_device_group("async", info, grouped_cache=False)
        self._loaded = True
        logger.debug(f"devices loaded in {time.time() - _start:.2f} s")

    def _load_device_group(
        self,
        group: Literal["baseline", "monitored", "async"],
        info: dict,
        grouped_cache: bool = True,
    ) -> None:
        device_group = (
            info.get("entry", {}).get("collection", {}).get("readout_groups", {}).get(group, {})
        )
        base_path = f"entry/collection/readout_groups/{group}"
        for device_name, device_info in device_group.items():
            entry_path = base_path if grouped_cache else f"{base_path}/{device_name}"
            self.devices[device_name] = DeviceDataReference(
                {
                    signal_name: SignalDataReference(
                        file_path=self._file_reference.file_path,
                        entry_path=entry_path,
                        dict_entry=[device_name, signal_name] if grouped_cache else [signal_name],
                    )
                    for signal_name in device_info
                },
                file_path=self._file_reference.file_path,
                entry_path=entry_path,
                dict_entry=device_name if grouped_cache else None,
            )


if __name__ == "__main__":  # pragma: no cover
    # scan item
    scan_item = ScanDataContainer()
    scan_item.set_file(
        "/Users/wakonig_k/software/work/bec/data/S00000-00999/S00248/S00248_master.h5"
    )
    start = time.time()
    print(dir(scan_item.devices))
    print(time.time() - start)
    print(scan_item.devices.aptrx.aptrx.read())
