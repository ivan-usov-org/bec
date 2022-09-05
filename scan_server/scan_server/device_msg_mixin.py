import time
import uuid
from typing import Callable

import numpy as np
from bec_utils import BECMessage, MessageEndpoints, ProducerConnector, bec_logger

from .errors import LimitError, ScanAbortion

DeviceMsg = BECMessage.DeviceInstructionMessage
logger = bec_logger.logger


class DeviceMsgMixin:
    def __init__(self, producer: ProducerConnector, device_msg_callback: Callable = None) -> None:
        self.producer = producer
        self.device_msg_metadata = device_msg_callback if not None else lambda self: {}

    @staticmethod
    def _exclude_nones(input_dict: dict):
        for key in list(input_dict.keys()):
            if input_dict[key] is None:
                input_dict.pop(key)

    def device_msg(self, **kwargs):
        msg = DeviceMsg(**kwargs)
        msg.metadata = {**self.device_msg_metadata(), **msg.metadata}
        return msg

    def send_rpc_and_wait(self, device, func_name, *args, **kwargs):
        rpc_id = str(uuid.uuid4())
        yield from self._run_rpc(device, func_name, rpc_id, *args, **kwargs)
        return self._get_from_rpc(rpc_id)

    def set_and_wait(self, *, device, positions):
        if not isinstance(positions, list) and not isinstance(positions, np.ndarray):
            positions = [positions]
        if len(positions) == 0:
            return
        for ind, val in enumerate(device):
            yield from self.set(
                device=val, value=positions[ind], group="scan_motor", wait_group="scan_motor"
            )
        yield from self.wait(
            device=device, wait_type="move", group="scan_motor", wait_group="scan_motor"
        )

    def _run_rpc(self, device, func_name, rpc_id, *args, **kwargs):
        yield self.device_msg(
            device=device,
            action="rpc",
            parameter={
                "device": device,
                "func": func_name,
                "rpc_id": rpc_id,
                "args": list(args),
                "kwargs": kwargs,
            },
        )

    def _get_from_rpc(self, rpc_id):
        while True:
            msg = self.producer.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.001)
        msg = BECMessage.DeviceRPCMessage.loads(msg)
        if not msg.content["success"]:
            error = msg.content["out"]
            raise ScanAbortion(
                f"During an RPC, the following error occured:\n{error['error']}: {error['msg']}.\nTraceback: {error['traceback']}\n The scan will be aborted."
            )
        logger.debug(msg.content.get("out"))
        return msg.content.get("return_val")

    def read_and_wait(self, group: str, wait_group: str, device: list = None):
        yield from self.read(device=device, group=group, wait_group=wait_group)
        yield from self.wait(device=device, wait_type="read", group=group, wait_group=wait_group)

    def open_scan(self, *, scan_motors: list, num_pos: int, scan_name: str, scan_type: str):
        yield self.device_msg(
            device=None,
            action="open_scan",
            parameter={
                "primary": scan_motors,
                "num_points": num_pos,
                "scan_name": scan_name,
                "scan_type": scan_type,
            },
        )

    def kickoff(self, *, device):
        yield self.device_msg(
            device=device,
            action="kickoff",
            parameter={},
            metadata={},
        )

    def close_scan(self):
        yield self.device_msg(device=None, action="close_scan", parameter={})

    def stage(self):
        yield self.device_msg(device=None, action="stage", parameter={})

    def unstage(self):
        yield self.device_msg(device=None, action="unstage", parameter={})

    def baseline_reading(self):
        yield self.device_msg(
            device=None,
            action="baseline_reading",
            parameter={},
            metadata={"stream": "baseline"},
        )

    def wait(
        self,
        *,
        wait_type: str,
        device=None,
        group: str = None,
        wait_group: str = None,
        wait_time=None,
    ):
        parameter = {"type": wait_type, "time": wait_time, "group": group, "wait_group": wait_group}
        self._exclude_nones(parameter)
        yield self.device_msg(
            device=device,
            action="wait",
            parameter=parameter,
        )

    def read(
        self, *, group: str, wait_group: str, device: list = None, pointID: int = None, target=None
    ):
        parameter = {"target": target, "group": group, "wait_group": wait_group}
        metadata = {"pointID": pointID}
        self._exclude_nones(parameter)
        self._exclude_nones(metadata)
        yield self.device_msg(
            device=device,
            action="read",
            parameter=parameter,
            metadata=metadata,
        )

    def trigger(self, *, group: str, pointID: int):
        yield self.device_msg(
            device=None,
            action="trigger",
            parameter={"group": group},
            metadata={"pointID": pointID},
        )

    def set(self, *, device: str, value: float, group: str, wait_group: str):
        yield self.device_msg(
            device=device,
            action="set",
            parameter={
                "value": value,
                "group": group,
                "wait_group": wait_group,
            },
        )

    def open_scan_def(self):
        yield self.device_msg(device=None, action="open_scan_def", parameter={})

    def close_scan_def(self):
        yield self.device_msg(device=None, action="close_scan_def", parameter={})

    def close_scan_group(self):
        yield self.device_msg(device=None, action="close_scan_group", parameter={})

    def rpc(self, device: str, parameter: dict):
        yield self.device_msg(
            device=device,
            action="rpc",
            parameter=parameter,
        )
