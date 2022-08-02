import enum
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from io import StringIO
from typing import Any

import bec_utils.BECMessage as BECMessage
import msgpack
import ophyd
from bec_utils import Alarms, BECService, MessageEndpoints, bec_logger
from bec_utils.connector import ConnectorBase
from ophyd.utils import errors as ophyd_errors

from device_server.devices import is_serializable
from device_server.devices.devicemanager import DeviceManagerDS

logger = bec_logger.logger

consumer_stop = threading.Event()


def rgetattr(obj, attr, *args):
    """See https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects"""

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split("."))


class DSStatus(enum.Enum):
    RUNNING = 1
    IDLE = 0
    ERROR = -1


class DeviceServer(BECService):
    """DeviceServer using ophyd as a service
    This class is intended to provide a thin wrapper around ophyd and the devicemanager. It acts as the entry point for other services
    """

    def __init__(self, bootstrap_server, connector_cls: ConnectorBase, scibec_url: str) -> None:
        super().__init__(bootstrap_server, connector_cls)
        self._status = DSStatus.IDLE
        self._tasks = []
        self.device_manager = DeviceManagerDS(self.connector, scibec_url)
        self.device_manager.initialize(bootstrap_server)
        self.threads = []
        self.sig_thread = None
        self.sig_thread = self.connector.consumer(
            MessageEndpoints.scan_queue_modification(),
            cb=self.consumer_interception_callback,
            parent=self,
        )
        self.sig_thread.start()
        self.executor = ThreadPoolExecutor(max_workers=4)

    def start(self) -> None:
        """start the device server"""
        if consumer_stop.is_set():
            consumer_stop.clear()

        self.threads = [
            self.connector.consumer(
                MessageEndpoints.device_instructions(),
                event=consumer_stop,
                cb=self.instructions_callback,
                parent=self,
            ),
        ]
        for t in self.threads:
            t.start()
        self._status = DSStatus.RUNNING

    def stop(self) -> None:
        """stop the device server"""
        consumer_stop.set()
        for t in self.threads:
            t.join()
        self._status = DSStatus.IDLE

    def shutdown(self) -> None:
        """shutdown the device server"""
        self.stop()
        self.sig_thread.signal_event.set()
        self.sig_thread.join()
        self.device_manager.shutdown()

    def _update_device_metadata(self, instr) -> None:
        dev_list = instr.content["device"]
        devices = []
        devices.extend([dev_list] if not isinstance(dev_list, list) else dev_list)
        for dev in devices:
            self.device_manager.devices.get(dev).metadata = instr.metadata

    @staticmethod
    def consumer_interception_callback(msg, *, parent, **kwargs) -> None:
        """callback for receiving scan modifications / interceptions"""
        mvalue = BECMessage.ScanQueueModificationMessage.loads(msg.value)
        logger.info(f"Receiving: {mvalue.content}")
        if mvalue.content.get("action") in ["pause", "abort"]:
            parent.stop_devices()

    def stop_devices(self) -> None:
        """stop all enabled devices"""
        logger.info("Stopping devices after receiving 'abort' request.")
        for dev in self.device_manager.devices.enabled_devices:
            dev.obj.stop()

    def handle_device_instructions(self, msg) -> None:

        instructions = BECMessage.DeviceInstructionMessage.loads(msg.value)
        if instructions.content["device"] is not None:
            # pylint: disable=protected-access
            self._update_device_metadata(instructions)
        action = instructions.content["action"]
        try:
            if action == "set":
                # pylint: disable=protected-access
                self._set_device(instructions)
            elif action == "read":
                # pylint: disable=protected-access
                self._read_device(instructions)
            elif action == "rpc":
                # pylint: disable=protected-access
                self._run_rpc(instructions)
            elif action == "kickoff":
                # pylint: disable=protected-access
                self._kickoff_device(instructions)
            elif action == "trigger":
                # pylint: disable=protected-access
                self._trigger_device(instructions)
        except ophyd_errors.LimitError as limit_error:
            content = limit_error.args[0] if len(limit_error.args) > 0 else ""
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=instructions.content,
                content=content,
                alarm_type=limit_error.__class__.__name__,
                metadata=instructions.metadata,
            )
        except Exception as exc:
            self.connector.log_error({"source": msg.value, "message": exc.args})
            content = exc.args[0] if len(exc.args) > 0 else ""
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=instructions.content,
                content=content,
                alarm_type=exc.__class__.__name__,
                metadata=instructions.metadata,
            )

    @staticmethod
    def instructions_callback(msg, *, parent, **kwargs) -> None:
        """callback for handling device instructions"""
        parent.executor.submit(parent.handle_device_instructions, msg)

    def _get_result_from_rpc(self, rpc_var: Any, instr_params: dict) -> Any:

        if callable(rpc_var):
            args = tuple(instr_params.get("args", ()))
            kwargs = instr_params.get("kwargs", {})
            if len(args) > 0 and len(args[0]) > 0 and len(kwargs) > 0:
                res = rpc_var(*args[0], **kwargs)
            elif len(args) > 0 and len(args[0]) > 0:
                res = rpc_var(*args[0])
            elif len(kwargs) > 0:
                res = rpc_var(**kwargs)
            else:
                res = rpc_var()
        else:
            res = rpc_var
        if not is_serializable(res):
            if isinstance(res, ophyd.StatusBase):
                res = {
                    "success": res.success,
                    "timeout": res.timeout,
                    "done": res.done,
                    "settle_time": res.settle_time,
                }
            else:
                res = None
                self.connector.raise_alarm(
                    severity=Alarms.WARNING,
                    source=instr_params,
                    content=f"Return value of rpc call {instr_params} is not serializable.",
                    metadata={},
                )
        return res

    def _run_rpc(self, instr: BECMessage.DeviceInstructionMessage) -> None:
        save_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        try:
            instr_params = instr.content.get("parameter")
            rpc_var = rgetattr(
                self.device_manager.devices[instr.content["device"]].obj,
                instr_params.get("func"),
            )
            res = self._get_result_from_rpc(rpc_var, instr_params)

            # send result to client
            self.producer.set(
                MessageEndpoints.device_rpc(instr_params.get("rpc_id")),
                BECMessage.DeviceRPCMessage(
                    device=instr.content["device"],
                    return_val=res,
                    out=result.getvalue(),
                    success=True,
                ).dumps(),
            )
            logger.trace(res)
        except KeyboardInterrupt as kbi:
            sys.stdout = save_stdout
            raise KeyboardInterrupt from kbi

        except Exception as exc:
            # pylint: disable=broad-except
            # send error to client
            self.producer.set(
                MessageEndpoints.device_rpc(instr_params.get("rpc_id")),
                BECMessage.DeviceRPCMessage(
                    device=instr.content["device"],
                    return_val=None,
                    out={
                        "error": exc.__class__.__name__,
                        "msg": exc.args,
                        "traceback": traceback.format_exc(),
                    },
                    success=False,
                ).dumps(),
            )
        finally:
            sys.stdout = save_stdout
        # self.producer.set(MessageEndpoints.device_rpc(), msgpack.dumps(res))

    def _trigger_device(self, instr: BECMessage.DeviceInstructionMessage) -> None:
        logger.debug(f"Kickoff device: {instr}")
        obj = self.device_manager.devices.get(instr.content["device"]).obj
        obj.trigger(metadata=instr.metadata, **instr.content["parameter"])

    def _kickoff_device(self, instr: BECMessage.DeviceInstructionMessage) -> None:
        logger.debug(f"Kickoff device: {instr}")
        obj = self.device_manager.devices.get(instr.content["device"]).obj
        obj.kickoff(metadata=instr.metadata, **instr.content["parameter"])

    def _set_device(self, instr: BECMessage.DeviceInstructionMessage) -> None:
        logger.debug(f"Setting device: {instr}")
        val = instr.content["parameter"]["value"]
        obj = self.device_manager.devices.get(instr.content["device"]).obj
        # self.device_manager.add_req_done_sub(obj)
        status = obj.set(val)
        status.add_callback(self._status_callback)

    def _status_callback(self, status):
        pipe = self.producer.pipeline()
        dev_msg = BECMessage.DeviceReqStatusMessage(
            device=status.device.name,
            success=status.success,
            metadata=self.device_manager.devices.get(status.device.name).metadata,
        ).dumps()
        logger.debug(f"req status for device {status.device.name}: {status.success}")
        self.producer.set_and_publish(
            MessageEndpoints.device_req_status(status.device.name), dev_msg, pipe
        )
        pipe.execute()

    def _read_device(self, instr: BECMessage.DeviceInstructionMessage) -> None:
        # check performance -- we might have to change it to a background thread
        dev_list = instr.content["device"]
        devices = []
        devices.extend([dev_list] if not isinstance(dev_list, list) else dev_list)
        start = time.time()
        pipe = self.producer.pipeline()
        for dev in devices:
            self.device_manager.devices.get(dev).metadata = instr.metadata
            obj = self.device_manager.devices.get(dev).obj
            signals = obj.read()
            metadata = self.device_manager.devices.get(dev).metadata
            self.producer.set_and_publish(
                MessageEndpoints.device_read(dev),
                BECMessage.DeviceMessage(signals=signals, metadata=metadata).dumps(),
                pipe,
            )
            self.producer.set(
                MessageEndpoints.device_status(dev),
                BECMessage.DeviceStatusMessage(device=dev, status=0, metadata=metadata).dumps(),
                pipe,
            )
        pipe.execute()
        logger.debug(
            f"Elapsed time for reading and updating status info: {(time.time()-start)*1000} ms"
        )

    @property
    def status(self) -> DSStatus:
        """get the current status of the device server"""
        return self._status

    @status.setter
    def status(self, val: DSStatus) -> None:
        if DSStatus(val) == DSStatus.RUNNING:
            if self.status != DSStatus.RUNNING:
                self.start()
                self._status = DSStatus.RUNNING
        elif DSStatus(val) == DSStatus.IDLE:
            if self.status != DSStatus.IDLE:
                self.stop()
                self._status = DSStatus.IDLE
