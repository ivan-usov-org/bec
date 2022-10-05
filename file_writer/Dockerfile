FROM python:3.8

RUN apt-get update
RUN apt-get install -y netcat
RUN apt install -y libopenmpi-dev

# set the working directory in the container
WORKDIR /code

# copy the content of the local bluekafka directory to the working directory
COPY --chown=node ./ ./bluekafka

WORKDIR /code/bluekafka
RUN pip install /code/bluekafka/bluekafka_utils/

WORKDIR /code/bluekafka/file_writer/
RUN pip install -r requirements.txt

ARG value
ENV BEC_CONFIG=$value

CMD python launch.py --config /code/bluekafka/${BEC_CONFIG}]