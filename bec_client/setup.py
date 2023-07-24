import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

bec_lib = f"{current_path}/../bec_lib/"


__version__ = "0.14.3"


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
        version=__version__,
        extras_require={
            "dev": [
                "pytest",
                "pytest-random-order",
                "pytest-asyncio",
                "coverage",
                "black",
                "pylint",
            ]
        },
    )
    local_deps = [bec_lib]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)
