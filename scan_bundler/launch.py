import argparse
import threading

from bec_client_lib.core import RedisConnector, ServiceConfig, bec_logger
from scan_bundler import ScanBundler

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="",
    help="path to the config file",
)
clargs = parser.parse_args()
config_path = clargs.config

config = ServiceConfig(config_path)

sb = ScanBundler(config, RedisConnector)

try:
    event = threading.Event()
    logger.success("Started ScanBundler")
    event.wait()
except KeyboardInterrupt as e:
    sb.shutdown()
