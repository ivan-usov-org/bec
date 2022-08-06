from bec_utils.connector import ConnectorBase


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    message_sent = {}

    def set(self, topic, msg):
        pass

    def send(self, topic, msg):
        self.message_sent = {"queue": topic, "msg": msg}

    def set_and_publish(self, topic, msg):
        self.message_sent = {"queue": topic, "msg": msg}

    def lpush(self, topic, msg):
        pass

    def rpush(self, topic, msg):
        pass

    def lrange(self, topic, start, stop):
        return []

    def get(self, topic):
        return None


class ConnectorMock(ConnectorBase):
    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock()
