from setuptools import setup

__version__ = "0.50.0"

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
        extras_require={
            "dev": ["pytest", "pytest-random-order", "coverage", "pandas", "black", "pylint"]
        },
        package_data={"bec_lib.tests": ["*.yaml"], "bec_lib.configs": ["*.yaml", "*.json"]},
        version=__version__,
    )
