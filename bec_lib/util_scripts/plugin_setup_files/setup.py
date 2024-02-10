from setuptools import setup

if __name__ == "__main__":
    setup(
        # specify the additional dependencies
        install_requires=[],
        # if you have additional dependencies for development, specify them here
        extras_require={"dev": ["pytest", "pytest-random-order", "coverage"]},
    )
