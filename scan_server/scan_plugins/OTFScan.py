from scan_server.scans import ScanBase, ScanArgType
from bec_utils import MessageEndpoints, BECMessage
import numpy as np
from typing import List
import time

class OTFScan(ScanBase):
    scan_name = "otf_scan"
    scan_report_hint = "table"
    required_kwargs = ["e1", "e2", "time"]
    arg_input = []
    arg_bundle_size = len(arg_input)
    scan_type = "fly"

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

    def _calculate_positions(self) -> None:
        pass

    def prepare_positions(self):
        yield None

    def _get_flyer_status(self) -> List:
        flyer = self.scan_motors[0]
        producer = self.device_manager.producer

        pipe = producer.pipeline()
        producer.lrange(MessageEndpoints.device_req_status(self.metadata["RID"]), 0, -1, pipe)
        producer.get(MessageEndpoints.device_readback(flyer), pipe)
        return pipe.execute()

    def scan_core(self):
        yield from self.stubs.kickoff(
            device=self.scan_motors[0],
            parameter=self.caller_kwargs,
        )
        yield from self.stubs.complete(
            device=self.scan_motors[0]
        )
        target_diid = self.DIID-1
        while True:
            status = self.stubs.get_req_status(device=self.scan_motors[0], RID=self.metadata["RID"], DIID=target_diid)
            progress = self.stubs.get_device_progress(device=self.scan_motors[0], RID=self.metadata["RID"])
            if progress:
                self.num_pos = progress
            if status:
                break                
            time.sleep(1)

