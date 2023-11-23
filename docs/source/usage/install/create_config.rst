While there is already a config file available for simulated devices (`bec_lib/configs/demo_config.yaml`), you can create new configs based on templates using:

.. code-block:: bash

    cd ./scibec; python ./init_scibec/create_config_file.py

This will create a config file :file:`./init_scibec/demo_config.yaml`.

As optional parameters, it can receive the output path + filename (--config) and the template type (--type). The latter must be one of the classes imported in
:file:`scibec/init_scibec/configs/__init__.py`. 

Currently :file:`init_scibec/configs/__init__.py`` supports `DemoConfig`, `TestConfig` and `LamNIConfig`. 
