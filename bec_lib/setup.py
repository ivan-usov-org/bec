from setuptools import setup

__version__ = "1.14.3"

if __name__ == "__main__":
    setup(
        install_requires=[
            "hiredis",
            "louie",
            "numpy",
            "scipy",
            "msgpack",
            "requests",
            "typeguard>=4.0.1",
            "pyyaml",
            "redis",
            "toolz",
            "rich",
            "pylint",
            "loguru",
            "psutil",
            "fpdf",
            "fastjsonschema",
            "lmfit",
        ],
        extras_require={
            "dev": [
                "pytest",
                "pytest-random-order",
                "pytest-timeout",
                "coverage",
                "pandas",
                "black",
                "pylint",
                "fakeredis",
            ]
        },
        entry_points={"console_scripts": ["bec-channel-monitor = bec_lib:channel_monitor_launch"]},
        package_data={"bec_lib.tests": ["*.yaml"], "bec_lib.configs": ["*.yaml", "*.json"]},
        version=__version__,
    )
