from unittest import mock

import pytest

from bec_lib.bec_events import BECEvents
from bec_lib.messages import (
    DeviceMessage,
    FileMessage,
    ProgressMessage,
    ScanQueueStatusMessage,
    ScanStatusMessage,
    VariableMessage,
)


@pytest.fixture
def bec_events_mock(connected_connector):
    parent = mock.MagicMock()
    parent.connector.return_value = connected_connector
    yield BECEvents(parent)


def test_scan_status(bec_events_mock):
    msg = ScanStatusMessage(
        scan_id="my_test",
        status="closed",
        info={"test": "test"},
        metadata={"test": "test_metadata"},
    )
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.scan_status.get_data()
    assert content == msg.content
    assert md == msg.metadata
    msg = None
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.scan_status.get_data()
    assert content is None
    assert md is None


def test_pre_scan_macros(bec_events_mock):
    msg = VariableMessage(value="my_test", metadata={"test": "test_metadata"})
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.scan_status.get_data()
    assert content == msg.content
    assert md == msg.metadata


def test_device_readback(bec_events_mock):
    msg = DeviceMessage(
        signals={"samx": {"value": 0, "timestamp": 0}}, metadata={"test": "test_metadata"}
    )
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.device_readback.get_data("samx")
    assert content == msg.content
    assert md == msg.metadata


def test_device_config_readback(bec_events_mock):
    msg = DeviceMessage(
        signals={"samx_velocity": {"value": 0, "timestamp": 0}}, metadata={"test": "test_metadata"}
    )
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.device_readback.get_data("samx")
    assert content == msg.content
    assert md == msg.metadata


def test_device_progress(bec_events_mock):
    msg = ProgressMessage(value=20, max_value=100, metadata={"test": "test_metadata"}, done=False)
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.device_readback.get_data("samx")
    assert content == msg.content
    assert md == msg.metadata


def test_file_events(bec_events_mock):
    msg = FileMessage(
        file_path="my_path", metadata={"test": "test_metadata"}, done=False, successful=False
    )
    msg2 = FileMessage(
        file_path="my_path2", metadata={"test": "test_metadata2"}, done=True, successful=True
    )
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.file_event.get_file_for_device("my_scan_id")
    assert content == msg.content
    assert md == msg.metadata
    bec_events_mock._parent.connector.keys.return_value = [
        bytes("my_key", "utf-8"),
        bytes("my_key2", "utf-8"),
    ]
    with mock.patch.object(bec_events_mock._parent.connector, "get", side_effect=[msg, msg2]):
        files = bec_events_mock.file_event.get_files_for_scan("my_scan_id")
        assert files == [(msg.content, msg.metadata), (msg2.content, msg2.metadata)]


def test_queue_status(bec_events_mock):
    msg = ScanQueueStatusMessage(
        queue={"primary": {"info": []}}, metadata={"test": "test_metadata"}
    )
    bec_events_mock._parent.connector.get.return_value = msg
    content, md = bec_events_mock.queue_status.get_data()
    assert content == msg.content
    assert md == msg.metadata
