import enum
import logging
import sys
import threading
import time
from functools import reduce
from io import StringIO

import bec_utils.BECMessage as BMessage
import msgpack
import ophyd
from bec_utils import Alarms, MessageEndpoints
from bec_utils.connector import ConnectorBase
from ophyd.utils import errors as ophyd_errors

from opaas.devices import is_serializable
from opaas.devices.devicemanageropaas import DeviceManagerOPAAS

logger = logging.getLogger(__name__)
consumer_stop = threading.Event()


def rgetattr(obj, attr, *args):
    """See https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects"""

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split("."))


class OPAASStatus(enum.Enum):
    RUNNING = 1
    IDLE = 0
    ERROR = -1


class OPAAS:
    """OPAAS - ophyd as a service
    This class is intended to provide a thin wrapper around ophyd and the devicemanager. It acts as the entry point for other services
    """

    def __init__(self, bootstrap, Connector: ConnectorBase, scibec_url: str) -> None:
        self._status = OPAASStatus.IDLE
        self._tasks = []
        self.connector = Connector(bootstrap)
        self.device_manager = DeviceManagerOPAAS(self.connector, scibec_url)
        self.device_manager.initialize(bootstrap)
        self.threads = []
        self.sig_thread = None
        self.sig_thread = self.connector.consumer(
            MessageEndpoints.scan_queue_modification(),
            cb=self.consumer_interception_callback,
            parent=self,
        )
        self.sig_thread.start()
        self.producer = self.connector.producer()

    def start(self) -> None:
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
        self._status = OPAASStatus.RUNNING

    def stop(self) -> None:
        consumer_stop.set()
        for t in self.threads:
            t.join()
        self._status = OPAASStatus.IDLE

    def shutdown(self) -> None:
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
        mvalue = BMessage.ScanQueueModificationMessage.loads(msg.value)
        logger.info("Receiving: %s", mvalue.content)
        if mvalue.content.get("action") == "deferred_pause":
            pass
        elif mvalue.content.get("action") == "pause":
            parent.stop_devices()
        # sig = int(msg.value)

    def stop_devices(self) -> None:
        logger.info("Stopping devices after receiving 'abort' request.")
        for dev in self.device_manager.devices.enabled_devices:
            dev.obj.stop()

    @staticmethod
    def instructions_callback(msg, *, parent, **kwargs) -> None:
        instructions = BMessage.DeviceInstructionMessage.loads(msg.value)
        if instructions.content["device"] is not None:
            # pylint: disable=protected-access
            parent._update_device_metadata(instructions)
        action = instructions.content["action"]
        try:
            if action == "set":
                # pylint: disable=protected-access
                parent._set_device(instructions)
            elif action == "read":
                # pylint: disable=protected-access
                parent._read_device(instructions)
            elif action == "rpc":
                # pylint: disable=protected-access
                parent._run_rpc(instructions)
        except ophyd_errors.LimitError as limit_error:
            content = limit_error.args[0] if len(limit_error.args) > 0 else ""
            parent.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=instructions.content,
                content=content,
                alarm_type=limit_error.__class__.__name__,
                metadata=instructions.metadata,
            )
        except Exception as exc:
            parent.connector.log_error({"source": msg.value, "message": exc.args})
            content = exc.args[0] if len(exc.args) > 0 else ""
            parent.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=instructions.content,
                content=content,
                alarm_type=exc.__class__.__name__,
                metadata=instructions.metadata,
            )

    def _run_rpc(self, instr) -> None:
        save_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        try:
            instr_params = instr.content.get("parameter")
            rpc_var = rgetattr(
                self.device_manager.devices[instr.content["device"]].obj,
                instr_params.get("func"),
            )
            if callable(rpc_var):
                args = tuple(instr_params.get("args", ()))
                kwargs = instr_params.get("kwargs", {})
                res = rpc_var(*args, **kwargs)
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
                    self.connector.raise_alarm(
                        severity=Alarms.WARNING,
                        source=instr,
                        content=f"Return value of rpc call {instr_params} is not serializable.",
                    )

            # send result to client
            self.producer.set(
                MessageEndpoints.device_rpc(instr_params.get("rpc_id")),
                BMessage.DeviceRPCMessage(
                    device=instr.content["device"],
                    return_val=res,
                    out=result.getvalue(),
                    success=True,
                ).dumps(),
            )
            print(res)
        except KeyboardInterrupt as kbi:
            sys.stdout = save_stdout
            raise KeyboardInterrupt from kbi
        except Exception as exc:
            # send error to client
            self.producer.set(
                MessageEndpoints.device_rpc(instr_params.get("rpc_id")),
                BMessage.DeviceRPCMessage(
                    device=instr.content["device"],
                    return_val=None,
                    out={"error": exc.__class__.__name__, "msg": exc.args},
                    success=False,
                ).dumps(),
            )
        finally:
            sys.stdout = save_stdout
        # self.producer.set(MessageEndpoints.device_rpc(), msgpack.dumps(res))

    def _set_device(self, instr) -> None:
        val = instr.content["parameter"]["value"]
        obj = self.device_manager.devices.get(instr.content["device"]).obj
        # self.device_manager.add_req_done_sub(obj)
        st = obj.set(val)
        st.add_callback(self._status_callback)

    def _status_callback(self, status):
        pipe = self.producer.pipeline()
        dev_msg = BMessage.DeviceReqStatusMessage(
            device=status.device.name,
            success=status.success,
            metadata=self.device_manager.devices.get(status.device.name).metadata,
        ).dumps()
        self.producer.set_and_publish(
            MessageEndpoints.device_req_status(status.device.name), dev_msg, pipe
        )
        pipe.execute()

    def _read_device(self, instr) -> None:
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
                BMessage.DeviceMessage(signals=signals, metadata=metadata).dumps(),
                pipe,
            )
            status_info = metadata
            status_info["status"] = 0
            status_info["timestamp"] = time.time()
            self.producer.set(MessageEndpoints.device_status(dev), msgpack.dumps(status_info), pipe)
        pipe.execute()
        logger.debug(
            f"Elapsed time for reading and updating status info: {(time.time()-start)*1000} ms"
        )

    @property
    def status(self) -> OPAASStatus:
        return self._status

    @status.setter
    def status(self, val) -> None:
        if OPAASStatus(val) == OPAASStatus.RUNNING:
            if self.status != OPAASStatus.RUNNING:
                self.start()
                self._status = OPAASStatus.RUNNING
        elif OPAASStatus(val) == OPAASStatus.IDLE:
            if self.status != OPAASStatus.IDLE:
                self.stop()
                self._status = OPAASStatus.IDLE
