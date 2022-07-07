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

import uuid
from scan_server.scans import ScanArgType, ScanBase
from bec_utils import MessageEndpoints, BECMessage
import numpy as np
import time
from bec_utils import bec_logger
MOVEMENT_SCALE_X = np.sin(np.radians(15))*np.cos(np.radians(30))
MOVEMENT_SCALE_Y = np.cos(np.radians(15))

logger = bec_logger.logger


def lamni_to_stage_coordinates(x:float,y:float) -> tuple:
    y_stage = y / MOVEMENT_SCALE_Y
    x_stage = 2*(x-y_stage * MOVEMENT_SCALE_X )
    return (x_stage, y_stage)

def lamni_from_stage_coordinates(x_stage:float,y_stage:float) -> tuple:
    x = x_stage * 0.5 + y_stage * MOVEMENT_SCALE_X
    y = y_stage * MOVEMENT_SCALE_Y
    return (x, y)




class LamNIFermatScan(ScanBase):
    scan_name = "lamni_fermat_scan"
    scan_report_hint = "table"
    required_kwargs = ["fov_size", "exp_time", "step"]
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

    def initialize(self):
        self.scan_motors = ["rtx", "rty"]

    def prepare_positions(self):
        self._calculate_positions()
        self.num_pos = len(self.positions)

    def _prepare_setup(self):
        yield from self.lamni_new_scan_center_interferometer(self.center_x, self.center_y)

    def _calculate_positions(self) -> None:
        pass

    def lamni_new_scan_center_interferometer(self, x,y):
        """move to new scan center. xy in mm """
        #rt_feedback_disable()
        time.sleep(0.05)
        lsamx_center = 8.866
        lsamy_center = 10.18
        lsamx_current = self.device_manager.devices.lsamx.read().get("value")
        lsamy_current = self.device_manager.devices.lsamy.read().get("value")
        rtx_current = self.device_manager.devices.rtx.read().get("value")
        rty_current = self.device_manager.devices.rty.read().get("value")

        x_stage, y_stage = lamni_to_stage_coordinates(x,y)

        x_center_expect, y_center_expect = lamni_from_stage_coordinates(lsamx_current-lsamx_center,lsamy_current-lsamy_center)

        #in microns
        x_drift = x_center_expect*1000-rtx_current
        y_drift = y_center_expect*1000-rty_current

        logger.info(f"Current uncompensated drift of setup is x={x_drift:.3f}, y={y_drift:.3f}")

        move_x = x_stage+lsamx_center+lamni_to_stage_coordinates(x_drift,y_drift)[0]/1000
        move_y = y_stage+lsamy_center+lamni_to_stage_coordinates(x_drift,y_drift)[1]/1000

        coarse_move_req_x = np.abs(lsamx_current - move_x)
        coarse_move_req_y = np.abs(lsamy_current - move_y)

        if np.abs(y_drift) > 150 or np.abs(x_drift) > 150 or (coarse_move_req_y<0.003 and coarse_move_req_x<0.003):
            logger.info("No drift correction.")
        else:
            logger.info(f"Compensating {[val/1000 for val in lamni_to_stage_coordinates(x_drift,y_drift)]}")

            yield from self._move_and_wait_devices(["lsamx","lsamy"], [move_x, move_y])
        
        rtx_current = self.device_manager.devices.rtx.read().get("value")
        rtx_current = self.device_manager.devices.rty.read().get("value")

        rpc_id=str(uuid.uuid4())
        yield from self.run_rpc("lsamx","controller.galil_show_all",str(rpc_id))
        val = self.get_from_rpc(rpc_id)

        logger.info(f"New scan center interferometer {rtx_current:.3f}, {rty_current:.3f} microns")


    def run_rpc(self, device, func_name, rpc_id, *args, **kwargs):
        yield self.device_msg(
            device=device,
            action="rpc",
            parameter={"device":device, "func":func_name, "rpc_id":rpc_id, "args":list(args), "kwargs":kwargs},
        )

    def get_from_rpc(self, rpc_id):
        while True:
            msg = self.device_manager.producer.get(MessageEndpoints.device_rpc(rpc_id))
            if msg:
                break
            time.sleep(0.1)
        msg = BECMessage.DeviceRPCMessage.loads(msg)
        print(msg.content.get("out"))
        return msg.content.get("return_val")       


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

    def run(self, simulate=False):
        self.simulate = simulate
        self.initialize()
        yield from self.read_scan_motors()
        self.prepare_positions()
        if not self.simulate:
            yield from self._prepare_setup()
        yield from self.open_scan()
        yield from self.stage()
        yield from self.run_baseline_reading()
        yield from self.scan_core()
        yield from self.finalize()
        yield from self.unstage()
        yield from self.cleanup()
    
