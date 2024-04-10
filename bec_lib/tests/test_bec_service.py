import contextlib
import os
from pathlib import Path
from unittest import mock

import pytest

import bec_lib
from bec_lib import bec_logger, messages
from bec_lib.bec_service import BECService
from bec_lib.endpoints import MessageEndpoints
from bec_lib.messages import BECStatus
from bec_lib.service_config import ServiceConfig

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

dir_path = os.path.dirname(bec_lib.__file__)


@contextlib.contextmanager
def bec_service(config, connector_cls=None, **kwargs):
    if connector_cls is None:
        connector_cls = mock.MagicMock()
    service = BECService(config=config, connector_cls=connector_cls, **kwargs)
    try:
        yield service
    finally:
        service.shutdown()
        bec_logger.logger.remove()
        bec_logger._reset_singleton()


def test_bec_service_init_with_service_config():
    config = ServiceConfig(redis={"host": "localhost", "port": 6379})
    with bec_service(config) as service:
        assert service._service_config == config
        assert service.bootstrap_server == "localhost:6379"
        assert service._unique_service is False


def test_bec_service_init_raises_for_invalid_config():
    with pytest.raises(TypeError):
        with bec_service(mock.MagicMock()):
            ...


def test_bec_service_init_with_service_config_path():
    with bec_service(config=f"{dir_path}/tests/test_service_config.yaml") as service:
        assert isinstance(service._service_config, ServiceConfig)
        assert service.bootstrap_server == "localhost:6379"
        assert service._unique_service is False


def test_init_runs_service_check():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        with bec_service(f"{dir_path}/tests/test_service_config.yaml", unique_service=True):
            mock_update_existing_services.assert_called_once()


def test_run_service_check_raises_for_existing_service():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        with bec_service(
            f"{dir_path}/tests/test_service_config.yaml", unique_service=True
        ) as service:
            service._services_info = {"BECService": mock.MagicMock()}
            with pytest.raises(RuntimeError):
                service._run_service_check(timeout_time=0, elapsed_time=10)


def test_run_service_check_repeats():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        with bec_service(
            f"{dir_path}/tests/test_service_config.yaml", unique_service=True
        ) as service:
            service._services_info = {"BECService": mock.MagicMock()}
            assert service._run_service_check(timeout_time=0.5, elapsed_time=0) is True


def test_bec_service_service_status():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        with bec_service(
            f"{dir_path}/tests/test_service_config.yaml", unique_service=True
        ) as service:
            mock_update_existing_services.reset_mock()
            status = service.service_status
            mock_update_existing_services.assert_called_once()


def test_bec_service_update_existing_services():
    service_keys = [
        MessageEndpoints.service_status("service1").endpoint.encode(),
        MessageEndpoints.service_status("service2").endpoint.encode(),
    ]
    service_msgs = [
        messages.StatusMessage(name="service1", status=BECStatus.RUNNING, info={}, metadata={}),
        messages.StatusMessage(name="service2", status=BECStatus.IDLE, info={}, metadata={}),
    ]
    connector_cls = mock.MagicMock()
    connector_cls().keys.return_value = service_keys
    connector_cls().get.side_effect = [msg for msg in service_msgs]
    with bec_service(
        f"{os.path.dirname(bec_lib.__file__)}/tests/test_service_config.yaml",
        connector_cls=connector_cls,
        unique_service=True,
    ) as service:
        assert service._services_info == {"service1": service_msgs[0], "service2": service_msgs[1]}


def test_bec_service_update_existing_services_ignores_wrong_msgs():
    service_keys = [
        MessageEndpoints.service_status("service1").endpoint.encode(),
        MessageEndpoints.service_status("service2").endpoint.encode(),
    ]
    service_msgs = [
        messages.StatusMessage(name="service1", status=BECStatus.RUNNING, info={}, metadata={}),
        None,
    ]
    connector_cls = mock.MagicMock()
    connector_cls().keys.return_value = service_keys
    connector_cls().get.side_effect = [service_msgs[0], None]
    with bec_service(
        f"{os.path.dirname(bec_lib.__file__)}/tests/test_service_config.yaml",
        connector_cls=connector_cls,
        unique_service=True,
    ) as service:
        assert service._services_info == {"service1": service_msgs[0]}


def test_bec_service_default_config():
    with bec_service(
        f"{os.path.dirname(bec_lib.__file__)}/tests/test_service_config.yaml", unique_service=True
    ) as service:
        assert service._service_config.service_config["file_writer"]["base_path"] == "./"

    config = ServiceConfig(redis={"host": "localhost", "port": 6379})
    with bec_service(config=config, unique_service=True) as service:
        assert os.path.abspath(
            service._service_config.service_config["file_writer"]["base_path"]
        ) == str(Path(bec_lib.service_config.__file__).resolve().parent.parent.parent)
