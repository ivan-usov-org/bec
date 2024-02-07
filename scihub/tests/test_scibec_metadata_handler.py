from unittest import mock

import pytest

from bec_lib import MessageEndpoints, messages
from bec_lib.redis_connector import MessageObject
from scihub.scibec.scibec_metadata_handler import SciBecMetadataHandler


@pytest.fixture
def md_handler():
    inst = SciBecMetadataHandler(mock.Mock())
    yield inst


def test_handle_scan_status(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scanID="scanID", status={}, info={})
    with mock.patch.object(md_handler, "update_scan_status") as mock_update_scan_status:
        md_handler._handle_scan_status(
            MessageObject(value=msg, topic="scan_status"), parent=md_handler
        )
        mock_update_scan_status.assert_called_once_with(msg)


def test_handle_scan_status_ignores_errors(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scanID="scanID", status={}, info={})
    with mock.patch("scihub.scibec.scibec_metadata_handler.logger") as mock_logger:
        with mock.patch.object(md_handler, "update_scan_status") as mock_update_scan_status:
            mock_update_scan_status.side_effect = Exception("test")
            md_handler._handle_scan_status(
                MessageObject(value=msg, topic="scan_status"), parent=md_handler
            )
            mock_update_scan_status.assert_called_once_with(msg)
            mock_logger.exception.assert_called_once_with(
                f"Failed to update scan status: {Exception('test')}"
            )


def test_update_scan_status_returns_without_scibec(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scanID="scanID", status={}, info={})
    md_handler.scibec_connector.scibec = None
    md_handler.update_scan_status(msg)


def test_update_scan_status(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scanID="scanID", status={}, info={"dataset_number": 12})
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    scibec_info = {
        "activeExperiment": {
            "id": "id",
            "readACL": ["readACL"],
            "writeACL": ["writeACL"],
            "owner": "owner",
        }
    }
    md_handler.scibec_connector.scibec_info = scibec_info
    type(scibec.scan.scan_controller_find()).body = mock.PropertyMock(return_value=[])
    type(scibec.dataset.dataset_controller_find()).body = mock.PropertyMock(return_value=[])
    type(scibec.dataset.dataset_controller_create()).body = mock.PropertyMock(
        return_value={"id": "id"}
    )
    md_handler.update_scan_status(msg)


def test_update_scan_status_patch(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scanID="scanID", status="closed", info={"dataset_number": 12})
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    scibec_info = {
        "activeExperiment": {
            "id": "id",
            "readACL": ["readACL"],
            "writeACL": ["writeACL"],
            "owner": "owner",
        }
    }
    md_handler.scibec_connector.scibec_info = scibec_info
    type(scibec.scan.scan_controller_find()).body = mock.PropertyMock(return_value=[{"id": "id"}])
    md_handler.update_scan_status(msg)
    scibec.scan.scan_controller_update_by_id.assert_called_once_with(
        path_params={"id": "id"}, body={"metadata": {"dataset_number": 12}, "exitStatus": "closed"}
    )


def test_handle_file_content(md_handler):
    # pylint: disable=protected-access
    msg = messages.FileContentMessage(file_path="my_file.h5", data={"data": {}})
    msg_raw = MessageObject(value=msg, topic="file_content")
    with mock.patch.object(md_handler, "update_scan_data") as mock_update_scan_data:
        md_handler._handle_file_content(msg_raw, parent=md_handler)
        mock_update_scan_data.assert_called_once_with(**msg.content)


def test_handle_file_content_ignores_errors(md_handler):
    # pylint: disable=protected-access
    msg = messages.FileContentMessage(file_path="my_file.h5", data={"data": {}})
    msg_raw = MessageObject(value=msg, topic="file_content")
    with mock.patch("scihub.scibec.scibec_metadata_handler.logger") as mock_logger:
        with mock.patch.object(md_handler, "update_scan_data") as mock_update_scan_data:
            mock_update_scan_data.side_effect = Exception("test")
            md_handler._handle_file_content(msg_raw, parent=md_handler)
            mock_update_scan_data.assert_called_once_with(**msg.content)
            mock_logger.exception.assert_called_once_with(
                f"Failed to update scan data: {Exception('test')}"
            )


def test_update_scan_data_return_without_scibec(md_handler):
    # pylint: disable=protected-access
    md_handler.scibec_connector.scibec = None
    md_handler.update_scan_data(file_path="my_file.h5", data={"data": {}})


def test_update_scan_data_without_scan(md_handler):
    # pylint: disable=protected-access
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    type(scibec.scan.scan_controller_find()).body = mock.PropertyMock(return_value=[])
    md_handler.update_scan_data(
        file_path="my_file.h5", data={"data": {}, "metadata": {"scanID": "scanID"}}
    )


def test_update_scan_data(md_handler):
    # pylint: disable=protected-access
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    type(scibec.scan.scan_controller_find()).body = mock.PropertyMock(
        return_value=[
            {"id": "id", "readACL": ["readACL"], "writeACL": ["writeACL"], "owner": "owner"}
        ]
    )
    md_handler.update_scan_data(
        file_path="my_file.h5", data={"data": {}, "metadata": {"scanID": "scanID"}}
    )
    scibec.scan_data.scan_data_controller_create_many.assert_called_once_with(
        body=scibec.models.ScanData(
            **{
                "readACL": "readACL",
                "writeACL": "readACL",
                "owner": "owner",
                "scanId": "id",
                "filePath": "my_file.h5",
                "data": {"data": {}, "metadata": {"scanID": "scanID"}},
            }
        )
    )
