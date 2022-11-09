from .config import TestConfig


class LamNIConfig(TestConfig):
    def run(self):
        self.write_galil_motors()
        self.write_rt_motors()
        self.write_smaract_motors()
        super().run()

    def write_galil_motors(self):
        lamni_galil_motors = [
            ("lsamx", "A", -1, 0.5),
            ("lsamy", "B", 1, 0.5),
            ("lsamrot", "C", 1, 0.5),
            # ("loptz", "D", -1, 0.5),
            # ("loptx", "E", 1, 0.5),
            # ("lopty", "F", 1, 0.5),
            ("leyex", "G", -1, 0.001),
            ("leyey", "H", -1, 0.001),
        ]
        out = dict()
        for m in lamni_galil_motors:
            out[m[0]] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "GalilMotor",
                    "deviceConfig": {
                        "axis_Id": m[1],
                        "name": m[0],
                        "labels": m[0],
                        "host": "mpc2680.psi.ch",
                        "port": 8081,
                        "sign": m[2],
                        "limits": [0, 0],
                        "tolerance": m[3],
                        "device_access": True,
                        "device_mapping": {"rt": "rtx"},
                    },
                    "acquisitionConfig": {"schedule": "sync", "acquisitionGroup": "userMotor"},
                    "deviceGroup": "lamni",
                }
            )
        self.write_section(out, "LamNI Galil motors")

    def write_rt_motors(self):
        lamni_rt_motors = [
            ("rtx", "A", 1),
            ("rty", "B", 1),
        ]
        out = dict()
        for m in lamni_rt_motors:
            out[m[0]] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "RtLamniMotor",
                    "deviceConfig": {
                        "axis_Id": m[1],
                        "name": m[0],
                        "labels": m[0],
                        "host": "mpc2680.psi.ch",
                        "port": 3333,
                        "limits": [0, 0],
                        "sign": m[2],
                        "device_access": True,
                    },
                    "acquisitionConfig": {"schedule": "sync", "acquisitionGroup": "userMotor"},
                    "deviceGroup": "lamni",
                }
            )
        self.write_section(out, "LamNI RT")

    def write_smaract_motors(self):
        lamni_smaract_motors = [
            ("losax", "A", -1),
            ("losay", "B", -1),
            ("losaz", "C", 1),
            ("lcsx", "D", -1),
            ("lcsy", "E", -1),
        ]
        out = dict()
        for m in lamni_smaract_motors:
            out[m[0]] = dict(
                {
                    "status": {"enabled": True, "enabled_set": True},
                    "deviceClass": "SmaractMotor",
                    "deviceConfig": {
                        "axis_Id": m[1],
                        "name": m[0],
                        "labels": m[0],
                        "host": "mpc2680.psi.ch",
                        "port": 8085,
                        "limits": [0, 0],
                        "sign": m[2],
                        "tolerance": 0.05,
                    },
                    "acquisitionConfig": {"schedule": "sync", "acquisitionGroup": "userMotor"},
                    "deviceGroup": "lamni",
                }
            )
        self.write_section(out, "LamNI SmarAct motors")
