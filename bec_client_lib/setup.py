import pathlib

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()


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
            "loguru",
            "psutil",
        ],
        extras_require={"dev": ["pytest", "pytest-random-order", "coverage", "pandas"]},
    )
