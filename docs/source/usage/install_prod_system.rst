
********************************************
Install BEC using Docker (production system)
********************************************

Prerequisites 
=============

Install docker
--------------
- Linux: https://docs.docker.com/desktop/install/linux-install/
- macOS: https://docs.docker.com/desktop/install/mac-install/

Create a new virtual environment
--------------------------------

.. note:: The minimum python version is 3.8. Although newer python versions are being tested, they are currently not actively supported.

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
======================
The easiest way of starting the backend services (MongoDB, SciBec and Redis) is to use Docker. Follow the instructions in `Start docker containers for MongoDB, SciBec API server, and Redis`_

Alternatively, you can also install them locally without Docker. Please follow the instructions on the official documentation for `MongoDB <https://www.mongodb.com/docs/manual/installation/>`_ , `Loopback 4 for SciBec <https://loopback.io/doc/en/lb4/Getting-started.html>`_ and `Redis <https://redis.io/docs/getting-started/>`_.

.. include:: install/start_docker_container.rst


.. include:: install/install_bec_services.rst


Update the configuration of the current session 
================================================

.. NOTE::
    Before you can update or modify the configuration, MongoDB AND the SciBec API server must be running. It's okay if the other services are not started.

    Please activate the proper environment as needed.

Create a config file
---------------------

.. include:: install/create_config.rst

.. _update_session:

Upload the (newly created) config file to SciBec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd ./scibec; python ./init_scibec/update_sessions.py

By default, :file:`update_sessions.py` will look for a config file :file:`./init_scibec/demo_config.yaml`. If you have specified a different name, you can use the `--config` option of :file:`update_sessions.py`, e.g.

.. code-block:: bash

    cd ./scibec; python ./init_scibec/update_sessions.py --config <path/to/my/yaml/file.yaml>


.. include:: install/start_python_services.rst

.. include:: install/start_client.rst

