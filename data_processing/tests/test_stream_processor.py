from unittest import mock

import pytest
from bec_lib.core import BECMessage

from data_processing.stream_processor import StreamProcessor


class DummyStreamProcessor(StreamProcessor):
    def process(self, data: dict, metadata: dict) -> tuple:
        return data, metadata


@pytest.fixture(scope="function")
def stream_processor():
    connector = mock.MagicMock()
    config = {
        "stream": "scan_segment",
        "output": "gaussian_fit_worker_3",
        "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
        "model": "GaussianModel",
    }
    return DummyStreamProcessor(connector, config)


def test_stream_processor_run_forever(stream_processor):
    """
    Test the StreamProcessor class run_forever method.
    """

    stream_processor.queue.append(
        BECMessage.ScanMessage(point_id=1, scanID="scanID", data={"x": 1, "y": 1})
    )
    with mock.patch.object(StreamProcessor, "_process_data") as mock_process_data:
        mock_process_data.return_value = [
            ({"x": 1, "y": 1}, {"scanID": "scanID"}),
        ]
        stream_processor._run_forever()
        mock_process_data.assert_called_once()


def test_stream_processor_publishes_bundled_data(stream_processor):
    """
    Test the StreamProcessor class run_forever method and make sure it publishes bundled data.
    """
    stream_processor.queue.append(
        BECMessage.ScanMessage(point_id=1, scanID="scanID", data={"x": 1, "y": 1})
    )
    with mock.patch.object(StreamProcessor, "_process_data") as mock_process_data:
        mock_process_data.return_value = [
            ({"x": 1, "y": 1}, {"scanID": "scanID"}),
            ({"x": 1, "y": 1}, {"scanID": "scanID"}),
        ]
        stream_processor._run_forever()
        mock_process_data.assert_called_once()
        assert stream_processor._connector.producer().set_and_publish.call_count == 1


def test_stream_processor_does_not_publish_empty_data(stream_processor):
    """
    Test the StreamProcessor class run_forever method and make sure does not publish empty data.
    """
    stream_processor.queue.append(
        BECMessage.ScanMessage(point_id=1, scanID="scanID", data={"x": 1, "y": 1})
    )
    with mock.patch.object(StreamProcessor, "_process_data") as mock_process_data:
        mock_process_data.return_value = [
            None,
        ]
        stream_processor._run_forever()
        mock_process_data.assert_called_once()
        assert stream_processor._connector.producer().set_and_publish.call_count == 0


def test_stream_processor_start_data_consumer(stream_processor):
    """
    Test the StreamProcessor class start_data_consumer method.
    """
    stream_processor.start_data_consumer()
    stream_processor._connector.consumer.assert_called_once()
    assert stream_processor._connector.consumer().start.call_count == 1


def test_stream_processor_start_data_consumer_stops_existing_consumer(stream_processor):
    """
    Test the StreamProcessor class start_data_consumer method and make sure it stops the existing consumer.
    """
    orig_consumer = mock.MagicMock()
    stream_processor.consumer = orig_consumer
    stream_processor.consumer.is_alive.return_value = True
    stream_processor.start_data_consumer()
    assert orig_consumer.shutdown.call_count == 1
