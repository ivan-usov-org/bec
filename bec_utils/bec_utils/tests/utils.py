import uuid

from bec_utils.connector import ConnectorBase
from bec_utils.redis_connector import Alarms


class PipelineMock:
    _pipe_buffer = []
    _producer = None

    def __init__(self, producer) -> None:
        self._producer = producer

    def execute(self):
        return [
            getattr(self._producer, method)(*args, **kwargs)
            for method, args, kwargs in self._pipe_buffer
        ]


class ConsumerMock:
    def start(self):
        pass


class ProducerMock:
    def __init__(self) -> None:
        self.message_sent = []
        self._get_buffer = {}

    def set(self, topic, msg, pipe=None, expire: int = None):
        if pipe:
            pipe._pipe_buffer.append(("set", (topic, msg), {"expire": expire}))
            return
        self.message_sent.append({"queue": topic, "msg": msg, "expire": expire})

    def send(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("send", (topic, msg)))
            return
        self.message_sent.append({"queue": topic, "msg": msg})

    def set_and_publish(self, topic, msg, pipe=None, expire: int = None):
        if pipe:
            pipe._pipe_buffer.append(("set_and_publish", (topic, msg), {"expire": expire}))
            return
        self.message_sent.append({"queue": topic, "msg": msg, "expire": expire})

    def lpush(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("lpush", (topic, msg), {}))
            return

    def rpush(self, topic, msg, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("rpush", (topic, msg), {}))
            return
        pass

    def lrange(self, topic, start, stop, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("lrange", (topic, start, stop), {}))
            return
        return []

    def get(self, topic, pipe=None):
        if pipe:
            pipe._pipe_buffer.append(("get", (topic,), {}))
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
            pipe._pipe_buffer.append(("delete", (topic,), {}))
            return

    def lset(self, topic: str, index: int, msgs: str, pipe=None) -> None:
        if pipe:
            pipe._pipe_buffer.append(("lrange", (topic, index, msgs), {}))
            return


class ConnectorMock(ConnectorBase):
    def consumer(self, *args, **kwargs) -> ConsumerMock:
        return ConsumerMock()

    def producer(self, *args, **kwargs):
        return ProducerMock()

    def raise_alarm(
        self, severity: Alarms, alarm_type: str, source: str, content: dict, metadata: dict
    ):
        pass


def create_session_from_config(config: dict) -> dict:
    device_configs = []
    session_id = str(uuid.uuid4())
    for name, conf in config.items():
        status = conf.pop("status")
        dev_conf = {
            "id": str(uuid.uuid4()),
            "accessGroups": "customer",
            "name": name,
            "sessionId": session_id,
            "enabled": status["enabled"],
            "enabled_set": status["enabled_set"],
        }
        dev_conf.update(conf)
        device_configs.append(dev_conf)
    session = {"accessGroups": "customer", "devices": device_configs}
    return session
