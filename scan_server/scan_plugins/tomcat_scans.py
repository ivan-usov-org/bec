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
        """Performs a single line scan with PSO output and data collection.

        Examples:
            >>> scans.aero_single_scan(startpos=42, scanrange=2*10+3*180, psodist=[10, 180, 0.01, 180, 0.01, 180])

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = []
        self.num_pos = 0

        self.scanStart = self.caller_kwargs.get("startpos")
        self.scanEnd = self.scanStart + self.caller_kwargs.get("scanrange")
        self.psoBounds = self.caller_kwargs.get("psodist")
        # self.scanDaqPts  = self.caller_kwargs.get("daqpoints")

    def pre_scan(self):
        # Move to start position
        st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.scanStart)
        st.wait()
        yield from self.stubs.pre_scan()

    def scan_core(self):
        # Configure PSO, DDC and motor
        yield from self.stubs.send_rpc_and_wait(
            "es1_roty",
            "configure",
            {"velocity": self.scanTra, "acceleration": self.scanTra / self.scanAcc},
        )
        yield from self.stubs.send_rpc_and_wait(
            "es1_psod", "configure", {"distance": self.psoBounds, "wmode": "toggle"}
        )
        yield from self.stubs.send_rpc_and_wait(
            "es1_ddaq",
            "configure",
            {"npoints": self.scanExpNum},
        )
        # DAQ with real trigger
        # yield from self.stubs.send_rpc_and_wait(
        #    "es1_ddaq", "configure", {"npoints": self.scanExpNum, "trigger": "HSINP0_RISE"},
        # )

        # Kick off PSO and DDC
        st = yield from self.stubs.send_rpc_and_wait("es1_psod", "kickoff")
        st.wait()
        st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "kickoff")
        st.wait()

        print("Start moving")
        # Start the actual movement
        yield from self.stubs.kickoff(
            device="es1_roty",
            parameter={"target": self.scanEnd},
        )
        # yield from self.stubs.set(device='es1_roty', value=self.scanEnd, wait_group="flyer")
        target_diid = self.DIID - 1

        # Wait for motion to finish
        while True:
            yield from self.stubs.read_and_wait(group="primary", wait_group="readout_primary")
            status = self.stubs.get_req_status(
                device="es1_roty", RID=self.metadata["RID"], DIID=target_diid
            )
            progress = self.stubs.get_device_progress(device="es1_roty", RID=self.metadata["RID"])
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
        """Performs a sequence scan with PSO output and data collection

        Examples:
            >>> scans.aero_sequence_scan(startpos=42, ranges=([179.9, 0.1, 5]), expnum=3600, repnum=3, repmode="PosNeg")

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = ["es1_roty"]
        self.num_pos = 0

        self.scanStart = self.caller_kwargs.get("startpos")
        self.scanRanges = self.caller_kwargs.get("ranges")
        self.scanExpNum = self.caller_kwargs.get("expnum", 25000)
        self.scanRepNum = self.caller_kwargs.get("repnum", 1)
        self.scanRepMode = self.caller_kwargs.get("repmode", "Pos")
        self.scanVel = self.caller_kwargs.get("velocity", 30)
        self.scanTra = self.caller_kwargs.get("travel", 80)
        self.scanAcc = self.caller_kwargs.get("acceleration", 500)
        self.scanSafeDist = self.caller_kwargs.get("safedist", 10)

        if isinstance(self.scanRanges[0], (int, float)):
            self.scanRanges = self.scanRanges

        if self.scanRepMode not in ["PosNeg", "Pos", "NegPos", "Neg"]:
            raise RuntimeError(f"Unexpected sequence repetition mode: {self.scanRepMode}")

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

        scanrange = 2 * AccDist + np.sum(self.psoBoundsPos)
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
        yield from self.stubs.send_rpc_and_wait(
            "es1_roty",
            "configure",
            {"velocity": self.scanTra, "acceleration": self.scanTra / self.scanAcc},
        )
        st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
        st.wait()

        yield from self.stubs.pre_scan()

    def scan_core(self):
        # Move to start position (with travel velocity)
        yield from self.stubs.send_rpc_and_wait(
            "es1_roty",
            "configure",
            {"velocity": self.scanTra, "acceleration": self.scanTra / self.scanAcc},
        )
        yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)

        # Condigure PSO, DDC and motorHSINP0_RISE
        yield from self.stubs.send_rpc_and_wait(
            "es1_psod", "configure", {"distance": self.psoBoundsPos, "wmode": "toggle"}
        )
        yield from self.stubs.send_rpc_and_wait(
            "es1_ddaq",
            "configure",
            {"npoints": self.scanExpNum},
        )
        # With real trigger
        # yield from self.stubs.send_rpc_and_wait(
        #    "es1_ddaq", "configure", {"npoints": self.scanExpNum, "trigger": "HSINP0_RISE"}
        # )
        yield from self.stubs.send_rpc_and_wait(
            "es1_roty",
            "configure",
            {"velocity": self.scanVel, "acceleration": self.scanVel / self.scanAcc},
        )

        # Kickoff pso and daq
        st = yield from self.stubs.send_rpc_and_wait("es1_psod", "kickoff")
        st.wait()
        st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "kickoff")
        st.wait()

        # Run the actual scan (haven't figured out the proggress bar)
        print("Starting actual scan loop")
        for ii in range(self.scanRepNum):
            print(f"Scan segment {ii}")
            # No option to reset the index counter...
            yield from self.stubs.send_rpc_and_wait("es1_psod", "dstArrayRearm.set", 1)

            if self.scanRepMode in ["Pos", "Neg"]:
                yield from self.stubs.send_rpc_and_wait(
                    "es1_roty",
                    "configure",
                    {"velocity": self.scanVel, "acceleration": self.scanVel / self.scanAcc},
                )
                st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosEnd)
                st.wait()
                yield from self.stubs.send_rpc_and_wait(
                    "es1_roty",
                    "configure",
                    {"velocity": self.scanTra, "acceleration": self.scanTra / self.scanAcc},
                )
                st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
                st.wait()
            elif self.scanRepMode in ["PosNeg", "NegPos"]:
                if ii % 2 == 0:
                    st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosEnd)
                    st.wait()
                else:
                    st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
                    st.wait()
            self.pointID += 1
            self.num_pos += 1
            time.sleep(0.2)

        # Complete (should complete instantly)
        yield from self.stubs.complete(device="es1_psod")
        yield from self.stubs.complete(device="es1_ddaq")
        st = yield from self.stubs.send_rpc_and_wait("es1_psod", "complete")
        st.wait()
        st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "complete")
        st.wait()

        # Collect -  Throws a warning due to returning a generator
        # st = yield from self.stubs.send_rpc_and_wait("es1_psod", "collect")
        # st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "collect")

        yield from self.stubs.read_and_wait(group="primary", wait_group="readout_primary")
        target_diid = self.DIID - 1

        yield from self.stubs.kickoff(
            device="es1_roty",
            parameter={"target": self.PosStart},
        )
        yield from self.stubs.wait(device=["es1_roty"], wait_group="kickoff", wait_type="move")
        yield from self.stubs.complete(device="es1_roty")

        # Wait for motion to finish
        while True:
            pso_status = self.stubs.get_req_status(
                device="es1_psod", RID=self.metadata["RID"], DIID=target_diid
            )
            daq_status = self.stubs.get_req_status(
                device="es1_ddaq", RID=self.metadata["RID"], DIID=target_diid
            )
            mot_status = self.stubs.get_req_status(
                device="es1_roty", RID=self.metadata["RID"], DIID=target_diid
            )
            progress = self.stubs.get_device_progress(device="es1_psod", RID=self.metadata["RID"])
            progress = self.stubs.get_device_progress(device="es1_ddaq", RID=self.metadata["RID"])
            progress = self.stubs.get_device_progress(device="es1_roty", RID=self.metadata["RID"])
            print(f"pso: {pso_status}\tdaq: {daq_status}\tmot: {mot_status}\tprogress: {progress}")
            if progress:
                self.num_pos = int(progress)
            if mot_status:
                break
            time.sleep(1)
        print("Scan done\n\n")

    def cleanup(self):
        """Set scan progress to 1 to finish the scan"""
        self.num_pos = 1
        return super().cleanup()


class AeroScriptedScan(FlyScanBase):
    scan_name = "aero_scripted_scan"
    scan_report_hint = "table"
    required_kwargs = ["filename", "subs"]
    arg_input = {}
    arg_bundle_size = {"bundle": len(arg_input), "min": None, "max": None}

    def __init__(self, *args, parameter: dict = None, **kwargs):
        """Executes an AeroScript template as a flyer

        The script is generated from a template file using jinja2.
        Examples:
            >>> scans.aero_scripted_scan(filename="AerotechSnapAndStepTemplate.ascript", subs={'startpos': 42, 'stepsize': 0.1, 'numsteps': 1800, 'exptime': 0.1})

        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = ["es1_roty"]
        self.num_pos = 0

        self.filename = self.caller_kwargs.get("filename")
        self.subs = self.caller_kwargs.get("subs")
        self.taskIndex = self.caller_kwargs.get("taskindex", 4)

    def pre_scan(self):
        print("TOMCAT Loading Aeroscript template")
        # Load the test file
        with open(self.filename) as f:
            templatetext = f.read()

        # Substitute jinja template
        import jinja2

        tm = jinja2.Template(templatetext)
        self.scripttext = tm.render(scan=self.subs)

        yield from self.stubs.pre_scan()

    def scan_core(self):
        print("TOMCAT Sequeence scan (via Jinjad AeroScript)")
        t_start = time.time()

        # Configure by copying text to controller file and compiling it
        yield from self.stubs.send_rpc_and_wait(
            "es1_aa1Tasks",
            "configure",
            {"text": self.scripttext, "filename": "becExec.ascript", "taskIndex": self.taskIndex},
        )

        # Kickoff
        st = yield from self.stubs.send_rpc_and_wait("es1_aa1Tasks", "kickoff")
        st.wait()
        time.sleep(0.5)

        # Complete
        yield from self.stubs.complete(device="es1_aa1Tasks")

        # Collect - up to implementation

        t_end = time.time()
        t_elapsed = t_end - t_start
        print(f"Elapsed scan time: {t_elapsed}")

    def cleanup(self):
        """Set scan progress to 1 to finish the scan"""
        self.num_pos = 1
        return super().cleanup()


class AeroSnapNStep(AeroScriptedScan):
    scan_name = "aero_snapNstep"
    scan_report_hint = "table"
    required_kwargs = ["startpos", "expnum"]
    arg_input = {}
    arg_bundle_size = {"bundle": len(arg_input), "min": None, "max": None}

    def __init__(self, *args, parameter: dict = None, **kwargs):
        """Executes a scripted SnapNStep scan

        This scan generates and executes an AeroScript file to run
        a hardware step scan on the Aerotech controller.
        The script is generated from a template file using jinja2.

        Examples:
            >>> scans.scans.aero_snapNstep(startpos=42, range=180, expnum=1800, exptime=0.1)
        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = ["es1_roty"]
        self.num_pos = 0

        self.filename = "/afs/psi.ch/user/m/mohacsi_i/ophyd_devices/ophyd_devices/epics/devices/aerotech/AerotechSnapAndStepTemplate.ascript"
        self.scanTaskIndex = self.caller_kwargs.get("taskindex", 4)

        self.scanStart = self.caller_kwargs.get("startpos")
        self.scanExpNum = self.caller_kwargs.get("expnum")
        self.scanRange = self.caller_kwargs.get("range", 180)
        self.scanExpTime = self.caller_kwargs.get("exptime", 0.1)
        self.scanStepSize = self.scanRange / self.scanExpNum
        # self.scanVel = self.caller_kwargs.get("velocity", 30)
        # self.scanTra = self.caller_kwargs.get("travel", 80)
        # self.scanAcc = self.caller_kwargs.get("acceleration", 500)

        self.subs = {
            "startpos": self.scanStart,
            "stepsize": self.scanStepSize,
            "numsteps": self.scanExpNum,
            "exptime": self.scanExpTime,
        }

    def scan_core(self):
        print("TOMCAT Snap N Step scan (via Jinjad AeroScript)")
        # Run template execution frm parent
        yield from super().scan_core()

        # Collect -  Throws a warning due to returning a generator
        yield from self.stubs.send_rpc_and_wait("es1_ddaq", "npoints.put", self.scanExpNum)
        # st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "collect")
        # st.wait()


class AeroScriptedSequence(AeroScriptedScan):
    scan_name = "aero_scripted_sequence"
    scan_report_hint = "table"
    required_kwargs = ["startpos", "ranges"]
    arg_input = {}
    arg_bundle_size = {"bundle": len(arg_input), "min": None, "max": None}

    def __init__(self, *args, parameter: dict = None, **kwargs):
        """Executes a scripted sequence scan

        This scan generates and executes an AeroScript file to run a hardware sequence scan on the
        Aerotech controller. You might win a few seconds this way, but it has some limtations...
        The script is generated from a template file using jinja2.

        Examples:
            >>> scans.aero_scripted_sequence(startpos=42, ranges=([179.9, 0.1, 5]), expnum=3600, repnum=3, repmode="PosNeg")
        """
        super().__init__(parameter=parameter, **kwargs)
        self.axis = []
        self.scan_motors = ["es1_roty"]
        self.num_pos = 0

        self.filename = "/afs/psi.ch/user/m/mohacsi_i/ophyd_devices/ophyd_devices/epics/devices/aerotech/AerotechSimpleSequenceTemplate.ascript"
        self.scanTaskIndex = self.caller_kwargs.get("taskindex", 4)

        self.scanStart = self.caller_kwargs.get("startpos")
        self.scanRanges = self.caller_kwargs.get("ranges")
        self.scanExpNum = self.caller_kwargs.get("expnum", 25000)
        self.scanRepNum = self.caller_kwargs.get("repnum", 1)
        self.scanRepMode = self.caller_kwargs.get("repmode", "Pos")

        self.scanVel = self.caller_kwargs.get("velocity", 30)
        self.scanTra = self.caller_kwargs.get("travel", 80)
        self.scanAcc = self.caller_kwargs.get("acceleration", 500)
        self.scanSafeDist = self.caller_kwargs.get("safedist", 10)

        self.subs = {
            "startpos": self.scanStart,
            "scandir": self.scanRepMode,
            "nrepeat": self.scanRepNum,
            "npoints": self.scanExpNum,
            "scanvel": self.scanVel,
            "jogvel": self.scanTra,
            "scanacc": self.scanAcc,
        }

        if self.scanRepMode not in ["PosNeg", "Pos", "NegPos", "Neg"]:
            raise RuntimeError(f"Unexpected sequence repetition mode: {self.scanRepMode}")

        if isinstance(self.scanRanges[0], (int, float)):
            self.scanRanges = self.scanRanges

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

        self.scanrange = 2 * AccDist + np.sum(self.psoBoundsPos)
        if self.scanRepMode in ["PosNeg", "Pos"]:
            self.PosStart = self.scanStart - AccDist
        elif self.scanRepMode in ["NegPos", "Neg"]:
            self.PosStart = self.scanStart + AccDist
        else:
            raise RuntimeError(f"Unexpected sequence repetition mode: {self.scanRepMode}")
        print(f"\tCalculated scan range: {self.PosStart} range {self.scanrange}")

        # ToDo: We could append all distances and write a much longer 'distance array'. this would elliminate the need of rearming...
        self.subs.update(
            {
                "psoBoundsPos": self.psoBoundsPos,
                "psoBoundsNeg": self.psoBoundsNeg,
                "scanrange": self.scanrange,
            }
        )

        # Move roughly to start position
        yield from self.stubs.send_rpc_and_wait(
            "es1_roty",
            "configure",
            {"velocity": self.scanTra, "acceleration": self.scanTra / self.scanAcc},
        )
        st = yield from self.stubs.send_rpc_and_wait("es1_roty", "move", self.PosStart)
        st.wait()

        yield from super().pre_scan()

    def scan_core(self):
        print("TOMCAT Sequence scan (via Jinjad AeroScript)")
        # Run template execution frm parent
        yield from super().scan_core()

        # Collect -  Throws a warning due to returning a generator
        yield from self.stubs.send_rpc_and_wait("es1_ddaq", "npoints.put", self.scanExpNum)
        # st = yield from self.stubs.send_rpc_and_wait("es1_ddaq", "collect")
        # st.wait()
