from scihub.scibec import SciBec

if __name__ == "__main__":
    import argparse

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
    parser.add_argument(
        "--activeExperiment",
        help="scibec url",
    )
    clargs = parser.parse_args()
    config_path = clargs.config
    scibec_url = clargs.url
    active_experiment = clargs.activeExperiment

    scibec = SciBec()
    scibec.url = scibec_url

    if active_experiment:
        experiment = scibec.get_experiment_by_pgroup(active_experiment)
        scibec.set_experiment_active(experiment_id=experiment[0]["id"])
    # beamlines = scibec.get_beamlines()
    # if not beamlines:
    #     scibec.add_beamline("TestBeamline")
    # scibec.update_session_with_file(config_path)
