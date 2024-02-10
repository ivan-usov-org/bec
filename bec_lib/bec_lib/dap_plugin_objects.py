from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING

from typeguard import typechecked

from bec_lib import messages
from bec_lib.device import DeviceBase
from bec_lib.endpoints import MessageEndpoints
from bec_lib.scan_items import ScanItem

if TYPE_CHECKING:
    from bec_lib.client import BECClient


class DAPPluginObjectBase:
    """
    Base class for DAP plugin objects. This class should not be used directly. Instead, use one of the derived classes.
    """

    def __init__(
        self,
        service_name: str,
        plugin_info: dict,
        client: BECClient = None,
        auto_run_supported: bool = False,
        service_info: dict = None,
    ) -> None:
        """
        Args:
            service_name (str): The name of the service.
            plugin_info (dict): Information about the plugin.
            client (BECClient, optional): The BEC client. Defaults to None.
            auto_run_supported (bool, optional): Whether the plugin supports auto run. Defaults to False.
            service_info (dict, optional): Information about the service. Defaults to None.
        """
        self._service_name = service_name
        self._plugin_info = plugin_info
        self._client = client
        self._auto_run_supported = auto_run_supported
        self._plugin_config = {}
        self._service_info = service_info

        # run must be an anonymous function to allow for multiple doc strings
        self._user_run = lambda *args, **kwargs: self._run(*args, **kwargs)

    def _run(self, *args, **kwargs):
        converted_args = []
        for arg in args:
            if isinstance(arg, ScanItem):
                converted_args.append(arg.scanID)
            else:
                converted_args.append(arg)
        args = converted_args
        converted_kwargs = {}
        for key, val in kwargs.items():
            if isinstance(val, ScanItem):
                converted_kwargs[key] = val.scanID
            else:
                converted_kwargs[key] = val
        kwargs = converted_kwargs
        request_id = str(uuid.uuid4())
        self._client.producer.set_and_publish(
            MessageEndpoints.dap_request(),
            messages.DAPRequestMessage(
                dap_cls=self._plugin_info["class"],
                dap_type="on_demand",
                config={
                    "args": args,
                    "kwargs": kwargs,
                    "class_args": self._plugin_info.get("class_args"),
                    "class_kwargs": self._plugin_info.get("class_kwargs"),
                },
                metadata={"RID": request_id},
            ),
        )

        response = self._wait_for_dap_response(request_id)
        return response.content["data"]

    def _wait_for_dap_response(self, request_id: str, timeout: float = 5.0):
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for DAP response.")
            response = self._client.producer.get(MessageEndpoints.dap_response(request_id))
            if not response:
                time.sleep(0.005)
                continue

            if response.metadata["RID"] != request_id:
                time.sleep(0.005)
                continue

            if response.content["success"]:
                return response
            raise RuntimeError(response.content["error"])

    def _update_dap_config(self, request_id: str = None):
        if not self._plugin_config.get("selected_device"):
            return
        self._plugin_config["class_args"] = self._plugin_info.get("class_args")
        self._plugin_config["class_kwargs"] = self._plugin_info.get("class_kwargs")
        self._client.producer.set_and_publish(
            MessageEndpoints.dap_request(),
            messages.DAPRequestMessage(
                dap_cls=self._plugin_info["class"],
                dap_type="continuous",
                config=self._plugin_config,
                metadata={"RID": request_id},
            ),
        )


class DAPPluginObject(DAPPluginObjectBase):
    """
    Default DAP plugin object. This class should be used for plugins that do not support auto run.
    To customize a plugin, create a new class that inherits from this class and override the methods as needed.
    """

    def get_data(self):
        """
        Get the data from last run.
        """
        msg = self._client.producer.get_last(MessageEndpoints.processed_data(self._service_name))
        if not msg:
            return None
        return msg.content["data"]


class DAPPluginObjectAutoRun(DAPPluginObject):
    """
    DAP plugin object that supports auto run. This class should be used for plugins that support auto run.
    To customize a plugin, create a new class that inherits from this class and override the methods as needed.
    """

    @property
    def auto_run(self):
        """
        Set to True to start a continously running worker.
        """
        return self._plugin_config.get("auto_run", False)

    @auto_run.setter
    @typechecked
    def auto_run(self, val: bool):
        self._plugin_config["auto_run"] = val
        request_id = str(uuid.uuid4())
        self._update_dap_config(request_id=request_id)


class LmfitService1D(DAPPluginObjectAutoRun):
    """
    Plugin for fitting 1D data using lmfit.
    """

    def select(self, device: DeviceBase | str, signal: str = None):
        """
        Select the device and signal to use for fitting.

        Args:
            device (DeviceBase | str): The device to use for fitting. Can be either a DeviceBase object or the name of the device.
            signal (str, optional): The signal to use for fitting. If not provided, the first signal in the device's hints will be used.
        """
        bec_device = (
            device
            if isinstance(device, DeviceBase)
            else self._client.device_manager.devices.get(device)
        )
        if not bec_device:
            raise AttributeError(f"Device {device} not found.")
        if signal:
            self._plugin_config["selected_device"] = [bec_device.name, signal]
        else:
            # pylint: disable=protected-access
            hints = bec_device._hints
            if not hints:
                raise AttributeError(
                    f"Device {bec_device.name} has no hints. Cannot select device without signal."
                )
            if len(hints) > 1:
                raise AttributeError(
                    f"Device {bec_device.name} has multiple hints. Please specify a signal."
                )
            self._plugin_config["selected_device"] = [bec_device.name, hints[0]]

        request_id = str(uuid.uuid4())
        self._update_dap_config(request_id=request_id)
