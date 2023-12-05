(developer.ophyd_device)=
# Ophyd devices
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

