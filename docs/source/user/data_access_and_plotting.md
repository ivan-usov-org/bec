(data_access_and_plotting) = 
## Data Acess and Plotting

Let's recapture how to do a scan, and assign it 

All currently available scans are accessible through `scans.`, e.g.

```python
s = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
```
Let's do a scan and explore the data contained within it. 
Note: scan data is also automatically stored in a h5 file structure. 
The internal layout of the h5 file may be cunstomized by the beamline.
Please contact your beamline contact for more information about this.
Nevertheless, all data that we can access via Redis, is also exposed throughout the client. Below is an example how to access it. 

### Inspect the scan data

The return value of a scan is a python object of type `ScanReport`. All data is stored in `<scan_report>.scan.data`, e.g.

```python
s = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
print(s.scan.data) # access to all of the data
```
Typically, only specific motors are of interest. 
A convenient access pattern `s.scan.data.device.hinted_signal.val` is implemented, that allows you to quickly access the data directly.
For example to access the data of `samx` and the above added device `gauss_bpm`, you may do the following:
```python
samx_data = s.scan.data.samx.samx.val # or s.scan.data['samx']['samx'].val 
gauss_bpm_data = s.scan.data.gauss_bpm.gauss_bpm.val # or s.scan.data['gauss_bpm']['gauss_bpm'].val
```

### Plot the scan data manually
Alternatively, you may install `pandas` as an additional dependency to directly import the data to a pandas dataframe. 
If on top, `matplotlib` is installed in the environment and imported `import matplotlib.pyplot as plt` within the BEC's IPython shell, you may directly plot the data from the shell.

```python
df = s.scan.to_pandas()
df.plot(x=('samx','samx','value'),y=('gauss_bpm','gauss_bpm','value'),kind='scatter')
plt.show()
```
This will plot the following curve from the device `gauss_bpm`, which simulates a gaussian signal.

```{image} ../assets/gauss_scatter_plot.png
:align: center
:alt: tab completion for finding devices
:width: 800
```
