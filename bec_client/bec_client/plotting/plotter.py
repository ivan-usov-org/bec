from collections import defaultdict
from typing import Any

import numpy as np
import pyqtgraph as pg
from pyqtgraph import mkPen
from pyqtgraph.Qt import QtCore


def center_of_mass(values):
    total_mass = np.sum(values)
    if total_mass:
        center_of_mass = np.sum(np.arange(len(values)) * values) / total_mass
        return center_of_mass
    return 0


class BasicPlot:
    def __init__(self, name="", y_value="bpm4i"):
        self._idle_time = 100
        self.y_value = y_value
        self.app = pg.mkQApp("")

        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")

        self.pw = pg.GraphicsView(useOpenGL=True)
        self.pw.setAntialiasing(True)
        self.pw.show()

        pen = mkPen(color=(56, 76, 107), width=5, style=QtCore.Qt.SolidLine)
        # pen2 = mkPen(color=(226, 138, 43), width=5, style=QtCore.Qt.SolidLine)

        self.layout = pg.GraphicsLayout()
        self.layout.setContentsMargins(10, 10, 75, 10)  # left, top, right, bottom
        self.pw.setCentralWidget(self.layout)

        # setup plots
        self.plot = pg.PlotItem()
        self.layout.addItem(self.plot)

        self.plot_data = self.plot.plot([], [], pen=pen, title=name)

        # self.com_line = pg.InfiniteLine(angle=90, movable=False)
        # self.com_line_label = pg.InfLineLabel(self.com_line, text="com {value:.4f}")
        # self.com_line.setVisible(False)

        # self.plot.addItem(self.com_line)
        # self.plot.addItem(self.com_line_label)

        # self.max_line = pg.InfiniteLine(angle=90, movable=False)
        # self.plot.addItem(self.max_line)

        # self.min_line = pg.InfiniteLine(angle=90, movable=False)
        # self.plot.addItem(self.min_line)

        self.com = None
        self.min = None
        self.max = None

        self.analysis_box = pg.TextItem(text="test")
        # self.analysis_box.setParentItem(self.plot)

        self.pw.addItem(self.analysis_box)

        self.plotter_data_x = []
        self.plotter_data_y = []
        self.plotter_scan_id = None

        self.crosshair_v = pg.InfiniteLine(angle=90, movable=False)
        self.crosshair_h = pg.InfiniteLine(angle=0, movable=False)
        self.plot.addItem(self.crosshair_v, ignoreBounds=True)
        self.plot.addItem(self.crosshair_h, ignoreBounds=True)
        self.proxy = pg.SignalProxy(
            self.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved
        )

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.started = False

    def mouse_moved(self, event):
        pos = event[0]
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.vb.mapSceneToView(pos)
            self.crosshair_v.setPos(mousePoint.x())
            self.crosshair_h.setPos(mousePoint.y())

    def update(self):
        if len(self.plotter_data_x) <= 1:
            return

        self.plot_data.setData(self.plotter_data_x, self.plotter_data_y)
        self.app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents)

    def _update_analysis(self):
        if not self.plotter_data_x or not self.plotter_data_y:
            return
        index = center_of_mass(np.asarray(self.plotter_data_y))
        self.com = np.interp(index, np.arange(len(self.plotter_data_x)), self.plotter_data_x)

        self.max = self.plotter_data_x[np.argmax(self.plotter_data_y)]

        self.min = self.plotter_data_x[np.argmin(self.plotter_data_y)]

        self.analysis_box.setText(f"COM: {self.com:.2f}\nMax: {self.max:.2f}\nMin: {self.min:.2f}")
        self.analysis_box.setPos(self.plot.width(), 0)

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
            self.plotter_data_x = []
            self.plotter_data_y = []
            self.plotter_scan_id = metadata["scanID"]

        plot_name = f"Scan {metadata['scan_number']}"
        self.pw.setWindowTitle(plot_name)

        scan_motors = metadata.get("scan_report_devices")

        if len(scan_motors) == 2:
            x = data["data"][scan_motors[0]][scan_motors[0]]["value"]
            y = data["data"][scan_motors[1]][scan_motors[1]]["value"]
            self.plot.setLabel("bottom", scan_motors[0])
            self.plot.setLabel("left", scan_motors[1])
        elif len(scan_motors) == 1:
            x = data["data"][scan_motors[0]][scan_motors[0]]["value"]
            y = data["data"][self.y_value][self.y_value]["value"]
            self.plot.setLabel("bottom", scan_motors[0])
            self.plot.setLabel("left", self.y_value)
            self._update_analysis()
        self.plotter_data_x.append(x)
        self.plotter_data_y.append(y)
        if len(self.plotter_data_x) <= 1:
            return
        # self.update()
