from setuptools import setup

if __name__ == "__main__":
    setup(
        install_requires=[
            "msgpack",
            "requests",
            "typeguard",
            "pyyaml",
            "redis",
            "loguru",
            "rich",
            "psutil",
        ]
    )
