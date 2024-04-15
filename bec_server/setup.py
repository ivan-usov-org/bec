import pathlib

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

__version__ = "2.4.0"


if __name__ == "__main__":
    setup(
        install_requires=[
            "bec-lib",
            "cytoolz",
            "h5py",
            "libtmux",
            "lmfit",
            "msgpack",
            "numpy",
            "ophyd",
            "ophyd_devices",
            "pydantic",
            "py-scibec",
            "pyyaml",
            "python-dotenv",
            "rich",
            "xmltodict",
        ],
        extras_require={
            "dev": [
                "black",
                "coverage",
                "isort",
                "pytest",
                "pytest-random-order",
                "pylint",
                "pytest-timeout",
            ]
        },
        entry_points={
            "console_scripts": [
                "bec-dap = bec_server.data_processing:main",
                "bec-device-server = bec_server.device_server:main",
                "bec-file-writer = bec_server.file_writer:main",
                "bec-scan-server = bec_server.scan_server:main",
                "bec-scan-bundler = bec_server.scan_bundler:main",
                "bec-scihub = bec_server.scihub:main",
                "bec-server = bec_server:main",
            ]
        },
        version=__version__,
    )
