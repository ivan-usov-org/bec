# This file is the entry point for the Scan Server.
# It is called either by the bec-scan-server entry point or directly from the command line.

import argparse
import threading

from bec_lib.logger import bec_logger
from bec_lib.redis_connector import RedisConnector
from bec_lib.service_config import ServiceConfig
from bec_server import scan_server

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the scan server.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", default="", help="path to the config file")
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    bec_server = scan_server.scan_server.ScanServer(config=config, connector_cls=RedisConnector)
    try:
        event = threading.Event()
        # pylint: disable=E1102
        logger.success("Started ScanServer")
        event.wait()
    except KeyboardInterrupt as e:
        bec_server.shutdown()
        event.set()
        raise e


if __name__ == "__main__":
    main()
