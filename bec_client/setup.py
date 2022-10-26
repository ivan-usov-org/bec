import pathlib
import subprocess

from setuptools import setup

current_path = pathlib.Path(__file__).parent.resolve()

utils = f"{current_path}/../bec_utils/"

if __name__ == "__main__":
    setup(
        install_requires=[
            "numpy",
            "msgpack",
            "requests",
            "typeguard",
            "pyyaml",
            "redis",
            "ipython",
            "cytoolz",
            "rich",
            "pyepics",
        ]
    )
    local_deps = [utils]
    for dep in local_deps:
        subprocess.run(f"pip install -e {dep}", shell=True, check=True)

        # install_requires=[
        #     "numpy==1.23.0",
        #     "msgpack==1.0.4",
        #     "requests==2.28.0",
        #     "typeguard==2.13.3",
        #     "pyyaml==6.0",
        #     "redis==4.3.3",
        #     "ipython==8.4.0",
        #     "cytoolz==0.11.2",
        #     "rich==12.4.4",
        # ]
