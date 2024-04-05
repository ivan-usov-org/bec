import multiprocessing
from types import SimpleNamespace
from unittest import mock

import IPython
import pytest

from bec_client import BECIPythonClient, main
from bec_lib import RedisConnector, ServiceConfig


def test_bec_entry_point_globals_and_post_startup(tmpdir, capfd):
    file_to_execute = tmpdir / "post_startup.py"
    main.main_dict["startup"] = SimpleNamespace(__file__=file_to_execute)
    with open(file_to_execute, "w") as f:
        f.write(
            """
completer=get_ipython().Completer
import sys
print(completer.all_completions('bec.'), flush=True)
print(completer.all_completions('BECIP'), flush=True)
exit()
"""
        )
    p = multiprocessing.Process(target=main.main, kwargs={"wait_for_server": False})
    p.start()
    p.join()
    output = capfd.readouterr().out
    assert "bec.device_manager" in output  # just one of many completions
    assert (
        "BECIPythonClient" not in output
    )  # just to ensure something we don't want is really not there


def test_ipython_device_completion(bec_client_mock):
    client = bec_client_mock
    # disable history saving (which runs in a separate thread)
    with mock.patch("IPython.core.history.HistoryManager.enabled", False):
        shell = IPython.terminal.interactiveshell.TerminalInteractiveShell.instance()
        shell.user_ns["dev"] = client.device_manager.devices
        completer = IPython.get_ipython().Completer
        assert "dev.samx" in completer.all_completions("dev.sa")
        assert len(completer.all_completions("dev.sa")) == 3


def test_ipython_device_completion_property_access(bec_client_mock):
    client = bec_client_mock
    # disable history saving (which runs in a separate thread)
    with mock.patch("IPython.core.history.HistoryManager.enabled", False):
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


def test_bec_client_start(service_config):
    client = BECIPythonClient(
        config=service_config,
        connector_cls=mock.MagicMock(spec=RedisConnector),
        wait_for_server=True,
    )
    try:
        with mock.patch.object(client._client, "wait_for_service") as wait_for_service:
            with mock.patch.object(client, "_configure_ipython") as configure_ipython:
                with mock.patch.object(client, "_load_scans"):
                    client.start()
                    configure_ipython.assert_called_once()
                    assert mock.call("ScanBundler", mock.ANY) in wait_for_service.call_args_list
                    assert mock.call("ScanServer", mock.ANY) in wait_for_service.call_args_list
                    assert mock.call("DeviceServer", mock.ANY) in wait_for_service.call_args_list
                    assert client.started
    finally:
        client.shutdown()
        client._client._reset_singleton()


def test_bec_client_start_without_bec_services(ipython_client):
    client = ipython_client
    with mock.patch.object(client, "wait_for_service") as wait_for_service:
        with mock.patch.object(client, "_configure_ipython") as configure_ipython:
            with mock.patch.object(client, "_load_scans"):
                client.start()
                configure_ipython.assert_called_once()
                wait_for_service.assert_not_called()
