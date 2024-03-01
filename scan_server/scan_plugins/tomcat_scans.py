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

    def pre_scan(self):
        st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.scanStart)
        st.wait()
        yield from self.stubs.pre_scan()

    def scan_core(self):
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
        yield from self.stubs.kickoff(device='es1_roty', parameter={'target': self.scanEnd},)
        #yield from self.stubs.set(device='es1_roty', value=self.scanEnd, wait_group="flyer")
        target_diid = self.DIID - 1
        
        # Wait for motion to finish
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



class AeroSequenceScan(FlyScanBase):
    scan_name = "aero_sequence_scan"
    scan_report_hint = "table"
    required_kwargs = ["startpos", "ranges"]
    arg_input = {}
    arg_bundle_size = {"bundle": len(arg_input), "min": None, "max": None}

    def __init__(self, *args, parameter: dict = None, **kwargs):
        """ Performs a sequence scan with PSO output and data collection

        Examples:
            >>> scans.aero_sequence_scan(startpos=42, ranges=([179.9, 0.1, 5]), expnum=3600, repnum=3, repmode="PosNeg")

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = ['es1_roty']


        self.scanStart   = self.caller_kwargs.get("startpos")
        self.scanRanges   = self.caller_kwargs.get("ranges")
        self.scanExpNum   = self.caller_kwargs.get("expnum", 25000)
        self.scanRepNum     = self.caller_kwargs.get("repnum", 1)
        self.scanRepMode     = self.caller_kwargs.get("repmode", "Pos")
        self.scanVel = self.caller_kwargs.get("velocity", 30)
        self.scanTra = self.caller_kwargs.get("travel", 80)
        self.scanAcc = self.caller_kwargs.get("acceleration", 500)
        self.scanSafeDist = self.caller_kwargs.get("safedist", 10)


        self.num_pos = self.scanRepNum
        if isinstance(self.scanRanges[0], (int, float)):
            self.scanRanges = (self.scanRanges)

    def pre_scan(self):
        # Calculate PSO positions from tables
        AccDist = 0.5 * self.scanVel * self.scanVel / self.scanAcc + self.scanSafeDist

        # Relative PSO bounds
        self.psoBoundsPos = [AccDist]
        try:
            for line in self.scanRanges:
                print(f"Line is: {line} of type {type(line)}")
                for rr in range(int(line[2])):
                    self.psoBoundsPos.append(line[0])
                    self.psoBoundsPos.append(line[1])
        except TypeError:
            line = self.scanRanges
            print(f"Line is: {line} of type {type(line)}")
            for rr in range(int(line[2])):
                self.psoBoundsPos.append(line[0])
                self.psoBoundsPos.append(line[1])
        del self.psoBoundsPos[-1]

        self.psoBoundsNeg = [AccDist]
        self.psoBoundsNeg.extend(self.psoBoundsPos[::-1])

        scanrange = 2*AccDist + np.sum(self.psoBoundsPos)
        if self.scanRepMode in ["PosNeg", "Pos"]:
            self.PosStart = self.scanStart - AccDist
            self.PosEnd = self.scanStart + scanrange
        elif self.scanRepMode in ["NegPos", "Neg"]:
            self.PosStart = self.scanStart + AccDist
            self.PosEnd = self.scanStart - scanrange
        else:
            raise RuntimeError(f"Unexpected sequence repetition mode: {self.scanRepMode}")
        print(f"\tCalculated scan range: {self.PosStart} to {self.PosEnd} range {scanrange}")        

        # ToDo: We could append all distances and write a much longer 'distance array'. this would elliminate the need of rearming...

        # Move roughly to start position 
        yield from self.stubs.send_rpc_and_wait("es1_roty", "configure", {'velocity': self.scanTra, "acceleration":self.scanTra/self.scanAcc})
        st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
        st.wait()

        yield from self.stubs.pre_scan()

    def scan_core(self):
        # Move to start position (with travel velocity)
        yield from self.stubs.send_rpc_and_wait("es1_roty", "configure", {'velocity': self.scanTra, "acceleration":self.scanTra/self.scanAcc})
        yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)

        # Condigure PSO, DDC and motor
        yield from self.stubs.send_rpc_and_wait("es1_psod", "configure", {'distance': self.psoBoundsPos, "wmode": "toggle"})
        yield from self.stubs.send_rpc_and_wait("es1_ddaq", "configure", {'npoints': self.scanExpNum})
        yield from self.stubs.send_rpc_and_wait("es1_roty", "configure", {'velocity': self.scanVel, "acceleration": self.scanVel/self.scanAcc})
        
        # Kickoff
        st = yield from self.stubs.send_rpc_and_wait("es1_psod", "kickoff")
        st.wait()
        st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "kickoff")
        st.wait()


        print("Starting actual scan loop")
        for ii in range(self.scanRepNum):
            print(f"Scan segment {ii}")
            # No option to reset the index counter...
            yield from self.stubs.send_rpc_and_wait("es1_psod", "dstArrayRearm.set", 1)
            #st = yield from self.stubs.set("es1_psod", "dstArrayRearm", 1)
            #st.wait()

            if self.scanRepMode in ["Pos", "Neg"]:
                yield from self.stubs.kickoff(device='es1_roty', parameter={'target': self.PosEnd},)
                yield from self.stubs.wait(device=['es1_roty'], wait_group="kickoff", wait_type="move")
                yield from self.stubs.complete(device='es1_roty')
                yield from self.stubs.kickoff(device='es1_roty', parameter={'target': self.PosStart},)
                yield from self.stubs.wait(device=['es1_roty'], wait_group="kickoff", wait_type="move")
                yield from self.stubs.complete(device='es1_roty')

                #st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosEnd)
                #st.wait()
                #st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
                #st.wait()

            if self.scanRepMode in ["PosNeg", "NegPos"]:
                if ii % 2 == 0:
                    yield from self.stubs.kickoff(device='es1_roty', parameter={'target': self.PosEnd},)
                    yield from self.stubs.wait(device=['es1_roty'], wait_group="kickoff", wait_type="move")
                    yield from self.stubs.complete(device='es1_roty')
                    #st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosEnd)
                    #st.wait()
                else:   
                    yield from self.stubs.kickoff(device='es1_roty', parameter={'target': self.PosStart},)
                    yield from self.stubs.wait(device=['es1_roty'], wait_group="kickoff", wait_type="move")
                    yield from self.stubs.complete(device='es1_roty')
                    #st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
                    #st.wait()
            self.pointID += 1
            self.num_pos += 1
            time.sleep(0.2)

        # Complete (should complete instantly)
        yield from self.stubs.complete(device='es1_psod')
        yield from self.stubs.complete(device='es1_ddaq')
        st = yield from self.stubs.send_rpc_and_wait("es1_psod", "complete")
        st.wait()
        st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "complete")
        st.wait()

        # Collect
        #st = yield from self.stubs.send_rpc_and_wait("es1_psod", "collect")
        #st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "collect")

        yield from self.stubs.read_and_wait(group="primary", wait_group="readout_primary")
        target_diid = self.DIID - 1
        
        # Wait for motion to finish
        while True:
            pso_status = self.stubs.get_req_status(device='es1_psod', RID=self.metadata["RID"], DIID=target_diid)
            daq_status = self.stubs.get_req_status(device='es1_ddaq', RID=self.metadata["RID"], DIID=target_diid)
            mot_status = self.stubs.get_req_status(device='es1_roty', RID=self.metadata["RID"], DIID=target_diid)
            progress = self.stubs.get_device_progress(device='es1_psod', RID=self.metadata["RID"])
            progress = self.stubs.get_device_progress(device='es1_ddaq', RID=self.metadata["RID"])
            progress = self.stubs.get_device_progress(device='es1_roty', RID=self.metadata["RID"])
            print(f"pso: {pso_status}\tdaq: {daq_status}\tmot: {mot_status}\tprogress: {progress}")
            if progress:
                self.num_pos = progress
            #if mot_status:
            #    break
            time.sleep(1)
            break

        print("Scan done\n\n")

    def cleanup(self):
        ret = super().cleanup()
        class CloseScanError(Exception):
            pass
        raise CloseScanError("Close the fucking scan!")

