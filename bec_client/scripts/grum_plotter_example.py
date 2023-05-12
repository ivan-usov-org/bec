from bec_client.plotting import GrumpyConnector
from collections import deque

_connector = GrumpyConnector()
_connector.connect()
_ID_plot_storage = deque(maxlen=50)
_y_selected = "bpm4i"
difference_title = "Difference between scans"
_plot_names = ["Scan 1", "Scan 2", difference_title]


def plot_polarisation_difference(data, metadata):
    _x_motor = metadata["primary"][0]
    scanID = metadata["scanID"]
    scan_item = bec.queue.scan_storage.find_scan_by_ID(scanID)

    if "pol" in metadata.keys():
        if scanID not in _ID_plot_storage:
            _ID_plot_storage.append(scanID)

        if metadata["pol"] == 1:
            if data["point_id"] == 0:
                _connector.new_plot("Difference in polarization, c+ - c-")
                _connector.set_data("Difference in polarization, c+ - c-", [[], []])

        elif metadata["pol"] == -1:
            scan_data = scan_item.data[data["point_id"]].content["data"]
            x = scan_data[_x_motor][_x_motor]["value"]
            y = scan_data[_y_selected][_y_selected]["value"]
            prev_scan_item = bec.queue.scan_storage.find_scan_by_ID(_ID_plot_storage[-2])
            prev_scan_data = prev_scan_item.data[data["point_id"]].content["data"]
            y_prev = prev_scan_data[_y_selected][_y_selected]["value"]
            y_diff = y_prev - y
            _connector.append_data([x, y_diff])


def test_cb(data, metadata):
    _x_motor = metadata["primary"][0]
    scanID = metadata["scanID"]
    scan_item = bec.queue.scan_storage.find_scan_by_ID(scanID)

    if "pol" in metadata.keys():
        # _connector.plot_multiple_plots("")
        if scanID not in _ID_plot_storage:
            _ID_plot_storage.append(scanID)

        if metadata["pol"] == 1:
            if data["point_id"] == 0:
                _initialize_plots()
                _clear_plots()
            _connector.current_plot = "Scan 1"
        elif metadata["pol"] == -1:
            _connector.current_plot = "Scan 2"

    else:
        plot_name = f"Scan number {metadata['scan_number']}"
        if scanID not in _ID_plot_storage:
            _connector.new_plot(plot_name, {})
        _connector.current_plot = f"Scan number {metadata['scan_number']}"

    scan_data = scan_item.data[data["point_id"]].content["data"]
    x = scan_data[_x_motor][_x_motor]["value"]
    y = scan_data[_y_selected][_y_selected]["value"]
    _connector.append_data([x, y])

    if "pol" in metadata.keys():
        if metadata["pol"] == -1:
            _plot_difference(data, x, y)


def _initialize_plots():
    for plot_name in _plot_names:
        # if plot_name not in _connector.get_list_names():
        _connector.new_plot(plot_name, {})


# _initialize_plots()


def _clear_plots():
    _connector.set_data("Scan 1", [[], []])
    _connector.set_data("Scan 2", [[], []])
    _connector.set_data(difference_title, [[], []])


def _plot_difference(data, x, y):
    prev_scan_item = bec.queue.scan_storage.find_scan_by_ID(_ID_plot_storage[-2])
    prev_scan_data = prev_scan_item.data[data["point_id"]].content["data"]
    y_prev = prev_scan_data[_y_selected][_y_selected]["value"]
    y_diff = y - y_prev
    _connector.current_plot = difference_title
    _connector.append_data([x, y_diff])
