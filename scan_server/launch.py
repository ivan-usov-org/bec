import argparse
import threading

from bec_client_lib.core import RedisConnector, ServiceConfig, bec_logger
from scan_server.scan_server import ScanServer

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="",
    help="path to the config file",
)
clargs = parser.parse_args()
config_path = clargs.config

config = ServiceConfig(config_path)
bec_logger.level = bec_logger.LOGLEVEL.INFO
logger = bec_logger.logger

bec_server = ScanServer(
    config=config,
    connector_cls=RedisConnector,
)
try:
    event = threading.Event()
    # pylint: disable=E1102
    logger.success("Started ScanServer")
    event.wait()
except KeyboardInterrupt as e:
    # bec_server.connector.raise_error("KeyboardInterrupt")
    bec_server.shutdown()
    event.set()
    raise e

# instruction = {}
# instruction["device"] = "b353bc75-5b1d-460b-8667-6ffb3098de1b"
# instruction["action"] = "move"
# instruction["parameter"] = {}
# instruction["parameter"]["value"] = 5
# instruction["parameter"]["group"] = "a"
