from unittest import mock

import pytest
from .utils import get_bec_client_mock
from bec_utils import Alarms
from bec_client.config_helper import ConfigHelper
from bec_client.scan_manager import ScanManager

from bec_client.alarm_handler import AlarmHandler
import IPython


def test_username():
    client = get_bec_client_mock()

    assert client.username == client._username


def test_start():
    client = get_bec_client_mock()
    assert client._initialized == True
    # if not client._initialized:
    #     raise RuntimeError("Client has not been initialized yet.")

    client._start_device_manager = mock.MagicMock()
    client._start_exit_handler = mock.MagicMock()
    client._configure_ipython = mock.MagicMock()
    client._start_scan_queue = mock.MagicMock()
    client._start_alarm_handler = mock.MagicMock()
    client._configure_logger = mock.MagicMock()
    client.load_all_user_scripts = mock.MagicMock()

    client.start()

    # client._start_device_manager.assert_called_once()
    # client._start_exit_handler.assert_called_once()
    # client._configure_ipython.assert_called_once()
    client._start_scan_queue.assert_called_once()
    # client._start_alarm_handler.assert_called_once()
    # client._configure_logger.assert_called_once()
    # client.load_all_user_scripts.assert_called_once()
    # assert client.config == ConfigHelper(client)


def test_start_scan_queue():
    client = get_bec_client_mock()

    assert client.queue == None

    client._start_scan_queue()

    # assert isinstance(client.queue, ScanManager)


def test_alarms():
    client = get_bec_client_mock()
    assert client.alarm_handler == None
    assert next(client.alarms()) == []

    client.alarm_handler = AlarmHandler(client.connector)
    # assert next(client.alarm_handler.get_alarm(severity=Alarms.WARNING)) == StopIteration
    assert isinstance(client.alarm_handler, AlarmHandler)
    # assert next(client.alarms()) == 1


def test_set_ipython_prompt_scan_number():
    client = get_bec_client_mock()
    assert client._ip == None
    client._ip = IPython.get_ipython()
    client._set_ipython_prompt_scan_number(233)
    if client._ip:
        assert client._ip.prompts.scan_number == 233 + 1
