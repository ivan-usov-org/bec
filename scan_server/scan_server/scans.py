import enum
import threading
import time
import uuid
from abc import ABC, abstractmethod

import numpy as np
from bec_utils import BECMessage, DeviceManagerBase, MessageEndpoints, bec_logger
from cytoolz import partition

from .errors import LimitError

DeviceMsg = BECMessage.DeviceInstructionMessage
ScanMsg = BECMessage.ScanQueueMessage

logger = bec_logger.logger


class ScanArgType(str, enum.Enum):
    DEVICE = "device"
    FLOAT = "float"
    INT = "int"
    BOOL = "boolean"
    STR = "str"
    LIST = "list"
    DICT = "dict"


def get_2D_raster_pos(axis, snaked=True):
    """get_2D_raster_post calculates and returns the positions for a 2D

    snaked==True:
        ->->->->-
        -<-<-<-<-
        ->->->->-
    snaked==False:
        ->->->->-
        ->->->->-
        ->->->->-

    Args:
        axis (list): list of positions for each axis
        snaked (bool, optional): If true, the positions will be calculcated for a snake scan. Defaults to True.

    Returns:
        array: calculated positions
    """

    x_grid, y_grid = np.meshgrid(axis[0], axis[1])
    if snaked:
        y_grid.T[::2] = np.fliplr(y_grid.T[::2])
    x_flat = x_grid.T.ravel()
    y_flat = y_grid.T.ravel()
    positions = np.vstack((x_flat, y_flat)).T
    return positions


# pylint: disable=too-many-arguments
def get_fermat_spiral_pos(
    m1_start, m1_stop, m2_start, m2_stop, step=1, spiral_type=0, center=False
):
    """[summary]

    Args:
        m1_start (float): start position motor 1
        m1_stop (float): end position motor 1
        m2_start (float): start position motor 2
        m2_stop (float): end position motor 2
        step (float, optional): Step size. Defaults to 1.
        spiral_type (float, optional): Angular offset in radians that determines the shape of the spiral.
        A spiral with spiral_type=2 is the same as spiral_type=0. Defaults to 0.
        center (bool, optional): Add a center point. Defaults to False.

    Raises:
        TypeError: [description]
        TypeError: [description]
        TypeError: [description]

    Returns:
        [type]: [description]

    Yields:
        [type]: [description]
    """
    positions = []
    phi = 2 * np.pi * ((1 + np.sqrt(5)) / 2.0) + spiral_type * np.pi

    start = int(not center)

    length_axis1 = abs(m1_stop - m1_start)
    length_axis2 = abs(m2_stop - m2_start)
    n_max = length_axis1 * length_axis2 * 2

    for ii in range(start, n_max):
        radius = step * 0.57 * np.sqrt(ii)
        if abs(radius * np.sin(ii * phi)) > length_axis1 / 2:
            continue
        if abs(radius * np.cos(ii * phi)) > length_axis2 / 2:
            continue
        positions.extend([(radius * np.sin(ii * phi), radius * np.cos(ii * phi))])
    return np.array(positions)


def get_round_roi_scan_positions(lx: float, ly: float, dr: float, nth: int, cenx=0, ceny=0):
    positions = []
    nr = 1 + int(np.floor(max([lx, ly]) / dr))
    for ir in range(1, nr + 2):
        rr = ir * dr
        dth = 2 * np.pi / (nth * ir)
        pos = [
            (rr * np.cos(ith * dth) + cenx, rr * np.sin(ith * dth) + ceny)
            for ith in range(nth * ir)
            if np.abs(rr * np.cos(ith * dth)) < lx / 2 and np.abs(rr * np.sin(ith * dth)) < ly / 2
        ]
        positions.extend(pos)
    return np.array(positions)


def get_round_scan_positions(r_in: float, r_out: float, nr: int, nth: int, cenx=0, ceny=0):
    """_summary_

    Args:
        r_in (float): inner radius
        r_out (float): outer radius
        nr (int): number of radii
        nth (int): number of angles in the inner ring
        cenx (int, optional): center in x. Defaults to 0.
        ceny (int, optional): center in y. Defaults to 0.

    Returns:
        _type_: _description_

    """
    positions = []
    dr = (r_in - r_out) / nr
    for ir in range(1, nr + 2):
        rr = r_in + ir * dr
        dth = 2 * np.pi / (nth * ir)
        positions.extend(
            [
                (rr * np.sin(ith * dth) + cenx, rr * np.cos(ith * dth) + ceny)
                for ith in range(nth * ir)
            ]
        )
    return np.array(positions)


class RequestBase(ABC):
    scan_name = ""
    scan_report_hint = None
    arg_input = [ScanArgType.DEVICE]
    arg_bundle_size = len(arg_input)
    required_kwargs = []

    def __init__(
        self,
        *args,
        device_manager: DeviceManagerBase = None,
        parameter=None,
        metadata=None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.parameter = parameter
        self.caller_args = parameter.get("args", {})
        self.caller_kwargs = parameter.get("kwargs", {})
        self.metadata = metadata
        self.device_manager = device_manager
        self.DIID = 0
        self.scan_motors = []
        self.positions = []
        self._get_scan_motors()
        if metadata is None:
            self.metadata = {}

    def device_msg(self, **kwargs):
        default_metadata = {"stream": "primary", "DIID": self.DIID}
        msg = DeviceMsg(**kwargs)
        msg.metadata = {**default_metadata, **self.metadata, **msg.metadata}
        self.DIID += 1
        return msg

    def initialize(self):
        pass

    def device_rpc(self, device, func_name, *args, **kwargs):
        rpc_id = str(uuid.uuid4())
        yield from self._run_rpc(device, func_name, rpc_id, *args, **kwargs)
        return self._get_from_rpc(rpc_id)

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
        # time.sleep(0.1)  # otherwise appeared to read wrong message
        while True:
            msg = self.device_manager.producer.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.001)
        msg = BECMessage.DeviceRPCMessage.loads(msg)
        logger.debug(msg.content.get("out"))
        return msg.content.get("return_val")

    def _check_limits(self):
        logger.debug("check limits")
        for ii, dev in enumerate(self.scan_motors):
            low_limit, high_limit = (
                self.device_manager.devices[dev].config["deviceConfig"].get("limits", [0, 0])
            )
            if low_limit >= high_limit:
                return
            for pos in self.positions:
                pos_axis = pos[ii]
                if not low_limit <= pos_axis <= high_limit:
                    raise LimitError(
                        f"Target position {pos} for motor {dev} is outside of range: [{low_limit}, {high_limit}]"
                    )

    def _get_scan_motors(self):
        if len(self.caller_args) > 0:
            self.scan_motors = list(self.caller_args.keys())

    @abstractmethod
    def run(self):
        pass


class ScanBase(RequestBase):
    """
    procedure:
    - initialize
    - read scan motors (to get start positions)
    - prepare positions
        - _calculate_positions
        - <add relative positions>
        - _check_limits
    - open scan
    - stage
    - run baseline readings
    - scan core
    - finalize
    - unstage
    - cleanup
    """

    scan_name = ""
    scan_report_hint = None
    scan_type = "step"
    arg_input = [ScanArgType.DEVICE]
    arg_bundle_size = len(arg_input)
    required_kwargs = []

    def __init__(
        self,
        *args,
        device_manager: DeviceManagerBase = None,
        parameter=None,
        metadata=None,
        **kwargs,
    ):
        super().__init__(
            *args, device_manager=device_manager, parameter=parameter, metadata=metadata, **kwargs
        )
        self.DIID = 0
        self.pointID = 0
        self.exp_time = self.caller_kwargs.get("exp_time", 0.1)

        self.relative = parameter["kwargs"].get("relative", True)
        self.burst_at_each_point = parameter["kwargs"].get("burst_at_each_point", 1)
        self.burst_index = 0

        self.start_pos = np.repeat(0, len(self.scan_motors)).tolist()
        self.positions = []
        self.num_pos = None

        if self.scan_name == "":
            raise ValueError("scan_name cannot be empty")

    def initialize(self):
        pass

    def read_scan_motors(self):
        yield self.device_msg(
            device=self.scan_motors,
            action="read",
            parameter={
                "group": "scan_motor",
                "wait_group": "scan_motor",
            },
        )
        yield self.device_msg(
            device=self.scan_motors,
            action="wait",
            parameter={
                "type": "read",
                "group": "scan_motor",
                "wait_group": "scan_motor",
            },
        )

    @abstractmethod
    def _calculate_positions(self) -> None:
        """Calculate the positions"""
        pass

    def prepare_positions(self):
        self._calculate_positions()
        self.num_pos = len(self.positions)
        self._set_position_offset()
        self._check_limits()

    def open_scan(self):
        yield self.device_msg(
            device=None,
            action="open_scan",
            parameter={
                "primary": self.scan_motors,
                "num_points": self.num_pos,
                "scan_name": self.scan_name,
                "scan_type": self.scan_type,
            },
        )

    def stage(self):
        yield self.device_msg(device=None, action="stage", parameter={})

    def run_baseline_reading(self):
        yield self.device_msg(
            device=None,
            action="baseline_reading",
            parameter={},
            metadata={"stream": "baseline"},
        )

    def _set_position_offset(self):
        self.start_pos = [
            self.device_manager.devices[dev].read().get("value") for dev in self.scan_motors
        ]
        if self.relative:
            self.positions += self.start_pos

    def close_scan(self):
        yield self.device_msg(device=None, action="close_scan", parameter={})

    def scan_core(self):
        for ind, pos in self._get_position():
            for self.burst_index in range(self.burst_at_each_point):
                yield from self._at_each_point(ind, pos)
            self.burst_index = 0

    def finalize(self):
        yield from self._move_and_wait(self.start_pos)
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={
                "type": "read",
                "group": "primary",
                "wait_group": "readout_primary",
            },
        )

    def unstage(self):
        yield self.device_msg(device=None, action="unstage", parameter={})

    def cleanup(self):
        yield from self.close_scan()

    def _at_each_point(self, ind=None, pos=None):
        yield from self._move_and_wait(pos)
        if ind > 0:
            yield self.device_msg(
                device=None,
                action="wait",
                parameter={
                    "type": "read",
                    "group": "primary",
                    "wait_group": "readout_primary",
                },
            )
        yield self.device_msg(
            device=None,
            action="trigger",
            parameter={"group": "trigger"},
            metadata={"pointID": self.pointID},
        )
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={"type": "trigger", "time": self.exp_time},
        )
        yield self.device_msg(
            device=None,
            action="read",
            parameter={
                "target": "primary",
                "group": "primary",
                "wait_group": "readout_primary",
            },
            metadata={"pointID": self.pointID},
        )
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={
                "type": "read",
                "group": "scan_motor",
                "wait_group": "readout_primary",
            },
        )
        self.pointID += 1

    def _move_and_wait(self, pos):
        if not isinstance(pos, list) and not isinstance(pos, np.ndarray):
            pos = [pos]
        if len(pos) == 0:
            return
        for ind, val in enumerate(self.scan_motors):
            yield self.device_msg(
                device=val,
                action="set",
                parameter={
                    "value": pos[ind],
                    "group": "scan_motor",
                    "wait_group": "scan_motor",
                },
            )
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={
                "type": "move",
                "group": "scan_motor",
                "wait_group": "scan_motor",
            },
        )

    def _get_position(self):
        for ind, pos in enumerate(self.positions):
            yield (ind, pos)

    def run(self):
        self.initialize()
        yield from self.read_scan_motors()
        self.prepare_positions()
        yield from self.open_scan()
        yield from self.stage()
        yield from self.run_baseline_reading()
        yield from self.scan_core()
        yield from self.finalize()
        yield from self.unstage()
        yield from self.cleanup()

    @classmethod
    def scan(cls, *args, **kwargs):
        scan = cls(args, **kwargs)
        yield from scan.run()

    @staticmethod
    def _parameter_bundler(args, bundle_size):
        """

        Args:
            args:
            bundle_size: number of parameters per bundle

        Returns:

        """
        params = {}
        for cmds in partition(bundle_size, args):
            params[cmds[0].name] = cmds[1:]
        return params


class ScanStub(RequestBase):
    pass


class OpenScanDef(ScanStub):
    scan_name = "open_scan_def"
    scan_report_hint = None

    def run(self):
        yield self.device_msg(device=None, action="open_scan_def", parameter={})


class CloseScanDef(ScanStub):
    scan_name = "close_scan_def"
    scan_report_hint = "table"

    def run(self):
        yield self.device_msg(device=None, action="close_scan_def", parameter={})


class CloseScanGroup(ScanStub):
    scan_name = "close_scan_group"

    def run(self):
        yield self.device_msg(device=None, action="close_scan_group", parameter={})


class DeviceRPC(ScanStub):
    scan_name = "device_rpc"
    arg_input = [
        ScanArgType.DEVICE,
        ScanArgType.STR,
        ScanArgType.LIST,
        ScanArgType.DICT,
    ]
    arg_bundle_size = len(arg_input)
    scan_report_hint = None

    def _get_scan_motors(self):
        pass

    def run(self):
        yield self.device_msg(
            device=self.parameter.get("device"),
            action="rpc",
            parameter=self.parameter,
        )


class Move(RequestBase):

    scan_name = "mv"
    arg_input = [ScanArgType.DEVICE, ScanArgType.FLOAT]
    arg_bundle_size = len(arg_input)
    scan_report_hint = None

    def __init__(self, *args, parameter=None, **kwargs):
        """
        Move device(s) to an absolute position
        Args:
            *args: pairs of device / position arguments
            **kwargs:

        Returns:
        Examples:
            >>> scans.mv(dev.samx, 1, dev.samy,2)
        """
        super().__init__(parameter=parameter, **kwargs)

    def _calculate_positions(self):
        self.positions = [[val[0] for val in self.caller_args.values()]]

    def _at_each_point(self, pos=None):
        for ii, motor in enumerate(self.scan_motors):
            yield self.device_msg(
                device=motor,
                action="set",
                parameter={
                    "value": self.positions[0][ii],
                    "group": "scan_motor",
                    "wait_group": "scan_motor",
                },
            )
        for motor in self.scan_motors:
            yield self.device_msg(
                device=motor,
                action="wait",
                parameter={"type": "move", "group": "scan_motor", "wait_group": "scan_motor"},
            )

    def cleanup(self):
        pass

    def prepare_positions(self):
        self._calculate_positions()
        self._check_limits()

    def run(self):
        self.initialize()
        self.prepare_positions()
        yield from self._at_each_point()


class UpdatedMove(Move):
    """
    Move device(s) to an absolute position and show live updates.
    Args:
        *args: pairs of device / position arguments
        **kwargs:

    Returns:
    Examples:
        >>> scans.umv(dev.samx, 1, dev.samy,2)
    """

    scan_name = "umv"
    scan_report_hint = "readback"


class Scan(ScanBase):
    scan_name = "grid_scan"
    scan_report_hint = "table"
    arg_input = [
        ScanArgType.DEVICE,
        ScanArgType.FLOAT,
        ScanArgType.FLOAT,
        ScanArgType.INT,
    ]
    arg_bundle_size = len(arg_input)
    required_kwargs = ["exp_time"]

    def __init__(self, *args, parameter=None, **kwargs):
        """
        Scan two motors in a grid.

        Args:
            *args: pairs of device / start position / end position / steps arguments
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.grid_scan(dev.motor1, -5, 5, 10, dev.motor2, -5, 5, 10, exp_time=0.1, relative=True)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []

    def _calculate_positions(self):
        for _, val in self.caller_args.items():
            self.axis.append(np.linspace(val[0], val[1], val[2]))
        if len(self.axis) > 1:
            self.positions = get_2D_raster_pos(self.axis)
        else:
            self.positions = np.vstack(tuple(self.axis)).T


class FermatSpiralScan(ScanBase):
    scan_name = "fermat_scan"
    scan_report_hint = "table"
    required_kwargs = ["exp_time", "step"]
    arg_input = [ScanArgType.DEVICE, ScanArgType.FLOAT, ScanArgType.FLOAT]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A scan following Fermat's spiral.

        Args:
            *args: pairs of device / start position / end position / steps arguments
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.fermat_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, step=0.5, exp_time=0.1, relative=True)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.step = parameter.get("kwargs", {}).get("step", 0.1)
        self.spiral_type = parameter.get("kwargs", {}).get("spiral_type", 0)

    def _calculate_positions(self):
        params = list(self.caller_args.values())
        self.positions = get_fermat_spiral_pos(
            params[0][0],
            params[0][1],
            params[1][0],
            params[1][1],
            step=self.step,
            spiral_type=self.spiral_type,
            center=False,
        )


class RoundScan(ScanBase):
    scan_name = "round_scan"
    scan_report_hint = "table"
    required_kwargs = ["exp_time"]
    arg_input = [
        ScanArgType.DEVICE,
        ScanArgType.DEVICE,
        ScanArgType.FLOAT,
        ScanArgType.FLOAT,
        ScanArgType.INT,
        ScanArgType.INT,
    ]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A scan following a round shell-like pattern.

        Args:
            *args: motor1, motor2, inner ring, outer ring, number of rings, number of positions in the first ring
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.round_scan(dev.motor1, dev.motor2, 0, 50, 5, 3, exp_time=0.1, relative=True)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []

    def _get_scan_motors(self):
        caller_args = list(self.caller_args.items())[0]
        self.scan_motors = [caller_args[0], caller_args[1][0]]

    def _calculate_positions(self):
        params = list(self.caller_args.values())[0]
        self.positions = get_round_scan_positions(
            r_in=params[1], r_out=params[2], nr=params[3], nth=params[4]
        )


class RoundScanFlySim(ScanBase):
    scan_name = "round_scan_fly"
    scan_report_hint = "table"
    scan_type = "fly"
    required_kwargs = ["exp_time"]
    arg_input = [
        ScanArgType.DEVICE,
        ScanArgType.DEVICE,
        ScanArgType.FLOAT,
        ScanArgType.FLOAT,
        ScanArgType.INT,
        ScanArgType.INT,
    ]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A scan following a round shell-like pattern.

        Args:
            *args: motor1, motor2, inner ring, outer ring, number of rings, number of positions in the first ring
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.round_scan(dev.motor1, dev.motor2, 0, 50, 5, 3, exp_time=0.1, relative=True)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []

    def _get_scan_motors(self):
        caller_args = list(self.caller_args.items())[0]
        self.scan_motors = [caller_args[0], caller_args[1][0]]

    def _calculate_positions(self):
        params = list(self.caller_args.values())[0]
        self.positions = get_round_scan_positions(
            r_in=params[1], r_out=params[2], nr=params[3], nth=params[4]
        )

    def scan_core(self):
        yield self.device_msg(
            device="flyer_sim",
            action="kickoff",
            parameter={"num_pos": self.num_pos},
            metadata={},
        )

        while True:
            yield self.device_msg(
                device=None,
                action="read",
                parameter={
                    "target": "primary",
                    "group": "primary",
                    "wait_group": "readout_primary",
                },
                metadata={},
            )
            yield self.device_msg(
                device=None,
                action="wait",
                parameter={
                    "type": "read",
                    "group": "primary",
                    "wait_group": "readout_primary",
                },
            )
            msg = self.device_manager.producer.get(MessageEndpoints.device_status("flyer_sim"))
            if msg:
                status = BECMessage.DeviceStatusMessage.loads(msg)
                if status.content.get("status", 1) == 0 and self.metadata.get(
                    "RID"
                ) == status.metadata.get("RID"):
                    break

            time.sleep(1)
            logger.debug("reading monitors")


class RoundROIScan(ScanBase):
    scan_name = "round_roi_scan"
    scan_report_hint = "table"
    required_kwargs = ["exp_time", "dr", "nth"]
    arg_input = [ScanArgType.DEVICE, ScanArgType.FLOAT]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A scan following a round-roi-like pattern.

        Args:
            *args: motor1, width for motor1, motor2, width for motor2,
            dr: shell width
            nth: number of points in the first shell
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.round_roi_scan(dev.motor1, 20, dev.motor2, 20, dr=2, nth=3, exp_time=0.1, relative=True)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.dr = parameter.get("kwargs", {}).get("dr", 1)
        self.nth = parameter.get("kwargs", {}).get("nth", 5)

    def _calculate_positions(self) -> None:
        params = list(self.caller_args.values())
        self.positions = get_round_roi_scan_positions(
            lx=params[0][0], ly=params[1][0], dr=self.dr, nth=self.nth
        )


class RepeatScan:
    pass


class LineScan(ScanBase):
    scan_name = "line_scan"
    scan_report_hint = "table"
    required_kwargs = ["exp_time", "steps"]
    arg_input = [ScanArgType.DEVICE, ScanArgType.FLOAT, ScanArgType.FLOAT]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A line scan for one or more motors.

        Args:
            *args: pairs of device / start position / end position
            exp_time: exposure time in s
            steps: number of steps (please note: 5 steps == 6 positions)
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.line_scan(dev.motor1, -5, 5, dev.motor2, -5, 5, steps=10, exp_time=0.1, relative=True)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.steps = parameter.get("kwargs", {}).get("steps", 10)

    def _calculate_positions(self) -> None:
        for _, val in self.caller_args.items():
            ax_pos = np.linspace(val[0], val[1], self.steps)
            self.axis.append(ax_pos)
        self.positions = np.array(list(zip(*self.axis)))


class OpenInteractiveScan(ScanBase):
    scan_name = "open_interactive_scan"
    scan_report_hint = ""
    required_kwargs = ["exp_time"]
    arg_input = [ScanArgType.DEVICE]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        An interactive scan for one or more motors.

        Args:
            *args: devices
            exp_time: exposure time in s
            steps: number of steps (please note: 5 steps == 6 positions)
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.open_interactive_scan(dev.motor1, dev.motor2, exp_time=0.1)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []

    def _calculate_positions(self):
        pass

    def _get_scan_motors(self):
        caller_args = list(self.caller_args.keys())
        self.scan_motors = caller_args

    def run(self):
        yield self.device_msg(device=None, action="open_scan_def", parameter={})
        self.initialize()
        yield from self.read_scan_motors()
        yield from self.open_scan()
        yield from self.stage()
        yield from self.run_baseline_reading()


class AddInteractiveScanPoint(ScanBase):
    scan_name = "interactive_scan_trigger"
    scan_report_hint = ""
    arg_input = [ScanArgType.DEVICE]
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        An interactive scan for one or more motors.

        Args:
            *args: devices
            exp_time: exposure time in s
            steps: number of steps (please note: 5 steps == 6 positions)
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.interactive_scan_trigger()

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []

    def _calculate_positions(self):
        pass

    def _get_scan_motors(self):
        self.scan_motors = list(self.caller_args.keys())

    def _at_each_point(self, ind=None, pos=None):
        yield self.device_msg(
            device=None,
            action="trigger",
            parameter={"group": "trigger"},
            metadata={"pointID": self.pointID},
        )
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={"type": "trigger", "time": self.exp_time},
        )
        yield self.device_msg(
            device=None,
            action="read",
            parameter={
                "target": "primary",
                "group": "primary",
                "wait_group": "readout_primary",
            },
            metadata={"pointID": self.pointID},
        )
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={
                "type": "read",
                "group": "scan_motor",
                "wait_group": "readout_primary",
            },
        )
        yield self.device_msg(
            device=None,
            action="wait",
            parameter={
                "type": "read",
                "group": "primary",
                "wait_group": "readout_primary",
            },
        )
        self.pointID += 1

    def run(self):
        yield from self.open_scan()
        yield from self._at_each_point()
        yield from self.close_scan()


class CloseInteractiveScan(ScanBase):
    scan_name = "close_interactive_scan"
    scan_report_hint = ""
    arg_input = []
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """
        An interactive scan for one or more motors.

        Args:
            *args: devices
            exp_time: exposure time in s
            steps: number of steps (please note: 5 steps == 6 positions)
            relative: Start from an absolute or relative position
            burst: number of acquisition per point

        Returns:

        Examples:
            >>> scans.close_interactive_scan(dev.motor1, dev.motor2, exp_time=0.1)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []

    def _calculate_positions(self):
        pass

    def run(self):
        yield from self.finalize()
        yield from self.unstage()
        yield from self.cleanup()
        yield self.device_msg(device=None, action="close_scan_def", parameter={})
