import collections
from typing import Any

from _collections_abc import dict_items, dict_keys, dict_values

from bec_lib import messages


class BLSignalData(dict):
    """
    BLSignalData is a container for storing signal data.
    """

    def __init__(self) -> None:
        self.data = {}
        super().__init__()

    def set(self, data: dict) -> None:
        """
        Set the signal data to the given data.

        Args:
            data(dict): the data to set the signal data to
        """
        self.data = data
        for key, value in data.items():
            self.__setattr__(key, value)

    @property
    def val(self):
        """return a list of values of the signal data"""
        return [self.data.get("value")]

    @property
    def timestamps(self):
        """return a list of timestamps of the signal data"""
        return [self.data.get("timestamp")]

    def __getitem__(self, key: Any) -> Any:
        if key in ["val", "value"]:
            return self.val
        if key == "timestamp":
            return self.timestamps
        return self.get(key)

    def get(self, index: Any, default=None) -> dict:
        if index in ["val", "value"]:
            return self.val
        if index == "timestamp":
            return self.timestamps
        return self.get(index, default)

    def __str__(self) -> str:
        return f"{self.data}"

    def __len__(self) -> int:
        return len(self.data)

    def items(self) -> dict_items:
        return self.data.items()

    def keys(self) -> dict_keys:
        return self.data.keys()

    def values(self) -> dict_values:
        return self.data.values()

    def __eq__(self, __value: object) -> bool:
        return self.data == __value


class BLDeviceData(dict):
    """
    BLSignalData is a container for storing device data for a baseline readings.
    """

    def __init__(self):
        self.__signals = collections.defaultdict(BLSignalData)
        super().__init__()

    def set(self, signals: dict) -> None:
        for signal, signal_data in signals.items():
            self.__signals[signal].set(signal_data)
            self.__setattr__(signal, self.__signals[signal])

    def __getitem__(self, key: Any) -> Any:
        return self.get(key)

    def __str__(self) -> str:
        return f"{dict(self.__signals)}"

    def __eq__(self, ref_data: object) -> bool:
        return {name: self.__signals[name].data for name in self.__signals} == ref_data

    def get(self, index: Any, default=None) -> Any:
        return self.__signals.get(index, default)

    def keys(self) -> dict_keys:
        return self.__signals.keys()

    def items(self) -> dict_items:
        return self.__signals.items()

    def values(self) -> dict_values:
        return self.__signals.values()


class BaselineData(dict):
    def __init__(self):
        self.message = []
        self.devices = collections.defaultdict(BLDeviceData)
        super().__init__()

    def set(self, msg: messages.ScanBaselineMessage):
        """
        Set the baseline data to the given message.

        Args:
            msg(messages.ScanBaselineMessage): the message to set the baseline data to
        """
        self.message = [msg]  # let's keep it as a list in case we want to store multiple messages
        for name, dev_data in msg.content["data"].items():
            self.devices[name].set(dev_data)
            self.__setattr__(name, self.devices[name])

    def __getitem__(self, key: Any) -> Any:
        if key in self.devices:
            return self.devices[key]
        return self.get(key)

    def __contains__(self, key: Any) -> bool:
        if key in self.devices:
            return True
        return False

    def get(self, index: Any, default=None) -> Any:
        return self.devices.get(index, default)

    def keys(self) -> dict_keys:
        return self.devices.keys()

    def items(self) -> dict_items:
        return self.devices.items()

    def values(self) -> dict_values:
        return self.devices.values()

    def __str__(self) -> str:
        return f"{dict(self.devices)}"

    def __len__(self) -> int:
        return len(self.message)
