import os
from unittest import mock

import pytest

import bec_lib
from bec_lib.core import BECService, ServiceConfig

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


def test_bec_service_init_with_service_config():
    config = ServiceConfig(redis={"host": "localhost", "port": 6379})
    service = BECService(config=config, connector_cls=mock.MagicMock())
    assert service._service_config == config
    assert service.bootstrap_server == "localhost:6379"
    assert service._unique_service is False


def test_bec_service_init_raises_for_invalid_config():
    with pytest.raises(TypeError):
        BECService(config=mock.MagicMock(), connector_cls=mock.MagicMock())


def test_bec_service_init_with_service_config_path():
    service = BECService(
        config=f"{os.path.dirname(bec_lib.__file__)}/core/tests/test_service_config.yaml",
        connector_cls=mock.MagicMock(),
    )
    assert isinstance(service._service_config, ServiceConfig)
    assert service.bootstrap_server == "localhost:6379"
    assert service._unique_service is False


def test_init_runs_service_check():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        service = BECService(
            config=f"{os.path.dirname(bec_lib.__file__)}/core/tests/test_service_config.yaml",
            connector_cls=mock.MagicMock(),
            unique_service=True,
        )
        mock_update_existing_services.assert_called_once()


def test_run_service_check_raises_for_existing_service():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        service = BECService(
            config=f"{os.path.dirname(bec_lib.__file__)}/core/tests/test_service_config.yaml",
            connector_cls=mock.MagicMock(),
            unique_service=True,
        )
        service._services_info = {"BECService": mock.MagicMock()}
        with pytest.raises(RuntimeError):
            service._run_service_check(timeout_time=0, elapsed_time=10)


def test_run_service_check_repeats():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        service = BECService(
            config=f"{os.path.dirname(bec_lib.__file__)}/core/tests/test_service_config.yaml",
            connector_cls=mock.MagicMock(),
            unique_service=True,
        )
        service._services_info = {"BECService": mock.MagicMock()}
        assert service._run_service_check(timeout_time=0.5, elapsed_time=0) is True


def test_bec_service_shutdown():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        service = BECService(
            config=f"{os.path.dirname(bec_lib.__file__)}/core/tests/test_service_config.yaml",
            connector_cls=mock.MagicMock(),
            unique_service=True,
        )
        service._service_info_event = mock.MagicMock()
        service._metrics_emitter_event = mock.MagicMock()
        service._service_info_thread = mock.MagicMock()
        service._metrics_emitter_thread = mock.MagicMock()

        service.shutdown()
        service._service_info_event.set.assert_called_once()
        service._metrics_emitter_event.set.assert_called_once()
        service._service_info_thread.join.assert_called_once()
        service._metrics_emitter_thread.join.assert_called_once()


def test_bec_service_service_status():
    with mock.patch.object(
        BECService, "_update_existing_services", return_value=False
    ) as mock_update_existing_services:
        service = BECService(
            config=f"{os.path.dirname(bec_lib.__file__)}/core/tests/test_service_config.yaml",
            connector_cls=mock.MagicMock(),
            unique_service=True,
        )
        mock_update_existing_services.reset_mock()
        status = service.service_status
        mock_update_existing_services.assert_called_once()
