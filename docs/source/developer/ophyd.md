## Ophyd 

[Ophyd](https://nsls-ii.github.io/ophyd/) is the hardware abstraction layer developed by NSLS-II and used by BEC to communicate with the hardware. It is a Python library that provides a uniform interface to different hardware components. Ophyd is used to control the hardware and to read out the data. It is also used to create a virtual representation of the hardware in the form of devices and signals.

It can be used to test the hardware without spinning up BEC, simply by importing the ophyd library.

Within BEC, ophyd objects are created dynamically on the devices server, following the specifications given in the device configuration. As explained in the [device configuration](#device-configuration) section, the device configuration can be loaded from and stored to a yaml file and contains all necessary information about the devices. 

An example of an ophyd device based on EPICS is a single PV, e.g. the synchrotron's ring current: 

```yaml
curr:
  acquisitionConfig:
    acquisitionGroup: monitor
    readoutPriority: baseline
    schedule: sync
  description: SLS ring current
  deviceClass: EpicsSignalRO
  deviceConfig:
    auto_monitor: true
    name: curr
    read_pv: ARIDI-PCT:CURRENT
  deviceTags:
    - cSAXS
  onFailure: buffer
  status:
    enabled: true
    enabled_set: false
```

The following sections explain the different parts of the device configuration in more detail.

### Device class
TODO

### Device config
TODO

### Acquisition config
TODO

### Status
TODO

### Device tags
TODO

### On failure
TODO

### Description
TODO

