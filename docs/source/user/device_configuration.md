## Device configuration
### Create a new configuration

BEC without devices is not of much use. 
To inform BEC about your devices, you need to create a configuration file. 
This file is a yaml file that contains all information about your devices.
If you already have a list of your devices and their configuration, you can skip this step and move on to the next one - *Load, save and update the configuration*.

```{note}
The configuration file is a yaml file. If you are not familiar with yaml, please have a look at the [yaml documentation](https://yaml.org/).
```

To allow our uses an easy first impression of BEC, we have prepared a demo config with a couple of simulated devices. 

Below is an example for two device that are available through the install package: ophyd_devices. 
A simulated motor (samx) and a monitor:
```
samx:
  acquisitionConfig:
    acquisitionGroup: motor
    readoutPriority: baseline
    schedule: sync
  deviceClass: SynAxisOPAAS
  deviceConfig:
    delay: 1
    labels: samx
    limits:
    - -50
    - 50
    name: samx
    speed: 100
    tolerance: 0.01
    update_frequency: 400
  deviceTags:
  - user motors
  status:
    enabled: true
    enabled_set: true
gauss_bpm:
  acquisitionConfig:
    acquisitionGroup: monitor
    readoutPriority: monitored
    schedule: sync
  deviceClass: SynGaussBEC
  deviceConfig:
    labels: gauss_bpm
    name: gauss_bpm
    tolerance: 0.5
  deviceTags:
  - beamline
  status:
    enabled: true
    enabled_set: true

```
*We are currently in the process of refactoring the device config.
In case the example below is not working anymore, please open an issue within the [bec repository](https://gitlab.psi.ch/bec)*
```{eval-rst}
.. include:: usage/install/create_config.rst
```



### Load, save and update the configuration

(upload_configuration)=
#### Upload a new configuration

To upload a new device configuration from the client using a yaml file, please start Redis and the BEC server (if they are not running already) and launch the client using

```{code-block} bash
bec
```

Once the client started, run the following command to update the session with a new device configuration file:

```{code-block} python
bec.config.update_session_with_file(<my-config.yaml>)
```

where `<my-config.yaml>` is the full path to your device config file, e.g. `/sls/x12sa/Data10/e12345/bec/my_config.yaml`.

#### Export the current configuration

To save the current session to disk, use

```python
bec.config.save_current_session("./config_saved.yaml") # this will save a file bec_client/config_saved.yaml
```

#### Update the configuration

##### Enable / disable a device

To disable a device (e.g. samx), use

```python
dev.samx.enabled=False # this disabled the device samx on all services and MongoDB
```

##### Update the device config

To update the device config, use

```python
dev.samx.set_device_config({"tolerance":0.02})
```

Set or update the user parameters

To set the device's user parameters (such as in/out positions), use

```python
dev.samx.set_user_parameter({"in": 2.6, "out": 0.2})
```

If instead you only want to update the user parameters, use

```python
dev.samx.update_user_parameter({"in":2.8})
```

```{hint}
The user parameters can be seen as a python dictionary. Therefore, the above commands are equivalent to updating a python dictionary using

```python
user_parameter = {"in": 2.6, "out": 0.2}    # equivalent to set_user_parameter
print(f"Set user parameter: {user_parameter}")


user_parameter.update({"in": 2.8})          # equivalent to update_user_parameter
print(f"Updated user parameter: {user_parameter}")
```

This will output:

``` 
Set user parameter: {'in': 2.6, 'out': 0.2}
Updated user parameter: {'in': 2.8, 'out': 0.2}
```