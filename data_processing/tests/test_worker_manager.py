from unittest import mock
from bec_lib import BECMessage

from bec_lib import MessageEndpoints
from bec_lib.redis_connector import MessageObject
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
            "worker_cls": "LmfitProcessor",
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
            "worker_cls": "LmfitProcessor",
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
            "worker_cls": "LmfitProcessor",
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


class DAPMockClass:
    def run(self):
        pass


class DAPMockWrongClass:
    def no_run(self):
        pass


def test_worker_manager_update_available_plugins():
    connector = mock.MagicMock()
    with mock.patch("data_processing.worker_manager.dap_plugins"):
        with mock.patch("data_processing.worker_manager.inspect.getmembers") as mock_getmembers:
            mock_getmembers.return_value = [
                ("CustomPlugin", DAPMockClass),
                ("WrongPlugin", DAPMockWrongClass),
            ]
            worker_manager = DAPWorkerManager(connector)
            assert "CustomPlugin" in worker_manager._worker_plugins
            assert "WrongPlugin" not in worker_manager._worker_plugins
            assert "LmfitProcessor" in worker_manager._worker_plugins


def test_worker_manager_start_worker():
    connector = mock.MagicMock()
    dap_plugin_cls = mock.MagicMock()
    with mock.patch.object(DAPWorkerManager, "_update_config"):
        with mock.patch.object(DAPWorkerManager, "run_worker") as mock_run_worker:
            worker_manager = DAPWorkerManager(connector)
            config = {
                "id": "gaussian_fit_worker_3",
                "config": {
                    "stream": "scan_segment",
                    "output": "gaussian_fit_worker_3",
                    "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
                    "model": "GaussianModel",
                    "worker_cls": "LmfitProcessor",
                },
            }
            worker_manager._start_worker(
                config,
                dap_plugin_cls,
            )
            assert "gaussian_fit_worker_3" in worker_manager._workers
            assert worker_manager._workers["gaussian_fit_worker_3"]["config"] == config["config"]
            mock_run_worker.assert_called_once_with(
                config["config"],
                worker_cls=dap_plugin_cls,
                connector_host=connector.bootstrap,
            )


def test_worker_manager_run_worker():
    with mock.patch("data_processing.worker_manager.mp") as mock_mp:
        worker_cls = mock.MagicMock()
        ret = DAPWorkerManager.run_worker(
            config={"stream": "scan_segment", "output": "gaussian_fit_worker_3"},
            worker_cls=worker_cls,
            connector_host=["localhost:6379"],
        )
        mock_mp.Process.assert_called_once_with(
            target=worker_cls.run,
            kwargs={
                "config": {"stream": "scan_segment", "output": "gaussian_fit_worker_3"},
                "connector_host": ["localhost:6379"],
            },
            daemon=True,
        )
        assert ret == mock_mp.Process()


def test_worker_manager_set_config():
    connector = mock.MagicMock()

    worker_manager = DAPWorkerManager(connector)
    msg = BECMessage.DAPConfigMessage(
        config={
            "workers": [
                {
                    "id": "gaussian_fit_worker_3",
                    "config": {
                        "stream": "scan_segment",
                        "output": "gaussian_fit_worker_3",
                        "input_xy": ["samx.samx.value", "gauss_bpm.gauss_bpm.value"],
                        "model": "GaussianModel",
                        "worker_cls": "LmfitProcessor",
                    },
                }
            ]
        }
    )
    msg_obj = MessageObject(msg.dumps(), MessageEndpoints.dap_config())
    with mock.patch.object(worker_manager, "update_config") as mock_update_config:
        msg_obj = MessageObject(msg.dumps(), MessageEndpoints.dap_config())
        worker_manager._set_config(msg_obj, worker_manager)
        mock_update_config.assert_called_once_with(msg)

        mock_update_config.reset_mock()
        msg_obj = MessageObject(None, MessageEndpoints.dap_config())
        worker_manager._set_config(msg_obj, worker_manager)
        mock_update_config.assert_not_called()


def test_worker_manager_shutdown():
    connector = mock.MagicMock()
    worker_manager = DAPWorkerManager(connector)
    worker_mock1 = mock.MagicMock()
    worker_mock2 = mock.MagicMock()
    worker_manager._workers = {
        "gaussian_fit_worker_1": {"worker": worker_mock1},
        "gaussian_fit_worker_2": {"worker": worker_mock2},
    }
    worker_manager.shutdown()
    worker_mock1.terminate.assert_called_once()
    worker_mock2.terminate.assert_called_once()
