"""
The DeviceConnector class is responsible for establishing connections to devices and constructing device objects. It
is used by the Device Server but can also be used by other modules, e.g. to validate device configurations.
"""

from __future__ import annotations

import inspect
import traceback
from typing import TYPE_CHECKING

from bec_lib import bec_logger, plugin_helper

logger = bec_logger.logger

if TYPE_CHECKING:
    from bec_server.device_server.devices.devicemanager import DeviceManagerDS

try:
    import ophyd
    import ophyd_devices as opd
    from ophyd import OphydObject
    from ophyd.signal import EpicsSignalBase
except ImportError:
    ophyd = None
    opd = None
    OphydObject = None
    EpicsSignalBase = None


class DeviceConnector:
    """Class to establish connections to devices and construct device objects"""

    @staticmethod
    def connect_device(obj, wait_for_all=False):
        """establish a connection to a device"""
        try:
            if obj.connected:
                return
            if hasattr(obj, "controller"):
                obj.controller.on()
                return
            if hasattr(obj, "wait_for_connection"):
                try:
                    obj.wait_for_connection(all_signals=wait_for_all, timeout=10)
                except TypeError:
                    obj.wait_for_connection(timeout=10)
                return
            logger.error(
                f"Device {obj.name} does not implement the socket controller interface nor"
                " wait_for_connection and cannot be turned on."
            )
            raise ConnectionError(f"Failed to establish a connection to device {obj.name}")
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"{error_traceback}. Failed to connect to {obj.name}.")
            raise ConnectionError(f"Failed to establish a connection to device {obj.name}") from e

    @staticmethod
    def disconnect_device(obj):
        """disconnect from a device"""
        if not obj.connected:
            return
        if hasattr(obj, "controller"):
            obj.controller.off()
            return
        obj.destroy()

    @staticmethod
    def construct_device_obj(
        dev: dict, device_manager: DeviceManagerDS
    ) -> tuple[OphydObject, dict]:
        """
        Construct a device object from a device config dictionary.

        Args:
            dev (dict): device config dictionary
            device_manager (DeviceManagerDS): device manager instance

        Returns:
            (OphydObject, dict): device object and updated config dictionary
        """
        name = dev.get("name")
        dev_cls = DeviceConnector._get_device_class(dev["deviceClass"])
        device_config = dev.get("deviceConfig")
        device_config = device_config if device_config is not None else {}
        config = device_config.copy()
        config["name"] = name

        # pylint: disable=protected-access
        device_classes = [dev_cls]
        if issubclass(dev_cls, ophyd.Signal):
            device_classes.append(ophyd.Signal)
        if issubclass(dev_cls, EpicsSignalBase):
            device_classes.append(EpicsSignalBase)
        if issubclass(dev_cls, ophyd.OphydObject):
            device_classes.append(ophyd.OphydObject)

        # get all init parameters of the device class and its parents
        class_params = set()
        for device_class in device_classes:
            class_params.update(inspect.signature(device_class)._parameters)
        class_params_and_config_keys = class_params & config.keys()

        init_kwargs = {key: config.pop(key) for key in class_params_and_config_keys}
        device_access = config.pop("device_access", None)
        if device_access or (device_access is None and config.get("device_mapping")):
            init_kwargs["device_manager"] = device_manager

        signature = inspect.signature(dev_cls)
        if "device_manager" in signature.parameters:
            init_kwargs["device_manager"] = device_manager

        # initialize the device object
        obj = dev_cls(**init_kwargs)
        return obj, config

    @staticmethod
    def _get_device_class(dev_type: str) -> type:
        """Get the device class from the device type"""
        return plugin_helper.get_plugin_class(dev_type, [opd, ophyd])
