Install BEC services 
=====================
All BEC services must be installed before they can be started. 
    
    Please make sure that the environment is activated before you install the services.


If you haven't cloned the BEC repository yet, please pull the latest version of BEC: 

.. code-block:: bash

    git clone https://gitlab.psi.ch/bec/bec.git

Additionally, clone the ophyd_devices repository:

.. code-block:: bash

    git clone https://gitlab.psi.ch/bec/ophyd_devices.git
    cd bec

.. NOTE:: 
    The default search path assumes that "**bec**" and "**ophyd_devices**" are in the same folder. Alternatively, the `ophyd_devices path` can also be set as an environment variable

    .. code-block:: bash

        export OPHYD_DEVICES_PATH=<path_to_the_ophyd_devices_repo>



Services can be installed with pip inside "bec" folder:

.. code-block:: bash

    pip install -e ./scan_server
    pip install -e ./device_server
    pip install -e ./scan_bundler
    pip install -e ./file_writer
    pip install -e ./bec_client
    pip install -e ./scihub
