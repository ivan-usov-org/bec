# set base image (host OS)
FROM python:3.8-alpine

# set the working directory in the container
WORKDIR /code

# copy the content of the local directory to the working directory
COPY ./scibec/init_scibec ./bec/scibec/init_scibec
COPY ./bec_utils ./bec/bec_utils/

RUN apk update && apk add gcc linux-headers
RUN pip install -e ./bec/bec_utils/
WORKDIR /code/bec/scibec/init_scibec

# command to run on container start
CMD [ "python", "/code/bec/scibec/init_scibec/update_sessions.py", "--config", "/code/bec/scibec/init_scibec/demo_config.yaml"]
