"""
Pre-startup script for BEC client. This script is executed before the BEC client
is started. It can be used to set up the BEC client configuration. The script is
executed in the global namespace of the BEC client. This means that all
variables defined here are available in the BEC client.

To set up the BEC client configuration, use the ServiceConfig class. For example,
to set the configuration file path, add the following lines to the script:

    import pathlib
    from bec_lib.core import ServiceConfig

    current_path = pathlib.Path(__file__).parent.resolve()
    CONFIG_PATH = f"{current_path}/<path_to_my_config_file.yaml>"

    config = ServiceConfig(CONFIG_PATH)

If this startup script defined a ServiceConfig object, the BEC client will use
it to configure itself. Otherwise, the BEC client will use the default config.
"""

# example:
# current_path = pathlib.Path(__file__).parent.resolve()
# CONFIG_PATH = f"{current_path}/../../../bec_config.yaml"
# config = ServiceConfig(CONFIG_PATH)
