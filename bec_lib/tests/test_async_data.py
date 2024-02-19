from unittest import mock

import numpy as np
import pytest

from bec_lib import messages
from bec_lib.async_data import AsyncDataHandler


@pytest.fixture
def async_data():
    producer = mock.MagicMock()
    yield AsyncDataHandler(producer)


def test_process_async_data_replace(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}},
                metadata={"async_update": "replace"},
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"].shape == (10, 10)


def test_process_async_multiple_signals(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={
                    "signal1": {"value": np.zeros((10, 10))},
                    "signal2": {"value": np.zeros((20, 20))},
                },
                metadata={"async_update": "replace"},
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["signal1"]["value"].shape == (10, 10)
    assert res["signal2"]["value"].shape == (20, 20)


def test_process_async_data_extend(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={"async_update": "extend"}
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"].shape == (100, 10)


def test_process_async_update_append(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={"async_update": "append"}
            )
        }
        for ii in range(10)
    ]
    res = async_data.process_async_data(data)
    assert res["data"][0]["value"].shape == (10, 10)
    assert len(res["data"]) == 10


def test_process_async_data_single(async_data):
    data = [
        {
            "data": messages.DeviceMessage(
                signals={"data": {"value": np.zeros((10, 10))}}, metadata={}
            )
        }
    ]
    res = async_data.process_async_data(data)
    assert res["data"]["value"].shape == (10, 10)
