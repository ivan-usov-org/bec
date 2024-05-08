# Description: Launch the scan bundler.
# This script is the entry point for the Scan Bundler. It is called either
# by the bec-scan-bundler entry point or directly from the command line.
import argparse
import threading

from bec_lib.logger import bec_logger
from bec_lib.redis_connector import RedisConnector
from bec_lib.service_config import ServiceConfig
from bec_server import scan_bundler

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the scan bundler.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", default="", help="path to the config file")
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    sb = scan_bundler.ScanBundler(config, RedisConnector)

    try:
        event = threading.Event()
        logger.success("Started ScanBundler")
        event.wait()
    except KeyboardInterrupt:
        sb.shutdown()


if __name__ == "__main__":
    main()
