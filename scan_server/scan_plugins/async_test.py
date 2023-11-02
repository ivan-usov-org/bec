import time

from scan_server.scans import ScanBase


class LineScanFlySim(ScanBase):
    scan_name = "line_scan_fly_sim"
    scan_report_hint = "scan_progress"
    required_kwargs = []
    arg_input = {}
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
        read_time: float = 0.1,
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
        self.start_y = start_y
        self.end_y = end_y
        self.interval_y = interval_y
        self.start_x = start_x
        self.end_x = end_x
        self.interval_x = interval_x
        self.exp_time = exp_time
        self.read_time = read_time
        super().__init__(*args, **kwargs)

    def _calculate_positions(self) -> None:
        pass

    def scan_report_instructions(self):
        if not self.scan_report_hint:
            yield None
            return
        yield from self.stubs.scan_report_instruction(
            {
                "readback": {
                    "RID": self.metadata["RID"],
                    "devices": ["samx"],
                    "start": [0],
                    "end": [10],
                }
            }
        )
        yield from self.stubs.scan_report_instruction({"scan_progress": ["async_dev1"]})

    def scan_core(self):
        yield from self.stubs.set_and_wait(device=["samx"], positions=[10])
        time.sleep(5)
        yield None

    def run(self):
        self.initialize()
        yield from self.read_scan_motors()
        yield from self.prepare_positions()
        yield from self.scan_report_instructions()
        yield from self.open_scan()
        yield from self.stage()
        yield from self.run_baseline_reading()
        yield from self.scan_core()
        yield from self.finalize()
        yield from self.unstage()
        yield from self.cleanup()
