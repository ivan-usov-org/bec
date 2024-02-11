(user.data_access_and_plotting)= 
# Data Acess and Plotting

Let's recapture how to do a scan, and explore the data contained within it. 

```ipython
s = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
```

```{note}
scan data is also automatically stored in a [HDF5 file structure](https://portal.hdfgroup.org/hdf5/develop/index.html) (h5 file). 
The internal layout of the h5 file is customizable by the beamline.
Please contact your beamline contact for more information about this.
```

Nevertheless, all data that we can access via Redis, is also exposed throughout the client. 
Below is an example how to access it. 

## Inspect the scan data

The return value of a scan is a python object of type `ScanReport`. All data is stored in `<scan_report>.scan.data`, e.g.

```python
print(s.scan.data) # access to all of the data
```
Typically, only specific motors are of interest. 
A convenient access pattern `s.scan.data.device.hinted_signal.val` is implemented, that allows you to quickly access the data directly.
For example to access the data of `samx` and the above added device `gauss_bpm`, you may do the following:
```python
samx_data = s.scan.data.samx.samx.val 
# or samx_data = s.scan.data['samx']['samx'].val

gauss_bpm_data = s.scan.data.gauss_bpm.gauss_bpm.val 
# or s.scan.data['gauss_bpm']['gauss_bpm'].val
```
You may now use the given data to manipulate it as you see fit.
Keep in mind though, these manipulations only happen locally for yourself in the IPython shell. 
They will not be forwarded to the BEC data in Redis, thus, your modification won't be stored in the raw data file (HDF5 file).

## Plot the scan data on your own
You can install `pandas` as an additional dependency to directly export the data to a panda's dataframe. 
If on top, `matplotlib` is installed in the environment and imported `import matplotlib.pyplot as plt`, one may use the built-in plotting capabilities of pandas to plot from the shell.

```python
df = s.scan.to_pandas()
df.plot(x=('samx','samx','value'),y=('gauss_bpm','gauss_bpm','value'),kind='scatter')
plt.show()
```
This will plot the following curve from the device `gauss_bpm`, which simulates a gaussian signal and was potentially added by you to the demo device config in the section [devices](#user.devices.add_gauss_bpm).

```{image} ../assets/gauss_scatter_plot.png
:align: center
:alt: tab completion for finding devices
:width: 800
```

## Fit the scan data
You can use the builtin models to fit the data. All models are available in the `bec.dap` namespace. As an example, we can fit the data with a Gaussian model and select the `samx` and `bpm4i` devices with their respective (readback) signals `samx` and `bpm4i`:
```python
s = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
res = bec.dap.GaussianModel.fit(s.scan, "samx", "samx", "bpm4i", "bpm4i")
```
The result of the fit is stored in the `res` object which contains the fit parameters and the fit result.
You can further optimize the fit by limiting the fit range, e.g. 
```python
res = bec.dap.GaussianModel.fit(scan_report.scan, "samx", "samx", "bpm4i", "bpm4i", x_min=-2, x_max=2)
```

To display the fit, you can use the `plot` method of the `res` object:
```python
res.plot()
```

Often, a fit is simply a means to find the optimal position of a motor. Therefore, the fit result can be used to move the motor to the optimal position, e.g. to the center position of the Gaussian:

```python
umv(dev.samx, res.center)
```





## Accessing scan data from the history
The BEC client maintains a local history of the 50 most recent scans since the client's startup. 
You can easily retrieve scan data from `bec.history`, which is a Python `list`, as demonstrated in the example below, where we fetch data from the latest scan:
```ipython
scan_data = bec.history[-1].scan
```

## Export scan data from client
BEC consistently saves data in h5 format, following the NX standard. 
It is recommended to access data through h5 files, as they also contain links to large detector data from secondary data services. 
Additionally, we provide a straightforward method to export scan data to `csv` using the client interface:

```ipython
with scans.scan_export("<path_to_output_file.csv>"):
    scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
    scans.grid_scan(dev.samx, -5, 5, 50, dev.samy, -1, 1, 10, exp_time=0.1, relative=False)
```

Running this code will generate the scan data output in `<path_to_output_file.csv>`. 
Additionally, you can directly import the export function `scan_to_csv`, enabling you to export scan data from previously conducted scans:

``` ipython
from bec_lib.utils import scan_to_csv

scan_data = bec.history[-1].scan
scan_to_csv(scan_data, "<path_to_output_file.csv>")
```

```{note}
Large data from 2D detectors are usually processing by backend services and are, therefore, not available for client-based export.
```