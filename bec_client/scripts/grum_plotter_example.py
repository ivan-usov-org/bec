from bec_client.plotting import GrumpyConnector
from collections import deque


class GrumPlotStorage:
    def __init__(self) -> None:
        self._ID_plot_storage = deque(maxlen=50)

    def get_plot_storage(self):
        return self._ID_plot_storage

    def append_to_plot_storage(self, ID: str):
        self._ID_plot_storage.append(ID)


_connector = GrumpyConnector()
_connector.connect()
_connector.select(dev.bpm4i)
_plot_storage = GrumPlotStorage()


def plot_polarisation_difference(data, metadata):
    _x_motor = metadata["primary"][0]
    scanID = metadata["scanID"]
    _y_selected = _connector._y_selected
    scan_item = bec.queue.scan_storage.find_scan_by_ID(scanID)

    if not "pol" in metadata:
        return

    if scanID not in _plot_storage.get_plot_storage():
        _plot_storage.append_to_plot_storage(scanID)

    if metadata["pol"] == 1:
        if data["point_id"] == 0:
            _connector.new_plot("Difference in polarization, c+ - c-")
            _connector.set_data("Difference in polarization, c+ - c-", [[], []])

    elif metadata["pol"] == -1:
        scan_data = scan_item.data[data["point_id"]].content["data"]
        x = scan_data[_x_motor][_x_motor]["value"]
        y = scan_data[_y_selected][_y_selected]["value"]
        prev_scan_item = bec.queue.scan_storage.find_scan_by_ID(
            _plot_storage.get_plot_storage()[-2]
        )
        prev_scan_data = prev_scan_item.data[data["point_id"]].content["data"]
        y_prev = prev_scan_data[_y_selected][_y_selected]["value"]
        y_diff = y_prev - y
        _connector.append_data([x, y_diff])
