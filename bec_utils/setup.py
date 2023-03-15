from setuptools import setup

if __name__ == "__main__":
    setup(
        install_requires=["msgpack", "requests", "typeguard<3.0", "pyyaml", "redis", "loguru", "rich"]
    )
