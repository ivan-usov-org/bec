from unittest import mock

from bec_client_lib.core import BECMessage, MessageEndpoints

from data_processing.worker_manager import DAPWorkerManager


def test_worker_manager_retrieves_config_on_startup():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "update_config") as mock_update_config:
        config = {
            "stream": "scan_segment",
            "output": "gaussian_fit_worker_3",
            "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
            "model": "GaussianModel",
        }
        worker_config = {"id": "gaussian_fit_worker_3", "config": config}
        connector.producer().get.return_value = BECMessage.DAPConfigMessage(
            config={"workers": [worker_config]}
        ).dumps()
        worker_manager = DAPWorkerManager(connector)
        mock_update_config.assert_called_once()


def test_worker_manager_retrieves_config_on_startup_empty():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "update_config") as mock_update_config:
        connector.producer().get.return_value = None
        worker_manager = DAPWorkerManager(connector)
        mock_update_config.assert_not_called()


def test_worker_manager_update_config():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "_start_worker") as mock_start_worker:
        connector.producer().get.return_value = None
        worker_manager = DAPWorkerManager(connector)
        config = {
            "stream": "scan_segment",
            "output": "gaussian_fit_worker_3",
            "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
            "model": "GaussianModel",
        }
        worker_config = {"id": "gaussian_fit_worker_3", "config": config}
        worker_manager.update_config(
            BECMessage.DAPConfigMessage(config={"workers": [worker_config]})
        )
        mock_start_worker.assert_called_once()


def test_worker_manager_update_config_no_workers():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "_start_worker") as mock_start_worker:
        connector.producer().get.return_value = None
        worker_manager = DAPWorkerManager(connector)
        worker_manager.update_config(BECMessage.DAPConfigMessage(config={"workers": []}))
        mock_start_worker.assert_not_called()


def test_worker_manager_update_config_worker_already_running():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "_start_worker") as mock_start_worker:
        connector.producer().get.return_value = None
        worker_manager = DAPWorkerManager(connector)
        config = {
            "stream": "scan_segment",
            "output": "gaussian_fit_worker_3",
            "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
            "model": "GaussianModel",
        }
        worker_config = {"id": "gaussian_fit_worker_3", "config": config}
        worker_manager._workers = {"gaussian_fit_worker_3": {"config": config, "worker": None}}
        worker_manager.update_config(
            BECMessage.DAPConfigMessage(config={"workers": [worker_config]})
        )
        mock_start_worker.assert_not_called()


def test_worker_manager_update_config_worker_already_running_different_config():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "_start_worker") as mock_start_worker:
        connector.producer().get.return_value = None
        worker_manager = DAPWorkerManager(connector)
        config = {
            "stream": "scan_segment",
            "output": "gaussian_fit_worker_3",
            "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
            "model": "GaussianModel",
        }
        w3_mock = mock.MagicMock()
        worker_config = {"id": "gaussian_fit_worker_3", "config": config}
        worker_manager._workers = {"gaussian_fit_worker_3": {"config": {}, "worker": w3_mock}}
        worker_manager.update_config(
            BECMessage.DAPConfigMessage(config={"workers": [worker_config]})
        )
        mock_start_worker.assert_called_once()
        w3_mock.terminate.assert_called_once()


def test_worker_manager_update_config_remove_outdated_workers():
    connector = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "_start_worker") as mock_start_worker:
        connector.producer().get.return_value = None
        worker_manager = DAPWorkerManager(connector)
        config = {
            "stream": "scan_segment",
            "output": "gaussian_fit_worker_3",
            "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
            "model": "GaussianModel",
        }
        w3_mock = mock.MagicMock()
        worker_config = {"id": "gaussian_fit_worker_3", "config": config}
        worker_manager._workers = {"gaussian_fit_worker_3": {"config": {}, "worker": w3_mock}}
        worker_manager.update_config(BECMessage.DAPConfigMessage(config={"workers": []}))
        mock_start_worker.assert_not_called()
        w3_mock.terminate.assert_called_once()
        assert worker_manager._workers == {}
