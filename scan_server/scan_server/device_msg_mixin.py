import time
import uuid
from typing import Callable, List, Union

import numpy as np
from bec_utils import BECMessage, MessageEndpoints, ProducerConnector, bec_logger

from .errors import DeviceMessageError, ScanAbortion

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

    def _device_msg(self, **kwargs):
        """"""
        msg = DeviceMsg(**kwargs)
        msg.metadata = {**self.device_msg_metadata(), **msg.metadata}
        return msg

    def send_rpc_and_wait(self, device: str, func_name: str, *args, **kwargs):
        """Perform an RPC (remote procedure call) on a device and wait for its return value.

        Args:
            device (str): Name of the device
            func_name (str): Function name. The function name will be appended to the device.
            args (tuple): Arguments to pass on to the RPC function
            kwargs (dict): Keyword arguments to pass on to the RPC function

        Raises:
            ScanAbortion: Raised if the RPC's success is False

        Returns:
            any: Return value of the executed rpc function

        Examples:
            >>> send_rpc_and_wait("samx", "controller.my_custom_function")

        """
        rpc_id = str(uuid.uuid4())
        parameter = {
            "device": device,
            "func": func_name,
            "rpc_id": rpc_id,
            "args": list(args),
            "kwargs": kwargs,
        }
        yield from self.rpc(device=device, parameter=parameter)
        return self._get_from_rpc(rpc_id)

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

    def set_and_wait(self, *, device: List[str], positions: Union[list, np.ndarray]):
        """Set devices to a specific position and wait completion.

        Args:
            device (List[str]): List of device names.
            positions (Union[list, np.ndarray]): Target position.

        """
        if not isinstance(positions, list) and not isinstance(positions, np.ndarray):
            positions = [positions]
        if len(positions) == 0:
            return
        for ind, val in enumerate(device):
            yield from self.set(device=val, value=positions[ind], wait_group="scan_motor")
        yield from self.wait(device=device, wait_type="move", wait_group="scan_motor")

    def read_and_wait(
        self, *, wait_group: str, device: list = None, group: str = None, pointID: int = None
    ):
        """Trigger a reading and wait for completion.

        Args:
            wait_group (str): wait group
            device (list, optional): List of device names. Can be specified instead of group. Defaults to None.
            group (str, optional): Group name of devices. Can be specified instead of device. Defaults to None.
            pointID (int, optional): _description_. Defaults to None.

        """
        self._check_device_and_groups(device, group)
        yield from self.read(device=device, group=group, wait_group=wait_group, pointID=pointID)
        yield from self.wait(device=device, wait_type="read", group=group, wait_group=wait_group)

    def open_scan(self, *, scan_motors: list, num_pos: int, scan_name: str, scan_type: str):
        """Open a new scan.

        Args:
            scan_motors (list): List of scan motors.
            num_pos (int): Number of positions within the scope of this scan.
            scan_name (str): Scan name.
            scan_type (str): Scan type (e.g. 'step' or 'fly')

        """
        yield self._device_msg(
            device=None,
            action="open_scan",
            parameter={
                "primary": scan_motors,
                "num_points": num_pos,
                "scan_name": scan_name,
                "scan_type": scan_type,
            },
        )

    def kickoff(self, *, device: str, parameter: dict = None):
        """Kickoff a fly scan device.

        Args:
            device (str): Device name of flyer.
            parameter (dict, optional): Additional parameters that should be forwarded to the device. Defaults to {}.
        """
        parameter = parameter if not None else {}
        yield self._device_msg(
            device=device,
            action="kickoff",
            parameter=parameter,
            metadata={},
        )

    def close_scan(self):
        """Close the scan."""
        yield self._device_msg(device=None, action="close_scan", parameter={})

    def stage(self):
        """Stage all devices"""
        yield self._device_msg(device=None, action="stage", parameter={})

    def unstage(self):
        """Unstage all devices"""
        yield self._device_msg(device=None, action="unstage", parameter={})

    def baseline_reading(self):
        """Run the baseline readings."""
        yield self._device_msg(
            device=None,
            action="baseline_reading",
            parameter={},
            metadata={"stream": "baseline"},
        )

    def wait(
        self,
        *,
        wait_type: str,
        device: Union[List[str], str] = None,
        group: str = None,
        wait_group: str = None,
        wait_time: float = None,
    ):
        """Wait for an event.

        Args:
            wait_type (str): wait type
            device (Union[List[str], str], optional): List of device names. Defaults to None.
            group (str, optional): Device group that can be used instead of the device argument. Defaults to None.
            wait_group (str, optional): Wait group. Defaults to None.
            wait_time (float, optional): Wait time (for wait_type="trigger"). Defaults to None.

        """
        self._check_device_and_groups(device, group)
        parameter = {"type": wait_type, "time": wait_time, "group": group, "wait_group": wait_group}
        self._exclude_nones(parameter)
        yield self._device_msg(
            device=device,
            action="wait",
            parameter=parameter,
        )

    def read(
        self,
        *,
        wait_group: str,
        device: list = None,
        pointID: int = None,
        group: str = None,
    ):
        """_summary_

        Args:
            wait_group (str): Wait group.
            device (list, optional): Device name. Can be used instead of group. Defaults to None.
            pointID (int, optional): pointID to assign this reading to point within the scan. Defaults to None.
            group (str, optional): Device group. Can be used instead of device. Defaults to None.

        """
        self._check_device_and_groups(device, group)
        parameter = {"group": group, "wait_group": wait_group}
        metadata = {"pointID": pointID}
        self._exclude_nones(parameter)
        self._exclude_nones(metadata)
        yield self._device_msg(
            device=device,
            action="read",
            parameter=parameter,
            metadata=metadata,
        )

    def trigger(self, *, group: str, pointID: int):
        """Trigger a device group

        Args:
            group (str): Device group that should receive the trigger.
            pointID (int): pointID that should be attached to this trigger event.

        """
        yield self._device_msg(
            device=None,
            action="trigger",
            parameter={"group": group},
            metadata={"pointID": pointID},
        )

    def set(self, *, device: str, value: float, wait_group: str):
        """Set the device to a specific value.

        Args:
            device (str): Device name
            value (float): Target value.
            wait_group (str): wait group for this event.

        """
        yield self._device_msg(
            device=device,
            action="set",
            parameter={
                "value": value,
                "wait_group": wait_group,
            },
        )

    def open_scan_def(self):
        """open a new scan definition"""
        yield self._device_msg(device=None, action="open_scan_def", parameter={})

    def close_scan_def(self):
        """close a scan definition"""
        yield self._device_msg(device=None, action="close_scan_def", parameter={})

    def close_scan_group(self):
        """close a scan group"""
        yield self._device_msg(device=None, action="close_scan_group", parameter={})

    def rpc(self, *, device: str, parameter: dict):
        """Perfrom an RPC (remote procedure call) on a device.

        Args:
            device (str): Device name.
            parameter (dict): parameters used for this rpc instructions.

        """
        yield self._device_msg(
            device=device,
            action="rpc",
            parameter=parameter,
        )

    def _check_device_and_groups(self, device, group):
        if device and group:
            raise DeviceMessageError("Device and device group was specified. Pick one.")
        if not device and not group:
            raise DeviceMessageError("Either devices or device groups have to be specified.")
