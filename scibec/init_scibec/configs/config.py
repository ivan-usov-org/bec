import abc
import os

import yaml


class ConfigBase(abc.ABC):
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        try:
            os.remove(self.config_path)
        except OSError:
            pass

    @abc.abstractmethod
    def run(self):
        pass

    def write_sep(self, sep_text, width=60, sep_type="header") -> str:
        sep_text = " " + sep_text + " "
        sep_len = len(sep_text)
        padding = [(width - sep_len) // 2, (width - sep_len) - (width - sep_len) // 2]

        if sep_type == "header":
            out = (
                "\n\n"
                + "".join("#" * width)
                + "\n"
                + "".join("#" * padding[0])
                + sep_text
                + "".join("#" * padding[1])
                + "\n"
                + "".join("#" * width)
                + "\n\n"
            )
        else:
            out = "\n\n" + "".join("#" * padding[0]) + sep_text + "".join("#" * padding[1]) + "\n\n"
        return out

    def write_section(self, out: dict, description: str) -> None:
        with open(self.config_path, "a") as f:
            f.write(self.write_sep(description))
            f.write(yaml.dump(out))
            f.write(self.write_sep(f"{description} end here", sep_type="footer"))


class DemoConfig(ConfigBase):
    def run(self):
        self.write_sim_detectors()
        self.write_sim_user_motors()
        self.write_sim_beamline_monitors()
        self.write_sim_beamline_motors()
        self.write_sim_read_only_signals()

    def write_sim_detectors(self):
        detectors = ["eiger"]
        out = {}
        for m in detectors:
            out[m] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "SynSLSDetector",
                    "deviceConfig": {
                        "name": m,
                        "labels": m,
                        "device_access": True,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "detector",
                        "readoutPriority": "primary",
                    },
                    "deviceTags": ["detector"],
                }
            )

        self.write_section(out, "Cameras and detectors")

    def write_sim_user_motors(self):
        user_motors = [
            "samx",
            "samy",
            "samz",
            "pinx",
            "piny",
            "pinz",
            "mbsx",
            "mbsy",
            "hx",
            "hy",
            "hz",
            "hrox",
            "hroy",
            "hroz",
            "eyex",
            "eyey",
            "eyefoc",
        ]

        out = {}
        for m in user_motors:
            out[m] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "SynAxisOPAAS",
                    "deviceConfig": {
                        "name": m,
                        "labels": m,
                        "delay": 1,
                        "speed": 100,
                        "update_frequency": 400,
                        "limits": [-50, 50],
                        "tolerance": 0.01,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "motor",
                        "readoutPriority": "secondary",
                    },
                    "deviceTags": ["user motors"],
                }
            )

        out["flyer_sim"] = dict(
            {
                "status": {"enabled": True, "enabled_set": True},
                "deviceClass": "SynFlyer",
                "deviceConfig": {
                    "name": "flyer_sim",
                    "labels": "flyer_sim",
                    "delay": 1,
                    "speed": 100,
                    "update_frequency": 400,
                    "device_access": True,
                },
                "acquisitionConfig": {
                    "schedule": "flyer",
                    "acquisitionGroup": "motor",
                    "readoutPriority": "secondary",
                },
                "deviceTags": ["flyer"],
            }
        )
        self.write_section(out, "User motors")

    def write_sim_beamline_monitors(self):
        beamline_monitor = [
            "temp",
            "ebpmux",
            "ebpmuy",
            "ebpmdx",
            "ebpmdy",
            "bpm3i",
            "bpm3x",
            "bpm3y",
            "bpm3z",
            "bpm4i",
            "bpm4x",
            "bpm4y",
            "bpm4z",
            "bpm4s",
            "bpm5i",
            "bpm5x",
            "bpm5y",
            "bpm5z",
            "bpm6i",
            "bpm6x",
            "bpm6y",
            "bpm6z",
            "transd",
            "bpm3a",
            "bpm3b",
            "bpm3c",
            "bpm3d",
            "bpm4a",
            "bpm4b",
            "bpm4c",
            "bpm4d",
            "bpm5a",
            "bpm5b",
            "bpm5c",
            "bpm5d",
            "bpm6a",
            "bpm6b",
            "bpm6c",
            "bpm6d",
            "ftp",
            "bpm4xf",
            "bpm4xm",
            "bpm4yf",
            "bpm4ym",
            "curr",
            "diode",
        ]

        out = {}
        for m in beamline_monitor:
            out[m] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "SynAxisMonitor",
                    "deviceConfig": {"name": m, "labels": m, "tolerance": 0.5},
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "monitor",
                        "readoutPriority": "primary",
                    },
                    "deviceTags": ["beamline"],
                }
            )
        self.write_section(out, "Beamline monitors")

    def write_sim_beamline_motors(self):
        beamline_motors = [
            "idgap",
            "bm1trx",
            "bm1try",
            "bm2trx",
            "bm2try",
            "di2trx",
            "di2try",
            "sl0trxo",
            "sl0trxi",
            "sl0ch",
            "sl0wh",
            "bm3trx",
            "bm3try",
            "sl1trxo",
            "sl1trxi",
            "sl1tryt",
            "sl1tryb",
            "sl1ch",
            "sl1cv",
            "sl1wh",
            "sl1wv",
            "fi1try",
            "fi2try",
            "fi3try",
            "motry",
            "motrz1",
            "motrz1e",
            "mopush1",
            "moth1",
            "moth1e",
            "moroll1",
            "motrx2",
            "motry2",
            "mopush2",
            "moth2",
            "moth2e",
            "mokev",
            "moyaw2",
            "moroll2",
            "mobdai",
            "mobdbo",
            "mobdco",
            "mobddi",
            "mobd",
            "bm4trx",
            "bm4try",
            "bpm4r",
            "mitrx",
            "mitry1",
            "mitry2",
            "mitry3",
            "mitry",
            "mith",
            "miroll",
            "mibd1",
            "mibd2",
            "mibd",
            "bm5trx",
            "bm5try",
            "bpm5r",
            "sl2trxo",
            "sl2trxi",
            "sl2tryt",
            "sl2tryb",
            "sl2ch",
            "sl2cv",
            "sl2wh",
            "sl2wv",
            "bm6trx",
            "bm6try",
            "sl3trxi",
            "sl3trxo",
            "sl3tryb",
            "sl3tryt",
            "sl3ch",
            "sl3cv",
            "sl3wh",
            "sl3wv",
            "ebfi1",
            "ebfi2",
            "ebfi3",
            "ebfi4",
            "ftrans",
            "fsh1x",
            "sl4trxi",
            "sl4trxo",
            "sl4tryb",
            "sl4tryt",
            "sl4ch",
            "sl4cv",
            "sl4wh",
            "sl4wv",
            "aptrx",
            "aptry",
            "ebtrx",
            "ebtry",
            "ebtrz",
            "fsh2x",
            "sl5trxi",
            "sl5trxo",
            "sl5tryb",
            "sl5tryt",
            "sl5ch",
            "sl5cv",
            "sl5wh",
            "sl5wv",
            "sttrx",
            "sttry",
            "strox",
            "stroy",
            "stroz",
            "fttrx1",
            "fttry1",
            "fttrz",
            "fttrx2",
            "fttry2",
            "bs1x",
            "bs1y",
            "bs2x",
            "bs2y",
            "dttrx",
            "dttry",
            "dttrz",
            "dtpush",
            "dtth",
            "dettrx",
            "burstn",
            "burstr",
            "ddg1a",
            "ddg1b",
            "ddg1c",
            "ddg1d",
            "ddg1e",
            "ddg1f",
            "ddg1g",
            "ddg1h",
            "ebcsx",
            "ebcsy",
            "ebfzpx",
            "ebfzpy",
            "bim2x",
            "bim2y",
        ]

        out = {}
        for m in beamline_motors:
            out[m] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "SynAxisOPAAS",
                    "deviceConfig": {
                        "name": m,
                        "labels": m,
                        "delay": 1,
                        "speed": 100,
                        "update_frequency": 400,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "motor",
                        "readoutPriority": "secondary",
                    },
                    "deviceTags": ["beamline"],
                }
            )
        self.write_section(out, "Beamline motors")

    def write_sim_read_only_signals(self):
        read_only_signals = ["ring_current_sim"]

        out = dict()
        for m in read_only_signals:
            out[m] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "SynSignalRO",
                    "deviceConfig": {
                        "name": m,
                        "labels": m,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "monitor",
                        "readoutPriority": "primary",
                    },
                    "deviceTags": ["beamline"],
                }
            )

        self.write_section(out, "Read-only signals")


class TestConfig(DemoConfig):
    def run(self):
        super().run()
        self.write_disabled_devices()

    def write_disabled_devices(self):

        out = {}
        for m in ["motor1_disabled", "motor2_disabled"]:
            out[m] = dict(
                {
                    "status": {"enabled": False, "enabled_set": True},
                    "deviceClass": "SynAxisOPAAS",
                    "deviceConfig": {
                        "name": m,
                        "labels": m,
                        "delay": 1,
                        "speed": 100,
                        "update_frequency": 400,
                        "limits": [-50, 50],
                        "tolerance": 0.01,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "motor",
                        "readoutPriority": "secondary",
                    },
                    "deviceTags": ["user motors"],
                }
            )
        for m in ["motor1_disabled_set", "motor2_disabled_set"]:
            out[m] = dict(
                {
                    "status": {"enabled": True, "enabled_set": False},
                    "deviceClass": "SynAxisOPAAS",
                    "deviceConfig": {
                        "name": m,
                        "labels": m,
                        "delay": 1,
                        "speed": 100,
                        "update_frequency": 400,
                        "limits": [-50, 50],
                        "tolerance": 0.01,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "motor",
                        "readoutPriority": "secondary",
                    },
                    "deviceTags": ["user motors"],
                }
            )
        self.write_section(out, "Disabled devices")


class X12SAConfig(ConfigBase):
    def run(self):
        super().run()
        self.write_x12sa_status()
        self.write_sls_status()

    def write_x12sa_status(self):
        x12sa_status = [
            ("x12sa_op_status", "ACOAU-ACCU:OP-X12SA"),
            ("x12sa_es1_shutter_status", "X12SA-OP-ST1:OPEN_EPS"),
            ("x12sa_fe_status", "X12SA-FE-PH1:CLOSE4BL"),
            # ("x12sa_temp_median", "X12SA-OP-CC:HEAT_TEMP_MED"),
            # ("x12sa_temp_current", "X12SA-OP-CC:HEAT_TEMP"),
            ("x12sa_storage_ring_vac", "X12SA-SR-VAC:SETPOINT"),
            ("x12sa_es1_valve", "X12SA-ES-VW1:OPEN"),
            ("x12sa_exposure_box1_pressure", "X12SA-ES-CH1MF1:PRESSURE"),
            ("x12sa_exposure_box2_pressure", "X12SA-ES-EB1MF1:PRESSURE"),
            ("x12sa_id_gap", "X12SA-ID-GAP:READ"),
        ]

        out = {}
        for name, pv in x12sa_status:
            out[name] = dict(
                {
                    "status": {"enabled": True, "enabled_set": False},
                    "deviceClass": "EpicsSignalRO",
                    "deviceConfig": {"read_pv": pv, "name": name, "auto_monitor": True},
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "status",
                        "readoutPriority": "skip",
                    },
                    "deviceTags": ["X12SA status"],
                }
            )
        self.write_section(out, "X12SA status PVs")

    def write_sls_status(self):
        sls_status = [
            ("sls_injection_mode", "ALIRF-GUN:INJ-MODE", True),
            ("sls_current_threshold", "ALIRF-GUN:CUR-LOWLIM", False),
            ("sls_current_deadband", "ALIRF-GUN:CUR-DBAND", False),
            ("sls_filling_pattern", "ACORF-FILL:PAT-SELECT", True),
            ("sls_filling_life_time", "ARIDI-PCT:TAU-HOUR", False),
            ("sls_orbit_feedback_mode", "ARIDI-BPM:OFB-MODE", True),
            ("sls_fast_orbit_feedback", "ARIDI-BPM:FOFBSTATUS-G", True),
            ("sls_ring_current", "ARIDI-PCT:CURRENT", False),
            ("sls_machine_status", "ACOAU-ACCU:OP-MODE", True),
            ("sls_crane_usage", "IBWKR-0101-QH10003:D01_H_D-WA", True),
        ]
        out = {}
        for name, pv, is_string in sls_status:
            out[name] = dict(
                {
                    "status": {"enabled": True, "enabled_set": False},
                    "deviceClass": "EpicsSignalRO",
                    "deviceConfig": {
                        "read_pv": pv,
                        "name": name,
                        "auto_monitor": True,
                        "string": is_string,
                    },
                    "acquisitionConfig": {
                        "schedule": "sync",
                        "acquisitionGroup": "monitor",
                        "readoutPriority": "secondary",
                    },
                    "onFailure": "buffer",
                    "deviceTags": ["SLS status"],
                }
            )
        self.write_section(out, "SLS status PVs")
        out["sls_operator"] = dict(
            {
                "status": {"enabled": True, "enabled_set": False},
                "deviceClass": "SLSOperatorMessages",
                "deviceConfig": {"name": "sls_operator"},
                "acquisitionConfig": {
                    "schedule": "sync",
                    "acquisitionGroup": "status",
                    "readoutPriority": "skip",
                },
                "onFailure": "buffer",
                "deviceTags": ["SLS status"],
            }
        )
        self.write_section(out, "SLS status PVs")
