import threading
import time
from queue import Queue

from bec_utils import BECMessage


class EmitterBase:
    def __init__(self, producer) -> None:
        self._send_buffer = Queue()
        self.producer = producer
        self._start_buffered_producer()

    def _start_buffered_producer(self):
        self._buffered_producer_thread = threading.Thread(
            target=self._buffered_publish, daemon=True
        )
        self._buffered_producer_thread.start()

    def add_message(self, msg: BECMessage.BECMessage, endpoint: str, public: str = None):
        self._send_buffer.put((msg, endpoint, public))

    def _buffered_publish(self):

        while True:
            msgs_to_send = []
            while not self._send_buffer.empty():
                msgs_to_send.append(self._send_buffer.get())
            if len(msgs_to_send) > 0:
                pipe = self.producer.pipeline()
                msgs = BECMessage.BundleMessage()
                _, endpoint, _ = msgs_to_send[0]
                for msg, endpoint, public in msgs_to_send:
                    msg_dump = msg.dumps()
                    msgs.append(msg_dump)
                    if public:
                        self.producer.set(
                            public,
                            msg_dump,
                            pipe=pipe,
                            expire=1800,
                        )
                self.producer.send(endpoint, msgs.dumps(), pipe=pipe)
                pipe.execute()
                continue
            time.sleep(0.1)
