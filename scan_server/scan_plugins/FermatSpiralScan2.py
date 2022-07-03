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
