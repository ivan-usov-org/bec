import argparse
import threading

from bec_lib.core import RedisConnector, ServiceConfig, bec_logger

from data_processing.dap_server import DAPServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config",
        default="",
        help="path to the config file",
    )
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)
    bec_logger.level = bec_logger.LOGLEVEL.DEBUG
    logger = bec_logger.logger

    bec_server = DAPServer(
        config=config,
        connector_cls=RedisConnector,
    )
    try:
        event = threading.Event()
        # pylint: disable=E1102
        logger.success("Started DAP server")
        event.wait()
    except KeyboardInterrupt as e:
        # bec_server.connector.raise_error("KeyboardInterrupt")
        bec_server.shutdown()
        event.set()
        raise e
