from bec_utils.connector import ConnectorBase


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    message_sent = {}

    def set(self, topic, msg):
        pass

    def send(self, queue, msg):
        self.message_sent = {"queue": queue, "msg": msg}

    def set_and_publish(self, queue, msg):
        self.message_sent = {"queue": queue, "msg": msg}

    def lpush(self, queue, msg):
        pass

    def rpush(self, queue, msg):
        pass

    def lrange(self, queue, start, stop):
        return []

    def get(self, queue):
        return None


class ConnectorMock(ConnectorBase):
    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock()
