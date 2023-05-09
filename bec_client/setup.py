import os
import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

utils = f"{current_path}/../bec_utils/"
bec_client_lib = f"{current_path}/../bec_client_lib/"

if __name__ == "__main__":
    setup(
        install_requires=[
            "numpy",
            "msgpack",
            "requests",
            "typeguard<3.0",
            "pyyaml",
            "redis",
            "ipython",
            "cytoolz",
            "rich",
            "pyepics",
            "pylint",
        ],
        scripts=["bec_client/bin/bec"],
    )
    local_deps = [utils, bec_client_lib]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
