(user.data_access_and_plotting)= 
# Data Acess and Plotting

Let's recapture how to do a scan, and explore the data contained within it. 

```python
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
You may install `pandas` as an additional dependency to directly export the data to a panda's dataframe. 
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
