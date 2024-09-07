import copy
import os

import fakeredis
import pytest
import yaml

import bec_lib
from bec_lib import messages
from bec_lib.bec_service import ServiceConfig
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.redis_connector import RedisConnector
from bec_server.device_server.device_server import DeviceServer
from bec_server.scan_server.scan_server import ScanServer

# overwrite threads_check fixture from bec_lib,
# to have it in autouse


@pytest.fixture(autouse=True)
def threads_check(threads_check):
    yield
    bec_logger.logger.remove()


@pytest.fixture()
def fake_redis_server():
    redis = fakeredis.FakeRedis()
    redis.flushall()
    print(redis.keys())
    yield redis
    redis.flushall()


class FakeRedisConnector(RedisConnector):
    def __init__(self, config, redis_cls=fakeredis.FakeRedis):
        super().__init__(config, redis_cls)


@pytest.fixture()
def session_config():
    config_file = os.path.join(os.path.dirname(bec_lib.__file__), "tests", "test_config.yaml")
    with open(config_file, "r") as file:
        session_config = yaml.safe_load(file)

    for name, config in session_config.items():
        if "deviceConfig" in config and config["deviceConfig"] is None:
            config["deviceConfig"] = {}
        config["name"] = name

    return list(session_config.values())


@pytest.fixture()
def device_server(fake_redis_server, session_config):
    server = DeviceServer(
        config=ServiceConfig(redis={"host": "localhost", "port": 1}),
        connector_cls=FakeRedisConnector,
    )
    server.start()
    msg = messages.AvailableResourceMessage(resource=session_config)
    server.connector.set(MessageEndpoints.device_config(), msg)
    server.device_manager.config_update_handler._reload_config()
    yield server
    server.shutdown()


@pytest.fixture()
def scan_server(fake_redis_server, device_server):
    server = ScanServer(
        config=ServiceConfig(redis={"host": "localhost", "port": 1}),
        connector_cls=FakeRedisConnector,
    )
    yield server
    server.shutdown()
