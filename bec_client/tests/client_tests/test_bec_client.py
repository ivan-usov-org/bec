from unittest import mock

import IPython
from bec_lib.core import RedisConnector, ServiceConfig
from bec_lib.core.tests.utils import ConnectorMock, bec_client

from bec_client import BECIPythonClient


def test_ipython_device_completion(bec_client):
    client = bec_client
    client.start()
    shell = IPython.terminal.interactiveshell.TerminalInteractiveShell.instance()
    shell.user_ns["dev"] = client.device_manager.devices
    completer = IPython.get_ipython().Completer
    assert "dev.samx" in completer.all_completions("dev.sa")
    assert len(completer.all_completions("dev.sa")) == 3


def test_bec_client_initialize():
    client = BECIPythonClient()
    config = ServiceConfig(
        redis={"host": "localhost", "port": 6379},
        scibec={"host": "localhost", "port": 5000},
        mongodb={"host": "localhost", "port": 50001},
    )
    client.initialize(config, RedisConnector)


def test_bec_client_start():
    client = BECIPythonClient()
    config = ServiceConfig(
        redis={"host": "localhost", "port": 6379},
        scibec={"host": "localhost", "port": 5000},
        mongodb={"host": "localhost", "port": 50001},
    )
    client.initialize(config, RedisConnector)
    client.connector = ConnectorMock("")

    with mock.patch.object(client, "wait_for_service") as wait_for_service:
        with mock.patch.object(client, "_start_exit_handler") as start_exit_handler:
            with mock.patch.object(client, "_configure_ipython") as configure_ipython:
                client.start()
                start_exit_handler.assert_called_once()
                configure_ipython.assert_called_once()
                wait_for_service.assert_called_once_with("DeviceServer")
