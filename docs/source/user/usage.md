## Client usage

### Starting the command-line client
The client can be started by running

```bash
bec
```

### Interface
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
s = scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1, relative=False)
```

### Inspect the scan data

The return value of a scan is a python object of type `ScanReport`. All data is stored in `<scan_report>.scan.data`, e.g.

```python
s = scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1, relative=False)
print(s.scan.data) # print the scan data
```
