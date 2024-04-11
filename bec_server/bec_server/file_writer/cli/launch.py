# This file is the entry point for the file writer service.
# It is called either by the bec-file-writer entry point or directly from the command line.
import argparse
import os
import threading

from bec_lib import RedisConnector, ServiceConfig, bec_logger
from bec_server import file_writer

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the file writer.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", default="", help="path to the config file")
    clargs = parser.parse_args()
    config_path = clargs.config

    config = ServiceConfig(config_path)

    file_writer_manager = file_writer.FileWriterManager(config, RedisConnector)
    file_writer_manager.file_writer.configure(
        layout_file=os.path.abspath("./layout_cSAXS_NXsas.xml")
    )
    try:
        event = threading.Event()
        logger.success("Started FileWriter")
        event.wait()
    except KeyboardInterrupt:
        file_writer_manager.shutdown()


if __name__ == "__main__":
    main()
