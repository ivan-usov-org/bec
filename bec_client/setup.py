import os
import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

bec_lib = f"{current_path}/../bec_lib/"


def get_version():
    """load the version from the version file"""
    version_file = os.path.join(current_path, "../semantic_release", "__init__.py")
    with open(version_file, "r", encoding="utf-8") as file:
        res = file.readline()
        version = res.split("=")[1]
    return version.strip().strip('"')


if __name__ == "__main__":
    setup(
        install_requires=[
            "numpy",
            "requests",
            "typeguard<3.0",
            "ipython",
            "rich",
            "pyepics",
            "h5py",
        ],
        scripts=["bec_client/bin/bec"],
        version=get_version(),
        extras_require={"dev": ["pytest", "pytest-random-order", "pytest-asyncio", "coverage"]},
    )
    local_deps = [bec_lib]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
