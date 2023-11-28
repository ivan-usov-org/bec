<!-- How do I use the BEC (client)? -->
(user)=
# User
BEC is a python package that provides a command-line interface (CLI), as well as a graphical user interface (GUI) for controlling devices and running scans.
The CLI is based on the [IPython](https://ipython.org/) interactive shell.
For the GUI, we develop modular widgets based on [PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/) and [pyqtgraph](https://www.pyqtgraph.org) which can be assembled to user-specific needs.
This section contains general information about BEC and aims to answer frequently asked questions about the usage of BEC from a user perspective.

This includes:
- Exploring BEC
- Starting BEC with simulated devices
- Getting to know the command-line interface (CLI) and graphical user interface (GUI)
- Accessing BEC data
- Scan commands
- Macros/Scripting

For more information on the underlying architecture, customization possibilities or extensions to deployed BEC systems at the beamline, please consider exploring the [Developer](#developer) section.


```{toctree}
---
maxdepth: 2
---

installation
devices
command_line_interface
graphical_user_interface
data_access_and_plotting
