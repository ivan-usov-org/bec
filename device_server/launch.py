import argparse
import logging
import threading

from bec_utils import RedisConnector, ServiceConfig

import device_server

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="",
    help="path to the config file",
)
clargs = parser.parse_args()
config_path = clargs.config

config = ServiceConfig(config_path)

logging.basicConfig(filename="device_server.log", level=logging.INFO, filemode="w+")
logging.getLogger("kafka").setLevel(50)
logging.getLogger().addHandler(logging.StreamHandler())

s = device_server.DeviceServer(config.redis, RedisConnector, config.scibec)
try:
    event = threading.Event()
    s.start()
    logging.info("Started DeviceServer")
    event.wait()
except KeyboardInterrupt as e:
    s.shutdown()
