#############
Installation
#############


Redis
------
To install Redis, you can either use conda 

.. code-block:: bash

    conda install redis

or install it manually by following the instructions `here <https://redis.io/docs/getting-started/>`_. Once installed, start it with 

.. code-block:: bash

    redis-server

If you prefer to run redis in Docker, you can also follow the instructions in `Start docker containers for MongoDB, SciBec API server, and Redis`_ instead of installing it through conda.


BEC
----

.. collapse:: Install user environment
    :open:

    If you want to install the BEC server as a user and not for development purposes, you can create a Python (>= 3.8) environment using

    .. code-block:: bash

        python -m venv ./bec_venv
        source ./bec_venv/bin/activate

    and install the BEC server using

    .. code-block:: bash

        pip install bec-server

    Once installed, you can start the server using

    .. code-block:: bash

        bec-server start

    To install the BEC client, run

    .. code-block:: bash

        pip install bec-ipython-client

    and start the client using

    .. code-block:: bash

        bec

    You are now ready to load your first device configuration. To this end, please follow the instructions given in :doc:`quickstart`.


.. collapse:: Install developer / expert environment

    If you want to install the BEC server for development purposes, make sure you have git and conda installed. Then, run 

    .. code-block:: bash

        git clone https://gitlab.psi.ch/bec/ophyd_devices.git
        git clone https://gitlab.psi.ch/bec/bec.git
        cd bec

        source ./bin/install_bec_dev.sh

    .. note::

        If you need to connect to redis on a different port than the default (6379), you can create a service config file based on the template
        in ``bec/bec_config_template.yaml`` and pass it to the bec-server using the ``--config`` flag.

    Once everything is installed, run

    .. code-block:: bash

        bec-server start

    To start the client, run

    .. code-block:: bash

        bec

    You are now ready to load your first device configuration. To this end, please follow the instructions given in :doc:`quickstart`.

