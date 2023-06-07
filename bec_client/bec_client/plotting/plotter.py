from collections import defaultdict
import threading
import time
from typing import Any

import numpy as np
import pyqtgraph as pg
from pyqtgraph import mkPen
from pyqtgraph.Qt import QtCore, QtWidgets

# from PyQt5.QtCore import pyqtSignal
from lmfit import models


def center_of_mass(values):
    total_mass = np.sum(values)
    if total_mass:
        center_of_mass = np.sum(np.arange(len(values)) * values) / total_mass
        return center_of_mass
    return 0


class BasicPlot(QtCore.QObject):
    update_signal = QtCore.pyqtSignal()

    def __init__(self, name="", y_value="bpm4i"):
        super().__init__()

        self._idle_time = 100

        # Initialize variables
        self.analysis_thread = None

        self.title = ""
        self.label_bottom = ""
        self.label_left = ""

        self.scan_motors = []
        self.y_value = y_value
        self.plotter_data_x = []
        self.plotter_data_y = []
        self.plotter_scan_id = None
        self.analysis_data_x = []
        self.analysis_data_y = []
        self.fit_data = []
        self.com = None
        self.min = None
        self.max = None
        self.com_fit = None
        self.min_fit = None
        self.max_fit = None
        self.model = models.GaussianModel()

        # Initialize app
        self.app = pg.mkQApp("")
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")

        self.pw = pg.GraphicsView(useOpenGL=True)
        self.pw.setAntialiasing(True)
        self.pw.show()

        self.layout = pg.GraphicsLayout()
        self.layout.setContentsMargins(10, 10, 75, 10)
        self.pw.setCentralWidget(self.layout)

        # setup plots
        self.plot = pg.PlotItem()
        self.layout.addItem(self.plot)
        self.pen = mkPen(color=(56, 76, 107), width=4, style=QtCore.Qt.DashLine)
        self.pen2 = mkPen(color=(226, 138, 43), width=4, style=QtCore.Qt.SolidLine)
        self.plot_data = self.plot.plot([], [], pen=self.pen, title=name)
        self.plot_data_fit = self.plot.plot([], [], pen=self.pen2, title=f"{name}-fit")
        self.crosshair_v = pg.InfiniteLine(angle=90, movable=False)
        self.plot.addItem(self.crosshair_v, ignoreBounds=True)

        # Add textItems
        self.add_text_items()

        # Manage signals
        self.proxy = pg.SignalProxy(
            self.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved
        )
        self.proxy_update = pg.SignalProxy(self.update_signal, rateLimit=25, slot=self.update)

    def add_text_items(self):
        self.analysis_box_data = pg.TextItem(text="Analysis data", color=self.pen.color())
        self.analysis_box_data.setPos(self.plot.width(), 0)
        self.pw.addItem(self.analysis_box_data)
        self.analysis_box_fit = pg.TextItem(text="Analysis fit", color=self.pen2.color())
        self.analysis_box_fit.setPos(self.plot.width(), 80)
        self.pw.addItem(self.analysis_box_fit)
        self.mouse_box_data = pg.TextItem(text="Mouse data", color=self.pen.color())
        self.mouse_box_data.setPos(self.plot.width(), 160)
        self.pw.addItem(self.mouse_box_data)
        self.mouse_box_fit = pg.TextItem(text="Mouse fit", color=self.pen2.color())
        self.mouse_box_fit.setPos(self.plot.width(), 220)
        self.pw.addItem(self.mouse_box_fit)

    def mouse_moved(self, event):
        pos = event[0]
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.vb.mapSceneToView(pos)
            self.crosshair_v.setPos(mousePoint.x())
            if self.plotter_data_x:
                closest_point = self.closest_x_y_value(
                    mousePoint.x(), self.plotter_data_x, self.plotter_data_y
                )

                self.mouse_box_data.setText(
                    f"X_data: {closest_point[0]:.2f}\nY_data: {closest_point[1]:.2f}\n"
                )
                closest_analysis_point = self.closest_x_y_value(
                    mousePoint.x(), self.analysis_data_x, self.fit_data.best_fit.tolist()
                )
                self.mouse_box_fit.setText(
                    f"X_fit: {closest_analysis_point[0]:.2f}\nY_fit: {closest_analysis_point[1]:.2f}"
                )

    def closest_x_y_value(self, input_value, list_x, list_y):
        arr = np.asarray(list_x)
        i = (np.abs(arr - input_value)).argmin()
        return list_x[i], list_y[i]

    def update(self):
        if len(self.plotter_data_x) <= 1:
            return
        self.pw.setWindowTitle(self.title)
        self.plot.setLabel("bottom", self.label_bottom)
        self.plot.setLabel("left", self.label_left)

        self.plot_data.setData(self.plotter_data_x, self.plotter_data_y)
        if len(self.scan_motors) == 1:
            if self.analysis_thread is None or not self.analysis_thread.is_alive():
                self._update_analysis()
        if self.fit_data:
            self.plot_data_fit.setData(
                self.analysis_data_x[: len(self.fit_data.best_fit.tolist())],
                self.fit_data.best_fit.tolist(),
            )
        if self.com is not None and self.max is not None and self.min is not None:
            self.analysis_box_data.setText(
                f"COM: {self.com:.2f}\nMax: {self.max:.2f}\nMin: {self.min:.2f}"
            )
        if self.com is not None and self.max_fit is not None and self.min_fit is not None:
            self.analysis_box_fit.setText(
                f"COM: {self.com:.2f}\nMax: {self.max_fit:.2f}\nMin: {self.min_fit:.2f}"
            )

    def _run_threaded_analysis(self):
        while True:
            if not self.plotter_data_x or not self.plotter_data_y:
                return

            # break if length of plotter_data is equal to the length of the analysis data
            if len(self.plotter_data_x) == len(self.analysis_data_x):
                break

            # get new plotter data
            self.analysis_data_x = self.plotter_data_x.copy()
            self.analysis_data_y = self.plotter_data_y.copy()
            # time.sleep(3)
            if len(self.analysis_data_x) > 3:
                fit_init_guess = self.model.guess(
                    np.asarray(self.analysis_data_y), np.asarray(self.analysis_data_x)
                )
                self.fit_data = self.model.fit(
                    np.asarray(self.analysis_data_y),
                    fit_init_guess,
                    x=np.asarray(self.analysis_data_x),
                )
            else:
                self.fit_data = []

            index = center_of_mass(np.asarray(self.analysis_data_y))
            self.com = np.interp(index, np.arange(len(self.analysis_data_x)), self.analysis_data_x)
            self.max = self.analysis_data_x[np.argmax(self.analysis_data_y)]
            self.min = self.analysis_data_x[np.argmin(self.analysis_data_y)]
            if self.fit_data:
                self.max_fit = self.analysis_data_x[np.argmax(self.fit_data.best_fit.tolist())]
                self.min_fit = self.analysis_data_x[np.argmin(self.fit_data.best_fit.tolist())]

        self.update_signal.emit()

    def _update_analysis(self):
        self.analysis_thread = threading.Thread(target=self._run_threaded_analysis, daemon=True)
        self.analysis_thread.start()

    def start(self):
        if not self.started:
            self.timer.start(100)
            self.started = True

    def __call__(self, data: dict, metadata: dict, **kwds: Any) -> None:
        """Update function that is called during the scan callback. To avoid
        too many renderings, the GUI is only processing events every <_idle_time> ms.

        Args:
            data (dict): Dictionary containing a new scan segment
            metadata (dict): Scan metadata

        """
        if metadata["scanID"] != self.plotter_scan_id:
            self.plotter_scan_id = metadata["scanID"]
            self._reset_plot_data()

        self.title = f"Scan {metadata['scan_number']}"

        self.scan_motors = scan_motors = metadata.get("scan_report_devices")

        if len(scan_motors) == 2:
            x = data["data"][scan_motors[0]][scan_motors[0]]["value"]
            y = data["data"][scan_motors[1]][scan_motors[1]]["value"]
            self.label_bottom = scan_motors[0]
            self.label_left = scan_motors[1]

        elif len(scan_motors) == 1:
            x = data["data"][scan_motors[0]][scan_motors[0]]["value"]
            y = data["data"][self.y_value][self.y_value]["value"]
            self.label_bottom = scan_motors[0]
            self.label_left = self.y_value

        self.plotter_data_x.append(x)
        self.plotter_data_y.append(y)
        if len(self.plotter_data_x) <= 1:
            return
        self.update_signal.emit()

    def _reset_plot_data(self):
        self.plotter_data_x = []
        self.plotter_data_y = []
        self.plot_data.setData([], [])
        self.fit_data = []
        self.analysis_data_x = []
        self.analysis_data_y = []
        self.plot_data_fit.setData([], [])
        # self.mouse_box_data.setText("Mouse data")
        # self.mouse_box_fit.setText("Mouse fit")


if __name__ == "__main__":
    print("main")
    from bec_client_lib.client import BECClient

    client = BECClient()
    client.start()
    plot = BasicPlot()
    client.callbacks.register("scan_segment", plot, sync=False)
    pg.exec()
