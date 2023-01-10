from unittest import mock
import pytest

from bec_utils.redis_connector import RedisProducer


@pytest.fixture
def producer():
    with mock.patch("bec_utils.redis_connector.redis.Redis"):
        prod = RedisProducer("localhost", 1)
        yield prod


def test_redis_producer_set(producer):
    producer.set("topic", "msg")
    producer.r.pipeline().set.assert_called_once()


def test_redis_producer_get(producer):
    producer.get("topic")
    producer.r.get.assert_called_once()


@pytest.mark.parametrize("pattern", ["samx", 32])
def test_redis_producer_keys(producer, pattern):

    producer.keys(pattern)
    producer.r.keys.assert_called_once_with(pattern)
