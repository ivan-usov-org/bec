# set base image (host OS)
FROM morgana-harbor.psi.ch/bec/python:3.9

# set the working directory in the container
WORKDIR /code

# copy the content of the local opaas directory to the working directory
COPY . ./bec

WORKDIR /code/bec/scihub
RUN pip install -e .

# command to run on container start
CMD [ "python", "launch.py", "--config", "/code/bec/ci/test_config.yaml"]
