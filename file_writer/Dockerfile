# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the content of the local opaas directory to the working directory
COPY . ./bec

WORKDIR /code/bec/file_writer
RUN pip install -e .

# command to run on container start
CMD [ "python", "launch.py", "--config", "/code/bec/test_config.yaml"]
