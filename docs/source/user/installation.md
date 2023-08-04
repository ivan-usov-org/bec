## Installation
If you are using BEC at the beamline, there is a good chance that the client is already installed. Please contact your beamline responsible for further information.  
If you need to install the client yourself, you can create a Python (>= 3.8) environment using

```{code-block} bash
    python -m venv ./bec_venv
    source ./bec_venv/bin/activate
```

and install the BEC server using

```{code-block} bash
    pip install bec-server
```

Once installed, you can start the server using

```{code-block} bash
    bec-server start
```

To install the BEC client, run

```{code-block} bash
    pip install bec-ipython-client
```

and start the client using

```{code-block} bash
    bec
```

You are now ready to load your first device configuration. To this end, please follow the instructions given in the following section.