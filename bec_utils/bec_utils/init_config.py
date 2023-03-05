import argparse

from bec_utils import ConfigHelper

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="./init_scibec/demo_config.yaml",
    help="path to the config file",
)
parser.add_argument(
    "--redis",
    default="localhost:6379",
    help="redis host and port",
)

clargs = parser.parse_args()

config_helper = ConfigHelper(clargs.redis)
config_helper.update_session_with_file(clargs.config)
