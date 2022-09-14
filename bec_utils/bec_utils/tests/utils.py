from bec_utils.connector import ConnectorBase


class PipelineMock:
    _pipe_buffer = []
    _producer = None

    def __init__(self, producer) -> None:
        self._producer = producer

    def execute(self):
        return [getattr(self._producer, method)(*args) for method, args in self._pipe_buffer]


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    def __init__(self) -> None:
        self.message_sent = {}
        self._get_buffer = {}

    def set(self, topic, msg, pipe=None, expire: int = None):
        if pipe:
            pipe._pipe_buffer.append(("set", (topic, msg)))
            return

    def send(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("send", (topic, msg)))
            return
        self.message_sent = {"queue": topic, "msg": msg}

    def set_and_publish(self, topic, msg, pipe=None, expire: int = None):
        if pipe:
            pipe._pipe_buffer.append(("set_and_publish", (topic, msg)))
            return
        self.message_sent = {"queue": topic, "msg": msg}

    def lpush(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("lpush", (topic, msg)))
            return

    def rpush(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("rpush", (topic, msg)))
            return
        pass

    def lrange(self, topic, start, stop, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("lrange", (topic, msg)))
            return
        return []

    def get(self, topic, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("get", (topic,)))
            return
        val = self._get_buffer.get(topic)
        if isinstance(val, list):
            return val.pop(0)
        self._get_buffer.pop(topic, None)
        return val

    def keys(self, pattern: str) -> list:
        return []

    def pipeline(self):
        return PipelineMock(self)

    def delete(self, topic, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("delete", (topic,)))
            return

    def lset(self, topic: str, index: int, msgs: str, pipe=None) -> None:
        if pipe:
            pipe._pipe_buffer.append(("lrange", (topic, index, msgs)))
            return


class ConnectorMock(ConnectorBase):
    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock()
