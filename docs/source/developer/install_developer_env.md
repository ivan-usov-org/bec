(developer.install_developer_env)=
# Install developer environment

If your goal is to install BEC in an environment for code development purposes, this section will guide you through the steps.
In contrast to a deployed production system of BEC, this installation will allow you to edit the code base of BEC actively while you are operating the system.
In that sense, installing BEC in _[dev]_ mode, is the right choice in case you like to:

- Integrate a new ophyd device at the beamline
- Add a new feature to the code base of BEC
- Allow more flexibility within code base, in particular useful during beamline commissioning

**Requirements:**

---
- [python](https://www.python.org) (>=3.10)
- [redis](https://redis.io)
- [tmux](https://github.com/tmux/tmux/wiki) (=3.2)
---


On a PSI-system, requirements are available via pmodules. If you run BEC on your own system, make sure to install the required packages.

**Step-by-Step Guide**
The first step is to clone the repository

1. Clone BEC

```bash
git clone https://gitlab.psi.ch/bec/ophyd_devices.git
git clone https://gitlab.psi.ch/bec/bec.git
```
and go to the bec directory.

```bash
cd bec
```

2. Satisfy requirements

On PSI-maintained systems with pmodules, you can simply load psi-python311/2024.02 and tmux/3.2 via

```{code-block} bash
module add psi-python311/2024.02
module add tmux/3.2
```

3. Create python virtual environment

Similar as in the [user guide](#user.installation), you have to create a virtual environment and activate it:

```bash
python -m venv ./bec_venv
source ./bec_venv/bin/activate
```

4. Install BEC

To keep things simple, we have compiled all dependencies within the `setup.py` from `bec_server`.
Note, you need to install the package in editable mode (with `-e` flag), to allow changes to the code base.

```bash
pip install -e './bec_server[dev]'
pip install -e './bec_ipython_client[dev]'
pip install -e './bec_lib[dev]'
```

```{note}
The extension [dev] will install additional dependencies, which are useful for code development such as for instance `pytest`, `black`.
```
5. Start Redis

Open a new terminal, and start Redis.
Make sure that you've either loaded the pmodule or installed Redis on your system.
```
module add redis/7.0.12
redis-server
```

Per default, Redis will start on port `6379`.

```{tip}
Redis will create a `dump.rdb`, where it regularly stores data on disk. Make sure that you have a few GB in the directory where you start Redis, i.e. avoid the home directory of the e-account at the beamline.
```

6. Start BEC server

Now we can start the BEC server.
Make sure that you activate the `bec_venv` created above, and that `tmux/3.2` is availabe, e.g. loaded via pmodule.
Then you can start the BEC server
```bash
bec-server start
```
Check the command-line printout for instructions of tmux.
You may open the tmux session to look at the different BEC services via

```bash
bec-server attach
```

and exit the tmux session again via `CTRL+B+D`.
```{note}
You can also connect to the tmux session via `tmux attach -t bec` and detach via `CTRL+B+D`.
```
Both commands are also highlighted in your command-line interface.

```{note}
Strictly speaking, you do not need to install tmux. However, if you do not use tmux, you need to start each service manually, e.g. `bec-scan-server start`, `bec-device-server start` etc.) each in a separate terminal. Tmux simplifies this process by starting all services in a single terminal.
```

7. Start the command-line interface

```bash
bec
```

You are now ready to load your first device configuration.
To this end, please follow the instructions given in [bec_config](#developer.bec_config).

8. Start services with different port

It could be the case, that port `6379` is already occupied or that you have to run multiple Redis server on the same system.
If this is the case, you can also spin up the system with a modified configuration, e.g. on port `xxxx`.
The redis-server can be passed on a specific port.

```bash
redis-server --port xxxx
```
In addition, you will have to start the bec-server with a customized config.
Please check the example file ``bec/bec_config_template.yaml`` to create a custom config and specify port `xxxx` and pass it to the bec-server upon start

``` bash
bec-server start --config my_new_bec_config.yaml
```
and finally also to the client

```bash
bec --config my_new_bec_config.yaml
```
