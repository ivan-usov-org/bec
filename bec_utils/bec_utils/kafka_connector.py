from kafka import KafkaConsumer, KafkaProducer
from .connector import ConnectorBase, ConsumerConnectorThreaded, ProducerConnector
from .KafkaMessage import LogMessage
from confluent_kafka import Producer


class KafkaConnector(ConnectorBase):
    def __init__(self, bootstrap: list):
        super().__init__(bootstrap)
        self._notifications_producer = KafkaConnectorProducerKafkaPython(
            bootstrap_servers=self.bootstrap
        )

    def producer(self, acks=1):
        return KafkaConnectorProducerKafkaPython(bootstrap_servers=self.bootstrap, acks=acks)

    def consumer(
        self, topics=None, pattern=None, group_id=None, event=None, cb=None, threaded=True, **kwargs
    ):
        if threaded:
            if topics is None and pattern is None:
                raise ValueError("Topics must be set for threaded consumer")
            listener = KafkaConnectorConsumer(
                self.bootstrap, topics, pattern, group_id, event, cb, **kwargs
            )
            self._threads.append(listener)
            return listener
        else:
            return KafkaConsumer(bootstrap_servers=self.bootstrap)

    def raise_warning(self, msg):
        self._notifications_producer.send("log", LogMessage(type="warning", content=msg).dumps())

    def send_log(self, msg):
        self._notifications_producer.send("log", LogMessage(type="log", content=msg).dumps())

    def raise_error(self, msg):
        self._notifications_producer.send("log", LogMessage(type="error", content=msg).dumps())


class KafkaConnectorProducerKafkaPython(ProducerConnector):
    def __init__(self, bootstrap_servers: list, acks: int = 1):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send(self, topic: str, msg) -> None:
        self.producer.send(topic=topic, value=msg)


class KafkaConnectorProducerConfluent(ProducerConnector):
    def __init__(self, bootstrap_servers: list, acks: int):
        conf = {
            "bootstrap.servers": "localhost:9092",
            "queue.buffering.max.messages": 1000000,
            "queue.buffering.max.ms": 2,  ### <==== FIXME: this is fine for large files where the total send time will be above 500ms, but for small files it will add some delay - there is no harm in decreasing this value to something like 10 or 100 ms. On the other hand that may be offset by a lower batch.num.messages, but that is typically not the way to go.
            "default.topic.config": {"acks": "all"},
        }
        self.producer = Producer(**conf)

    def send(self, topic: str, msg):
        try:
            self.producer.produce(topic, value=msg)
            # self.producer.poll(0)
        except BufferError as e:
            self.producer.poll(0.1)
            self.producer.produce(topic, value=msg)


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
