## Install developer / expert environment



If you want to install the BEC server for development purposes, make sure you have git and conda installed. Then, run


```bash

    git clone https://gitlab.psi.ch/bec/ophyd_devices.git
    git clone https://gitlab.psi.ch/bec/bec.git
    cd bec
```
On PSI-maintained systems with pmodules, you can skip the installation of redis and tmux and run

```bash
    module add redis/7.0.2
    module add tmux/3.2
    source ./bin/install_bec_dev.sh --no-redis --no-tmux
```
On all other systems, run

```bash
    source ./bin/install_bec_dev.sh
```

```{note}

    If you need to connect to redis on a different port than the default (6379), you can create a service config file based on the template
    in ``bec/bec_config_template.yaml`` and pass it to the bec-server using the ``--config`` flag.
```

Once everything is installed, run

```bash

    bec-server start
```
To start the client, run

```bash
    bec
```

You are now ready to load your first device configuration. To this end, please follow the instructions given in :doc:`quickstart`.