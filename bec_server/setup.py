import os
import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()


def get_version():
    """load the version from the version file"""
    version_file = os.path.join(current_path, "../semantic_release", "__init__.py")
    with open(version_file, "r", encoding="utf-8") as file:
        res = file.readline()
        version = res.split("=")[1]
    return version.strip().strip('"')


if __name__ == "__main__":
    setup(
        entry_points={"console_scripts": ["bec-server = bec_server:main"]},
        install_requires=["libtmux"],
        version=get_version(),
        extras_require={"dev": ["pytest", "pytest-random-order", "pytest-asyncio", "coverage"]},
    )
    bec_deps = [
        "bec_lib",
        "bec_client",
        "scan_server",
        "scan_bundler",
        "file_writer",
        "data_processing",
        "scihub",
    ]
    deps = [f"{current_path}/../{dep}/" for dep in bec_deps]
    for dep in deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
