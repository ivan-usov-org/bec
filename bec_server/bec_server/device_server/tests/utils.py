import enum
import time
from typing import Protocol

from ophyd import DeviceStatus, Kind
from ophyd_devices.interfaces.protocols.bec_protocols import (
    BECDeviceProtocol,
    BECPositionerProtocol,
    BECSignalProtocol,
)

from bec_lib.devicemanager import DeviceContainer
from bec_lib.tests.utils import ConnectorMock

# pylint: disable=missing-function-docstring
# pylint: disable=protected-access

POSITIONER_SIGNALS = {
    "readback": {"kind": "normal", "value": 0, "precision": 3},
    "setpoint": {"kind": "normal", "value": 0, "precision": 3},
    "velocity": {"kind": "config", "value": 0, "precision": 3},
    "acceleration": {"kind": "config", "value": 0, "precision": 3},
}


class DeviceMockType(enum.Enum):
    POSITIONER = "positioner"
    SIGNAL = "signal"


class DeviceObjectMock(BECDeviceProtocol, Protocol):
    def __init__(self, name: str, kind=Kind.normal, dev_type=None, parent=None):
        self._name = name
        self._kind = kind if isinstance(kind, Kind) else getattr(Kind, kind)
        self._parent = parent
        self._read_only = False
        self._enabled = True
        self._dev_type = dev_type
        self._signals_container = None
        self._connected = True
        self._destroyed = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, val):
        self._kind = val

    @property
    def parent(self):
        return self._parent

    @property
    def hints(self):
        if self._dev_type == DeviceMockType.POSITIONER:
            return {"fields": [self.name]}
        else:
            return {"fields": []}

    @property
    def root(self):
        return self if self.parent is None else self.parent

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        self._connected = val

    def destroy(self):
        self._connected = False
        self._destroyed = True
        if self._signals_container is None:
            return
        for signal in self._signals_container.values():
            signal["signal"].destroy()

    def trigger(self) -> None:
        # status = DeviceStatus(self)
        # status.set_finished()
        # return status
        pass


class MockSignal(DeviceObjectMock, BECSignalProtocol):

    def __init__(
        self, name: str, value: any = 0, kind: Kind = Kind.normal, parent=None, precision=None
    ):
        super().__init__(name, dev_type=DeviceMockType.SIGNAL, parent=parent, kind=kind)
        self._value = value
        self._config = {"deviceConfig": {"limits": [0, 0]}, "userParameter": None}
        self._metadata = dict(read_access=True, write_access=True, precision=precision)

    def read(self):
        return {self.name: {"value": self._value, "timestamp": time.time()}}

    def read_configuration(self):
        return self.read()

    def get(self):
        return self._value

    def put(self, value: any, force: bool = False, timeout: float = None):
        self._value = value

    def set(self, value: any, timeout: float = None):
        self._value = value

    @property
    def metadata(self):
        return self._metadata.copy()

    @property
    def write_access(self):
        return self._metadata["write_access"]

    @property
    def read_access(self):
        return self._metadata["read_access"]

    @property
    def hints(self):
        if (~Kind.normal & Kind.hinted) & self.kind:
            return {"fields": [self.name]}
        else:
            return {"fields": []}

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, val):
        self._limits = val

    @property
    def low_limit(self):
        return self.limits[0]

    @property
    def high_limit(self):
        return self.limits[1]

    @property
    def precision(self):
        return self._metadata["precision"]

    def check_value(self, value):
        limits = self.limits
        if limits[0] == limits[1]:
            return
        if not limits[0] <= value <= limits[1]:
            raise ValueError(f"Value {value} is outside limits {limits}")


class PositionerMock(DeviceObjectMock, BECPositionerProtocol):

    def __init__(self, name: str, kind: Kind = Kind.normal, parent=None):
        super().__init__(name, dev_type=DeviceMockType.POSITIONER, parent=parent, kind=kind)
        if getattr(self, "readback", None):
            self.readback.name = self.name
        self._signals_container = POSITIONER_SIGNALS
        self._config = {"deviceConfig": {"limits": [-50, 50]}, "userParameter": None}
        self._create_attrs()
        if hasattr(self, "readback"):
            self.readback.name = self.name

    def _create_attrs(self):
        for name, options in self._signals_container.items():
            setattr(
                self,
                name,
                MockSignal(
                    name=f"{self.name}_{name}",
                    kind=options["kind"],
                    value=options["value"],
                    parent=self,
                    precision=options["precision"],
                ),
            )
            self._signals_container[name].update({"signal": getattr(self, name)})

    def read(self):
        ret = {}
        for name, signal_info in self._signals_container.items():
            if (
                signal_info["signal"].kind == Kind.normal
                or signal_info["signal"].kind == Kind.hinted
            ):
                ret.update(signal_info["signal"].read())
        return ret

    def read_configuration(self):
        ret = {}
        for signal_info in self._signals_container.values():
            if signal_info["signal"].kind == Kind.config:
                ret.update(signal_info["signal"].read())
        return ret

    def describe_configuration(self) -> dict:
        ret = {}
        for name, signal_info in self._signals_container.items():
            if signal_info["signal"].kind == Kind.config:
                ret.update(
                    {
                        name: {
                            "source": signal_info["signal"].__class__.__name__,
                            "dtype": type(signal_info["signal"]._value),
                            "shape": [],
                        }
                    }
                )
        return ret

    def describe(self) -> dict:
        ret = {}
        for name, signal_info in self._signals_container.items():
            if (
                signal_info["signal"].kind == Kind.normal
                or signal_info["signal"].kind == Kind.hinted
            ):
                ret.update(
                    {
                        name: {
                            "source": signal_info["signal"].__class__.__name__,
                            "dtype": type(signal_info["signal"]._value),
                            "shape": [],
                            "precision": signal_info["signal"].precision,
                        }
                    }
                )
        return ret

    @property
    def precision(self):
        if getattr(self, "readback", None):
            return self.readback.precision
        raise AttributeError(f"PositionerMock {self.name} does not have readback signal")

    @property
    def limits(self):
        return self._config["deviceConfig"]["limits"]

    @limits.setter
    def limits(self, val: tuple):
        self._config["deviceConfig"]["limits"] = val

    @property
    def low_limit(self):
        return self.limits[0]

    @property
    def high_limit(self):
        return self.limits[1]

    def check_value(self, value):
        limits = self.limits
        if limits[0] == limits[1]:
            return
        if not limits[0] <= value <= limits[1]:
            raise ValueError(f"Value {value} is outside limits {limits}")

    def move(self, position: float, **kwargs) -> None:
        self.check_value(position)

        if getattr(self, "setpoint", None) and getattr(self, "readback", None):
            self.setpoint.put(position)
            self.readback.put(position)
        else:
            raise AttributeError(
                f"PositionerMock {self.name} does not have setpoint or readback signals from signals: {self._signals_container}"
            )

    def set(self, position: float, **kwargs):
        self.move(position)


class DMMock:
    devices = DeviceContainer()
    connector = ConnectorMock()

    def add_device(self, name, value=None, dev_type: DeviceMockType = DeviceMockType.POSITIONER):
        if dev_type == DeviceMockType.POSITIONER:
            self.devices[name] = PositionerMock(name=name)
        elif dev_type == DeviceMockType.SIGNAL:
            self.devices[name] = MockSignal(name=name)
        else:
            raise ValueError(f"Unknown device type {dev_type}")
        if value is not None:
            self.devices[name].readback.put(value)
