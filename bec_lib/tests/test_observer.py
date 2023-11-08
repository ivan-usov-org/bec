import os
from unittest import mock

import pytest
import yaml

import bec_lib
from bec_lib.core import BECMessage, MessageEndpoints
from bec_lib.core.devicemanager import DeviceManagerBase
from bec_lib.core.observer import Observer, ObserverManager
from bec_lib.core.tests.utils import ConnectorMock, create_session_from_config

dir_path = os.path.dirname(bec_lib.__file__)


@pytest.mark.parametrize(
    "kwargs,raised_error",
    [
        (
            {
                "name": "stop scan if ring current drops",
                "device": "ring_current",
                "on_trigger": "pause",
                "on_resume": "restart",
            },
            AttributeError,
        ),
        (
            {
                "name": "stop scan if ring current drops",
                "device": "ring_current",
                "on_trigger": "pause",
                "on_resume": "whatever",
            },
            ValueError,
        ),
        (
            {
                "name": "stop scan if ring current drops",
                "device": "ring_current",
                "on_trigger": "pause",
                "on_resume": "restart",
                "limits": [380, 420],
            },
            None,
        ),
        (
            {
                "name": "stop scan if ring current drops",
                "device": "ring_current",
                "on_trigger": "pause",
                "on_resume": "restart",
                "limits": [380, 420],
                "target_value": 20,
            },
            AttributeError,
        ),
        (
            {
                "name": "stop scan if ring current drops",
                "device": "ring_current",
                "on_trigger": "pause",
                "on_resume": "restart",
                "limits": 20,
            },
            TypeError,
        ),
        (
            {
                "name": "stop scan if ring current drops",
                "device": "ring_current",
                "on_trigger": "pause",
                "on_resume": "restart",
                "limits": [380, 420],
                "low_limit": 20,
            },
            AttributeError,
        ),
    ],
)
def test_observer(kwargs, raised_error):
    if not raised_error:
        observer = Observer(**kwargs)
        return
    with pytest.raises(raised_error):
        observer = Observer(**kwargs)


@pytest.fixture()
def device_manager():
    connector = ConnectorMock("")
    dm = DeviceManagerBase(connector, "")
    with open(f"{dir_path}/core/tests/test_config.yaml", "r") as f:
        dm._session = create_session_from_config(yaml.safe_load(f))
    dm._load_session()
    with mock.patch.object(dm, "_get_config"):
        dm.initialize("")
    return dm


def test_observer_manager_None(device_manager):
    with mock.patch.object(device_manager.producer, "get", return_value=None) as producer_get:
        observer_manager = ObserverManager(device_manager=device_manager)
        producer_get.assert_called_once_with(MessageEndpoints.observer())
        assert len(observer_manager._observer) == 0


def test_observer_manager_msg(device_manager):
    msg = BECMessage.ObserverMessage(
        observer=[
            {
                "name": "test_observer",
                "device": "samx",
                "on_trigger": "pause",
                "on_resume": "restart",
                "limits": [380, None],
            }
        ]
    ).dumps()
    with mock.patch.object(device_manager.producer, "get", return_value=msg) as producer_get:
        observer_manager = ObserverManager(device_manager=device_manager)
        producer_get.assert_called_once_with(MessageEndpoints.observer())
        assert len(observer_manager._observer) == 1


@pytest.mark.parametrize(
    "observer,raises_error",
    [
        (
            Observer.from_dict(
                {
                    "name": "test_observer",
                    "device": "samx",
                    "on_trigger": "pause",
                    "on_resume": "restart",
                    "limits": [380, None],
                }
            ),
            False,
        )
    ],
)
def test_add_observer(device_manager, observer, raises_error):
    with mock.patch.object(device_manager.producer, "get", return_value=None) as producer_get:
        observer_manager = ObserverManager(device_manager=device_manager)
        observer_manager.add_observer(observer)
        with pytest.raises(AttributeError):
            observer_manager.add_observer(observer)


@pytest.mark.parametrize(
    "observer,raises_error",
    [
        (
            Observer.from_dict(
                {
                    "name": "test_observer",
                    "device": "samx",
                    "on_trigger": "pause",
                    "on_resume": "restart",
                    "limits": [380, None],
                }
            ),
            True,
        ),
        (
            Observer.from_dict(
                {
                    "name": "test_observer",
                    "device": "samy",
                    "on_trigger": "pause",
                    "on_resume": "restart",
                    "limits": [380, None],
                }
            ),
            False,
        ),
    ],
)
def test_add_observer_existing_device(device_manager, observer, raises_error):
    default_observer = Observer.from_dict(
        {
            "name": "test_observer",
            "device": "samx",
            "on_trigger": "pause",
            "on_resume": "restart",
            "limits": [380, None],
        }
    )
    with mock.patch.object(device_manager.producer, "get", return_value=None) as producer_get:
        observer_manager = ObserverManager(device_manager=device_manager)
        observer_manager.add_observer(default_observer)
        if raises_error:
            with pytest.raises(AttributeError):
                observer_manager.add_observer(observer)
        else:
            observer_manager.add_observer(observer)
