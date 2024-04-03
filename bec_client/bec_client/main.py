import argparse
import sys
from importlib.metadata import version
from importlib.metadata import entry_points

from IPython.terminal.ipapp import TerminalIPythonApp

from bec_client.bec_ipython_client import BECIPythonClient
from bec_lib import RedisConnector, ServiceConfig, bec_logger

# pylint: disable=wrong-import-position
# pylint: disable=protected-access
# pylint: disable=unused-import
# pylint: disable=ungrouped-imports

try:
    from bec_widgets.cli import BECFigure
except ImportError:
    BECFigure = None

logger = bec_logger.logger


def main():
    parser = argparse.ArgumentParser(
        prog="BEC IPython client", description="BEC command line interface"
    )
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--nogui", action="store_true", default=False)
    parser.add_argument("--config", action="store", default=None)

    # look for plugins, complete parser with extra args
    discovered_plugins = entry_points(group='bec.plugins')
    plugin_modules = []
    for plugin in discovered_plugins:
        print(f"Loading BEC plugin: {plugin.name}")
        plugin_module = plugin.load()
        plugin_modules.append(plugin_module)
        plugin_module.extend_command_line_args(parser)

    args, left_args = parser.parse_known_args()

    # remove already parsed args from command line args
    sys.argv = sys.argv[:1] + left_args

    if args.version:
        print(f"BEC IPython client: {version('bec_client')}")
        sys.exit(0)

    config_file = args.config
    if config_file:
        if not os.path.isfile(config_file):
            raise FileNotFoundError("Config file not found.")
        print("Using config file: ", config_file)
        config = ServiceConfig(config_file)

    config = ServiceConfig()

    app = TerminalIPythonApp()
    app.interact = True
    app.initialize(argv=[])

    bec = BECIPythonClient(config, RedisConnector)
    bec.load_high_level_interface("spec_hli")
    bec.start()

    dev = bec.device_manager.devices
    scans = bec.scans

    if not args.nogui and BECFigure is not None:
        fig = bec.fig = BECFigure()
        fig.show()

    ####################### END OF INIT #############################
    #################################################################

    # MODIFY THE SECTIONS BELOW TO CUSTOMIZE THE BEC

    ################################################################
    ################################################################
    import numpy as np  # not needed but always nice to have

    bec._ip.prompts.status = 1

    # SETUP BEAMLINE INFO
    from bec_client.plugins.SLS.sls_info import OperatorInfo, SLSInfo

    bec._beamline_mixin._bl_info_register(SLSInfo)
    bec._beamline_mixin._bl_info_register(OperatorInfo)

    # go through plugins and initialize those
    for plugin in plugin_modules:
        plugin.setup(parser)

    try:
        app.start()
    finally:
        bec.shutdown()


if __name__ == "__main__":
    main()
