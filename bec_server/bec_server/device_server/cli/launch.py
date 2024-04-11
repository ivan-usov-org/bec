# This file is the entry point for the BEC device server. It is responsible for
# launching the device server and handling command line arguments.
# It is called either by the bec-device-server entry point or directly from the command line.

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# we need to run the startup script before we import anything else. This is
# to ensure that the epics environment variables are set correctly.

try:
    from bec_plugins.device_server import startup
except ImportError:
    startup = None

if startup is not None:
    startup.run()


import argparse
import threading

from bec_lib import RedisConnector, ServiceConfig, bec_logger
from bec_server import device_server

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the BEC device server.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", default="", help="path to the config file")
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    s = device_server.DeviceServer(config, RedisConnector)
    try:
        event = threading.Event()
        s.start()
        logger.success("Started DeviceServer")
        event.wait()
    except KeyboardInterrupt:
        s.shutdown()


if __name__ == "__main__":
    main()
