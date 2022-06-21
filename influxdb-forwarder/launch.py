import argparse
import logging

from bec_utils import RedisConnector, ServiceConfig, MessageEndpoints, BECMessage
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision, rest
from influxdb_client.client.write_api import SYNCHRONOUS

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default="",
    help="path to the config file",
)
clargs = parser.parse_args()
config_path = clargs.config

config = ServiceConfig(config_path)

logging.basicConfig(filename="influxdb-forwarder.log", level=logging.INFO, filemode="w+")
# logging.getLogger("kafka").setLevel(50)
logging.getLogger().addHandler(logging.StreamHandler())


def influxdb_ingest(msg, influxdb_writer=None, **kwargs):
    msg = BECMessage.DeviceMessage.loads(msg.value)
    signals = msg.content["signals"]
    for dev, data in signals.items():
        try:
            point = (
                Point(dev)
                .tag("readback", dev)
                .field(
                    "value",
                    float(data.get("value"))
                    if type(data.get("value")) == int
                    else data.get("value"),
                )
                .time(datetime.utcnow(), WritePrecision.NS)
            )
            influxdb_writer.write(bucket, org, point)
        except rest.ApiException as e:
            print(f"exception: {e.message}")


# You can generate an API token from the "API Tokens Tab" in the UI
token = "3fochbsfIA4A1ixmlD3okhVmbGQX5Sg9rhMicmiUFRYAVL7YTu0poLYCsq1bi4sOLO45fzlJkIbppTgJAlpjrA=="
org = "PSI"
bucket = "bec"

with InfluxDBClient(url="http://129.129.195.115:8086", token=token, org=org) as client:
    print("started")

    write_api = client.write_api(write_options=SYNCHRONOUS)
    connector = RedisConnector(bootstrap=config.redis)
    device_readback = connector.consumer(
        pattern=MessageEndpoints.device_readback("*"),
        cb=influxdb_ingest,
        influxdb_writer=write_api,
        threaded=False,
    )
    while True:
        device_readback.poll_messages()
