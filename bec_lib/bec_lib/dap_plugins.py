from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING

from bec_lib import messages
from bec_lib.device import DeviceBase
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.scan_items import ScanItem
from bec_lib.signature_serializer import dict_to_signature

logger = bec_logger.logger

if TYPE_CHECKING:
    from bec_lib.client import BECClient


class DAPPluginObject:
    def __init__(
        self,
        service_name: str,
        plugin_info: dict,
        client: BECClient = None,
        auto_fit_supported: bool = False,
        service_info: dict = None,
    ) -> None:
        self._service_name = service_name
        self._plugin_info = plugin_info
        self._client = client
        self._auto_fit_supported = auto_fit_supported
        self._plugin_config = {}
        self._service_info = service_info

        # run must be an anonymous function to allow for multiple doc strings
        self.fit = lambda *args, **kwargs: self._fit(*args, **kwargs)

    def _fit(self, *args, **kwargs):
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
            ).dumps(),
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

            response = messages.DAPResponseMessage.loads(response)
            if not response:
                time.sleep(0.005)
                continue
            if response.metadata["RID"] != request_id:
                time.sleep(0.005)
                continue

            if response.content["success"]:
                return response
            raise RuntimeError(response.content["error"])

    @property
    def auto_fit(self):
        """
        Set to True to automatically fit the model to the data.
        """
        return self._plugin_config.get("auto_fit", False)

    @auto_fit.setter
    def auto_fit(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("auto_fit must be a boolean.")
        self._plugin_config["auto_fit"] = val
        request_id = str(uuid.uuid4())
        self._update_dap_config(request_id=request_id)

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

    def get_data(self):
        """
        Get the data from last fit.
        """
        msg = self._client.producer.get_last(MessageEndpoints.processed_data(self._service_name))
        if not msg:
            return None
        msg = messages.ProcessedDataMessage.loads(msg)
        return msg.content["data"]

    def get_params(self):
        """
        Get the currently set fit parameters.
        """
        pass

    def set_params(self, params: dict):
        """
        Set the fit parameters.
        """
        pass

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
            ).dumps(),
        )


class DAPPlugins:
    def __init__(self, parent):
        self._parent = parent
        self._available_dap_plugins = {}
        self._import_dap_plugins()
        self._selected_model = None
        self._auto_fit = False
        self._selected_device = None

    def refresh(self):
        self._import_dap_plugins()

    def _import_dap_plugins(self):
        available_services = self._parent.service_status
        if not available_services:
            # not sure how we got here...
            return
        dap_services = [
            service for service in available_services if service.startswith("DAPServer/")
        ]
        for service in dap_services:
            msg_raw = self._parent.producer.get(MessageEndpoints.dap_available_plugins(service))
            if msg_raw is None:
                logger.warning("No plugins available. Are redis and the BEC server running?")
                return
            available_plugins = messages.AvailableResourceMessage.loads(msg_raw)
            if not available_plugins:
                return
            for plugin_name, plugin_info in available_plugins.content["resource"].items():
                try:
                    if plugin_name in self._available_dap_plugins:
                        continue
                    name = plugin_info["user_friendly_name"]
                    auto_fit_supported = plugin_info.get("auto_fit_supported", False)
                    self._available_dap_plugins[name] = DAPPluginObject(
                        name,
                        plugin_info,
                        client=self._parent,
                        auto_fit_supported=auto_fit_supported,
                        service_info=available_services[service].content,
                    )
                    self._set_plugin(
                        name,
                        plugin_info.get("class_doc"),
                        plugin_info.get("fit_doc"),
                        plugin_info.get("signature"),
                    )
                except Exception as e:
                    logger.error(f"Error importing plugin {plugin_name}: {e}")

    def _set_plugin(
        self, plugin_name: str, class_doc_string: str, fit_doc_string: str, signature: dict
    ):
        setattr(self, plugin_name, self._available_dap_plugins[plugin_name])
        setattr(getattr(self, plugin_name), "__doc__", class_doc_string)
        setattr(getattr(self, plugin_name).fit, "__doc__", fit_doc_string)
        setattr(getattr(self, plugin_name).fit, "__signature__", dict_to_signature(signature))
