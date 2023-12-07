(developer.ophyd)=
# Ophyd 

[Ophyd](https://nsls-ii.github.io/ophyd/) is the hardware abstraction layer developed by NSLS-II and used by BEC to communicate with the hardware. 
It is a Python library that provides a uniform interface to different hardware components. 
Ophyd is used to control the hardware and to read out the data. 
It is also used to create a virtual representation of the hardware in the form of `devices` and `signals`.

It can be used to test the hardware without spinning up BEC, simply by importing the ophyd library.

Within BEC, ophyd objects are created dynamically on the devices server, following the specifications given in the device configuration. 
As explained in the [device configuration](#developer.bec_config) section, the device configuration can be loaded from and stored to a yaml file and contains all necessary information about the devices. 

An example of an ophyd device based on EPICS is a single PV, e.g. the synchrotron's ring current: 

```yaml
curr:
  readoutPriority: baseline
  deviceType: monitor
  description: SLS ring current
  deviceClass: EpicsSignalRO
  deviceConfig:
    auto_monitor: true
    read_pv: ARIDI-PCT:CURRENT
  deviceTags:
    - cSAXS
  onFailure: buffer
  enabled: true
  readOnly: True
```

The following sections explain the different parts of the device configuration in more detail.

* **deviceClass** \
The device class specifies the type of the device. In the example above, the device class is `EpicsSignalRO`, which is a read-only signal based on EPICS. Another example is `EpicsMotor` for motors based on EPICS. For a full list of available device classes, please refer to the [Ophyd documentation](https://nsls-ii.github.io/ophyd/architecture.html#device-classes) and the [Ophyd devices repository](https://gitlab.psi.ch/bec/ophyd_devices).

* **deviceType** \
The device type specifies the type of the device. In the example above, the device type is `monitor`. The device type is used to group devices and to filter devices. The available device types are `positioner`, `detector`, `monitor`, `controller`, `misc`. 

* **deviceConfig** \
The device config contains the configuration of the device. In the example above, the device config contains the read PV (`read_pv`). The read PV is the PV that is read out by the device. In this case, the read PV is `ARIDI-PCT:CURRENT`. The device config can contain any configuration parameter that is supported by the device class. 
The device is constructed by passing the device config to the device class. In the example above, the device is constructed by calling `EpicsSignalRO(name='curr', read_pv='ARIDI-PCT:CURRENT', auto_monitor=True)`.

* **readoutPriority** \
The readout priority specifies the priority with which the device is read out. For BEC controlled readouts, set the readout priority either to `on_request`, `baseline` or `monitored`. The ignored priority is used for devices that should not be read out during the scan. The baseline priority is used for devices that are read out at the beginning of the scan and whose value does not change during the scan. The monitored priority is used for devices that are read out during the scan and whose value may change during the scan. If the readout of the device is asynchronous to the monitored devices, set the readout priority to `async`. For devices that are read out continuously, set the readout priority to `continuous`. 

* **enabled** \
The enabled status specifies whether the device is enabled. 

* **readOnly** \
The read only status specifies whether the device is read only. If the device is read only, the device cannot be written to.

* **deviceTags** \
The device tags contain the tags of the device. The tags are used to group devices and to filter devices.

* **onFailure** \
The on failure parameter specifies the behavior of the device in case of a failure. It can be either `buffer`, `retry` or `raise`. If an error occurs and the on failure parameter is set to `buffer`, the device readout will fall back to the last value in Redis. If the on failure parameter is set to `retry`, the device readout will retry to read the device and raises an error if it fails again. If the on failure parameter is set to `raise`, the device readout will raise an error immediately.

* **description** \
The description contains the description of the device. It is used to provide additional information about the device.

## Ophyd device
to be added..

### PositionerBase
to be added..

### OphydFlyer
to be added..

### ADBase
to be added..

## Components
to be added..

### Epics PV
to be added..

### Custom Signals
to be added..

### Kind
to be added..


