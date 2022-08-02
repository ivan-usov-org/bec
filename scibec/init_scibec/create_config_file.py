import numpy as np
import yaml

USE_LAMNI = True


lamni_galil_motors = [
    ("lsamx", "A", -1),
    ("lsamy", "B", 1),
    ("lsamrot", "C", 1),
    # ("loptz", "D", -1),
    # ("loptx", "E", 1),
    # ("lopty", "F", 1),
    ("leyex", "G", -1),
    ("leyey", "H", -1),
]

lamni_rt_motors = [
    ("rtx", "A", 1),
    ("rty", "B", 1),
]

lamni_smaract_motors = [
    ("losax", "A", -1),
    ("losay", "B", -1),
    ("losaz", "C", 1),
    ("lcsx", "D", -1),
    ("lcsy", "E", -1),
]

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


def write_sep(sep_text, width=60, sep_type="header") -> str:
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


out = dict()
for m in user_motors:
    out[m] = dict(
        {
            "status": {"enabled": True},
            "type": "SynAxisOPAAS",
            "config": {
                "name": m,
                "labels": m,
                "delay": 1,
                "speed": 100,
                "update_frequency": 400,
                "limits": [-50, 50],
                "tolerance": 0.01,
            },
            "acquisition": {"schedule": "sync"},
            "deviceGroup": "userMotor",
        }
    )

out["flyer_sim"] = dict(
    {
        "status": {"enabled": True},
        "type": "SynFlyer",
        "config": {
            "name": "flyer_sim",
            "labels": "flyer_sim",
            "delay": 1,
            "speed": 100,
            "update_frequency": 400,
            "device_access": True,
        },
        "acquisition": {"schedule": "flyer"},
        "deviceGroup": "userMotor",
    }
)

with open("demo_config.yaml", "w+") as f:
    f.write(write_sep("User motors"))
    f.write(yaml.dump(out))
    f.write(write_sep("User motors end here", sep_type="footer"))

if USE_LAMNI:
    out = dict()
    for m in lamni_galil_motors:
        out[m[0]] = dict(
            {
                "status": {"enabled": True},
                "type": "GalilMotor",
                "config": {
                    "axis_Id": m[1],
                    "name": m[0],
                    "labels": m[0],
                    "host": "mpc2680.psi.ch",
                    "port": 8081,
                    "sign": m[2],
                    "limits": [0, 0],
                    "tolerance": 0.5,
                    "device_access": True,
                    "device_mapping": {"rt": "rtx"},
                },
                "acquisition": {"schedule": "sync"},
                "deviceGroup": "userMotor",
            }
        )
    for m in lamni_smaract_motors:
        out[m[0]] = dict(
            {
                "status": {"enabled": True},
                "type": "SmaractMotor",
                "config": {
                    "axis_Id": m[1],
                    "name": m[0],
                    "labels": m[0],
                    "host": "mpc2680.psi.ch",
                    "port": 8085,
                    "limits": [0, 0],
                    "sign": m[2],
                    "tolerance": 0.05,
                },
                "acquisition": {"schedule": "sync"},
                "deviceGroup": "userMotor",
            }
        )

    for m in lamni_rt_motors:
        out[m[0]] = dict(
            {
                "status": {"enabled": True},
                "type": "RtLamniMotor",
                "config": {
                    "axis_Id": m[1],
                    "name": m[0],
                    "labels": m[0],
                    "host": "mpc2680.psi.ch",
                    "port": 3333,
                    "limits": [0, 0],
                    "sign": m[2],
                    "device_access": True,
                },
                "acquisition": {"schedule": "sync"},
                "deviceGroup": "userMotor",
            }
        )

    with open("demo_config.yaml", "a") as f:
        f.write(write_sep("LamNI motors"))
        f.write(yaml.dump(out))
        f.write(write_sep("LamNI motors end here", sep_type="footer"))


# out = dict()
# for m in ["px", "py", "pz"]:
#     out[m] = dict(
#         {
#             "status": {"enabled": True},
#             "type": "NPointAxis",
#             "config": {"name": m, "labels": m, "settling_time": 0.1},
#             "acquisition": {"schedule": "sync"},
#             "deviceGroup": "userMotor",
#         }
#     )

# with open("demo_config.yaml", "a") as f:
#     f.write(write_sep("NPoint motors"))
#     f.write(yaml.dump(out))
#     f.write(write_sep("NPoint motors end here", sep_type="footer"))

out = dict()
for m in beamline_monitor:
    out[m] = dict(
        {
            "status": {"enabled": True},
            "type": "SynAxisMonitor",
            "config": {"name": m, "labels": m, "tolerance": 0.5},
            "acquisition": {"schedule": "sync"},
            "deviceGroup": "monitor",
        }
    )

with open("demo_config.yaml", "a") as f:
    f.write(write_sep("Beamline monitors"))
    f.write(yaml.dump(out))
    f.write(write_sep("Beamline monitors end here", sep_type="footer"))

out = dict()
for m in beamline_motors:
    out[m] = dict(
        {
            "status": {"enabled": True},
            "type": "SynAxisOPAAS",
            "config": {
                "name": m,
                "labels": m,
                "delay": 1,
                "speed": 100,
                "update_frequency": 400,
            },
            "acquisition": {"schedule": "sync"},
            "deviceGroup": "beamlineMotor",
        }
    )

with open("demo_config.yaml", "a") as f:
    f.write(write_sep("Beamline motors"))
    f.write(yaml.dump(out))
    f.write(write_sep("Beamline motors end here", sep_type="footer"))


sls_status = [
    ("ring_current", "ARIDI-PCT:CURRENT"),
    ("current_deadband", "ALIRF-GUN:CUR-DBAND"),
    ("orbit_feedback_mode", "ARIDI-BPM:OFB-MODE"),
    ("sls_filling_lifetime", "ARIDI-PCT:TAU-HOUR"),
    ("sls_filling_pattern", "ACORF-FILL:PAT-SELECT"),
    ("fast_orbit_feedback", "ARIDI-BPM:FOFBSTATUS-G"),
    ("sls_current_threshold", "ALIRF-GUN:CUR-LOWLIM"),
    ("sls_machine_status", "ACOAU-ACCU:OP-MODE"),
    ("sls_crane_usage", "IBWKR-0101-QH10003:D01_H_D-WA"),
    ("sls_injection_mode", "ALIRF-GUN:INJ-MODE"),
]

x12sa_status = [
    ("x12sa_op_status", "ACOAU-ACCU:OP-X12SA"),
    ("x12sa_es1_shutter_status", "X12SA-OP-ST1:OPEN_EPS"),
    ("x12sa_fe_status", "X12SA-FE-PH1:CLOSE4BL"),
    ("x12sa_temp_median", "X12SA-OP-CC:HEAT_TEMP_MED"),
    ("x12sa_temp_current", "X12SA-OP-CC:HEAT_TEMP"),
    ("sec_21_vibration", "XCOVI-AXIS21:PSDV1MAX"),
    ("x12sa_storage_ring_vac", "X12SA-SR-VAC:SETPOINT"),
    ("x12sa_es1_valve", "X12SA-ES-VW1:OPEN"),
    ("x12sa_exposure_box1_pressure", "X12SA-ES-CH1MF1:PRESSURE"),
    ("x12sa_exposure_box2_pressure", "X12SA-ES-EB1MF1:PRESSURE"),
    ("x12sa_id_gap", "X12SA-ID-GAP:READ"),
]

out = dict()
for name, pv in sls_status:
    out[name] = dict(
        {
            "status": {"enabled": True},
            "type": "EpicsSignalRO",
            "config": {"read_pv": pv, "name": name, "auto_monitor": True},
            "acquisition": {"schedule": "monitor"},
            "deviceGroup": "status",
        }
    )

# with open("demo_config.yaml", "a") as f:
#     f.write(write_sep("SLS status PVs"))
#     f.write(yaml.dump(out))
#     f.write(write_sep("SLS status PVs end here", sep_type="footer"))


#  GalilMotor("H", name="leyey", host="mpc2680.psi.ch", port=8081, sign=-1)
