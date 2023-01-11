from unittest import mock

import pytest
import redis

from bec_utils.BECMessage import AlarmMessage, LogMessage
from bec_utils.connector import ConsumerConnectorError
from bec_utils.endpoints import MessageEndpoints
from bec_utils.redis_connector import (
    Alarms,
    RedisConnector,
    RedisConsumer,
    RedisConsumerThreaded,
    RedisProducer,
)


@pytest.fixture
def producer():
    with mock.patch("bec_utils.redis_connector.redis.Redis"):
        prod = RedisProducer("localhost", 1)
        yield prod


@pytest.fixture
def connector():
    with mock.patch("bec_utils.redis_connector.redis.Redis"):
        connector = RedisConnector("localhost:1")
        yield connector


@pytest.fixture
def consumer():
    with mock.patch("bec_utils.redis_connector.redis.Redis"):
        consumer = RedisConsumer("localhost", "1")
        yield consumer


def test_redis_connector_producer(connector):
    ret = connector.producer()
    assert isinstance(ret, RedisProducer)


@pytest.mark.parametrize(
    "topics, threaded", [["topics", True], ["topics", False], [None, True], [None, False]]
)
def test_redis_connector_consumer(connector, threaded, topics):

    pattern = None
    len_of_threads = len(connector._threads)

    if threaded:
        if topics is None and pattern is None:
            with pytest.raises(ValueError) as exc_info:
                ret = connector.consumer(
                    topics=topics, threaded=threaded, cb=lambda *args, **kwargs: ...
                )

            assert exc_info.value.args[0] == "Topics must be set for threaded consumer"
        else:
            ret = connector.consumer(
                topics=topics, threaded=threaded, cb=lambda *args, **kwargs: ...
            )
            assert len(connector._threads) == len_of_threads + 1
            assert isinstance(ret, RedisConsumerThreaded)

    else:
        if not topics:
            with pytest.raises(ConsumerConnectorError):
                ret = connector.consumer(
                    topics=topics, threaded=threaded, cb=lambda *args, **kwargs: ...
                )
            return
        ret = connector.consumer(topics=topics, threaded=threaded, cb=lambda *args, **kwargs: ...)
        assert isinstance(ret, RedisConsumer)


def test_redis_connector_log_warning(connector):
    connector._notifications_producer.send = mock.MagicMock()

    connector.log_warning("msg")
    connector._notifications_producer.send.assert_called_once_with(
        MessageEndpoints.log(), LogMessage(log_type="warning", content="msg").dumps()
    )


def test_redis_connector_log_message(connector):
    connector._notifications_producer.send = mock.MagicMock()

    connector.log_message("msg")
    connector._notifications_producer.send.assert_called_once_with(
        MessageEndpoints.log(), LogMessage(log_type="log", content="msg").dumps()
    )


def test_redis_connector_log_error(connector):
    connector._notifications_producer.send = mock.MagicMock()

    connector.log_error("msg")
    connector._notifications_producer.send.assert_called_once_with(
        MessageEndpoints.log(), LogMessage(log_type="error", content="msg").dumps()
    )


@pytest.mark.parametrize(
    "severity, alarm_type, source, content, metadata",
    [
        [Alarms.MAJOR, "alarm", "source", {"content": "content1"}, {"metadata": "metadata1"}],
        [Alarms.MINOR, "alarm", "source", {"content": "content1"}, {"metadata": "metadata1"}],
        [Alarms.WARNING, "alarm", "source", {"content": "content1"}, {"metadata": "metadata1"}],
    ],
)
def test_redis_connector_raise_alarm(connector, severity, alarm_type, source, content, metadata):
    connector._notifications_producer.set_and_publish = mock.MagicMock()

    connector.raise_alarm(severity, alarm_type, source, content, metadata)

    connector._notifications_producer.set_and_publish.assert_called_once_with(
        MessageEndpoints.alarm(),
        AlarmMessage(
            severity=severity,
            alarm_type=alarm_type,
            source=source,
            content=content,
            metadata=metadata,
        ).dumps(),
    )


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


@pytest.mark.parametrize("pattern", ["samx", "samy"])
def test_redis_producer_keys(producer, pattern):

    ret = producer.keys(pattern)
    producer.r.keys.assert_called_once_with(pattern)
    assert ret == redis.Redis().keys()


def test_redis_producer_pipeline(producer):
    ret = producer.pipeline()
    producer.r.pipeline.assert_called_once()
    assert ret == redis.Redis().pipeline()


@pytest.mark.parametrize("topic,use_pipe", [["topic1", True], ["topic2", False]])
def test_redis_producer_delete(producer, topic, use_pipe):
    pipe = use_pipe_fcn(producer, use_pipe)

    producer.delete(topic, pipe)

    if pipe:
        producer.pipeline().delete.assert_called_once_with(topic)
    else:
        producer.r.delete.assert_called_once_with(topic)


@pytest.mark.parametrize(
    "topic, use_pipe, is_dict",
    [
        ["topic1", True, True],
        ["topic2", False, True],
        ["topic3", True, False],
        ["topic4", False, False],
    ],
)
def test_redis_producer_get(producer, topic, use_pipe, is_dict):
    pipe = use_pipe_fcn(producer, use_pipe)

    ret = producer.get(topic, pipe, is_dict)
    if is_dict:
        if pipe:
            producer.pipeline().hgetall.assert_called_once_with(f"{topic}:val")
            assert ret == redis.Redis().pipeline().hgetall()

        else:
            producer.r.hgetall.assert_called_once_with(f"{topic}:val")
            assert ret == redis.Redis().hgetall()

    else:
        if pipe:
            producer.pipeline().get.assert_called_once_with(f"{topic}:val")
            assert ret == redis.Redis().pipeline().get()

        else:
            producer.r.get.assert_called_once_with(f"{topic}:val")
            assert ret == redis.Redis().get()


def use_pipe_fcn(producer, use_pipe):
    if use_pipe:
        return producer.pipeline()
    return None


def test_redis_consumer_additional_kwargs(connector):
    cons = connector.consumer(topics="topic", parent="here", cb=lambda *args, **kwargs: ...)
    assert "parent" in cons.kwargs


# @pytest.mark.parametrize("pattern, topics", [["pattern", "topics1"], [None, "topics2"]])
# def test_redis_consumer_initialize_connector(consumer, pattern, topics):
#     consumer.pattern = pattern
#     print(consumer.topics)

#     consumer.topics = topics
#     print(consumer.topics)
#     consumer.initialize_connector()

#     if consumer.pattern is not None:
#         consumer.pubsub.psubscribe.assert_called_once_with(consumer.pattern)
#     else:
#         consumer.pubsub.subscribe.assert_called_with(consumer.topics)
