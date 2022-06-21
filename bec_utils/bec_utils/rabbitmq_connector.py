from asyncio import queues
import functools
from kafka import KafkaConsumer, KafkaProducer
from .connector import ConnectorBase, ConsumerConnectorThreaded, ProducerConnector
from .BECMessage import LogMessage
import pika


class RabbitMQConnector(ConnectorBase):
    def __init__(self, bootstrap: list):
        super().__init__(bootstrap)
        self._notifications_producer = RabbitMQProducer(bootstrap_servers=self.bootstrap)

    def producer(self, acks=1):
        return RabbitMQProducer(bootstrap_servers=self.bootstrap)

    def consumer(
        self, topics=None, pattern=None, group_id=None, event=None, cb=None, threaded=True, **kwargs
    ):
        listener = RabbitMQConsumer(self.bootstrap, topics, cb, **kwargs)
        self._threads.append(listener)
        return listener

    def raise_warning(self, msg):
        self._notifications_producer.send("log", LogMessage(type="warning", content=msg).dumps())

    def send_log(self, msg):
        self._notifications_producer.send("log", LogMessage(type="log", content=msg).dumps())

    def raise_error(self, msg):
        self._notifications_producer.send("log", LogMessage(type="error", content=msg).dumps())


class RabbitMQProducer(ProducerConnector):
    def __init__(self, bootstrap_servers: list):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=bootstrap_servers))
        self._channel = connection.channel()

    def send(self, topic: str, msg) -> None:
        self._channel.basic_publish(exchange="", routing_key=topic, body=msg)

    def create_topic(self, topic: str):
        self._channel.queue_declare(queue=topic)


def rabbitmq_callback(ch, method, properties, body, args):
    (cb, kwargs) = args
    cb(body, **kwargs)


class RabbitMQConsumer(ConsumerConnectorThreaded):
    def __init__(self, bootstrap_servers: list, topics, cb, **kwargs) -> None:
        super().__init__(bootstrap_server=bootstrap_servers, topics=topics, cb=cb, **kwargs)

    def initialize_connector(self) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.bootstrap))
        self._channel = self.connection.channel()
        self.create_topic()

    def create_topic(self):
        self._channel.queue_declare(queue=self.topics)

    def run(self):
        self.initialize_connector()

        self._consume()

    def _consume(self):
        on_message_callback = functools.partial(rabbitmq_callback, args=(self.cb, self.kwargs))

        self._channel.basic_consume(
            queue=self.topics, auto_ack=True, on_message_callback=on_message_callback
        )
        self._channel.start_consuming()


class KafkaConnectorConsumer(ConsumerConnectorThreaded):
    def __init__(
        self, bootstrap, topics, pattern=None, group_id=None, event=None, cb=None, **kwargs
    ):
        super().__init__(bootstrap, topics, pattern, group_id, event, cb, **kwargs)
        self.auto_offset_reset = kwargs.get("auto_offset_reset", "latest")

    def initialize_connector(self) -> None:
        self.connector = KafkaConsumer(
            bootstrap_servers=self.bootstrap,
            group_id=self.group_id,
            auto_offset_reset=self.auto_offset_reset,
        )
        if self.pattern is not None:
            self.connector.subscribe(pattern=self.pattern)
        else:
            self.connector.subscribe(self.topics)


if __name__ == "__main__":
    connector = RabbitMQConnector("localhost")
