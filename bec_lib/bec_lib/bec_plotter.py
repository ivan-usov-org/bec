import builtins
import importlib
import json
import select

# import multiprocessing
import subprocess

# import sys
import uuid
from typing import List, Union

# from qtpy.QtWidgets import QApplication
from typeguard import typechecked

from bec_lib import BECClient, MessageEndpoints, messages

DEFAULT_CONFIG = {
    "plot_settings": {
        "background_color": "white",
        "axis_width": 2,
        "num_columns": 5,
        "colormap": "plasma",
        "scan_types": False,
    },
    "plot_data": [
        {
            "plot_name": "BPM4i plots vs samx",
            "x": {"label": "Motor Y", "signals": [{"name": "samx"}]},
            "y": {"label": "bpm4i", "signals": [{"name": "bpm4i"}]},
        }
    ],
}


class BECWidgetsConnector:
    """
    A class to connect to the BEC widgets.
    """

    def __init__(self, bec_client: BECClient = None) -> None:
        self._client = bec_client

        # TODO replace with a global producer
        if self._client is None:
            if "bec" in builtins.__dict__:
                self._client = builtins.bec
            else:
                self._client = BECClient()
                self._client.start()
        self._producer = self._client.connector.producer()

    def set_plot_config(self, plot_id: str, config: dict) -> None:
        """
        Set the plot config.

        Args:
            plot_id (str): The id of the plot.
            config (dict): The config to set.
        """
        msg = messages.GUIConfigMessage(config=config)
        self._producer.set_and_publish(MessageEndpoints.gui_config(plot_id), msg.dumps())

    def close(self, plot_id: str) -> None:
        """
        Close the plot.

        Args:
            plot_id (str): The id of the plot.
        """
        msg = messages.GUIInstructionMessage(action="close", parameter={})
        self._producer.set_and_publish(MessageEndpoints.gui_instructions(plot_id), msg.dumps())

    def send_data(self, plot_id: str, data: dict) -> None:
        """
        Send data to the plot.

        Args:
            plot_id (str): The id of the plot.
            data (dict): The data to send.
        """
        msg = messages.GUIDataMessage(data=data)
        self._producer.xadd(MessageEndpoints.gui_data(plot_id), {"data": msg.dumps()})

    def clear(self, plot_id: str) -> None:
        """
        Clear the plot.

        Args:
            plot_id (str): The id of the plot.
        """
        msg = messages.GUIInstructionMessage(action="clear", parameter={})
        self._producer.set_and_publish(MessageEndpoints.gui_instructions(plot_id), msg.dumps())


class BECPlotter:
    """
    A class to plot data from the BEC. Internally, it uses redis to communicate with the plot running
    in a separate process.
    """

    def __init__(
        self, name: str, plot_id: str = None, widget_connector=None, default_config: dict = None
    ) -> None:
        """
        Initialize the BECPlotter.

        Args:
            name (str): The name of the plot.
            widget_connector (BECWidgetsConnector, optional): The plot connector to use. Defaults to None.
            default_config (dict, optional): The default config to use. Defaults to None.
            bec_client (BECClient, optional): The BECClient to use. Defaults to None.
        """
        self.name = name
        self._plot_id = (
            plot_id if plot_id is not None else str(uuid.uuid4())
        )  # Generate a unique id for the plot to be used in redis
        self._config = default_config if default_config is not None else DEFAULT_CONFIG
        self.plot_connector = (
            widget_connector if widget_connector is not None else BECWidgetsConnector()
        )

        self._process = None
        self._xdata = None
        self._ydata = {}
        self._data_changed = False
        self._config_changed = False

    @typechecked
    def set_xlabel(self, xlabel: str) -> None:
        """
        Set the xlabel of the figure.

        Args:
            xlabel (str): The xlabel to set.
        """
        self._config["plot_data"][0]["x"]["label"] = xlabel
        self._config_changed = True

    @typechecked
    def set_ylabel(self, ylabel: str, axis: int = 0) -> None:
        """
        Set the ylabel of the figure.

        Args:
            ylabel (str): The ylabel to set.
            axis (int, optional): The axis to set the ylabel for. Defaults to 0.
        """
        self._config["plot_data"][0]["y"]["label"] = ylabel
        self._config_changed = True

    @typechecked
    def set_xsource(self, source: str) -> None:
        """
        Set the source of the xdata of the figure.

        Args:
            source (str): The source to set. Must be either a valid device name
        """
        self._config["plot_data"][0]["x"]["signals"][0]["name"] = source
        self._config_changed = True

    @typechecked
    def set_ysource(self, source: str, axis: int = 0) -> None:
        """
        Set the source of the ydata of the figure.

        Args:
            source (str): The source to set. Must be either a valid device name
            axis (int, optional): The axis to set the ydata for. Defaults to 0.
        """
        self._config["plot_data"][0]["y"]["signals"][axis]["name"] = source
        self._config_changed = True

    @typechecked
    def set_xdata(self, xdata: List[float]) -> None:
        """
        Set the xdata of the figure.

        Args:
            xdata (List[float]): The xdata to set.
        """

        self._set_source_to_redis("x")

        # update data
        self._xdata = {"action": "set", "data": xdata}
        self._data_changed = True

    @typechecked
    def set_ydata(self, ydata: List[float], axis: int = 0) -> None:
        """
        Set the ydata of the figure.

        Args:
            ydata (List[float]): The ydata to set.
            axis (int, optional): The axis to set the ydata for. Defaults to 0.
        """
        self._set_source_to_redis("y", axis)

        # update data
        self._ydata[axis] = {"action": "set", "data": ydata}
        self._data_changed = True

    def _set_source_to_redis(self, axis: str, axis_id: int = 0) -> None:
        """
        Set the source of the data to redis.

        Args:
            axis (str): The axis to set the source for.
            axis_id (int, optional): The axis id to set the source for. Defaults to 0.
        """
        config = self._config["plot_data"][0][axis]["signals"][axis_id]
        if config["source"] != "redis" or config["endpoint"] != MessageEndpoints.gui_data(
            self._plot_id
        ):
            config.update({"source": "redis", "endpoint": MessageEndpoints.gui_data(self._plot_id)})
            self._config_changed = True

    @typechecked
    def append_xdata(self, xdata: Union[float, List[float]]) -> None:
        """
        Append the xdata to the figure. If xdata is a list, it the existing data will be extended by xdata.

        Args:
            xdata (Union[float,List[float]]): The xdata to append.

        """
        self._set_source_to_redis("x")

        # update data
        self._xdata = {"action": "append", "data": xdata}
        self._data_changed = True

    @typechecked
    def append_ydata(self, ydata: Union[float, List[float]], axis: int = 0) -> None:
        """
        Append the ydata to the figure. If ydata is a list, it the existing data will be extended by ydata.

        Args:
            ydata (Union[float,List[float]]): The ydata to append.
            axis (int, optional): The axis to append the ydata for. Defaults to 0.
        """
        self._set_source_to_redis("y", axis)

        # update data
        self._ydata[axis] = {"action": "append", "data": ydata}
        self._data_changed = True

    @typechecked
    def set_xydata(self, xdata: List[float], ydata: List[float], axis: int = 0) -> None:
        """
        Set the xdata and ydata of the figure.

        Args:
            xdata (List[float]): The xdata to set.
            ydata (List[float]): The ydata to set.
            axis (int, optional): The axis to set the ydata for. Defaults to 0.
        """
        self.set_xdata(xdata)
        self.set_ydata(ydata, axis)

    @typechecked
    def append_xydata(
        self, xdata: Union[float, List[float]], ydata: Union[float, List[float]]
    ) -> None:
        """
        Append the xdata and ydata to the figure. If xdata or ydata is a list, it the existing data will be extended
        by xdata or ydata.

        Args:
            xdata (Union[float,List[float]]): The xdata to append.
            ydata (Union[float,List[float]]): The ydata to append.
        """
        self.append_xdata(xdata)
        self.append_ydata(ydata)

    def clear(self) -> None:
        """
        Clear the figure.
        """
        self.plot_connector.clear(self._plot_id)

    def refresh(self) -> None:
        """
        Refresh the figure. This call is indempotent, i.e. multiple calls to refresh will not have any effect
        if the data has not changed.
        """
        if self._config_changed:
            self.plot_connector.set_plot_config(self._plot_id, self._config)
            self._config_changed = False
        if self._data_changed:
            data = {"x": self._xdata, "y": self._ydata}
            self.plot_connector.send_data(self._plot_id, data)
            self._data_changed = False
            self._xdata = None
            self._ydata = None

    def show(self) -> None:
        """
        Show the figure.
        """
        if self._process is None or self._process.poll() is not None:
            self._start_plot_process()

    def close(self) -> None:
        """
        Close the figure.
        """
        if self._process is None:
            return
        self.plot_connector.close(self._plot_id)
        self._process.kill()
        self._process = None

    def _start_plot_process(self) -> None:
        """
        Start the plot in a new process.
        """
        # pylint: disable=subprocess-run-check
        monitor_module = importlib.import_module("bec_widgets.widgets.monitor.monitor")
        monitor_path = monitor_module.__file__

        command = (
            f"python {monitor_path} --id {self._plot_id} --config '{json.dumps(self._config)}'"
        )
        self._process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def print_log(self) -> None:
        """
        Print the log of the plot process.
        """
        if self._process is None:
            return
        print(self._get_stderr_output())

    def _get_stderr_output(self) -> str:
        stderr_output = []
        while self._process.poll() is not None:
            readylist, _, _ = select.select([self._process.stderr], [], [], 0.1)
            if not readylist:
                break
            line = self._process.stderr.readline()
            if not line:
                break
            stderr_output.append(line.decode("utf-8"))
        return "".join(stderr_output)

    def __del__(self) -> None:
        self.close()


if __name__ == "__main__":  # pragma: no cover
    plotter = BECPlotter("test")

    plotter.set_xlabel("xlabel")
    plotter.set_ylabel("ylabel")
    plotter.set_xydata(xdata=[1, 2, 3], ydata=[1, 2, 3])
    plotter.refresh()

    # or just
    # plotter.plot(xlabel="xlabel", ylabel="ylabel", xdata=[1, 2, 3], ydata=[1, 2, 3])

    plotter.show()
    plotter.close()
