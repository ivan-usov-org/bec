import argparse

import configs as cfgs

DEFAULT_CONFIG_PATH = "./init_scibec/demo_config.yaml"
DEFAULT_CONFIG_CLASS = "DemoConfig"

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--config",
    default=DEFAULT_CONFIG_PATH,
    help="path to the config file",
)
parser.add_argument(
    "--type",
    default=DEFAULT_CONFIG_CLASS,
    help="Config class",
)

clargs = parser.parse_args()
config_path = clargs.config

if not hasattr(cfgs, clargs.type):
    raise ValueError(f"Config class {clargs.type} does not exist.")

config_cls = getattr(cfgs, clargs.type)


out = config_cls(config_path)
out.run()
