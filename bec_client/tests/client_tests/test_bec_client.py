from unittest import mock

import IPython
import pytest
from bec_lib import RedisConnector, ServiceConfig
from bec_lib.tests.utils import ConnectorMock, bec_client, dm, dm_with_devices

from bec_client import BECIPythonClient


def test_ipython_device_completion(bec_client):
    client = bec_client
    client.start()
    shell = IPython.terminal.interactiveshell.TerminalInteractiveShell.instance()
    shell.user_ns["dev"] = client.device_manager.devices
    completer = IPython.get_ipython().Completer
    assert "dev.samx" in completer.all_completions("dev.sa")
    assert len(completer.all_completions("dev.sa")) == 3


def test_ipython_device_completion_property_access(bec_client):
    client = bec_client
    client.start()
    shell = IPython.terminal.interactiveshell.TerminalInteractiveShell.instance()
    shell.user_ns["dev"] = client.device_manager.devices
    completer = IPython.get_ipython().Completer
    assert "dev.samx.dummy_controller.some_var" in completer.all_completions(
        "dev.samx.dummy_controller.som"
    )


@pytest.fixture
def service_config():
    return ServiceConfig(
        redis={"host": "localhost", "port": 5000},
        scibec={"host": "localhost", "port": 5001},
        mongodb={"host": "localhost", "port": 50002},
    )


@pytest.fixture
def ipython_client(service_config):
    client = BECIPythonClient(
        config=service_config,
        connector_cls=mock.MagicMock(spec=RedisConnector),
        wait_for_server=False,
    )
    yield client
    client.shutdown()
    client._client._reset_singleton()


def test_bec_client_initialize(ipython_client):
    with mock.patch.object(ipython_client, "_load_scans"):
        with mock.patch.object(ipython_client, "wait_for_service"):
            ipython_client.start()
            assert ipython_client.started is True


def test_bec_client_start(service_config):
    client = BECIPythonClient(
        config=service_config,
        connector_cls=mock.MagicMock(spec=RedisConnector),
        wait_for_server=True,
    )
    with mock.patch.object(client._client, "wait_for_service") as wait_for_service:
        with mock.patch.object(client, "_start_exit_handler") as start_exit_handler:
            with mock.patch.object(client, "_configure_ipython") as configure_ipython:
                with mock.patch.object(client, "_load_scans"):
                    client.start()
                    start_exit_handler.assert_called_once()
                    configure_ipython.assert_called_once()
                    assert mock.call("ScanBundler", mock.ANY) in wait_for_service.call_args_list
                    assert mock.call("ScanServer", mock.ANY) in wait_for_service.call_args_list
                    assert mock.call("DeviceServer", mock.ANY) in wait_for_service.call_args_list


def test_bec_client_start_without_bec_services(ipython_client):
    client = ipython_client
    with mock.patch.object(client, "wait_for_service") as wait_for_service:
        with mock.patch.object(client, "_start_exit_handler") as start_exit_handler:
            with mock.patch.object(client, "_configure_ipython") as configure_ipython:
                with mock.patch.object(client, "_load_scans"):
                    client.start()
                    start_exit_handler.assert_called_once()
                    configure_ipython.assert_called_once()
                    wait_for_service.assert_not_called()
