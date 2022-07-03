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
- unstage                                # unstage all devices that have been staged before
- cleanup                                # send a close scan message and perform additional cleanups if needed
"""

from scan_server.scans import ScanArgType, ScanBase, get_fermat_spiral_pos


class FermatSpiralScan2(ScanBase):
    scan_name = "fermat_scan2"
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
