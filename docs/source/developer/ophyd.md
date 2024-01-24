(developer.ophyd)=
# Ophyd 

[Ophyd](https://nsls-ii.github.io/ophyd/) is the hardware abstraction layer developed by NSLS-II and used by BEC to communicate with the hardware. 
It is a Python library that provides a uniform interface to different hardware components. 
Ophyd is used to control the hardware and to read out the data. 
It is also used to create a virtual representation of the hardware in the form of `devices` and `signals`.

It can be used to test the hardware without spinning up BEC, simply by importing the ophyd library.

## Ophyd device configuration
Within BEC, ophyd objects are created dynamically on the devices server, following the specifications given in the device configuration. 
As explained in the [device configuration](#developer.bec_config) section, the device configuration can be loaded from and stored to a yaml file and contains all necessary information about the devices. 

An example of an ophyd device based on EPICS is a single PV, e.g. the synchrotron's ring current: 

```yaml
curr:
  readoutPriority: baseline
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
  softwareTrigger: False
```

The following sections explain the different parts of the device configuration in more detail.

* **deviceClass** \
The device class specifies the type of the device. In the example above, the device class is `EpicsSignalRO`, which is a read-only signal based on EPICS. Another example is `EpicsMotor` for motors based on EPICS. For a full list of available device classes, please refer to the [Ophyd documentation](https://nsls-ii.github.io/ophyd/architecture.html#device-classes) and the [Ophyd devices repository](https://gitlab.psi.ch/bec/ophyd_devices).

* **deviceConfig** \
The device config contains the configuration of the device. In the example above, the device config contains the read PV (`read_pv`). The read PV is the PV that is read out by the device. In this case, the read PV is `ARIDI-PCT:CURRENT`. The device config can contain any configuration parameter that is supported by the device class. 
The device is constructed by passing the device config to the device class. In the example above, the device is constructed by calling `EpicsSignalRO(name='curr', read_pv='ARIDI-PCT:CURRENT', auto_monitor=True)`.

* **readoutPriority** \
The readout priority specifies the priority with which the device is read out. For BEC controlled readouts, set the readout priority either to `on_request`, `baseline` or `monitored`. The ignored priority is used for devices that should not be read out during the scan. The baseline priority is used for devices that are read out at the beginning of the scan and whose value does not change during the scan. The monitored priority is used for devices that are read out during the scan and whose value may change during the scan. If the readout of the device is asynchronous to the monitored devices, set the readout priority to `async`. For devices that are read out continuously, set the readout priority to `continuous`. 

* **enabled** \
The enabled status specifies whether the device is enabled. 

* **readOnly** \
The read only indicates if the device is read-only. When set to true, writing to the device is disabled. It's optional in the device configuration and defaults to false.

* **softwareTrigger** \
The software trigger determines if BEC should explicitly invoke the device's trigger method during a scan. It's an optional parameter in the device configuration, defaulting to false

* **deviceTags** \
The device tags contain the tags of the device. The tags are used to group devices and to filter devices.

* **onFailure** \
The on failure parameter specifies the behavior of the device in case of a failure. It can be either `buffer`, `retry` or `raise`. If an error occurs and the on failure parameter is set to `buffer`, the device readout will fall back to the last value in Redis. If the on failure parameter is set to `retry`, the device readout will retry to read the device and raises an error if it fails again. If the on failure parameter is set to `raise`, the device readout will raise an error immediately.

* **description** \
The description contains the description of the device. It is used to provide additional information about the device.

(developer.ophyd.config_validation)=
## Validation of the device config
To avoid errors during loading of the device config, the device config should be validated before loading it. This can be done by installing the `ophyd_devices` package and running the following command:

```bash
ophyd_test --config ./path/to/my/config/file.yaml
```

This will perform a static validation of the device config and will print any errors that are found. For checking if the devices can be created and connect successfully, an additional flag can be passed:

```bash
ophyd_test --config ./path/to/my/config/file.yaml --connect
``` 

(developer.ophyd.ophyd_device)=
## Ophyd devices
As Ophyd provides a uniform interface to different hardware components, only a few commands are needed to control the hardware. The following section explains the available commands that are used by BEC:

* **stage** \
Called by before the scan starts and is used to prepare the hardware for the scan. While for most devices, nothing needs to be done, for some devices such as detectors, the stage command can be used to automatically set the exposure time to the correct value. Please refer to the [device bootstrapping](#device-bootstrapping) section for more information.
* **unstage** \
Called after the scan has finished and is used to clean up the hardware. It can be used to reset values that were changed during the scan or to perform additional checks to ensure that the hardware has completed the scan successfully. However, it is important to ensure that unstage is idempotent, i.e. can be called multiple times. Please refer to the [device bootstrapping](#device-bootstrapping) section for more information.
* **hints** \
As every device may contain many signals, it is important to declare their priority. The hints command is used to retrieve a list of important signals. 
* **describe** \
Provides the schema and metadata for the `read()` method of the device. 
* **describe_configuration** \
Provides the schema and metadata for the `read_configuration()` method of the device.
* **name** \
Returns the name of the device.
* **stop** \
Stops the device.
* **set** \
Sets the value of the device.
* **read** \
Reads all normal and hinted signals of the device and returns a dictionary with the values and timestamps. The dictionary is structured as follows:
```python
{ '<device_name>': 
  { '<device_name>_<signal_name1>': 
    { 'value': value, 
    'timestamp': timestamp 
    } 
  },
  { '<device_name>_<signal_name2>': 
    { 'value': value, 
    'timestamp': timestamp 
    } 
  } 
}
```
<!-- 
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
to be added.. -->


