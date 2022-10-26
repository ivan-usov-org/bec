from bec_utils.scibec import SciBec

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
    beamlines = scibec.get_beamlines()
    if not beamlines:
        scibec.add_beamline("TestBeamline")
    scibec.update_session_with_file(config_path)
