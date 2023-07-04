from unittest import mock

import IPython
from bec_lib.core import RedisConnector, ServiceConfig
from bec_lib.core.tests.utils import bec_client

from bec_client import BECIPythonClient

CONFIG_PATH = "../ci/test_config.yaml"


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
    config = ServiceConfig(CONFIG_PATH)
    client.initialize(config, RedisConnector)


def test_bec_client_start():
    client = BECIPythonClient()
    config = ServiceConfig(CONFIG_PATH)
    client.initialize(config, RedisConnector)

    with mock.patch.object(client, "wait_for_service") as wait_for_service:
        with mock.patch.object(client, "_start_exit_handler"):
            with mock.patch.object(client, "_configure_ipython"):
                client.start()
                client._start_exit_handler.assert_called_once()
                client._configure_ipython.assert_called_once()
                wait_for_service.assert_called_once_with("DeviceServer")
