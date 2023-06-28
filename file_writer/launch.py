import argparse
import os
import threading

from bec_lib.core import RedisConnector, ServiceConfig, bec_logger

from file_writer import FileWriterManager

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

file_writer = FileWriterManager(config, RedisConnector)
file_writer.file_writer.configure(layout_file=os.path.abspath("./layout_cSAXS_NXsas.xml"))
try:
    event = threading.Event()
    logger.success("Started FileWriter")
    event.wait()
except KeyboardInterrupt as e:
    file_writer.shutdown()
