import argparse
import logging
import threading

from bluekafka_utils import RedisConnector, ServiceConfig

from file_writer import FileWriterManager

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

sb = FileWriterManager(config.redis, RedisConnector, config.scibec)

try:
    event = threading.Event()
    logging.info("Started FileWriter")
    event.wait()
except KeyboardInterrupt as e:
    sb.shutdown()
