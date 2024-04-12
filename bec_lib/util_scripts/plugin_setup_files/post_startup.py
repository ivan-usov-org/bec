"""
Post startup script for the BEC client. This script is executed after the
IPython shell is started. It is used to load the beamline specific
information and to setup the prompts.

The script is executed in the global namespace of the IPython shell. This
means that all variables defined here are available in the shell.

If needed, bec command-line arguments can be parsed here. For example, to
parse the --session argument, add the following lines to the script:

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", help="Session name", type=str, default="my_default_session")
    args = parser.parse_args()

    if args.session == "my_session":
        print("Loading my_session session")
        from bec_plugins.bec_ipython_client.plugins.my_session import *
    else:
        print("Loading default session")
        from bec_plugins.bec_ipython_client.plugins.default_session import *
"""

# pylint: disable=invalid-name, unused-import, import-error, undefined-variable, unused-variable, unused-argument, no-name-in-module

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("--session", help="Session name", type=str, default="my_default_session")
# args = parser.parse_args()

# if args.session == "my_session":
#     print("Loading my_session session")
#     from bec_plugins.bec_ipython_client.plugins.my_session import *
# else:
#     print("Loading default session")
#     from bec_plugins.bec_ipython_client.plugins.default_session import *


# SETUP BEAMLINE INFO
# from bec_ipython_client.plugins.SLS.sls_info import OperatorInfo, SLSInfo

# from bec_plugins.bec_ipython_client.plugins.MyBeamline.beamline_info import BeamlineInfo

# bec._beamline_mixin._bl_info_register(BeamlineInfo)
# bec._beamline_mixin._bl_info_register(SLSInfo)
# bec._beamline_mixin._bl_info_register(OperatorInfo)

# SETUP PROMPTS
# bec._ip.prompts.username = args.session
# bec._ip.prompts.status = 1


# REGISTER BEAMLINE CHECKS
# from bec_lib.bl_conditions import (
#     LightAvailableCondition,
#     ShutterCondition,
# )

# _light_available_condition = LightAvailableCondition(dev.sls_machine_status)
# _shutter_condition = ShutterCondition(dev.x12sa_es1_shutter_status)
# bec.bl_checks.register(_light_available_condition)
# bec.bl_checks.register(_shutter_condition)
