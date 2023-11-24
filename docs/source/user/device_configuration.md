## Device configuration
### Create a new configuration

BEC without devices is not of much use. 
To inform BEC about your devices, you need to create a configuration file. 
This file is a yaml file that contains all information about your devices.
If you already have a list of your devices and their configuration, you can skip the following step and move on to explore how you can - *Load, save and update the configuration*.

```{note}
The configuration file is a yaml file. If you are not familiar with yaml, please have a look at the [yaml documentation](https://yaml.org/).
```

But don't worry, we have prepared a device config with simulated devices for you, which allows us to explore BEC right away.

### Load demo device configuration for simulation
You can load the demo config `demo_config.yaml` directly in the command line interface via: 

```{code-block} python
bec.config.load_demo_config()
```
Once loaded, the device config will be stored on the running Redis server, and remain intact even after restarting the client or the server.
With the demo config loaded, we can now explore the conventional way of loading a device config into BEC. 

### Export the current configuration

To save the current session to disk, use

```{code-block} python
bec.config.save_current_session("./config_saved.yaml")
```
which will save a file `config_saved.yaml` in directory in which the client is running.
To modify and add a new device to the config, open `config_saved.yaml` with a suitable editor, for instance *VSCode*, and add a new device to the device config. 
For this, you may use the device gauss_bpm which is shown below. 
For more information about fields within the device config, you can check out the section [Ophyd](#developer.ophyd) in our developer guide.
``` {code-block} yaml
gauss_bpm:
  acquisitionConfig:
    acquisitionGroup: monitor
    readoutPriority: monitored
    schedule: sync
  deviceClass: sim:sim:SynGaussBEC
  deviceConfig:
    labels: gauss_bpm
    name: gauss_bpm
    sigma: 1
    noise: 'uniform'
    noise_multiplier: 0.4
  deviceTags:
  - beamline
  status:
    enabled: true
    enabled_set: true
```
### Upload a new device configuration

From the client, you can now run the follow command to update the session with a new device configuration file.
You can now reload the config from the BEC client.
```{code-block} python
bec.config.update_session_with_file(<my-config.yaml>)
```
In our case, `<my-config.yaml>` could be for example the stored and updated config `config_saved.yaml` from above.
Throughout these steps, you have exported and imported a device config, and in addition also extended the config with a new device.

### Update the configuration
We can update the device config from the command line interface. 
This allows us for instance to enable/disable, set limits or store user_parameter (e.g. in/out positions) in the config file that will be hosted, and if wanted, also exported with the device config.  

#### Enable / disable a device

To disable a device (e.g. samx), use

```{code-block} python
dev.samx.enabled=False 
```
The device `samx` is now disabled on all services as well as for the BEC database (MongoDB). 

#### Update the device config

To update the device config, use

```{code-block}  python
dev.samx.set_device_config({"tolerance":0.02})
```
 which will update the tolerance window for the motor to reach its target position. 
 Keep in mind though, that the parameter exposed through the device_config must be configurable in the [ophyd_device](#developer.ophyd) of the bespoken device.

#### Set or update the user parameters

To set the device's user parameters (such as in/out positions), use

```{code-block}  python
dev.samx.set_user_parameter({"in": 2.6, "out": 0.2})
```

If instead you only want to update the user parameters, use

```{code-block} python
dev.samx.update_user_parameter({"in":2.8})
```

```{hint}
The user parameters can be seen as a python dictionary. Therefore, the above commands are equivalent to updating a python dictionary.
```
See the following example:

```python
my_user_parameter = {"in": 2.6, "out": 0.2}    # equivalent to set_user_parameter
print(f"Set user parameter: {my_user_parameter}")


my_user_parameter.update({"in": 2.8})          # equivalent to update_user_parameter
print(f"Updated user parameter: {my_user_parameter}")
```

This will output:

``` 
Set user parameter: {'in': 2.6, 'out': 0.2}
Updated user parameter: {'in': 2.8, 'out': 0.2}
```