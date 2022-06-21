import threading
import logging
import argparse

from scan_bundler import ScanBundler
from bluekafka_utils import RedisConnector, ServiceConfig

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="",
    help="path to the config file",
)
clargs = parser.parse_args()
config_path = clargs.config

config = ServiceConfig(config_path)

logging.basicConfig(filename="scan_bundler.log", level=logging.INFO, filemode="w+")
logging.getLogger("kafka").setLevel(50)
logging.getLogger().addHandler(logging.StreamHandler())

sb = ScanBundler(config.redis, RedisConnector, config.scibec)

try:
    event = threading.Event()
    logging.info("Started ScanBundler")
    event.wait()
except KeyboardInterrupt as e:
    sb.shutdown()
