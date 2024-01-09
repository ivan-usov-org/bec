(user.graphical_user_interface)=
# Graphical User Interface (GUI)

BEC Widgets is a comprehensive extension for BEC that enables user interaction with the code via a graphical user interface (GUI). For detailed guidance on utilizing the GUI, please visit the [BEC Widgets documentation](https://bec-widgets.readthedocs.io/en/latest/).

Additionally, some GUI elements can be directly accessed through the command line interface if `BEC Widgets` is installed.

## BECPlotter

`BECPlotter` is a straightforward plotting window designed for visualizing simulation data.
To use `BECPlotter`, it must be imported as it is not included by default:


```python
from bec_lib.bec_plotter import BECPlotter
```

Creating and displaying an instance of the BECPlotter class with the default configuration is simple:

```python
plotter = BECPlotter("test")
plotter.show()
```

Modifying the axis labels is possible with `set_xlabels` and `set_ylabels` methods:

```python
plotter.set_xlabels("x")
plotter.set_ylabels("y")
```

The displayed signal can be changed using the `set_ysource` method:

```python
plotter.set_ysource("bpm4a")
```

For plotting custom data, use the `set_xydata` method:

```python
plotter.set_xydata(xdata=[1,2,3,4,5],ydata=[1,2,3,4,5],ytag='test data')
```

To apply these changes, the `refresh` method must be called:

```python
plotter.refresh()
```

A GUI configuration dialog can be opened with the `config_dialog` method:

```python
plotter.config_dialog()
```

### Example of BECPlotter usage
![BECPlotter example](../_static/gif/bec_plotter.gif)

[//]: # ()
[//]: # (#TODO how to upload gif???)