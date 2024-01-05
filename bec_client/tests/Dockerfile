# set base image (host OS)
ARG PY_VERSION=3.9
FROM morgana-harbor.psi.ch/bec/python:${PY_VERSION}

# set the working directory in the container
WORKDIR /code

# copy the content of the local opaas directory to the working directory
COPY . ./bec

WORKDIR /code/bec/bec_client
RUN pip install -e . -e ../bec_lib
RUN pip install pytest pytest-timeout pytest-random-order

# command to run on container start
CMD [ "pytest", "-v", "--random-order", "./tests/end-2-end"]
