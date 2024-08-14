import fakeredis
import pytest

from bec_lib import bec_logger
from bec_lib.client import BECClient
from bec_lib.redis_connector import RedisConnector

# overwrite threads_check fixture from bec_lib,
# to have it in autouse


@pytest.fixture(autouse=True)
def threads_check(threads_check):
    yield
    bec_logger.logger.remove()


@pytest.fixture(autouse=True)
def bec_client_singleton_reset():
    """Reset the BECClient singleton before and after each test."""
    # pylint: disable=protected-access
    BECClient._reset_singleton()
    yield
    BECClient._reset_singleton()


def fake_redis_server(host, port):
    redis = fakeredis.FakeRedis()
    return redis


@pytest.fixture
def connected_connector():
    connector = RedisConnector("localhost:1", redis_cls=fake_redis_server)
    connector._redis_conn.flushall()
    try:
        yield connector
    finally:
        connector.shutdown()
