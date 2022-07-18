# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the content of the local opaas directory to the working directory
COPY . ./bec

WORKDIR /code/bec/bec_client
RUN pip install -e .
RUN pip install pytest pytest-timeout pytest-random-order

# command to run on container start
CMD [ "pytest", "-v", "--random-order", "./tests"]
