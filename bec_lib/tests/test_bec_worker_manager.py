from unittest import mock

import pytest

from bec_lib.bec_worker_manager import BECWorker, BECWorkerManager
from bec_lib import BECMessage
from bec_lib.endpoints import MessageEndpoints


@pytest.fixture
def worker_manager():
    connector = mock.MagicMock()
    connector.producer().get.return_value = BECMessage.DAPConfigMessage(
        config={
            "workers": [
                {"id": "test", "config": {"test": "test"}},
                {"id": "test2", "config": {"test": "test"}},
            ]
        }
    ).dumps()
    yield BECWorkerManager(connector)


def test_bec_worker():
    """Test BECWorker class."""
    manager = mock.MagicMock()
    worker = BECWorker("test", {"test": "test"}, worker_manager=manager)
    assert worker.id == "test"
    assert worker.config == {"test": "test"}
    assert worker.to_dict() == {"id": "test", "config": {"test": "test"}}
    assert (
        BECWorker.from_dict({"id": "test", "config": {"test": "test"}}, worker_manager=manager)
        == worker
    )


def test_bec_worker_manager():
    connector = mock.MagicMock()
    with mock.patch("bec_lib.bec_worker_manager.BECWorkerManager._get_workers") as mock_get_workers:
        manager = BECWorkerManager(connector)
        mock_get_workers.assert_called_once()


def test_bec_worker_manager_get_worker(worker_manager):
    assert worker_manager.get_worker("test") == BECWorker("test", {"test": "test"})
    assert worker_manager.workers == [
        BECWorker("test", {"test": "test"}),
        BECWorker("test2", {"test": "test"}),
    ]
    assert worker_manager.num_workers == 2


def test_bec_worker_remove(worker_manager):
    worker_manager.remove_worker("test")
    assert worker_manager._workers == [BECWorker("test2", {"test": "test"})]
    worker_manager.remove_worker("test2")
    assert worker_manager._workers == []


def test_bec_worker_update_config(worker_manager):
    worker_manager._update_config()
    config = BECMessage.DAPConfigMessage(
        config={
            "workers": [
                {"id": "test", "config": {"test": "test"}},
                {"id": "test2", "config": {"test": "test"}},
            ]
        }
    ).dumps()
    worker_manager.producer.set_and_publish.assert_called_once_with(
        MessageEndpoints.dap_config(), config
    )


def test_bec_worker_add_worker(worker_manager):
    worker_manager.add_worker("test3", {"test": "test"})
    assert worker_manager._workers == [
        BECWorker("test", {"test": "test"}),
        BECWorker("test2", {"test": "test"}),
        BECWorker("test3", {"test": "test"}),
    ]
    worker_manager.add_worker("test4", {"test4": "test4"})
    assert worker_manager._workers == [
        BECWorker("test", {"test": "test"}),
        BECWorker("test2", {"test": "test"}),
        BECWorker("test3", {"test": "test"}),
        BECWorker("test4", {"test4": "test4"}),
    ]
    with pytest.raises(ValueError):
        worker_manager.add_worker("test", {"test": "test"})


def test_bec_worker_update_worker(worker_manager):
    worker_manager.update_worker("test", {"test": "test"})
    assert worker_manager._workers == [
        BECWorker("test", {"test": "test"}),
        BECWorker("test2", {"test": "test"}),
    ]
    worker_manager.update_worker("test2", {"test": "test2"})
    assert worker_manager._workers == [
        BECWorker("test", {"test": "test"}),
        BECWorker("test2", {"test": "test2"}),
    ]
    with pytest.raises(ValueError):
        worker_manager.update_worker("test3", {"test": "test"})
