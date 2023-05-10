from collections import deque

from blinker import signal

from bec_client.devicemanager_client import DeviceBase
from bec_client.plotting.plot_connector import GrumpyConnector


class BECPlotter:
    def __init__(self) -> None:
        self._connector = GrumpyConnector()
        self._connector.connect()
        self.scan_data_signal = signal("scan_item_point")
        self.scan_data_signal.connect(self._on_scan_data_update)
        self._plot_storage = deque(maxlen=50)
        self._y_selected = "bpm4i"

    def _on_scan_data_update(self, data) -> None:
        scanID = data["scanID"]
        scan_item = bec.queue.scan_storage.find_scan_by_ID(scanID)
        if scanID not in self._plot_storage:
            self._connector.new_plot(str(scan_item.scan_number), {})
            self._plot_storage.append(scanID)
        scan_data = scan_item.data[data["point_id"]].content["data"]
        self._connector.append_data(
            [scan_data["samx"]["samx"]["value"], scan_data["samy"]["samy"]["value"]]
        )

    def plot_select(self, device: DeviceBase):
        pass
