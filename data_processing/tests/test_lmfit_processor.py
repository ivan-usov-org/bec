from unittest import mock

import numpy as np
import pytest

from data_processing.stream_processor import LmfitProcessor


def test_LmfitProcessor_get_model_needs_config():
    """
    Test the LmfitProcessor class get_model method.
    """
    connector = mock.MagicMock()
    with pytest.raises(ValueError):
        LmfitProcessor(connector, {})


def test_LmfitProcessor_get_model_returns_correct_model():
    """
    Test the LmfitProcessor class get_model method.
    """
    connector = mock.MagicMock()
    config = {"model": "GaussianModel"}
    processor = LmfitProcessor(connector, config)
    assert processor.model.name == "Model(gaussian)"


def test_LmfitProcessor_process_gaussian():
    """
    Test the LmfitProcessor class process method with a gaussian model.
    """
    connector = mock.MagicMock()
    config = {"model": "GaussianModel", "input_xy": ["x", "y"], "output": "gaussian_fit"}
    processor = LmfitProcessor(connector, config)
    processor.data = {"x": [1, 2, 3], "y": [1, 2, 3]}
    data = {"data": {"x": 4, "y": 4}}
    metadata = {}
    result_data, result_metadata = processor.process(data, metadata)
    assert np.allclose(result_data["gaussian_fit"], processor.data["y"], atol=0.1)
    assert {"amplitude", "sigma", "center"} & set(result_metadata["fit_parameters"]) == {
        "amplitude",
        "sigma",
        "center",
    }
    assert len(processor.data["x"]) == 4
    assert len(processor.data["y"]) == 4


def test_LmfitProcessor_resets_scan_data():
    """
    Test the LmfitProcessor class make sure it resets the data when the scan id changes.
    """
    connector = mock.MagicMock()
    config = {"model": "GaussianModel", "input_xy": ["x", "y"], "output": "gaussian_fit"}
    processor = LmfitProcessor(connector, config)
    processor.data = {"x": [1, 2, 3], "y": [1, 2, 3]}
    data = {"data": {"x": 4, "y": 4}, "scanID": 1}
    metadata = {}
    result = processor.process(data, metadata)
    assert result is None
    assert len(processor.data["x"]) == 1


def test_LmfitProcessor_resets_scan_data_with_existing_id():
    """
    Test the LmfitProcessor class to make sure it resets the data when the scan id changes.
    """
    connector = mock.MagicMock()
    config = {"model": "GaussianModel", "input_xy": ["x", "y"], "output": "gaussian_fit"}
    processor = LmfitProcessor(connector, config)
    processor.scan_id = 1
    processor.data = {"x": [1, 2, 3], "y": [1, 2, 3]}
    data = {"data": {"x": 4, "y": 4}, "scanID": 2}
    metadata = {}
    result = processor.process(data, metadata)
    assert result is None
    assert len(processor.data["x"]) == 1
