import os

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "129.129.122.255 sls-x12sa-cagw.psi.ch:5836"
import argparse
import threading

from bec_utils import RedisConnector, ServiceConfig, bec_logger

import device_server

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

s = device_server.DeviceServer(config, RedisConnector)
try:
    event = threading.Event()
    s.start()
    logger.success("Started DeviceServer")
    event.wait()
except KeyboardInterrupt as e:
    s.shutdown()
