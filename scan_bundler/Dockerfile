# set base image (host OS)
ARG PY_VERSION=3.9
FROM morgana-harbor.psi.ch/bec/python:${PY_VERSION}

# set the working directory in the container
WORKDIR /code

# copy the content of the local opaas directory to the working directory
COPY . ./bec

WORKDIR /code/bec/scan_bundler
RUN pip install -e . -e ../bec_lib --config-settings editable_mode=strict

# command to run on container start
CMD [ "python", "launch.py", "--config", "/code/bec/ci/test_config.yaml"]
