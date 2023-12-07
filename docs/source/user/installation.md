(user.installation)=
## Installation

If you are using BEC at the beamline, there is a good chance that BEC is already installed.
Please contact your beamline responsible for further information.  
If you need to install BEC yourself, the following section will guide you through this.

**Requirements:**

---
- [python](https://www.python.org) (>=3.9)
- [redis](https://redis.io)
- [tmux](https://github.com/tmux/tmux/wiki) (=3.2)
---

On a PSI-system, requirements are available via pmodules. If you run BEC on your own system, make sure to install the required packages. 
```{code-block} bash 
module add psi-python39/2021.11
module add redis/7.0.12
module add tmux/3.2
```
**Step-by-Step Guide**

1. Create a virtual environment and activate it afterwards

```{code-block} bash
python -m venv ./bec_venv
source ./bec_venv/bin/activate
```
2. Install the BEC server

```{code-block} bash
pip install bec-server
```
3. Start Redis in a new terminal


```{code-block} bash
redis-server
```
BEC services are connected via Redis, a message broker sitting at the core of all BEC services. 
Thus, Redis needs to be started on your system. 
If the pmodule is loaded (or Redis installed on your system), open a new terminal and start a redis server.
Redis will automatically dump data on disk into the file `dump.rdb`, up to a few GB, and should therefore be started in a location with sufficient storage.


4. Start the BEC server

Now you can go back to the terminal where the bec_venv is still activated and start the bec-server.

```{code-block} bash
bec-server start
```
The BEC server will automatically start in a tmux session. 
More detailed information about Redis and the BEC server can be found in [architecture](#developer.architecture) and [developer install guide](#developer.install_developer_env)

5. Start BEC client

```{code-block} bash
bec
```
BEC is running now and you would be ready to load your first device configuration. 
To this end, please follow the instructions given in the section [devices](#user.devices).
