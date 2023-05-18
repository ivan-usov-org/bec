from scihub.scibec import SciBec

if __name__ == "__main__":
    import argparse

    config_path = "./init_scibec/demo_config.yaml"

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config",
        default="./init_scibec/demo_config.yaml",
        help="path to the config file",
    )
    parser.add_argument(
        "--url",
        default="http://localhost:3030",
        help="scibec url",
    )
    clargs = parser.parse_args()
    config_path = clargs.config
    scibec_url = clargs.url

    scibec = SciBec()
    scibec.url = scibec_url
    beamline = scibec.get_beamline("TestBeamline")
    if not beamline:
        beamline = scibec.add_beamline("TestBeamline")

    if not beamline.get("activeExperiment"):
        experiment = {
            "name": "demo",
            "readACL": ["demoGroup"],
            "createACL": ["demoGroup"],
            "updateACL": ["demoGroup"],
            "beamlineId": beamline["id"],
            "writeAccount": "demoGroup",
            "experimentInfo": {},
        }
        res = scibec.add_experiment(experiment)
        scibec.set_experiment_active(res["id"])
        beamline["activeExperiment"] = res["id"]

    data = scibec.load_config_from_file(config_path)
    scibec.set_session_data(experiment_id=beamline["activeExperiment"], data=data)
