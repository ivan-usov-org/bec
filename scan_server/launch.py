import argparse
import logging
import threading

from bec_utils import RedisConnector, ServiceConfig

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

logging.basicConfig(filename="ScanServer.log", level=logging.INFO, filemode="w+")
# logging.getLogger("kafka").setLevel(50)
logging.getLogger().addHandler(logging.StreamHandler())

try:
    event = threading.Event()
    # pylint: disable=E1102
    k = ScanServer(
        bootstrap_server=config.redis,
        connector_cls=RedisConnector,
        scibec_url=config.scibec,
    )
    logging.info("Started ScanServer")
    event.wait()
    print("started")
except KeyboardInterrupt as e:
    k.connector.raise_error("KeyboardInterrupt")
    k.shutdown()
    event.set()
    raise e

# instruction = {}
# instruction["device"] = "b353bc75-5b1d-460b-8667-6ffb3098de1b"
# instruction["action"] = "move"
# instruction["parameter"] = {}
# instruction["parameter"]["value"] = 5
# instruction["parameter"]["group"] = "a"
