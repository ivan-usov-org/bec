# set base image (host OS)
FROM python:3.9

RUN apt-get update
RUN apt-get install -y netcat
RUN apt install -y libopenmpi-dev

# set the working directory in the container
WORKDIR /code

# copy the content of the local opaas directory to the working directory
COPY bec/ ./bec

WORKDIR /code/bec
RUN pip install ./bec_utils/
RUN pip install ./koss/
RUN pip install ./ophyd/

WORKDIR /code/bec/opaas/
RUN pip install -r requirements.txt

# command to run on container start
# CMD [ "ipython", "-i", "-c", "%run launch.py --bootstrap host.docker.internal:6379" ]
CMD "ipython"
# ipython -i -c "%run launch.py --bootstrap host.docker.internal:6379"