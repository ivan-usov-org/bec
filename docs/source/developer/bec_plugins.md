(developer.bec_plugins)=
# BEC Plugins

BEC plugins are a way to extend the functionality of BEC. They are written in Python and can be used to add new features to BEC or to modify existing ones. This enables beamlines to customize BEC to their needs without having to modify the core code. Plugins can be used for various purposes but the most common ones are:
* Adding new scan types
* Adding new device types
* Adding additional services, e.g. for data analysis
* Customizing the BEC CLI startup procedure (e.g. to load additional modules)
* Customizing the file structure

Plugins are commonly provided to BEC by installing them as a Python package `bec_plugins`. Clients and BEC services can then load the specific plugins they need.

## Plugin Structure

The following sections describe the structure of a BEC plugin. As plugins typically live on gitlab, we will use the following example structure of a "beamline_XX_plugins" repository to explain the different parts of BEC plugins. Instead of creating the structure manually, you can also use the script located in BEC library to create the structure for you.
```bash
python ./<path_to_bec>/bec/bec_lib/util_scripts/create_plugin_structure.py <path_to_new_plugin>
```

```
beamline_XX_plugins/
├── bec_plugins/
│   ├── bec_client/
│   │   ├── high_level_interface/
│   │   │   ├── __init__.py
│   │   │   └── custom_hli.py
│   │   ├── plugins/
│   │   │   ├── BeamlineXX/
│   │   │   │   ├── __init__.py
│   │   │   │   └── custom_XX_class.py
│   │   │   └── __init__.py
│   │   ├── startup/
│   │   │   ├── __init__.py
│   │   │   ├── post_startup.py
│   │   │   └── pre_startup.py
│   │   └── __init__.py
│   ├── scan_server/
│   │   ├── scan_plugins/
│   │   │   ├── __init__.py
│   │   │   └── custom_scan.py
│   │   └── __init__.py
│   ├── device_server/
│   │   ├── __init__.py
│   │   └── startup.py
│   ├── dap_services/
│   │   ├── __init__.py
│   │   └── custom_dap.py
│   ├── devices/
│   │   ├── __init__.py
│   │   └── custom_XX_device.py
│   └── device_configs/
│       ├── __init__.py
│       └── tomography_config.yaml
├── bin/
│   └── helper_script.sh
├── setup.cfg
└── setup.py
```
<!-- done with https://tree.nathanfriend.io  -->
<!--
beamline_XX_plugins
  bec_plugins
    bec_client
      high_level_interface
        __init__.py
        custom_hli.py
      plugins
        BeamlineXX
          __init__.py
          custom_XX_class.py
        __init__.py
      startup
        __init__.py
        post_startup.py
        pre_startup.py
      __init__.py
    scan_server
      scan_plugins
        __init__.py
        custom_scan.py
      __init__.py
    device_server
      __init__.py
      startup.py
    dap_services
      __init__.py
      custom_dap.py
    devices
      __init__.py
      custom_XX_device.py
    device_configs
      __init__.py
      tomography_config.yaml
  bin
    helper_script.sh
  setup.cfg
  setup.py
   -->

Within the root directory of your repository, place the [setup files](#setup_files) and the plugins folder. The plugins folder contains the actual plugins and is structured as follows:
* `bec_client`: Contains plugins that are used by the BEC client. This includes plugins to customize the startup procedure, adding helper classes and functions to the CLI or adding aliases to the CLI to simplify the usage of BEC.
* `device_server`: Contains plugins that are used by the device server.
* `scan_server`: Contains plugins that are used by the scan server. This includes plugins to add new scan types.
* `devices`: Contains plugins that are used to add support for new devices that are not covered by the shared ophyd_devices package.
* `device_configs`: Contains the configuration files for the devices.


{#setup_files}
### Setup files

The setup files are used to install the plugin as a Python package. The `setup.py` file is the main file that is used to install the package. It contains the information about the package and the dependencies. The `setup.cfg` file contains additional information about the package. For more information about the setup files, see the [Python documentation](https://packaging.python.org/tutorials/packaging-projects/).

**setup.py**

```python
from setuptools import setup

if __name__ == "__main__":
    setup(
        # specify the additional dependencies
        install_requires=["pyyaml", "pyepics"],

        # if you have additional dependencies for development, specify them here
        extras_require={"dev": ["pytest", "pytest-random-order", "coverage"]},
    )

```

**setup.cfg**

```cfg
[metadata]
name = bec_plugins
description = BEC plugins to modify the behaviour of services within the BEC framework
long_description = file: README.md
long_description_content_type = text/markdown
url = https://gitlab.psi.ch/bec/bec
project_urls =
    Bug Tracker = https://gitlab.psi.ch/bec/bec/issues
classifiers =
    Programming Language :: Python :: 3
    Development Status :: 3 - Alpha
    Topic :: Scientific/Engineering

[options]
package_dir =
    = .
packages = find:
python_requires = >=3.10

[options.packages.find]
where = .

```


``` {note}
While the `setup.py` file can (and probably should) be modified to fit your needs, the `setup.cfg` file and especially the name of the package ("bec_plugins") should not be changed. This is because the BEC services and clients look for plugins in a package called "bec_plugins".
```
