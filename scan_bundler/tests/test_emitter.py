from unittest import mock
from bec_lib import messages

import pytest

from bec_lib import MessageEndpoints
from scan_bundler.emitter import EmitterBase


@pytest.mark.parametrize(
    "msgs",
    [
        ([]),
        (
            [
                (
                    messages.ScanMessage(point_id=1, scanID="scanID", data={}, metadata={}),
                    "endpoint",
                    None,
                )
            ]
        ),
        (
            [
                (
                    messages.ScanMessage(point_id=1, scanID="scanID", data={}, metadata={}),
                    "endpoint",
                    None,
                ),
                (
                    messages.ScanMessage(point_id=2, scanID="scanID", data={}, metadata={}),
                    "endpoint",
                    None,
                ),
            ]
        ),
        (
            [
                (
                    messages.ScanMessage(point_id=1, scanID="scanID", data={}, metadata={}),
                    "endpoint",
                    "public_endpoint",
                ),
                (
                    messages.ScanMessage(point_id=2, scanID="scanID", data={}, metadata={}),
                    "endpoint",
                    "public_endpoint",
                ),
            ]
        ),
    ],
)
def test_publish_data(msgs):
    producer = mock.MagicMock()
    with mock.patch.object(EmitterBase, "_start_buffered_producer") as start:
        emitter = EmitterBase(producer)
        start.assert_called_once()
        with mock.patch.object(emitter, "_get_messages_from_buffer", return_value=msgs) as get_msgs:
            emitter._publish_data()
            get_msgs.assert_called_once()

            if not msgs:
                producer.send.assert_not_called()
                return

            pipe = producer.pipeline()
            msgs_bundle = messages.BundleMessage()
            _, endpoint, _ = msgs[0]
            for msg, endpoint, public in msgs:
                msg_dump = msg.dumps()
                msgs_bundle.append(msg_dump)
                if public:
                    producer.set.assert_has_calls(
                        producer.set(public, msg_dump, pipe=pipe, expire=1800)
                    )

            producer.send.assert_called_with(endpoint, msgs_bundle.dumps(), pipe=pipe)


@pytest.mark.parametrize(
    "msg,endpoint,public",
    [
        (
            messages.ScanMessage(point_id=1, scanID="scanID", data={}, metadata={}),
            "endpoint",
            None,
        ),
        (
            messages.ScanMessage(point_id=1, scanID="scanID", data={}, metadata={}),
            "endpoint",
            "public",
        ),
    ],
)
def test_add_message(msg, endpoint, public):
    producer = mock.MagicMock()
    emitter = EmitterBase(producer)
    emitter.add_message(msg, endpoint, public)
    msgs = emitter._get_messages_from_buffer()
    out_msg, out_endpoint, out_public = msgs[0]
    assert out_msg == msg
    assert out_endpoint == endpoint
    assert out_public == public
