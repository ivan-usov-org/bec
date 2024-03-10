import threading
import time
from unittest import mock

import fakeredis
import pytest
import redis
from redis.client import Pipeline
from test_redis_connector import TestMessage

from bec_lib import messages
from bec_lib.endpoints import MessageEndpoints
from bec_lib.redis_connector import MessageObject, RedisConnector
from bec_lib.serialization import MsgpackSerialization

# pylint: disable=protected-access
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument


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


@pytest.mark.parametrize(
    "topics, threaded", [["topics", True], ["topics", False], [None, True], [None, False]]
)
def test_redis_connector_register_threaded(connected_connector, threaded, topics):
    connector = connected_connector
    if topics is None:
        with pytest.raises(ValueError):
            ret = connector.register(
                topics=topics, cb=lambda *args, **kwargs: ..., start_thread=threaded
            )
        return
    ret = connector.register(topics=topics, cb=lambda *args, **kwargs: ..., start_thread=threaded)
    if threaded:
        assert connector._events_listener_thread is not None


@pytest.mark.parametrize(
    "subscribed_topics, subscribed_patterns, msgs",
    [
        ["topics1", None, ["topics1"]],
        [["topics1", "topics2"], None, ["topics1", "topics2"]],
        [None, "pattern1", ["pattern1"]],
        [None, ["patt*", "top*"], ["pattern1", "topics1"]],
    ],
)
def test_redis_connector_register(
    connected_connector, subscribed_topics, subscribed_patterns, msgs
):
    connector = connected_connector
    test_msg = TestMessage("test")
    cb_mock = mock.Mock(spec=[])  # spec is here to remove all attributes
    if subscribed_topics:
        connector.register(
            subscribed_topics, subscribed_patterns, cb=cb_mock, start_thread=False, a=1
        )
        for msg in msgs:
            connector.send(msg, TestMessage(msg))
            connector.poll_messages()
            msg_object = MessageObject(msg, TestMessage(msg))
            cb_mock.assert_called_with(msg_object, a=1)
    if subscribed_patterns:
        connector.register(
            subscribed_topics, subscribed_patterns, cb=cb_mock, start_thread=False, a=1
        )
        for msg in msgs:
            connector.send(msg, TestMessage(msg))
            connector.poll_messages()
            msg_object = MessageObject(msg, TestMessage(msg))
            cb_mock.assert_called_with(msg_object, a=1)


def test_redis_register_poll_messages(connected_connector):
    connector = connected_connector
    cb_fcn_has_been_called = False

    def cb_fcn(msg, **kwargs):
        nonlocal cb_fcn_has_been_called
        cb_fcn_has_been_called = True
        assert kwargs["a"] == 1

    test_msg = TestMessage("test")
    connector.register("test", cb=cb_fcn, a=1, start_thread=False)
    connector._redis_conn.publish("test", MsgpackSerialization.dumps(test_msg))

    connector.poll_messages(timeout=1)

    assert cb_fcn_has_been_called

    with pytest.raises(TimeoutError):
        connector.poll_messages(timeout=0.1)


@pytest.mark.parametrize(
    "pipeline, raise_exception",
    [(None, True), (5, True), ({"a": 1}, True), (mock.MagicMock(spec=Pipeline), False)],
)
def test_redis_connector_execute_pipeline(connected_connector, pipeline, raise_exception):
    connector = connected_connector
    if raise_exception:
        with pytest.raises(TypeError):
            connector.execute_pipeline(pipeline)
    else:
        connector.execute_pipeline(pipeline)
        assert pipeline.execute.call_count == 1


def test_redis_connector_execute_pipeline_returns_list(connected_connector):
    connector = connected_connector
    pipe = connector.pipeline()
    connector.lpush(
        "test", messages.ScanMessage(point_id=5, scanID="1234", data={"a": 1}), pipe=pipe
    )

    res = connector.execute_pipeline(pipe)
    assert isinstance(res, list) and len(res) == 1

    pipe = connector.pipeline()
    connector.lpush(
        "test", messages.ScanMessage(point_id=5, scanID="1234", data={"a": 1}), pipe=pipe
    )
    connector.lpush(
        "test", messages.ScanMessage(point_id=5, scanID="1234", data={"a": 1}), pipe=pipe
    )

    res = connector.execute_pipeline(pipe)
    assert isinstance(res, list) and len(res) == 2


def test_redis_connector_lpush(connected_connector):
    connector = connected_connector
    connector.lpush("test", "test_msg")
    assert connector._redis_conn.lrange("test", 0, -1) == [b"test_msg"]


def test_redis_connector_lset(connected_connector):
    connector = connected_connector
    connector.lpush("test", "test_msg")
    connector.lset("test", 0, "test_msg2")
    assert connector._redis_conn.lrange("test", 0, -1) == [b"test_msg2"]


def test_redis_connector_lset_index_out_of_range(connected_connector):
    connector = connected_connector
    connector.lpush("test", "test_msg")
    with pytest.raises(redis.exceptions.ResponseError):
        connector.lset("test", 1, "test_msg2")


def test_redis_connector_xadd(connected_connector):
    connector = connected_connector
    connector.xadd("test", {"a": 1})
    assert connector._redis_conn.xrange("test", "-", "+")[0][1] == {
        b"a": MsgpackSerialization.dumps(1)
    }

    assert connector.xread("test", count=1) == [{"a": 1}]

    assert connector.xread("test2", count=1) is None
    connector.xadd("test2", {"a": 2})
    assert connector.xread("test2", count=1) == [{"a": 2}]


def test_redis_connector_xread_repeated(connected_connector):
    connector = connected_connector
    connector.xadd("test", {"a": 1})
    connector.xadd("test", {"a": 2})
    connector.xadd("test", {"a": 3})
    assert connector.xread("test", count=2, from_start=True) == [{"a": 1}, {"a": 2}]
    assert connector.xread("test", count=2) == [{"a": 3}]
    assert connector.xread("test", count=2) is None


def test_redis_connector_xrange(connected_connector):
    connector = connected_connector
    connector.xadd("test", {"a": 1})
    connector.xadd("test", {"a": 2})
    connector.xadd("test", {"a": 3})
    assert connector.xrange("test", "-", "+", count=2) == [{"a": 1}, {"a": 2}]
    assert connector.xrange("test", "-", "+") == [{"a": 1}, {"a": 2}, {"a": 3}]

    assert connector.xrange("test2", "-", "+") is None


def test_redis_connector_get_last(connected_connector):
    connector = connected_connector
    connector.xadd("test", {"data": 1})
    connector.xadd("test", {"data": 2})
    connector.xadd("test", {"data": 3})
    assert connector.get_last("test") == {"data": 3}
    assert connector.get_last("test") == {"data": 3}
    assert connector.get_last("test2") is None
    assert connector.get_last(5) is None


@pytest.mark.timeout(5)
def test_redis_connector_register_stream(connected_connector):
    connector = connected_connector
    cb_mock = mock.Mock(spec=[])  # spec is here to remove all attributes
    stream_id = connector.register_stream("test", cb=cb_mock, start_thread=False, a=1)
    time.sleep(0.1)
    connector.xadd("test", {"data": 1})
    connector.poll_stream_messages()
    assert mock.call({"data": 1}, a=1) in cb_mock.mock_calls
    connector.xadd("test", {"data": 2})
    connector.poll_stream_messages()
    assert mock.call({"data": 2}, a=1) in cb_mock.mock_calls
    connector.unregister_stream(stream_id)
    assert connector._stream_topics_cb[stream_id] == []


@pytest.mark.timeout(5)
@pytest.mark.parametrize(
    "endpoint",
    [["test"], [MessageEndpoints.processed_data("test"), MessageEndpoints.processed_data("test2")]],
)
def test_redis_connector_register_stream_list(connected_connector, endpoint):
    connector = connected_connector
    cb_mock = mock.Mock(spec=[])  # spec is here to remove all attributes
    stream_id = connector.register_stream(endpoint, cb=cb_mock, start_thread=False, a=1)
    time.sleep(0.1)
    for ep in endpoint:
        connector.xadd(ep, {"data": 1})
    connector.poll_stream_messages()
    assert mock.call({"data": 1}, a=1) in cb_mock.mock_calls

    for ep in endpoint:
        connector.xadd(ep, {"data": 2})
    connector.poll_stream_messages()
    assert mock.call({"data": 2}, a=1) in cb_mock.mock_calls
    for str_id in stream_id:
        connector.unregister_stream(str_id)
        assert connector._stream_topics_cb[str_id] == []


@pytest.mark.timeout(5)
@pytest.mark.parametrize("endpoint", ["test", MessageEndpoints.processed_data("test")])
def test_redis_connector_register_stream_newest_only(connected_connector, endpoint):
    connector = connected_connector
    cb_mock = mock.Mock(spec=[])  # spec is here to remove all attributes
    stream_id = connector.register_stream(
        endpoint, cb=cb_mock, newest_only=True, start_thread=False, a=1
    )
    time.sleep(0.1)
    connector.xadd(endpoint, {"data": 1})
    while cb_mock.call_count == 0:
        time.sleep(0.1)
    assert mock.call({"data": 1}, a=1) in cb_mock.mock_calls
    connector.xadd(endpoint, {"data": 2})
    while cb_mock.call_count == 1:
        time.sleep(0.1)
    assert mock.call({"data": 2}, a=1) in cb_mock.mock_calls
    assert cb_mock.call_count == 2
    num_threads = threading.active_count()
    connector.unregister_stream(stream_id)
    assert threading.active_count() == num_threads - 1


@pytest.mark.timeout(5)
@pytest.mark.parametrize("endpoint", [["test"], [MessageEndpoints.processed_data("test")]])
def test_redis_connector_register_stream_newest_only_list(connected_connector, endpoint):
    connector = connected_connector
    cb_mock = mock.Mock(spec=[])  # spec is here to remove all attributes
    stream_id = connector.register_stream(
        endpoint, cb=cb_mock, newest_only=True, start_thread=False, a=1
    )
    time.sleep(0.1)
    for ep in endpoint:
        connector.xadd(ep, {"data": 1})
    while cb_mock.call_count == 0:
        time.sleep(0.1)
    assert mock.call({"data": 1}, a=1) in cb_mock.mock_calls

    for ep in endpoint:
        connector.xadd(ep, {"data": 2})
    while cb_mock.call_count == 1:
        time.sleep(0.1)
    assert mock.call({"data": 2}, a=1) in cb_mock.mock_calls
    assert cb_mock.call_count == 2
    num_threads = threading.active_count()

    for str_id in stream_id:
        connector.unregister_stream(str_id)
    assert threading.active_count() == num_threads - 1


def test_register_raises_if_no_cb(connected_connector):
    connector = connected_connector
    with pytest.raises(ValueError):
        connector.register("test", cb=None, start_thread=False)


def test_register_stream_raises_if_no_cb(connected_connector):
    connector = connected_connector
    with pytest.raises(ValueError):
        connector.register_stream("test", cb=None, start_thread=False)


def test_register_stream_raises_if_no_topic_nor_pattern(connected_connector):
    connector = connected_connector
    with pytest.raises(ValueError):
        connector.register_stream(None, cb=mock.Mock(), start_thread=False)


@pytest.mark.parametrize("topics", [5, [5, "test"], [5, 5], [None, "test"], None, [None, None]])
def test_register_stream_raises_if_topic_is_not_str_nor_list(connected_connector, topics):
    connector = connected_connector
    with pytest.raises(ValueError):
        connector.register_stream(topics, cb=lambda *args, **kwargs: ..., start_thread=False)


@pytest.mark.parametrize("val", [messages.ScanMessage(point_id=5, scanID="1234", data={"a": 1})])
def test_lrange_parses_messages(connected_connector, val):
    connected_connector.lpush("test", val)
    res = connected_connector.lrange("test", 0, -1)
    assert isinstance(res[0], messages.ScanMessage)
