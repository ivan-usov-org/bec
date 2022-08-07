import getpass
import socket
import threading
import time
import uuid

from . import BECMessage
from .connector import ConnectorBase
from .endpoints import MessageEndpoints
from .logger import bec_logger

logger = bec_logger.logger


class BECService:
    def __init__(self, bootstrap_server: list, connector_cls: ConnectorBase) -> None:
        self.bootstrap_server = bootstrap_server
        self._connector_cls = connector_cls
        self.connector = connector_cls(bootstrap_server)
        self.producer = self.connector.producer()
        self._service_id = str(uuid.uuid4())
        self._user = getpass.getuser()
        self._hostname = socket.gethostname()
        self._service_info_thread = None
        self._service_info_event = threading.Event()
        self._initialize_logger()
        self._start_update_service_info()

    def _initialize_logger(self) -> None:
        bec_logger.configure(
            self.bootstrap_server, self._connector_cls, service_name=self.__class__.__name__
        )

    def _update_service_info(self):
        while not self._service_info_event.is_set():
            logger.trace("Updating service info")
            self.producer.set_and_publish(
                topic=MessageEndpoints.service_status(self._service_id),
                msg=BECMessage.StatusMessage(status=BECMessage.BECStatus.RUNNING).dumps(),
            )
            time.sleep(3)

    def _start_update_service_info(self):
        self._service_info_thread = threading.Thread(target=self._update_service_info, daemon=True)
        self._service_info_thread.start()

    def shutdown(self):
        """shutdown the BECService"""
        self._service_info_event.set()
        if self._service_info_thread:
            self._service_info_thread.join()
