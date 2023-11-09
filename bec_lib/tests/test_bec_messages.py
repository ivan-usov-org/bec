import numpy as np
import pytest

from bec_lib import messages


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2])
def test_bec_message_compression_version(version):
    msg = messages.DeviceInstructionMessage(
        device="samx",
        action="set",
        parameter={"set": 0.5},
        metadata={"RID": "1234"},
        version=version,
    )
    res = msg.dumps()
    print(res)
    res_loaded = messages.DeviceInstructionMessage.loads(res)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2])
def test_bec_message_compression_numpy_ndarray(version):
    msg = messages.DeviceMessage(
        signals={"samx": {"value": np.random.rand(20)}},
        metadata={"RID": "1234"},
        version=version,
    )
    res = msg.dumps()
    print(res)
    res_loaded = messages.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2])
def test_bec_message_compression_numpy_float(version):
    msg = messages.DeviceMessage(
        signals={"samx": {"value": np.float32(5.2)}},
        metadata={"RID": "1234"},
        version=version,
    )
    res = msg.dumps()
    print(res)
    res_loaded = messages.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2])
def test_bec_message_serializer_json(version):
    msg = messages.DeviceMessage(
        signals={"samx": {"value": 5.2}},
        metadata={"RID": "1234"},
        version=version,
    )
    msg.compression_handler = msg._get_compression_handler("json")
    msg.compression = "json"
    res = msg.dumps()
    print(res)
    res_loaded = messages.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


def test_bec_message_reader():
    msg = messages.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.MessageReader.loads(res)
    assert res_loaded == msg


def test_bec_message_reader_with_bundled_data():
    sub_msg = messages.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    msg = messages.BundleMessage()
    msg.append(sub_msg)
    msg.append(sub_msg)
    res = msg.dumps()
    res_loaded = messages.MessageReader.loads(res)
    assert res_loaded == [sub_msg, sub_msg]


def test_bundled_message():
    sub_msg = messages.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    msg = messages.BundleMessage()
    msg.append(sub_msg)
    msg.append(sub_msg)
    res = msg.dumps()
    res_loaded = messages.DeviceMessage.loads(res)
    assert res_loaded == [sub_msg, sub_msg]


def test_ScanQueueModificationMessage():
    msg = messages.ScanQueueModificationMessage(
        scanID="1234",
        action="halt",
        parameter={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueModificationMessage.loads(res)
    assert res_loaded == msg


def test_ScanQueueModificationMessage_with_wrong_action_returns_None():
    msg = messages.ScanQueueModificationMessage(
        scanID="1234",
        action="wrong_action",
        parameter={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueModificationMessage.loads(res)
    assert res_loaded is None


def test_ScanQueueStatusMessage_must_include_primary_queue():
    msg = messages.ScanQueueStatusMessage(
        queue={},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueStatusMessage.loads(res)
    assert res_loaded is None


def test_ScanQueueStatusMessage_loads_successfully():
    msg = messages.ScanQueueStatusMessage(
        queue={"primary": {}},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueStatusMessage.loads(res)
    assert res_loaded == msg


def test_DeviceMessage_loads_successfully():
    msg = messages.DeviceMessage(
        signals={"samx": {"value": 5.2}},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.DeviceMessage.loads(res)
    assert res_loaded == msg


def test_DeviceMessage_must_include_signals_as_dict():
    msg = messages.DeviceMessage(
        signals="wrong_signals",
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.DeviceMessage.loads(res)
    assert res_loaded is None
