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
- self.open_scan                         # send an open_scan message including the scan name, the number of points and the scan motor names
- self.stage                             # stage all devices for the upcoming acquisiton
- self.run_baseline_readings             # read all devices to get a baseline for the upcoming scan
- self.scan_core                         # run a loop over all position
    - self._at_each_point(ind, pos)      # called at each position with the current index and the target positions as arguments
- self.finalize                          # clean up the scan, e.g. move back to the start position; wait everything to finish
- self.unstage                           # unstage all devices that have been staged before
- self.cleanup                           # send a close scan message and perform additional cleanups if needed
"""

import time

from scan_server.scans import FlyScanBase, ScanArgType


class SgalilGrid(FlyScanBase):
    scan_name = "sgalil_grid"
    scan_report_hint = "scan_progress"
    required_kwargs = []
    arg_input = []
    arg_bundle_size = len(arg_input)

    def __init__(
        self,
        start_y: float,
        end_y: float,
        interval_y: int,
        start_x: float,
        end_x: float,
        interval_x: int,
        *args,
        exp_time: float = 0.1,
        readout_time: float = 0.1,
        **kwargs
    ):
        """
        SGalil-based grid scan.

        Args:
            start_y (float): start position of y axis (fast axis)
            end_y (float): end position of y axis (fast axis)
            interval_y (int): number of points in y axis
            start_x (float): start position of x axis (slow axis)
            end_x (float): end position of x axis (slow axis)
            interval_x (int): number of points in x axis
            exp_time (float): exposure time in seconds. Default is 0.1s
            read_time (float): readout time in seconds, minimum of .5e-3s (0.5ms)

        """
        super().__init__(*args, **kwargs)
        self.start_y = start_y
        self.end_y = end_y
        self.interval_y = interval_y
        self.start_x = start_x
        self.end_x = end_x
        self.interval_x = interval_x
        self.exp_time = exp_time
        self.readout_time = readout_time
        self.num_pos = int(interval_x * interval_y)

    def scan_report_instructions(self):
        if not self.scan_report_hint:
            yield None
            return
        yield from self.stubs.scan_report_instruction({"progress": ["async_dev1"]})

    def scan_core(self):
        """
        This is the main event loop.
        """

        # set up the delay generators
        status_ddg_detectors_burst = yield from self.stubs.send_rpc_and_wait(
            "ddg_detectors",
            "burst_enable",
            count=self.interval_y,
            delay=0,
            period=(self.exp_time + self.readout_time),
            config="first",
        )
        status_ddg_mcs_burst = yield from self.stubs.send_rpc_and_wait(
            "ddg_mcs",
            "burst_enable",
            count=self.interval_y + 1,
            delay=0,
            period=(self.exp_time + self.readout_time),
            config="first",
        )
        # TODO disable fsh ddg bc SGalil trigger it directly
        # Setup triggering
        status_ddg_detectors_source = yield from self.stubs.send_rpc_and_wait(
            "ddg_detectors", "source.set", 2
        )
        status_ddg_mcs_source = yield from self.stubs.send_rpc_and_wait("ddg_mcs", "source.set", 1)
        # Setup mcs_points per line
        status_mcs_points_per_line = yield from self.stubs.send_rpc_and_wait(
            "mcs", "num_use_all.set", self.interval_y + 1
        )
        status_mcs_lines = yield from self.stubs.send_rpc_and_wait(
            "mcs", "num_lines.set", self.interval_x
        )

        status_ddg_mcs_ttlwidth = yield from self.stubs.send_rpc_and_wait(
            "ddg_mcs", "set_channels", "width", 3e-3
        )
        status_ddg_mcs_ttldelay = yield from self.stubs.send_rpc_and_wait(
            "ddg_mcs", "set_channels", "delay", 0
        )

        # wait for the delay generators to finish setting up
        status_ddg_detectors_source.wait()
        status_ddg_mcs_source.wait()
        status_mcs_points_per_line.wait()
        status_mcs_lines.wait()

        yield from self.stubs.kickoff(
            device="samx",
            parameter={
                "start_y": self.start_y,
                "end_y": self.end_y,
                "interval_y": self.interval_y,
                "start_x": self.start_x,
                "end_x": self.end_x,
                "interval_x": self.interval_x,
                "exp_time": self.exp_time,
                "readout_time": self.readout_time,
            },
        )

        # while True:
        #     status = self.stubs.get_req_status(
        #         device=self.scan_motors[0], RID=self.metadata["RID"], DIID=target_diid
        #     )
        #     if status:
        #         break
        #     time.sleep(1)
