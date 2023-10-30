import numpy as np
import pytest

from bec_lib.core import BECMessage


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2, 1.3])
def test_bec_message_compression_version(version):
    msg = BECMessage.DeviceInstructionMessage(
        device="samx",
        action="set",
        parameter={"set": 0.5},
        metadata={"RID": "1234"},
        version=version,
    )
    res = msg.dumps()
    print(res)
    res_loaded = BECMessage.DeviceInstructionMessage.loads(res)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2, 1.3])
def test_bec_message_compression_numpy_ndarray(version):
    msg = BECMessage.DeviceMessage(
        signals={"samx": {"value": np.random.rand(20)}},
        metadata={"RID": "1234"},
        version=version,
    )
    res = msg.dumps()
    print(res)
    res_loaded = BECMessage.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2, 1.3])
def test_bec_message_compression_numpy_float(version):
    msg = BECMessage.DeviceMessage(
        signals={"samx": {"value": np.float32(5.2)}},
        metadata={"RID": "1234"},
        version=version,
    )
    res = msg.dumps()
    print(res)
    res_loaded = BECMessage.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2, 1.3])
def test_bec_message_serializer_json(version):
    msg = BECMessage.DeviceMessage(
        signals={"samx": {"value": 5.2}},
        metadata={"RID": "1234"},
        version=version,
    )
    msg.compression_handler = msg._get_compression_handler("json")
    msg.compression = "json"
    res = msg.dumps()
    print(res)
    res_loaded = BECMessage.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


def test_bec_message_reader():
    msg = BECMessage.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = BECMessage.MessageReader.loads(res)
    assert res_loaded == msg


def test_bec_message_reader_with_bundled_data():
    sub_msg = BECMessage.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    msg = BECMessage.BundleMessage()
    msg.append(sub_msg)
    msg.append(sub_msg)
    res = msg.dumps()
    res_loaded = BECMessage.MessageReader.loads(res)
    assert res_loaded == [sub_msg, sub_msg]


def test_bundled_message():
    sub_msg = BECMessage.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    msg = BECMessage.BundleMessage()
    msg.append(sub_msg)
    msg.append(sub_msg)
    res = msg.dumps()
    res_loaded = BECMessage.DeviceMessage.loads(res)
    assert res_loaded == [sub_msg, sub_msg]


def test_ScanQueueModificationMessage():
    msg = BECMessage.ScanQueueModificationMessage(
        scanID="1234",
        action="halt",
        parameter={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = BECMessage.ScanQueueModificationMessage.loads(res)
    assert res_loaded == msg


def test_ScanQueueModificationMessage_with_wrong_action_returns_None():
    msg = BECMessage.ScanQueueModificationMessage(
        scanID="1234",
        action="wrong_action",
        parameter={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = BECMessage.ScanQueueModificationMessage.loads(res)
    assert res_loaded is None


def test_ScanQueueStatusMessage_must_include_primary_queue():
    msg = BECMessage.ScanQueueStatusMessage(
        queue={},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = BECMessage.ScanQueueStatusMessage.loads(res)
    assert res_loaded is None


def test_ScanQueueStatusMessage_loads_successfully():
    msg = BECMessage.ScanQueueStatusMessage(
        queue={"primary": {}},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = BECMessage.ScanQueueStatusMessage.loads(res)
    assert res_loaded == msg


def test_DeviceMessage_loads_successfully():
    msg = BECMessage.DeviceMessage(
        signals={"samx": {"value": 5.2}},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = BECMessage.DeviceMessage.loads(res)
    assert res_loaded == msg


def test_DeviceMessage_must_include_signals_as_dict():
    msg = BECMessage.DeviceMessage(
        signals="wrong_signals",
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = BECMessage.DeviceMessage.loads(res)
    assert res_loaded is None
