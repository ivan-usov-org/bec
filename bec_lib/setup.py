import os
import pathlib

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
        install_requires=[
            "numpy",
            "msgpack",
            "requests",
            "typeguard<3.0",
            "pyyaml",
            "redis",
            "cytoolz",
            "rich",
            "pylint",
            "loguru",
            "psutil",
            "fpdf",
        ],
        extras_require={"dev": ["pytest", "pytest-random-order", "coverage", "pandas"]},
        version=get_version(),
    )
