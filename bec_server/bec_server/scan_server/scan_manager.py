import inspect

from bec_lib import MessageEndpoints, bec_logger, plugin_helper
from bec_lib.messages import AvailableResourceMessage
from bec_lib.signature_serializer import signature_to_dict

from . import scans as ScanServerScans

logger = bec_logger.logger


class ScanManager:

    def __init__(self, *, parent):
        """
        Scan Manager loads and manages the available scans.
        """
        self.parent = parent
        self.available_scans = {}
        self.scan_dict = {}
        self._plugins = {}
        self.load_plugins()
        self.update_available_scans()
        self.publish_available_scans()

    def load_plugins(self):
        """load scan plugins"""
        plugins = plugin_helper.get_scan_plugins()
        if not plugins:
            return
        for name, cls in plugins.items():
            if not issubclass(cls, ScanServerScans.RequestBase):
                logger.error(
                    f"Plugin {name} is not a valid scan plugin as it does not inherit from RequestBase. Skipping."
                )
                continue
            self._plugins[name] = cls
            logger.info(f"Loading scan plugin {name}")

    def update_available_scans(self):
        """load all scans and plugin scans"""
        members = inspect.getmembers(ScanServerScans)
        for member_name, cls in self._plugins.items():
            members.append((member_name, cls))

        for name, scan_cls in members:
            try:
                is_scan = issubclass(scan_cls, ScanServerScans.RequestBase)
            except TypeError:
                is_scan = False

            if not is_scan or not scan_cls.scan_name:
                logger.debug(f"Ignoring {name}")
                continue
            if scan_cls.scan_name in self.available_scans:
                logger.error(f"{scan_cls.scan_name} already exists. Skipping.")
                continue

            report_classes = [
                ScanServerScans.RequestBase,
                ScanServerScans.ScanBase,
                ScanServerScans.AsyncFlyScanBase,
                ScanServerScans.SyncFlyScanBase,
                ScanServerScans.ScanStubs,
                ScanServerScans.ScanComponent,
            ]

            for report_cls in report_classes:
                if issubclass(scan_cls, report_cls):
                    base_cls = report_cls.__name__
            self.scan_dict[scan_cls.__name__] = scan_cls
            self.available_scans[scan_cls.scan_name] = {
                "class": scan_cls.__name__,
                "base_class": base_cls,
                "arg_input": scan_cls.arg_input,
                "required_kwargs": scan_cls.required_kwargs,
                "arg_bundle_size": scan_cls.arg_bundle_size,
                "scan_report_hint": scan_cls.scan_report_hint,
                "doc": scan_cls.__doc__ or scan_cls.__init__.__doc__,
                "signature": signature_to_dict(scan_cls.__init__),
            }

    def publish_available_scans(self):
        """send all available scans to the broker"""
        self.parent.connector.set(
            MessageEndpoints.available_scans(),
            AvailableResourceMessage(resource=self.available_scans),
        )
