import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

utils = f"{current_path}/../bec_utils/"

ophyd_devices = f"{current_path}/../../ophyd_devices/"


if __name__ == "__main__":
    setup(install_requires=["numpy", "cytoolz", "ophyd"])
    local_deps = [utils, ophyd_devices]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
