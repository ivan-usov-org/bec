# set base image (host OS)
FROM python:3.8-alpine

# set the working directory in the container
WORKDIR /code

# copy the content of the local directory to the working directory
COPY ./scibec/init_scibec ./bec/scibec/init_scibec
COPY ./bec_client_lib ./bec/bec_client_lib/
COPY ./scihub ./bec/scihub/
COPY ./semantic_release ./bec/semantic_release/


RUN apk update && apk add gcc libc-dev build-base linux-headers
RUN pip install -e ./bec/bec_client_lib/
RUN pip install -e ./bec/scihub/
WORKDIR /code/bec/scibec/init_scibec

# command to run on container start
CMD [ "python", "/code/bec/scibec/init_scibec/update_sessions.py", "--config", "/code/bec/scibec/init_scibec/demo_config.yaml"]
