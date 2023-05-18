Start the python services
--------------------------

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
    cd ./scihub; python launch.py --config ../bec_config.yaml


where :file:`bec_config.yaml` is a service config file.  

.. cf. [TODO: COMPARE TO?]`bec_config_template.yaml`.