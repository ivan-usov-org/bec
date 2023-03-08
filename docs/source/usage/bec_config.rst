##########################
BEC configuration
##########################


**********************
Service configuration
**********************

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

The service config file is always passed as command-line argument to a BEC service, e.g. 

.. code-block:: bash

    python launch.py --config ./bec_config.yaml

During the setup process, you may have created a new config file based on the template file. If the name deviates from :file:`bec_config.yaml`, please make sure to launch the services with the newly created file. 
In addition, modify the client config as described in the following section.

**********************
Client configuration
**********************

The startup routine used by the `bec` command can be found in :file:`bec_client/bec_client/bin/bec_startup.py`.
If the name of the service config file has changed, please make sure to update the CONFIG_PATH variable accordingly.

