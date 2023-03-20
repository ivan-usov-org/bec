from scan_server.scans import FlyScanBase


class OTFScan(FlyScanBase):
    scan_name = "otf_scan"
    scan_report_hint = "table"
    required_kwargs = ["e1", "e2", "time"]
    arg_input = []
    arg_bundle_size = len(arg_input)

    def __init__(self, *args, parameter=None, **kwargs):
        """


        Args:
            device:
            start position:
            end position:

        Returns:

        Examples:
            >>> scans.otf_scan(e1=700, e2=740, time=4)

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = ["otf"]
        self.num_pos = 0
