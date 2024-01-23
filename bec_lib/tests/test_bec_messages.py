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
        signals={"samx": {"value": np.random.rand(20)}}, metadata={"RID": "1234"}, version=version
    )
    res = msg.dumps()
    print(res)
    res_loaded = messages.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2])
def test_bec_message_compression_numpy_float(version):
    msg = messages.DeviceMessage(
        signals={"samx": {"value": np.float32(5.2)}}, metadata={"RID": "1234"}, version=version
    )
    res = msg.dumps()
    print(res)
    res_loaded = messages.DeviceMessage.loads(res)
    np.testing.assert_equal(res_loaded, msg)
    assert res_loaded == msg


@pytest.mark.parametrize("version", [1.0, 1.1, 1.2])
def test_bec_message_serializer_json(version):
    msg = messages.DeviceMessage(
        signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"}, version=version
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
        scanID="1234", action="halt", parameter={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueModificationMessage.loads(res)
    assert res_loaded == msg


def test_ScanQueueModificationMessage_with_wrong_action_returns_None():
    msg = messages.ScanQueueModificationMessage(
        scanID="1234", action="wrong_action", parameter={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueModificationMessage.loads(res)
    assert res_loaded is None


def test_ScanQueueStatusMessage_must_include_primary_queue():
    msg = messages.ScanQueueStatusMessage(queue={}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ScanQueueStatusMessage.loads(res)
    assert res_loaded is None


def test_ScanQueueStatusMessage_loads_successfully():
    msg = messages.ScanQueueStatusMessage(queue={"primary": {}}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ScanQueueStatusMessage.loads(res)
    assert res_loaded == msg


def test_DeviceMessage_loads_successfully():
    msg = messages.DeviceMessage(signals={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.DeviceMessage.loads(res)
    assert res_loaded == msg


def test_DeviceMessage_must_include_signals_as_dict():
    msg = messages.DeviceMessage(signals="wrong_signals", metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.DeviceMessage.loads(res)
    assert res_loaded is None


def test_DeviceRPCMessage():
    msg = messages.DeviceRPCMessage(
        device="samx", return_val=1, out="done", success=True, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.DeviceRPCMessage.loads(res)
    assert res_loaded == msg


def test_DeviceStatusMessage():
    msg = messages.DeviceStatusMessage(device="samx", status="done", metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.DeviceStatusMessage.loads(res)
    assert res_loaded == msg


def test_DeviceReqStatusMessage():
    msg = messages.DeviceReqStatusMessage(device="samx", success=True, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.DeviceReqStatusMessage.loads(res)
    assert res_loaded == msg


def test_DeviceInfoMessage():
    msg = messages.DeviceInfoMessage(
        device="samx", info={"version": "1.0"}, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.DeviceInfoMessage.loads(res)
    assert res_loaded == msg


def test_ScanMessage():
    msg = messages.ScanMessage(point_id=1, scanID=2, data={"value": 3}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ScanMessage.loads(res)
    assert res_loaded == msg


def test_ScanBaselineMessage():
    msg = messages.ScanBaselineMessage(scanID=2, data={"value": 3}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ScanBaselineMessage.loads(res)
    assert res_loaded == msg


@pytest.mark.parametrize(
    "action,valid",
    [("add", True), ("set", True), ("update", True), ("reload", True), ("wrong_action", False)],
)
def test_DeviceConfigMessage(action, valid):
    msg = messages.DeviceConfigMessage(
        action=action, config={"device": "samx"}, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.DeviceConfigMessage.loads(res)
    if valid:
        assert res_loaded == msg
    else:
        assert res_loaded is None


def test_LogMessage():
    msg = messages.LogMessage(
        log_type="error", content="An error occurred", metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.LogMessage.loads(res)
    assert res_loaded == msg


def test_AlarmMessage():
    msg = messages.AlarmMessage(
        severity=2,
        alarm_type="major",
        source="system",
        content={"error": "An error occurred"},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.AlarmMessage.loads(res)
    assert res_loaded == msg


def test_StatusMessage():
    msg = messages.StatusMessage(
        name="system",
        status=messages.BECStatus.RUNNING,
        info={"version": "1.0"},
        metadata={"RID": "1234"},
    )
    res = msg.dumps()
    res_loaded = messages.StatusMessage.loads(res)
    assert res_loaded == msg


def test_FileMessage():
    msg = messages.FileMessage(
        file_path="/path/to/file", done=True, successful=True, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.FileMessage.loads(res)
    assert res_loaded == msg


def test_VariableMessage():
    msg = messages.VariableMessage(value="value", metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.VariableMessage.loads(res)
    assert res_loaded == msg


def test_ObserverMessage():
    msg = messages.ObserverMessage(observer=[{"name": "observer1"}], metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ObserverMessage.loads(res)
    assert res_loaded == msg


def test_ServiceMetricMessage():
    msg = messages.ServiceMetricMessage(
        name="service1", metrics={"metric1": 1}, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.ServiceMetricMessage.loads(res)
    assert res_loaded == msg


def test_ProcessedDataMessage():
    msg = messages.ProcessedDataMessage(data={"samx": {"value": 5.2}}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ProcessedDataMessage.loads(res)
    assert res_loaded == msg


def test_DAPConfigMessage():
    msg = messages.DAPConfigMessage(config={"val": "val"}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.DAPConfigMessage.loads(res)
    assert res_loaded == msg


def test_AvailableResourceMessage():
    msg = messages.AvailableResourceMessage(
        resource={"resource": "available"}, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.AvailableResourceMessage.loads(res)
    assert res_loaded == msg


def test_ProgressMessage():
    msg = messages.ProgressMessage(value=0.5, max_value=10, done=False, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.ProgressMessage.loads(res)
    assert res_loaded == msg


def test_GUIConfigMessage():
    msg = messages.GUIConfigMessage(config={"config": "value"}, metadata={"RID": "1234"})
    res = msg.dumps()
    res_loaded = messages.GUIConfigMessage.loads(res)
    assert res_loaded == msg


def test_ScanQueueHistoryMessage():
    msg = messages.ScanQueueHistoryMessage(
        status="running", queueID="queueID", info={"val": "val"}, metadata={"RID": "1234"}
    )
    res = msg.dumps()
    res_loaded = messages.ScanQueueHistoryMessage.loads(res)
    assert res_loaded == msg
