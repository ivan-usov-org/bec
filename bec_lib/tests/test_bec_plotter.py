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
