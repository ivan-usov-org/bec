from unittest import mock

import lmfit
import pytest

from data_processing.lmfit1d_service import LmfitService1D


@pytest.fixture
def lmfit_service():
    yield LmfitService1D(model="GaussianModel", continuous=False, bec_client=mock.MagicMock())


@pytest.mark.parametrize("model, exists", [("GaussianModel", True), ("ModelDoesntExist", False)])
def test_LmfitService1D(model, exists):
    client = mock.MagicMock()
    if exists:
        service = LmfitService1D(model=model, bec_client=client)
        return
    with pytest.raises(AttributeError):
        service = LmfitService1D(model=model, bec_client=client)


def test_LmfitService1D_available_models(lmfit_service):
    models = lmfit_service.available_models()
    assert len(models) > 0
    assert all(issubclass(model, lmfit.model.Model) for model in models)
    assert all(
        model.__name__ not in ["Gaussian2dModel", "ExpressionModel", "Model", "SplineModel"]
        for model in models
    )


def test_LmfitService1D_get_provided_services(lmfit_service):
    services = lmfit_service.get_provided_services()
    assert isinstance(services, dict)
    assert len(services) > 0
    for model, service in services.items():
        assert isinstance(service, dict)
        assert "class" in service
        assert "user_friendly_name" in service
        assert "class_doc" in service
        assert "fit_doc" in service


def test_LmfitService1D_get_data_from_current_scan_without_devices(lmfit_service):
    scan_item = mock.MagicMock()
    scan_item.data = mock.MagicMock()
    scan_item.data[0].metadata = {"scan_report_devices": ["device_x", "device_y"]}

    data = lmfit_service.get_data_from_current_scan(scan_item)
    assert data is None


def test_LmfitService1D_get_data_from_current_scan(lmfit_service):
    scan_item = mock.MagicMock()
    scan_item.data = mock.MagicMock()
    lmfit_service.device_x = "device_x"
    lmfit_service.signal_x = "signal_x"
    lmfit_service.device_y = "device_y"
    lmfit_service.signal_y = "signal_y"

    scan_item.data = {
        "device_x": {"signal_x": {"value": [1, 2, 3], "timestamp": 0}},
        "device_y": {"signal_y": {"value": [4, 5, 6], "timestamp": 0}},
    }
    data = lmfit_service.get_data_from_current_scan(scan_item)
    assert data == {"x": [1, 2, 3], "y": [4, 5, 6]}


def test_LmfitService1D_process(lmfit_service):
    lmfit_service.data = {"x": [1, 2, 3], "y": [4, 5, 6]}
    lmfit_service.model = mock.MagicMock()

    result = lmfit_service.process()
    assert isinstance(result, tuple)
    assert isinstance(result[0], dict)
    assert isinstance(result[1], dict)
    lmfit_service.model.fit.assert_called_once_with([4, 5, 6], x=[1, 2, 3])
