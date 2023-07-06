##########################
BEC Service Configuration
##########################

The template config file (:file:`bec_config_template.yaml`) for BEC services contains the following definitions:

.. code-block:: yaml

    redis:
        host: localhost
        port: 6379
    mongodb:
        host: localhost
        port: 27017
    scibec:
        host: http://[::1]
        port: 3030
        beamline: "TestBeamline"
    service_config:
        general:
            reset_queue_on_cancel: True
            enforce_ACLs: False
        file_writer:
            plugin: default_NeXus_format
            base_path: ./

The service config file can always be passed as command-line argument to a single BEC service, e.g. 

.. code-block:: bash

    bec-file-writer --config ./bec_config.yaml

or even to the bec-server command, which will then pass the config file to all services:

.. code-block:: bash

    bec-server start --config ./bec_config.yaml


**********************
Client configuration
**********************

The startup routine used by the `bec` command can be found in :file:`bec_client/bec_client/bin/bec_startup.py`.
If the name of the service config file has changed, please make sure to update the CONFIG_PATH variable accordingly.

