from unittest import mock
import pytest

from bec_utils.redis_connector import RedisProducer
import redis


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


@pytest.mark.parametrize(
    "topic , index , msgs, use_pipe", [["topic1", 1, "msg1", True], ["topic2", 4, "msg2", False]]
)
def test_redis_producer_lset(producer, topic, index, msgs, use_pipe):
    pipe = use_pipe_fcn(producer, use_pipe)

    ret = producer.lset(topic, index, msgs, pipe)

    if pipe:
        producer.r.pipeline().lset.assert_called_once_with(f"{topic}:val", index, msgs)
        assert ret == redis.Redis().pipeline().lset()
    else:
        producer.r.lset.assert_called_once_with(f"{topic}:val", index, msgs)
        assert ret == redis.Redis().lset()


@pytest.mark.parametrize(
    "topic, msgs, use_pipe", [["topic1", "msg1", True], ["topic2", "msg2", False]]
)
def test_redis_producer_rpush(producer, topic, msgs, use_pipe):
    pipe = use_pipe_fcn(producer, use_pipe)

    ret = producer.rpush(topic, msgs, pipe)

    if pipe:
        producer.r.pipeline().rpush.assert_called_once_with(f"{topic}:val", msgs)
        assert ret == redis.Redis().pipeline().rpush()
    else:
        producer.r.rpush.assert_called_once_with(f"{topic}:val", msgs)
        assert ret == redis.Redis().rpush()


@pytest.mark.parametrize(
    "topic, start, end, use_pipe", [["topic1", 0, 4, True], ["topic2", 3, 7, False]]
)
def test_redis_producer_lrange(producer, topic, start, end, use_pipe):
    pipe = use_pipe_fcn(producer, use_pipe)

    ret = producer.lrange(topic, start, end, pipe)

    if pipe:
        producer.r.pipeline().lrange.assert_called_once_with(f"{topic}:val", start, end)
        assert ret == redis.Redis().pipeline().lrange()
    else:
        producer.r.lrange.assert_called_once_with(f"{topic}:val", start, end)
        assert ret == redis.Redis().lrange()


@pytest.mark.parametrize(
    "topic, msg, pipe, expire", [["topic1", "msg1", None, 400], ["topic2", "msg2", None, None]]
)
def test_redis_producer_set_and_publish(producer, topic, msg, pipe, expire):

    producer.set_and_publish(topic, msg, pipe, expire)

    producer.r.pipeline().publish.assert_called_once_with(f"{topic}:sub", msg)
    producer.r.pipeline().set.assert_called_once_with(f"{topic}:val", msg)
    if expire:
        producer.r.pipeline().expire.assert_called_once_with(f"{topic}:val", expire)
    if not pipe:
        producer.r.pipeline().execute.assert_called_once()


@pytest.mark.parametrize(
    "topic, msg, is_dict, expire", [["topic1", "msg1", True, None], ["topic2", "msg2", False, 400]]
)
def test_redis_producer_set(producer, topic, msg, is_dict, expire):
    pipe = None
    producer.set(topic, msg, pipe, is_dict, expire)

    if is_dict:
        producer.r.pipeline().hmset.assert_called_once_with(f"{topic}:val", msg)
    else:
        producer.r.pipeline().set.assert_called_once_with(f"{topic}:val", msg)
    if expire:
        producer.r.pipeline().expire.assert_called_once_with(f"{topic}:val", expire)
    if not pipe:
        producer.r.pipeline().execute.assert_called_once()


@pytest.mark.parametrize("pattern", ["samx", 32])
def test_redis_producer_keys(producer, pattern):

    producer.keys(pattern)
    producer.r.keys.assert_called_once_with(pattern)


def test_redis_producer_get(producer):
    producer.get("topic")
    producer.r.get.assert_called_once()


def use_pipe_fcn(producer, use_pipe):
    if use_pipe:
        return producer.pipeline()
    else:
        return None
