import abc
import functools
import subprocess

from bec_utils import Device
from grum import rpc


class PlotConnectorConnectionError(Exception):
    pass


def connection_required(fcn):
    """Decorator to ensure that the plot connector has an established connection."""

    @functools.wraps(fcn)
    def wrapper(self, *args, **kwargs):
        if not self.connected:
            raise PlotConnectorConnectionError(f"{self.__class__.__name__} is not connected.")
        return fcn(self, *args, **kwargs)

    return wrapper


class PlotConnector(abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        self.connected = False

    @abc.abstractmethod
    @connection_required
    def select(self, device: Device, *args, **kwargs) -> None:
        """Select a device for the y axis.

        Args:
            device (Device): Device that ought to be plotted on the y axis.
        """

    @abc.abstractmethod
    @connection_required
    def append_data(self, data: list, *args, **kwargs) -> None:
        """Append a new data point to the plot

        Args:
            data (list): Data x/y
        """

    def connect(self, *args, **kwargs):
        self.connected = True

    def new_plot(self, *args, **kwargs):
        pass


class GrumpyConnector(PlotConnector):
    def __init__(self) -> None:
        super().__init__()
        self.client = None
        self._grum_process = None
        self.current_plot = None

    @connection_required
    def select(self, device: Device, *args, **kwargs) -> None:
        pass

    @connection_required
    def append_data(self, data: list, *args, **kwargs) -> None:
        self.client.append_data(self.current_plot, data)

    @connection_required
    def set_data(self, title, data: list, *args, **kwargs) -> None:
        self.client.set_data(title, data)

    @connection_required
    def get_list_names(self, *args, **kwargs) -> None:
        return self.client.get_list_names()

    def connect(self):
        self.client = rpc.RPCClient("localhost", 8000)
        try:
            self.client.utils.ping()
        except ConnectionRefusedError:
            self._grum_process = subprocess.Popen(["grum", "-w", "single"])
            self.client = rpc.RPCClient("localhost", 8000)
        self._wait_for_connection()
        super().connect()

    def _wait_for_connection(self):
        while True:
            try:
                self.client.utils.ping()
                break
            except ConnectionRefusedError:
                pass

    def new_plot(self, title, *args, **kwargs):
        super().new_plot(*args, **kwargs)
        self.current_plot = title
        self.client.new_plot(title, {})
