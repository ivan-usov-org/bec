from bec_utils.connector import ConnectorBase


class PipelineMock:
    def execute(self):
        pass


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    message_sent = {}

    def set(self, topic, msg, pipe=None):
        pass

    def send(self, topic, msg, pipe=None):
        self.message_sent = {"queue": topic, "msg": msg}

    def set_and_publish(self, topic, msg, pipe=None):
        self.message_sent = {"queue": topic, "msg": msg}

    def lpush(self, topic, msg, pipe=None):
        pass

    def rpush(self, topic, msg, pipe=None):
        pass

    def lrange(self, topic, start, stop, pipe=None):
        return []

    def get(self, topic, pipe=None):
        return None

    def pipeline(self):
        return PipelineMock()

    def delete(self, topic, pipe=None):
        pass

    def lset(self, topic: str, index: int, msgs: str, pipe=None) -> None:
        pass


class ConnectorMock(ConnectorBase):
    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock()
