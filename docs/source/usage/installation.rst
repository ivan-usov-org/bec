Installation
============

Prerequisites 
---------------

Install docker
~~~~~~~~~~~~~~
- Linux: https://docs.docker.com/desktop/install/linux-install/
- macOS: https://docs.docker.com/desktop/install/mac-install/

Create a new virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python environment
^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    python -m venv ./bec_venv
    source ./bec_venv/bin/activate


Conda environment
^^^^^^^^^^^^^^^^^^

Instead of using a python environment, you can also use conda

- Linux: https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
- macOS: https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html

.. code-block:: bash
    
    conda create --name bec python=3.8
    conda activate bec


Start backend services
------------------------
The easiest way of starting the backend services (MongoDB, SciBec and Redis) is to use Docker. Follow the instructions in `Start docker containers for MongoDB, SciBec API server, and Redis`_

Alternatively, you can also install them locally without Docker. Please follow the instructions on the official documentation for `MongoDB <https://www.mongodb.com/docs/manual/installation/>`_ , `Loopback 4 for SciBec <https://loopback.io/doc/en/lb4/Getting-started.html>`_ and `Redis <https://redis.io/docs/getting-started/>`_.

Start docker containers for MongoDB, SciBec API server, and Redis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. NOTE::
    - **This step requires sudo privileges or docker running with elevated permissions.**
    - The minimum docker version is 18.09.
    - As SciBec tries to establish a connection to MongoDB and Redis, make sure that they are running before you start SciBec.

Linux:
^^^^^^^^^^^^^^^^^^

Run MongoDB on docker:

.. code-block:: bash

    sudo docker run -p 27017:27017 --name mongo-bec -d mongo

Run redis on docker: 

.. code-block:: bash

    sudo docker run --network=host --name redis-bec -d redis
 
Run SciBec on docker (clone code, build, and run SciBec API server):

.. code-block:: bash

    git clone https://gitlab.psi.ch/bec/bec.git
    cd bec/scibec
    sudo docker build -t scibec -f ./Dockerfile .
    sudo docker run --network=host --name scibec -d scibec


Now you could open a browser and check out `<http://localhost:3030>`_ page.



macOS:
^^^^^^^^^^^^^^^^^^
.. warning::
    **MacOS does not support network=host**. Instead you have to expose all ports explicitly. This also leads to a significant increase in latency for redis.


Run MongoDB on docker:

.. code-block:: bash

    sudo docker run -p 27017:27017 --name mongo-bec -d mongo

Run redis on docker: 

.. code-block:: bash

    sudo docker run -p 6379:6379 --name redis-bec -d redis
 
Run SciBec on docker (clone code, build, and run SciBec API server):

.. code-block:: bash

    git clone https://gitlab.psi.ch/bec/bec.git
    cd bec/scibec
    sudo docker build -t scibec -f ./Dockerfile .
    sudo docker run -p 3030:3030 --name scibec -d scibec


Now you could open a browser and check out `<http://localhost:3030>`_ page.



Inspect services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Check the running docker containers:
  ```
  sudo docker ps
  ```
* Connect to a running docker container:
  ```
  sudo docker exec -it <container-name> /bin/bash
  ```

MongoDB
^^^^^^^^^^^^^^^^^^
Inspect MongoDB 

If the MongoDB instance is running on docker, first connect to the container using <br>
```
sudo docker exec -it <container-name> /bin/bash
```
Running `mongo` (mongoDB version < 6) or `mongosh` (mongoDB version >= 6) will connect you to the mongo shell. Once connected, the database can be selected with `use scibec` . 
You can now run queries on e.g. devices using `db.Device.find()` .
To delete everything, use `db.Device.drop()`

If you want to reset the entire database, you will have to delete the data stored in Beamline, Session and Device.


Install BEC services 
------------------------
All BEC services must be installed before they can be started. Best practise is to create a virtual python environment first (please see `Python environment`_). 
    
    Please make sure that the environment is activated before you install the services.


If you haven't cloned the BEC repository yet (e.g. during the installation of backend services), please pull the latest version of BEC: 

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


Update the configuration of the current session 
------------------------------------------------

.. NOTE::
    Before you can update or modify the configuration, MongoDB AND the SciBec API server must be running. It's okay if the other services are not started.

    Please activate the proper environment as needed.

Create a config file
~~~~~~~~~~~~~~~~~~~~~
While there is already a config file available for simulated devices (`scibec/init_scibec/demo_config.yaml`), you can create new configs based on templates using:

.. code-block:: bash

    cd ./scibec; python ./init_scibec/create_config_file.py

This will create a config file :file:`./init_scibec/demo_config.yaml`.

As optional parameters, it can receive the output path + filename (--config) and the template type (--type). The latter must be one of the classes imported in
:file:`scibec/init_scibec/configs/__init__.py`. 

Currently :file:`init_scibec/configs/__init__.py`` supports `DemoConfig`, `TestConfig` and `LamNIConfig`. 

.. _update_session:

Upload the (newly created) config file to SciBec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd ./scibec; python ./init_scibec/update_sessions.py

By default, :file:`update_sessions.py` will look for a config file :file:`./init_scibec/demo_config.yaml`. If you have specified a different name, you can use the `--config` option of :file:`update_sessions.py`, e.g.

.. code-block:: bash

    cd ./scibec; python ./init_scibec/update_sessions.py --config <path/to/my/yaml/file.yaml>


Start the python services
------------------

For now please launch the following four services in separate terminal tabs, starting from "bec" folder.
Please activate the proper environment **in each terminal** as needed.

Please prepare a test bec_config.yaml by copying from the provided template file: 

.. code-block:: bash

    cp bec_config_template.yaml bec_config.yaml

To start the services, run

.. code-block:: bash

    cd ./scan_server; python launch.py --config ../bec_config.yaml
    cd ./device_server; python launch.py --config ../bec_config.yaml
    cd ./scan_bundler; python launch.py --config ../bec_config.yaml
    cd ./file_writer; python launch.py --config ../bec_config.yaml


where :file:`bec_config.yaml` is a service config file where the hostnames and ports of MongoDB, SciBec, and Redis are listed.  

.. cf. [TODO: COMPARE TO?]`bec_config_template.yaml`.

Start the client
------------------
Open a new terminal and start the BEC client:

    Please make sure that the environment is activated.

.. code-block:: bash

    cd bec_client
    ipython

Once started, run 

.. code-block:: python

    %run demo.py

:file:`demo.py` will config SciBec with a YAML file. 

.. [TODO: MORE DETAILS AS NEEDED]

