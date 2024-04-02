(user.installation)=
## Installation

If you are using BEC at the beamline, there is a good chance that BEC is already installed.
Please contact your beamline responsible for further information.
If you need to install a BEC client yourself, the following section will guide you through this.
If the BEC server is not installed, please follow the [developer instructions](developer.install_developer_env).

**Requirements:**

---
- [python](https://www.python.org) (>=3.10)
---

On a PSI-system, requirements are available via pmodules. If you run BEC on your own system, make sure to install the required packages.
```{code-block} bash
module add psi-python311/2024.02
```
**Step-by-Step Guide**

1. Create a virtual environment and activate it afterwards

```{code-block} bash
python -m venv ./bec_venv
source ./bec_venv/bin/activate
```
2. Install the BEC client

```{code-block} bash
pip install bec-ipython-client
```

3. Start BEC client

```{code-block} bash
bec
```
BEC is running now and you would be ready to load your first device configuration.
In case BEC did not successfully start, please check with your beamline responsible if all BEC services are running and reachable.
To this end, please follow the instructions given in the section [devices](#user.devices).
