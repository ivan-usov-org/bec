# Description: Launch the SciHub connector.
# This script is the entry point for the SciHub connector. It is called either
# by the bec-dap entry point or directly from the command line.
import argparse
import threading

from bec_lib.logger import bec_logger
from bec_lib.redis_connector import RedisConnector
from bec_lib.service_config import ServiceConfig
from bec_server import scihub

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the SciHub connector.
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", default="", help="path to the config file")
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    sh = scihub.SciHub(config, RedisConnector)

    try:
        event = threading.Event()
        logger.success("Started SciHub connector")
        event.wait()
    except KeyboardInterrupt:
        sh.shutdown()


if __name__ == "__main__":
    main()
