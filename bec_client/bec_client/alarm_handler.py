from collections import deque
from bec_utils import Alarms, BECMessage, RedisConnector, MessageEndpoints
from collections import deque


class AlarmException(Exception):
    pass


class AlarmBase(Exception):
    def __init__(
        self, alarm: BECMessage.AlarmMessage, alarm_type: str, severity: Alarms, handled=False
    ) -> None:
        self.alarm = alarm
        self.severity = severity
        self.handled = handled
        self.alarm_type = alarm_type
        super().__init__(self.alarm.content)

    def __str__(self) -> str:
        self.handled = True
        return f"An alarm has occured. Severity: {self.severity.name}. Source: {self.alarm.content['source']}.\n{self.alarm_type}.\n\t {self.alarm.content['content']}"


class AlarmHandler:
    def __init__(self, connector: RedisConnector) -> None:
        self.connector = connector
        self.alarm_consumer = None
        self.alarms_stack = deque(maxlen=100)

    def start(self):
        self.alarm_consumer = self.connector.consumer(
            topics=MessageEndpoints.alarm(), cb=self._alarm_consumer_callback, parent=self
        )
        self.alarm_consumer.start()

    @staticmethod
    def _alarm_consumer_callback(msg, *, parent, **kwargs):
        msg = BECMessage.AlarmMessage.loads(msg.value)
        severity = Alarms(msg.content["severity"])
        parent.alarms_stack.appendleft(
            AlarmBase(
                alarm=msg, alarm_type=msg.content["alarm_type"], severity=severity, handled=False
            )
        )

    def get_unhandled_alarms(self, severity=Alarms.WARNING):
        return [
            alarm for alarm in self.alarms_stack if not alarm.handled and alarm.severity >= severity
        ]

    def raise_alarms(self, severity=Alarms.MINOR):
        alarms = self.get_unhandled_alarms(severity=severity)
        if len(alarms) > 0:
            raise alarms[0]

    def shutdown(self):
        self.alarm_consumer.shutdown()
