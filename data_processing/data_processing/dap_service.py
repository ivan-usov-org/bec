from __future__ import annotations

import abc
import inspect
import threading
import time
from typing import TYPE_CHECKING

import lmfit
import numpy as np

# import numpy as np
from bec_lib import DeviceBase, MessageEndpoints, bec_logger, messages

if TYPE_CHECKING:
    from bec_lib import BECClient
    from bec_lib.scan_items import ScanItem


logger = bec_logger.logger


class DAPError(Exception):
    pass


class DAPServiceBase(abc.ABC):
    """
    Base class for data processing services.
    """

    AUTO_FIT_SUPPORTED = False

    def __init__(self, *args, bec_client: BECClient, **kwargs) -> None:
        super().__init__()
        self.client = bec_client
        self.scans = None
        self.scan_id = None
        self.current_scan_item = None

    def _update_scan_id_and_item(self, status: dict):
        """
        Update the scan ID and the current scan item with the provided scan status.

        Args:
            status (dict): Scan status
        """
        scan_id = status.get("scanID")
        if scan_id != self.scan_id:
            self.current_scan_item = self.client.queue.scan_storage.find_scan_by_ID(scan_id)
        self.scan_id = scan_id

    def _process_scan_status_update(self, status: dict, metadata: dict):
        """
        Process a scan status update. This method is called by the service manager and
        should not be overridden or invoked directly.

        Args:
            status (dict): Scan status
            metadata (dict): Scan metadata
        """
        self._update_scan_id_and_item(status)
        self.on_scan_status_update(status, metadata)

    def on_scan_status_update(self, status: dict, metadata: dict):
        """
        Override this method to process a continuous dap request.
        The underlying service manager will call this method when a
        scan status update is received.

        Args:
            status (dict): Scan status
            metadata (dict): Scan metadata

        Example:
            >>> def on_scan_status_update(self, status: dict, metadata: dict):
            >>>     if status.get("status") == "closed":
            >>>         self.process()
        """

    def configure(self, *args, **kwargs):
        """
        Configure the service using the provided parameters by the user.
        The process request's config dictionary will be passed to this method.
        """

    def process(self):
        """
        Process the data and return the result. Ensure that the return value
        is a tuple of (stream_output, metadata) and that it is serializable.
        """


class LmfitService1D(DAPServiceBase):
    """
    Lmfit service for 1D data.
    """

    AUTO_FIT_SUPPORTED = True

    def __init__(self, model: str, *args, continuous: bool = False, **kwargs):
        """
        Initialize the lmfit service. This is a multiplexer service that provides
        access to multiple lmfit models.

        Args:
            model (str): Model name
            continuous (bool, optional): Continuous processing. Defaults to False.
        """
        super().__init__(*args, **kwargs)
        self.scan_id = None
        self.device_x = None
        self.signal_x = None
        self.device_y = None
        self.signal_y = None
        self.parameters = None
        self.current_scan_item = None
        self.finished_id = None
        self.model = getattr(lmfit.models, model)()
        self.finish_event = None
        self.data = None
        self.continuous = continuous

    @staticmethod
    def available_models():
        models = []
        for name, model_cls in inspect.getmembers(lmfit.models):
            try:
                is_model = issubclass(model_cls, lmfit.model.Model)
            except TypeError:
                is_model = False
            if is_model and name not in [
                "Gaussian2dModel",
                "ExpressionModel",
                "Model",
                "SplineModel",
            ]:
                models.append(model_cls)
        return models

    @staticmethod
    def get_model(model: str) -> lmfit.Model:
        """Get the model from the config and convert it to an lmfit model."""

        if isinstance(model, str):
            model = getattr(lmfit.models, model, None)
        if not model:
            raise ValueError(f"Unknown model {model}")

        return model

    def on_scan_status_update(self, status: dict, metadata: dict):
        """
        Process a scan segment.

        Args:
            data (dict): Scan segment data
            metadata (dict): Scan segment metadata
        """
        if self.finish_event is None:
            self.finish_event = threading.Event()
            threading.Thread(target=self.process_until_finished, args=(self.finish_event,)).start()

        if status.get("status") != "open":
            time.sleep(0.2)
            self.finish_event.set()
            self.finish_event = None

    def process_until_finished(self, event: threading.Event):
        """
        Process until the scan is finished.
        """
        while not event.is_set():
            data = self.get_data_from_current_scan(scan_item=self.current_scan_item)
            if not data:
                time.sleep(0.1)
                continue
            self.data = data
            out = self.process()
            if out:
                stream_output, metadata = out
                self.client.producer.xadd(
                    MessageEndpoints.processed_data(self.model.__class__.__name__),
                    msg={
                        "data": messages.ProcessedDataMessage(
                            data=stream_output, metadata=metadata
                        ).dumps()
                    },
                )
            time.sleep(0.1)

    def configure(
        self,
        *args,
        scan_item: ScanItem | str = None,
        device_x: DeviceBase | str = None,
        signal_x: DeviceBase | str = None,
        device_y: DeviceBase | str = None,
        signal_y: DeviceBase | str = None,
        parameters: dict = None,
        **kwargs,
    ):
        """


        Args:
            scan_item (ScanItem): Scan item or scan ID
            device_x (DeviceBase | str): Device name for x
            signal_x (DeviceBase | str): Signal name for x
            device_y (DeviceBase | str): Device name for y
            signal_y (DeviceBase | str): Signal name for y
            parameters (dict): Fit parameters
        """
        # we only receive scan IDs from the client. However, users may
        # pass in a scan item in the CLI which is converted to a scan ID
        # within BEC lib.

        selected_device = kwargs.get("selected_device")
        if selected_device:
            device_y, signal_y = selected_device

        scan_id = scan_item
        if scan_id != self.scan_id or not self.current_scan_item:
            scan_item = self.client.queue.scan_storage.find_scan_by_ID(scan_id)
        else:
            scan_item = self.current_scan_item

        if device_x:
            self.device_x = device_x
        if signal_x:
            self.signal_x = signal_x
        if device_y:
            self.device_y = device_y
        if signal_y:
            self.signal_y = signal_y
        if parameters:
            self.parameters = parameters

        if not self.continuous:
            if not scan_item:
                logger.warning("Failed to access scan item")
                return
            if not self.device_x or not self.signal_x or not self.device_y or not self.signal_y:
                raise DAPError("Device and signal names are required")
            self.data = self.get_data_from_current_scan(scan_item=scan_item)

    def get_data_from_current_scan(self, scan_item: ScanItem, devices: dict = None) -> dict | None:
        """
        Get the data from the current scan.

        Args:
            scan_item (ScanItem): Scan item
            devices (dict): Device names for x and y axes. If not provided, the default values will be used.

        Returns:
            dict: Data for the x and y axes
        """
        if not scan_item:
            logger.warning("Failed to access scan item")
            return None
        if not devices:
            devices = {}
        device_x = devices.get("device_x", self.device_x)
        signal_x = devices.get("signal_x", self.signal_x)
        device_y = devices.get("device_y", self.device_y)
        signal_y = devices.get("signal_y", self.signal_y)

        if not device_x:
            if not scan_item.data:
                return None
            scan_report_devices = scan_item.data[0].metadata.get("scan_report_devices", [])
            if not scan_report_devices:
                logger.warning("Failed to find scan report devices")
                return None
            device_x = scan_report_devices[0]
            bec_device_x = self.client.device_manager.devices.get(device_x)
            if not bec_device_x:
                logger.warning(f"Failed to find device {device_x}")
                return None
            hints = bec_device_x._hints
            if not hints:
                logger.warning(f"Failed to find hints for device {device_x}")
                return None
            if len(hints) > 1:
                logger.warning(f"Multiple hints found for device {device_x}")
                return None
            signal_x = hints[0]

        # get the event data
        if not scan_item.data:
            return None
        x = scan_item.data.get(device_x).get(signal_x).get("value")
        if not x:
            logger.warning(f"Failed to find signal {device_x}.{signal_x}")
            return None
        y = scan_item.data.get(device_y).get(signal_y).get("value")
        if not y:
            logger.warning(f"Failed to find signal {device_y}.{signal_y}")
            return None

        # check if the data is long enough to fit
        if len(x) < 3 or len(y) < 3:
            return None
        return {"x": x, "y": y}

    def process(self) -> tuple[dict, dict]:
        """
        Process data and return the result.
        """
        # get the data
        if not self.data:
            return None

        x = self.data["x"]
        y = self.data["y"]

        # fit the data
        # if self.parameters:
        result = self.model.fit(y, x=x)

        # add the fit result to the output
        stream_output = {"x": np.asarray(x), "y": result.best_fit}

        # add the fit parameters to the metadata
        metadata = {}
        metadata["fit_parameters"] = result.best_values
        metadata["fit_summary"] = result.summary()
        logger.info(f"fit summary: {metadata['fit_summary']}")

        return (stream_output, metadata)
