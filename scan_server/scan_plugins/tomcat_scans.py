import time

import numpy as np

from bec_lib import bec_logger
from scan_server.scans import FlyScanBase, ScanArgType, ScanBase

logger = bec_logger.logger



class AeroSingleScan(FlyScanBase):
    scan_name = "aero_single_scan"
    scan_report_hint = "table"
    required_kwargs = ["startpos", "scanrange", "psodist"]
    arg_input = {}
    arg_bundle_size = {"bundle": len(arg_input), "min": None, "max": None}

    def __init__(self, *args, parameter: dict = None, **kwargs):
        """ Performs a single line scan with PSO output and data collection

        Examples:
            >>> scans.aero_single_scan(startpos=42, scanrange=2*10+3*180, psodist=[10, 180, 0.01, 180, 0.01, 180])

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = []
        self.num_pos = 0

        self.scanStart   = self.caller_kwargs.get("startpos")
        self.scanEnd     = self.scanStart + self.caller_kwargs.get("scanrange")
        self.scanPsoDist = self.caller_kwargs.get("psodist")
        #self.scanDaqPts  = self.caller_kwargs.get("daqpoints")

    def scan_report_instructions(self):
        """Scan report instructions for the progress bar, yields from mcs card"""
        if not self.scan_report_hint:
            yield None
            return
        yield from self.stubs.scan_report_instruction({"scan_progress": ["es1_roty1"]})

    def pre_scan(self):
        st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.scanStart)
        st.wait()
        yield from self.stubs.pre_scan()

    def scan_core(self):
        #yield from self.stubs.rpc(, parameter={}|self, *, device: str, parameter: dict, metadata=None):
        # Refresh the PSO distance array        
        st = yield from self.stubs.send_rpc_and_wait('es1_psod', 'dstDistanceArr.set', self.scanPsoDist)
        st.wait()

        # Kick off PSO and DDC
        st = yield from self.stubs.send_rpc_and_wait('es1_psod', 'kickoff')
        st.wait()
        st = yield from self.stubs.send_rpc_and_wait('es1_ddaq', 'kickoff')
        st.wait()

        print("Start moving")
        # Start the actual movement
        #yield from self.stubs.set_and_wait(device=["es1_roty"], positions=[self.scanEnd])
        yield from self.stubs.set(device="es1_roty", value=self.scanEnd, wait_group="flyer")
        target_diid = self.DIID - 1

        # Wait for motion to finish
        #yield from self.stubs.wait(device="es1_roty", wait_group="flyer", wait_type="move")
        while True:
            yield from self.stubs.read_and_wait(group="primary", wait_group="readout_primary")
            status = self.stubs.get_req_status(device='es1_roty', RID=self.metadata["RID"], DIID=target_diid)
            progress = self.stubs.get_device_progress(device='es1_roty', RID=self.metadata["RID"])
            print(f"status: {status}\tprogress: {progress}")
            if progress:
                self.num_pos = progress
            if status:
                break
            time.sleep(1)
        print("Scan done\n\n")

