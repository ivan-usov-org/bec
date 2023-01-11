from unittest import mock
import pytest

from bec_utils.redis_connector import RedisProducer


@pytest.fixture
def producer():
    with mock.patch("bec_utils.redis_connector.redis.Redis"):
        prod = RedisProducer("localhost", 1)
        yield prod


@pytest.mark.parametrize("topic , msg", [["topic1", "msg1"], ["topic2", "msg2"]])
def test_redis_producer_send(producer, topic, msg):
    producer.send(topic, msg)
    producer.r.publish.assert_called_once_with(f"{topic}:sub", msg)

    producer.send(topic, msg, pipe=producer.pipeline())
    producer.r.pipeline().publish.assert_called_once_with(f"{topic}:sub", msg)


@pytest.mark.parametrize(
    "topic, msgs, max_size, expire",
    [["topic", "msgs", None, None], ["topic", "msgs", 10, None], ["topic", "msgs", None, 100]],
)
def test_redis_producer_lpush(producer, topic, msgs, max_size, expire):
    pipe = None
    producer.lpush(topic, msgs, pipe, max_size, expire)

    producer.r.pipeline().lpush.assert_called_once_with(f"{topic}:val", msgs)

    if max_size:
        producer.r.pipeline().ltrim.assert_called_once_with(f"{topic}:val", 0, max_size)
    if expire:
        producer.r.pipeline().expire.assert_called_once_with(f"{topic}:val", expire)
    if not pipe:
        producer.r.pipeline().execute.assert_called_once()


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
