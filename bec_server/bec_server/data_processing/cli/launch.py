# Description: Launch the data processing server.
# This script is the entry point for the Data Processing Server. It is called either
# by the bec-dap entry point or directly from the command line.
import argparse
import threading

import bec_server.data_processing as data_processing
from bec_lib.logger import bec_logger
from bec_lib.redis_connector import RedisConnector
from bec_lib.service_config import ServiceConfig
from bec_server.data_processing.lmfit1d_service import LmfitService1D

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the data processing server.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", default="", help="path to the config file")
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    bec_server = data_processing.dap_server.DAPServer(
        config=config, connector_cls=RedisConnector, provided_services=[LmfitService1D]
    )
    bec_server.start()

    try:
        event = threading.Event()
        logger.success(
            f"Started DAP server for {bec_server._service_id} services. Press Ctrl+C to stop."
        )
        event.wait()
    except KeyboardInterrupt:
        bec_server.shutdown()
        event.set()


if __name__ == "__main__":
    main()
