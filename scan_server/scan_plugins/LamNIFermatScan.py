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

from scan_server.scans import ScanArgType, ScanBase


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
        self._prepare_setup()

    def _prepare_setup(self):
        pass

    def _calculate_positions(self) -> None:
        pass
