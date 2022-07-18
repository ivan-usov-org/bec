"""
SCAN PLUGINS

All new scans should be derived from ScanBase. ScanBase provides various methods that can be customized and overriden
but they are executed in a specific order:

- self.initialize                        # initialize the class if needed
- self.read_scan_motors                  # used to retrieve the start position (and the relative position shift if needed)
- self.prepare_positions                 # prepare the positions for the scan. The preparation is split into multiple sub fuctions:
    - self._calculate_positions          # calculate the positions
    - self._set_positions_offset         # apply the previously retrieved scan position shift (if needed)
    - self._check_limits                 # tests to ensure the limits won't be reached
- self.open_scan                         # send and open_scan message including the scan name, the number of points and the scan motor names
- self.stage                             # stage all devices for the upcoming acquisiton
- self.run_baseline_readings             # read all devices to get a baseline for the upcoming scan
- self.scan_core                         # run a loop over all position 
    - self._at_each_point(ind, pos)      # called at each position with the current index and the target positions as arguments
- self.finalize                          # clean up the scan, e.g. move back to the start position; wait everything to finish
- self.unstage                           # unstage all devices that have been staged before
- self.cleanup                           # send a close scan message and perform additional cleanups if needed
"""

import time
import uuid

import numpy as np
from bec_utils import BECMessage, MessageEndpoints, bec_logger
from scan_server.scans import ScanBase

MOVEMENT_SCALE_X = np.sin(np.radians(15)) * np.cos(np.radians(30))
MOVEMENT_SCALE_Y = np.cos(np.radians(15))

logger = bec_logger.logger


def lamni_to_stage_coordinates(x: float, y: float) -> tuple:
    """convert from lamni coordinates to stage coordinates"""
    y_stage = y / MOVEMENT_SCALE_Y
    x_stage = 2 * (x - y_stage * MOVEMENT_SCALE_X)
    return (x_stage, y_stage)


def lamni_from_stage_coordinates(x_stage: float, y_stage: float) -> tuple:
    """convert to lamni coordinates from stage coordinates"""
    x = x_stage * 0.5 + y_stage * MOVEMENT_SCALE_X
    y = y_stage * MOVEMENT_SCALE_Y
    return (x, y)


class LamNIFermatScan(ScanBase):
    scan_name = "lamni_fermat_scan"
    scan_report_hint = "table"
    required_kwargs = ["fov_size", "exp_time", "step", "angle"]
    arg_input = []
    arg_bundle_size = None

    def __init__(self, *args, parameter=None, **kwargs):
        """
        A LamNI scan following Fermat's spiral.

        Kwargs:
            shift_x: extra shift in x. The shift will not be rotated. (default 0).
            shift_y: extra shift in y. The shift will not be rotated. (default 0).
            center_x: center position in x at 0 deg.  (optional)
            center_y: center position in y at 0 deg.  (optional)
            angle: rotation angle (will rotate first)
        Returns:

        Examples:
            >>> scans.lamni_fermat_scan(fov_size=[20], step=0.5, exp_time=0.1)
            >>> scans.lamni_fermat_scan(fov_size=[20, 25], center_x=20, step=0.5, exp_time=0.1)
        """

        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        scan_kwargs = parameter.get("kwargs", {})
        self.fov_size = scan_kwargs.get("fov_size")
        if len(self.fov_size) == 1:
            self.fov_size *= 2  # if we only have one argument, let's assume it's a square
        self.step = scan_kwargs.get("step", 0.1)
        self.center_x = scan_kwargs.get("center_x", 0)
        self.center_y = scan_kwargs.get("center_y", 0)
        self.shift_x = scan_kwargs.get("shift_x", 0)
        self.shift_y = scan_kwargs.get("shift_y", 0)
        self.angle = scan_kwargs.get("angle", 0)

    def initialize(self):
        self.scan_motors = ["rtx", "rty"]

    def prepare_positions(self):
        self._calculate_positions()
        self.num_pos = len(self.positions)

    def _prepare_setup(self):
        yield from self.lamni_rotation(self.angle)
        yield from self.lamni_new_scan_center_interferometer(self.center_x, self.center_y)

    def _calculate_positions(self) -> None:
        pass

    def lamni_rotation(self, angle):
        # get last setpoint (cannot be based on pos get because they will deviate slightly)
        lsamrot_current_setpoint = yield from self.device_rpc("lsamrot", "user_setpoint.get")
        if angle == lsamrot_current_setpoint:
            logger.info("No rotation required")
        else:
            logger.info("Rotating to requested angle")
            yield from self._move_and_wait_devices(["lsamrot"], [angle])

    def lamni_new_scan_center_interferometer(self, x, y):
        """move to new scan center. xy in mm"""
        lsamx_center = 8.866
        lsamy_center = 10.18

        # could first check if feedback is enabled
        yield from self.device_rpc("rtx", "controller.feedback_disable")
        time.sleep(0.05)

        rtx_current = yield from self.device_rpc("rtx", "readback.get")
        rty_current = yield from self.device_rpc("rty", "readback.get")
        lsamx_current = yield from self.device_rpc("lsamx", "readback.get")
        lsamy_current = yield from self.device_rpc("lsamy", "readback.get")

        # lsamx_current = self.device_manager.devices.lsamx.read().get("value")
        # lsamy_current = self.device_manager.devices.lsamy.read().get("value")
        # rtx_current = self.device_manager.devices.rtx.read().get("value")
        # rty_current = self.device_manager.devices.rty.read().get("value")

        x_stage, y_stage = lamni_to_stage_coordinates(x, y)

        x_center_expect, y_center_expect = lamni_from_stage_coordinates(
            lsamx_current - lsamx_center, lsamy_current - lsamy_center
        )

        # in microns
        x_drift = x_center_expect * 1000 - rtx_current
        y_drift = y_center_expect * 1000 - rty_current

        logger.info(f"Current uncompensated drift of setup is x={x_drift:.3f}, y={y_drift:.3f}")

        move_x = x_stage + lsamx_center + lamni_to_stage_coordinates(x_drift, y_drift)[0] / 1000
        move_y = y_stage + lsamy_center + lamni_to_stage_coordinates(x_drift, y_drift)[1] / 1000

        coarse_move_req_x = np.abs(lsamx_current - move_x)
        coarse_move_req_y = np.abs(lsamy_current - move_y)

        if (
            np.abs(y_drift) > 150
            or np.abs(x_drift) > 150
            or (coarse_move_req_y < 0.003 and coarse_move_req_x < 0.003)
        ):
            logger.info("No drift correction.")
        else:
            logger.info(
                f"Compensating {[val/1000 for val in lamni_to_stage_coordinates(x_drift,y_drift)]}"
            )

            yield from self._move_and_wait_devices(["lsamx", "lsamy"], [move_x, move_y])

        time.sleep(0.01)
        rtx_current = yield from self.device_rpc("rtx", "readback.get")
        rty_current = yield from self.device_rpc("rty", "readback.get")

        logger.info(f"New scan center interferometer {rtx_current:.3f}, {rty_current:.3f} microns")

        # second iteration
        x_center_expect, y_center_expect = lamni_from_stage_coordinates(x_stage, y_stage)

        # in microns
        x_drift2 = x_center_expect * 1000 - rtx_current
        y_drift2 = y_center_expect * 1000 - rty_current
        logger.info(
            f"Uncompensated drift of setup after first iteration is x={x_drift2:.3f}, y={y_drift2:.3f}"
        )

        if np.abs(x_drift2) > 5 or np.abs(y_drift2) > 5:
            logger.info(
                f"Compensating second iteration {[val/1000 for val in lamni_to_stage_coordinates(x_drift2,y_drift2)]}"
            )
            move_x = (
                x_stage
                + lsamx_center
                + lamni_to_stage_coordinates(x_drift, y_drift)[0] / 1000
                + lamni_to_stage_coordinates(x_drift2, y_drift2)[0] / 1000
            )
            move_y = (
                y_stage
                + lsamy_center
                + lamni_to_stage_coordinates(x_drift, y_drift)[1] / 1000
                + lamni_to_stage_coordinates(x_drift2, y_drift2)[1] / 1000
            )
            yield from self._move_and_wait_devices(["lsamx", "lsamy"], [move_x, move_y])
            time.sleep(0.01)
            rtx_current = yield from self.device_rpc("rtx", "readback.get")
            rty_current = yield from self.device_rpc("rty", "readback.get")

            logger.info(
                f"New scan center interferometer after second iteration {rtx_current:.3f}, {rty_current:.3f} microns"
            )
            x_drift2 = x_center_expect * 1000 - rtx_current
            y_drift2 = y_center_expect * 1000 - rty_current
            logger.info(
                f"Uncompensated drift of setup after second iteration is x={x_drift2:.3f}, y={y_drift2:.3f}"
            )
        else:
            logger.info("No second iteration required")

        yield from self.device_rpc("rtx", "controller.feedback_enable_without_reset")

        # set_lm rtx _interferometer_pos_x-30 _interferometer_pos_x+30
        # set_lm rty _interferometer_pos_y-30 _interferometer_pos_y+30

    def _move_and_wait_devices(self, devices, pos):
        if not isinstance(pos, list) and not isinstance(pos, np.ndarray):
            pos = [pos]
        for ind, val in enumerate(devices):
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
            device=devices,
            action="wait",
            parameter={
                "type": "move",
                "group": "scan_motor",
                "wait_group": "scan_motor",
            },
        )

    def open_scan(self):
        yield self.device_msg(
            device=None,
            action="open_scan",
            parameter={
                "primary": self.scan_motors,
                "num_points": self.num_pos,
                "scan_name": self.scan_name,
            },
        )

    def run(self):
        self.initialize()
        yield from self.read_scan_motors()
        self.prepare_positions()
        yield from self._prepare_setup()
        yield from self.open_scan()
        yield from self.stage()
        yield from self.run_baseline_reading()
        yield from self.scan_core()
        yield from self.finalize()
        yield from self.unstage()
        yield from self.cleanup()
