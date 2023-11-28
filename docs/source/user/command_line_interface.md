(user.command_line_interface)=
## Command-Line Interface (CLI)

In the previous sections, you have succesfully started BEC and also already interacted with the CLI to update the device configuration. 
This section aims to explore the CLI capabilities further.

### Start-up
The CLI can be started from a terminal after activating the [previously installed bec_venv](#user.installation) using the shell command within the directory where ``bec_venv`` is installed.
```{code-block} bash
source ./bec_venv/bin/activate
```
```{code-block} bash
bec
```

### Client interface
The CLI is based on the [IPython](https://ipython.org/) interactive shell. 
As seen in the screenshot below, the prompt is prefixed with, e.g. ``demo [4/522] >>``. 
The prefix contains the name of the current session (*demo*), the current cell number (*4*) and the next scan number (*522*).

### Device access
Devices are grouped in ``dev``. 
This allows users to use tab-completion for finding devices.

```{image} ../assets/tab-complete-devices.png
:align: center
:alt: tab completion for finding devices
:width: 300
```

```{hint}
``dev`` is imported as a builtin. As a result, you can access ``dev`` from everywhere. ``dev`` itself is just an alias for ``bec.device_manager.devices``.
```

### Inspect a device

To inspect the device samx, you can simply type ``dev.samx`` and you'll get a printout of the relevant information about this device.
```ipython
demo [1/31] ❯❯ dev.samx
Out[1]:
Positioner(name=samx, enabled=True):
--------------------
Details:
	Description: samx
	Status: enabled
	Set enabled: True
	Last recorded value: {'samx': {'value': 0.02237977124951616, 'timestamp': 1701081400.226357}, 'samx_setpoint': {'value': 0.022316991706485642, 'timestamp': 1701081400.161551}, 'samx_motor_is_moving': {'value': 0, 'timestamp': 1701081400.226239}}
	Device class: SynAxisOPAAS
	Acquisition group: motor
	Acquisition readoutPriority: baseline
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

A very common operation in the beginning is to be able to move a device. 
For this, there are two variants of device movements: `updated move` and `move`.

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

```{note}
Be aware of benefits and risks of executing a non-blocking command. A ``CTRL-C`` will not stop its motion, but it needs to be explicitly called via ``dev.samx.stop()`` ``%abort`` or ``%halt``.
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
````

### Run a scan

All currently available scans are accessible through `scans.`, e.g.

```python
scans.line_scan(dev.samx, -5, 5, steps=50, exp_time=0.1, relative=False)
```
You may in addition, scan multiple axis simultaneously, e.g.
```python
scans.line_scan(dev.samx, -5, 5, dev.samy, -5, 5, steps=50, exp_time=0.1, relative=False)
```
which would be a diagonal trajectory in the xy plane, assuming that samx and samy are in an rectangular coordinate system.
There are also multiple ways plot and investigate the data, for this please explore [data access and plotting](#user.data_access_and_plotting). 
This also includes live plotting of data.

BEC has various different type of scans, for instance `scans.grid_scan`, `scans.list_scan`, which you can explore in the simulation. 

#### Explore docstring documentation 
What can be very convenient while exploring built-in scans, is using the [Ipython syntax](https://ipython.readthedocs.io/en/stable/interactive/tutorial.html) `?` to print out all sort of useful information about an object, e.g. for `scans.list_scan` 

```ipython
demo [3/31] ❯❯ scans.list_scan?
Signature: scans.list_scan(*args, parameter: dict = None, **kwargs)
Docstring:
A scan following the positions specified in a list.
Please note that all lists must be of equal length.

Args:
    *args: pairs of motors and position lists
    relative: Start from an absolute or relative position
    burst: number of acquisition per point

Returns:
    ScanReport

Examples:
    >>> scans.list_scan(dev.motor1, [0,1,2,3,4], dev.motor2, [4,3,2,1,0], exp_time=0.1, relative=True)
File:      ~/work_psi_awi/bec_workspace/bec/bec_lib/bec_lib/scans.py
Type:      function
```
The shell printout provides information about the scan signature, parameters, as well as a syntax example at the bottom.

### How to write a script
-----------------------

Scripts are user defined functions that can be executed from the BEC console (CLI). 
They are stored in the ``scripts`` folder and can be edited with any text editor. 
The scripts are loaded automatically on startup of the BEC console but can also be reloaded by typing ``bec.load_all_user_scripts()`` in the command-line.
This command will load scripts from three locations: `~/bec/scripts/.`, `bec/bec_lib/scripts/.` and the beamline plugin directory, e.g. `/csaxs-bec/bec_plugins/scripts/.`


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

As seen above, scans can be access through `scans.`. 
However, sometimes it is necessary to run a sequence of functions as if it were a scan. 
For example, we might want to run a grid scan (2D scan) with our sample motor stages but move the sample position in z after each 2D scan. 
Normally, this would create multiple output files that one would need to merge together later. 

This is where the scan definition comes in. 
It allows us to run a sequence of functions as if it were a scan, resulting in a single `scan_number`, a single `scanID` and a single output file. 

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


