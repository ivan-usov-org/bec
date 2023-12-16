from unittest import mock

import pytest

from bec_lib import MessageEndpoints, messages
from bec_lib.bec_plotter import BECPlotter, BECWidgetsConnector


@pytest.fixture
def bec_client():
    client = mock.MagicMock()
    yield client


def test_bec_widgets_connector_set_plot_config(bec_client):
    connector = BECWidgetsConnector(bec_client)
    config = {"x": "test", "y": "test", "color": "test", "size": "test", "shape": "test"}
    connector.set_plot_config(plot_id="plot_id", config=config)
    msg = messages.GUIConfigMessage(config=config).dumps()
    bec_client.connector.producer().set_and_publish.assert_called_once_with(
        MessageEndpoints.gui_config("plot_id"), msg
    ) is None


def test_bec_widgets_connector_close(bec_client):
    connector = BECWidgetsConnector(bec_client)
    connector.close("plot_id")
    msg = messages.GUIInstructionMessage(action="close", parameter={}).dumps()
    bec_client.connector.producer().set_and_publish.assert_called_once_with(
        MessageEndpoints.gui_instructions("plot_id"), msg
    )


def test_bec_widgets_connector_send_data(bec_client):
    connector = BECWidgetsConnector(bec_client)
    data = {"x": [1, 2, 3], "y": [1, 2, 3]}
    connector.send_data("plot_id", data)
    msg = messages.GUIDataMessage(data=data).dumps()
    bec_client.connector.producer().xadd.assert_called_once_with(
        MessageEndpoints.gui_data("plot_id"), {"data": msg}
    )


def test_bec_widgets_connector_clear(bec_client):
    connector = BECWidgetsConnector(bec_client)
    connector.clear("plot_id")
    msg = messages.GUIInstructionMessage(action="clear", parameter={}).dumps()
    bec_client.connector.producer().set_and_publish.assert_called_once_with(
        MessageEndpoints.gui_instructions("plot_id"), msg
    )


@pytest.fixture
def plotter(bec_client):
    widget_connector = BECWidgetsConnector(bec_client)
    plotter = BECPlotter("test", widget_connector=widget_connector)
    yield plotter


def test_bec_plotter_show(plotter):
    assert plotter._process is None
    with mock.patch.object(plotter, "_start_plot_process") as start_plot_process:
        plotter.show()
        start_plot_process.assert_called_once()


def test_bec_plotter_show_process_not_reset(plotter):
    assert plotter._process is None
    plotter._process = mock.MagicMock()
    with mock.patch.object(plotter, "_start_plot_process") as start_plot_process:
        with mock.patch.object(plotter._process, "poll", return_value=1) as poll:
            plotter.show()
            start_plot_process.assert_called_once()


def test_bec_plotter_refresh_config_changed(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        plotter._config_changed = True
        plotter.refresh()
        plot_connector.set_plot_config.assert_called_once_with(plotter._plot_id, plotter._config)


def test_bec_plotter_refresh_config_didnt_change(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        plotter._config_changed = False
        plotter.refresh()
        plot_connector.set_plot_config.assert_not_called()


def test_bec_plotter_refresh_data_changed(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        plotter._data_changed = True
        data = {"x": plotter._xdata, "y": plotter._ydata}
        plotter.refresh()
        plot_connector.send_data.assert_called_once_with(plotter._plot_id, data)


def test_bec_plotter_refresh_data_didnt_change(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        plotter._data_changed = False
        plotter.refresh()
        plot_connector.send_data.assert_not_called()


def test_bec_plotter_clear(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        plotter.clear()
        plot_connector.clear.assert_called_once_with(plotter._plot_id)


def test_bec_plotter_close(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        process = mock.MagicMock()
        plotter._process = process
        plotter.close()
        plot_connector.close.assert_called_once_with(plotter._plot_id)
        process.kill.assert_called_once()
        assert plotter._process is None


def test_bec_plotter_close_process_not_called(plotter):
    with mock.patch.object(plotter, "plot_connector") as plot_connector:
        plotter._process = None
        plotter.close()
        plotter.plot_connector.close.assert_not_called()


def test_bec_plotter_set_xdata(plotter):
    with mock.patch.object(plotter, "_set_source_to_redis") as set_source_to_redis:
        plotter.set_xdata([1, 2, 3])
        set_source_to_redis.assert_called_once_with("x")
        assert plotter._xdata == {"action": "set", "data": [1, 2, 3]}


def test_bec_plotter_set_ydata(plotter):
    with mock.patch.object(plotter, "_set_source_to_redis") as set_source_to_redis:
        plotter.set_ydata([1, 2, 3])
        set_source_to_redis.assert_called_once_with("y", 0)
        assert plotter._ydata == {0: {"action": "set", "data": [1, 2, 3]}}


def test_bec_plotter_set_xsource(plotter):
    assert plotter._config_changed is False
    plotter.set_xsource("samx")
    assert plotter._config["plot_data"][0]["sources"][0]["signals"]["x"][0]["name"] == "samx"
    assert plotter._config_changed is True


def test_bec_plotter_set_ysource(plotter):
    assert plotter._config_changed is False
    plotter.set_ysource("samy")
    assert plotter._config["plot_data"][0]["sources"][0]["signals"]["y"][0]["name"] == "samy"
    assert plotter._config_changed is True


def test_bec_plotter_set_xlabel(plotter):
    assert plotter._config_changed is False
    plotter.set_xlabel("samx")
    assert plotter._config["plot_data"][0]["x_label"] == "samx"
    assert plotter._config_changed is True


def test_bec_plotter_set_ylabel(plotter):
    assert plotter._config_changed is False
    plotter.set_ylabel("samy")
    assert plotter._config["plot_data"][0]["y_label"] == "samy"
    assert plotter._config_changed is True


# def test_bec_plotter_set_source_to_redis(plotter):
#     config = plotter._config["plot_data"][0]["x"]["signals"][0]
#     config["source"] = "scan_segment"
#     plotter._set_source_to_redis("x")
#     assert plotter._config_changed is True
#     assert config["source"] == "redis"
#     assert config["endpoint"] == MessageEndpoints.gui_data(plotter._plot_id)
#
#
# def test_bec_plotter_set_source_to_redis_no_change(plotter):
#     config = plotter._config["plot_data"][0]["x"]["signals"][0]
#     config["source"] = "redis"
#     config["endpoint"] = MessageEndpoints.gui_data(plotter._plot_id)
#     plotter._set_source_to_redis("x")
#     assert plotter._config_changed is False


def test_bec_plotter_append_xdata(plotter):
    with mock.patch.object(plotter, "_set_source_to_redis") as set_source_to_redis:
        plotter.append_xdata([1, 2, 3])
        set_source_to_redis.assert_called_once_with("x")
        assert plotter._xdata == {"action": "append", "data": [1, 2, 3]}
        assert plotter._data_changed is True


def test_bec_plotter_append_ydata(plotter):
    with mock.patch.object(plotter, "_set_source_to_redis") as set_source_to_redis:
        plotter.append_ydata([1, 2, 3])
        set_source_to_redis.assert_called_once_with("y", 0)
        assert plotter._ydata == {0: {"action": "append", "data": [1, 2, 3]}}
        assert plotter._data_changed is True


def test_bec_plotter_set_xydata(plotter):
    with mock.patch.object(plotter, "_set_source_to_redis") as set_source_to_redis:
        plotter.set_xydata([1, 2, 3], [1, 2, 3])
        assert plotter._xdata == {"action": "set", "data": [1, 2, 3]}
        assert plotter._data_changed is True
        assert plotter._ydata == {0: {"action": "set", "data": [1, 2, 3]}}
        assert plotter._data_changed is True


def test_bec_plotter_append_xydata(plotter):
    with mock.patch.object(plotter, "_set_source_to_redis") as set_source_to_redis:
        plotter.append_xydata([1, 2, 3], [1, 2, 3])
        assert plotter._xdata == {"action": "append", "data": [1, 2, 3]}
        assert plotter._data_changed is True
        assert plotter._ydata == {0: {"action": "append", "data": [1, 2, 3]}}
        assert plotter._data_changed is True


def test_bec_plotter_print_log(plotter):
    with mock.patch.object(plotter, "_get_stderr_output") as get_stderr_output:
        plotter._process = mock.MagicMock()
        plotter.print_log()
        get_stderr_output.assert_called_once()


def test_bec_plotter_print_log_not_called(plotter):
    with mock.patch.object(plotter, "_get_stderr_output") as get_stderr_output:
        plotter.print_log()
        get_stderr_output.assert_not_called()


def test_bec_plotter_get_stderr_output(plotter):
    plotter._process = mock.MagicMock()
    plotter._process.poll.return_value = [1, None]
    with mock.patch("bec_lib.bec_plotter.select") as select:
        select.select.side_effect = [
            (mock.MagicMock(), None, None),
            (mock.MagicMock(), None, None),
            (None, None, None),
        ]
        plotter._process.stderr.readline.side_effect = [b"test", b"2", None]
        out = plotter._get_stderr_output()
        plotter._process.stderr.readline.call_count == 2
    assert out == "test2"
