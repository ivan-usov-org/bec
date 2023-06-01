import numpy as np
import pytest

from bec_client_lib.core import BECMessage


@pytest.mark.parametrize("version", [1.0, 1.1])
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


@pytest.mark.parametrize("version", [1.0, 1.1])
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


@pytest.mark.parametrize("version", [1.0, 1.1])
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


@pytest.mark.parametrize("version", [1.0, 1.1])
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
