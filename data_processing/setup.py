import os
import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()
utils = f"{current_path}/../bec_lib/"


def get_version():
    """load the version from the version file"""
    version_file = os.path.join(current_path, "../semantic_release", "__init__.py")
    with open(version_file, "r", encoding="utf-8") as file:
        res = file.readline()
        version = res.split("=")[1]
    return version.strip().strip('"')


if __name__ == "__main__":
    setup(
        install_requires=["lmfit", "numpy"],
        version=get_version(),
        entry_points={"console_scripts": ["bec-dap = data_processing:main"]},
        extras_require={"dev": ["pytest", "pytest-random-order", "coverage"]},
    )
    local_deps = [utils]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
