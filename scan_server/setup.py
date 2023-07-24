import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

utils = f"{current_path}/../bec_lib/"

__version__ = "0.14.4"

if __name__ == "__main__":
    setup(
        install_requires=["numpy", "msgpack", "pyyaml", "cytoolz", "rich"],
        version=__version__,
        extras_require={"dev": ["pytest", "pytest-random-order", "coverage", "black", "pylint"]},
        entry_points={"console_scripts": ["bec-scan-server = scan_server:main"]},
    )
    local_deps = [utils]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
