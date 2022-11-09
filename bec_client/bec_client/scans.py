from __future__ import annotations

import asyncio
import uuid
from contextlib import ContextDecorator
from typing import TYPE_CHECKING

import msgpack
from bec_utils import BECMessage, MessageEndpoints, bec_logger
from bec_utils.connector import ConsumerConnector
from cytoolz import partition

from .devicemanager_client import Device
from .scan_manager import ScanReport

if TYPE_CHECKING:
    from bec_client import BECClient

logger = bec_logger.logger


class ScanObject:
    def __init__(self, scan_name: str, scan_info: dict, parent: BECClient = None) -> None:
        self.scan_name = scan_name
        self.scan_info = scan_info
        self.parent = parent

        # run must be an anonymous function to allow for multiple doc strings
        self.run = lambda *args, **kwargs: self._run(*args, **kwargs)

    def _run(self, *args, **kwargs):
        scans = self.parent.scans

        # handle reserved kwargs:
        hide_report_kwarg = kwargs.get("hide_report", False)
        hide_report = hide_report_kwarg or scans._hide_report

        if scans._scan_group:
            if "md" not in kwargs:
                kwargs["md"] = {}
            kwargs["md"]["queue_group"] = scans._scan_group
        if scans._scan_def_id:
            if "md" not in kwargs:
                kwargs["md"] = {}
            kwargs["md"]["scan_def_id"] = scans._scan_def_id

        request = Scans.prepare_scan_request(self.scan_name, self.scan_info, *args, **kwargs)
        requestID = str(uuid.uuid4())  # TODO: move this to the API server
        request.metadata["RID"] = requestID

        self._send_scan_request(request)
        scan_report_type = self._get_scan_report_type(hide_report)
        self.parent.callback_manager.process_request(request, scan_report_type)

        return ScanReport.from_request(request, client=self.parent)

    def _get_scan_report_type(self, hide_report) -> str:
        if hide_report:
            return None
        return self.scan_info.get("scan_report_hint")

    def _start_consumer(self, request: BECMessage.ScanQueueMessage) -> ConsumerConnector:
        consumer = self.parent.device_manager.connector.consumer(
            [
                MessageEndpoints.device_readback(dev)
                for dev in request.content["parameter"]["args"].keys()
            ],
            threaded=False,
            cb=(lambda msg: msg),
        )
        return consumer

    def _send_scan_request(self, request: BECMessage.ScanQueueMessage) -> None:
        self.parent.device_manager.producer.send(
            MessageEndpoints.scan_queue_request(), request.dumps()
        )


class Scans:
    def __init__(self, parent):
        self.parent = parent
        self._available_scans = {}
        self._import_scans()
        self._scan_group = None
        self._scan_def_id = None
        self._scan_group_ctx = ScanGroup(parent=self)
        self._scan_def_ctx = ScanDef(parent=self)
        self._hide_report = None
        self._hide_report_ctx = HideReport(parent=self)

    def _import_scans(self):

        available_scans = msgpack.loads(
            self.parent.producer.get(MessageEndpoints.available_scans())
        )
        for scan_name, scan_info in available_scans.items():
            self._available_scans[scan_name] = ScanObject(scan_name, scan_info, parent=self.parent)
            setattr(
                self,
                scan_name,
                self._available_scans[scan_name].run,
            )
            setattr(getattr(self, scan_name), "__doc__", scan_info.get("doc"))

    @staticmethod
    def get_arg_type(in_type: str):
        """translate type string into python type"""
        # pylint: disable=too-many-return-statements
        if in_type == "float":
            return (float, int)
        if in_type == "int":
            return int
        if in_type == "list":
            return list
        if in_type == "boolean":
            return bool
        if in_type == "str":
            return str
        if in_type == "dict":
            return dict
        if in_type == "device":
            return Device
        raise TypeError(f"Unknown type {in_type}")

    @staticmethod
    def prepare_scan_request(
        scan_name: str, scan_info: dict, *args, **kwargs
    ) -> BECMessage.ScanQueueMessage:
        """Prepare scan request message with given scan arguments

        Args:
            scan_name (str): scan name (matching a scan name on the scan server)
            scan_info (dict): dictionary describing the scan (e.g. doc string, required kwargs etc.)

        Raises:
            TypeError: Raised if not all required keyword arguments have been specified.
            TypeError: Raised if the number of args do fit into the required bundling pattern.
            TypeError: Raised if an argument is not of the required type as specified in scan_info.

        Returns:
            BECMessage.ScanQueueMessage: _description_
        """
        arg_input = scan_info.get("arg_input", [])
        arg_bundle_size = scan_info.get("arg_bundle_size")
        if len(arg_input) > 0:
            if len(args) % len(arg_input) != 0:
                raise TypeError(
                    f"{scan_info.get('doc')}\n {scan_name} takes multiples of {len(arg_input)} arguments ({len(args)} given).",
                )
            if not all(req_kwarg in kwargs for req_kwarg in scan_info.get("required_kwargs")):
                raise TypeError(
                    f"{scan_info.get('doc')}\n Not all required keyword arguments have been specified. The required arguments are: {scan_info.get('required_kwargs')}"
                )
            for ii, arg in enumerate(args):
                if not isinstance(arg, Scans.get_arg_type(arg_input[ii % len(arg_input)])):
                    raise TypeError(
                        f"{scan_info.get('doc')}\n Argument {ii} must be of type {arg_input[ii%len(arg_input)]}, not {type(arg).__name__}."
                    )
        else:
            logger.warning("Could not check arguments against scan input types.")
        metadata = {}
        if "md" in kwargs:
            metadata = kwargs.pop("md")
        params = {
            "args": Scans._parameter_bundler(args, arg_bundle_size),
            "kwargs": kwargs,
        }
        return BECMessage.ScanQueueMessage(
            scan_type=scan_name, parameter=params, queue="primary", metadata=metadata
        )

    @staticmethod
    def _parameter_bundler(args, bundle_size):
        """

        Args:
            args:
            bundle_size: number of parameters per bundle

        Returns:

        """
        if not bundle_size:
            return args
        params = {}
        for cmds in partition(bundle_size, args):
            cmds_serialized = [cmd.name if hasattr(cmd, "name") else cmd for cmd in cmds]
            params[cmds_serialized[0]] = cmds_serialized[1:]
        return params

    @property
    def scan_group(self):
        """Context manager / decorator for defining scan groups"""
        return self._scan_group_ctx

    @property
    def scan_def(self):
        """Context manager / decorator for defining new scans"""
        return self._scan_def_ctx

    @property
    def hide_report(self):
        """Context manager / decorator for hiding the report"""
        return self._hide_report_ctx


class ScanGroup(ContextDecorator):
    def __init__(self, parent: Scans = None) -> None:
        super().__init__()
        self.parent = parent

    def __enter__(self):
        group_id = str(uuid.uuid4())
        self.parent._scan_group = group_id
        return self

    def __exit__(self, *exc):
        self.parent.close_scan_group()
        self.parent._scan_group = None


class ScanDef(ContextDecorator):
    def __init__(self, parent: Scans = None) -> None:
        super().__init__()
        self.parent = parent

    def __enter__(self):
        scan_def_id = str(uuid.uuid4())
        self.parent._scan_def_id = scan_def_id
        self.parent.open_scan_def()
        return self

    def __exit__(self, *exc):
        self.parent.close_scan_def()
        self.parent._scan_def_id = None


class HideReport(ContextDecorator):
    def __init__(self, parent: Scans = None) -> None:
        super().__init__()
        self.parent = parent

    def __enter__(self):
        if self.parent._hide_report is None:
            self.parent._hide_report = True
        return self

    def __exit__(self, *exc):
        self.parent._hide_report = None
