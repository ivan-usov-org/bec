## Client usage

In the previous sections, you have succesfully started BEC and also already interacted with the client interface to update the device configuration. 
This section aims to introduce the client (command line interace) further.

### Starting the command-line client
The client can be started by running

```{code-block} bash
bec
```
from a terminal where the `bec_venv` is activated.
The initial environment was created in [installation](#user.installation), and needs to be activated within the shall that you like to start the client. 
```{code-block} bash
source ./bec_venv/bin/activate
`````` 

### Client interface
The client interface is based on the [IPython](https://ipython.org/) interactive shell. As seen in the screenshot below, the prompt is prefixed with, e.g. `demo [4/522] >>`. The prefix contains the name of the current session (demo), the current cell number (4) and the next scan number (522).


### Device access
Devices are grouped in `dev`. This allows users to use tab-completion for finding devices.

```{image} ../assets/tab-complete-devices.png
:align: center
:alt: tab completion for finding devices
:width: 300
```

```{hint}
`dev` is imported as a builtin. As a result, you can access `dev` from everywhere. `dev` itself is just an alias for `bec.device_manager.devices`.
```


### Inspect a device

```ipython
LamNI [2/522] >> dev.samx

Out[2]:
        Positioner(name=samx, enabled=True):
        --------------------
        Details:
            Status: enabled
            Last recorded value: {'value': 0, 'timestamp': 1671796007.547235}
            Device class: SynAxisOPAAS
            Acquisition group: motor
            Acquisition readoutPriority: monitored
            Device tags: ['user motors']
            User parameter: None
        --------------------
        Config:
            delay: 1
            labels: samx
            limits: [-50, 50]
            name: samx
            speed: 100
            tolerance: 0.01
            update_frequency: 400
```

### Move a motor

There are two variants of device movements: `updated move` and `move`.

#### Updated move (umv)

A umv command blocks the command-line until the motor arrives at the target position (or an error occurs).

```python
scans.umv(dev.samx, 5, relative=False)
```

#### Move (mv)

A mv command is non-blocking, i.e. it does not wait until the motor reaches the target position.

```python
scans.mv(dev.samx, 5, relative=False)
```

However, it can be made a blocking call by

```python
scans.mv(dev.samx, 5, relative=False).wait()
```

The same mv command can also be executed by calling the device method `move`

```python
dev.samx.move(5, relative=False)
```

````{note}
mv and umv can receive multiple devices, e.g.
```python
scans.umv(dev.samx, 5, dev.samy, 10, relative=False)
```
```````

### Run a scan

All currently available scans are accessible through `scans.`, e.g.

```python
s = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
```

### Inspect the scan data

The return value of a scan is a python object of type `ScanReport`. All data is stored in `<scan_report>.scan.data`, e.g.

```python
s = scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
print(s.scan.data) # access to all of the data
```
Typically, only specific motors are of interest. 
A convenient access pattern `data[device][hinted_signal].val` is implemented, that allows you to quickly access the data directly.
For example to access the data of `samx` and the above added device `gauss_bpm`, you may do the following:
```python
samx_data = s.scan.data['samx']['samx'].val
samx_data = s.scan.data['gauss_bpm']['gauss_bpm'].val
```

### Plot the scan data manually
Alternatively, you may install `pandas` as an additional dependency to directly import the data to a pandas dataframe. 
If on top, `matplotlib` is installed in the environment and imported `import matplotlib.pyplot as plt` within the BEC's IPython shell, you may directly plot the data from the ipython shell.

```python
df = s.scan.to_pandas()
df.plot(x=('samx','samx','value'),y=('gauss_bpm','gauss_bpm','value'),kind='scatter')
plt.show()
```
This will plot the following curve from the device `gauss_bpm`, which simulated a gaussian signal.
```{image} ../assets/gauss_scatter_plot.png
:align: center
:alt: tab completion for finding devices
:width: 800
```


### How to write a script
-----------------------

Scripts are user defined functions that can be executed from the BEC console. They are stored in the ``scripts`` folder and can be edited with any text editor. 
The scripts are loaded automatically on startup of the BEC console but can also be reloaded by typing ``bec.load_all_user_scripts()`` in the BEC console.
An example of a user script could be a function to move a specific motor to a predefined position:

```python 
    def samx_in():
        umv(dev.samx, 0)
```

or 

```python 

    def close_shutter():
        print("Closing the shutter")
        umv(dev.shutter, 0)
```

A slightly more complex example could be a sequence of scans that are executed in a specific order:

```python

    def overnight_scan():
        open_shutter()
        samx_in()
        for i in range(10):
            scans.line_scan(dev.samy, 0, 10, steps=100, exp_time=1, relative=False)
        samx_out()
        close_shutter()
```

This script can be executed by typing ``overnight_scan()`` in the BEC console and would execute the following sequence of commands:

1. Open the shutter
2. Move the sample in
3. Perform 10 line scans on the sample
4. Move the sample out
5. Close the shutter

### Create a custom scan

As seen above, scans can be access through `scans.`. However, sometimes it is necessary to run a sequence of functions as if it were a scan. For example, we might want to run a grid scan (2D scan) with our sample motor stages but move the sample position in z after each 2D scan. 
Normally, this would create multiple output files that one would need to merge together later. 

This is where the scan definition comes in: it allows us to run a sequence of functions as if it were a scan, resulting in a single :term:`scan_number`, a single :term:`scanID` and a single output file. 


```python

    @scans.scan_def
    def overnight_scan():
        open_shutter()
        samx_in()
        for i in range(10):
            scans.grid_scan(dev.samy, 0, 10, steps=100, exp_time=1, relative=False)
        samx_out()
        close_shutter()
```

By adding the decorator ``@scans.scan_def`` to the function definition, we mark this function as a scan definition.
