import enum
import getpass
import socket
import threading
import time
import uuid
from typing import Any

from . import BECMessage
from .BECMessage import BECStatus
from .connector import ConnectorBase
from .endpoints import MessageEndpoints
from .logger import bec_logger

logger = bec_logger.logger


class BECService:
    def __init__(
        self, bootstrap_server: list, connector_cls: ConnectorBase, unique_service=False
    ) -> None:
        self.bootstrap_server = bootstrap_server
        self._connector_cls = connector_cls
        self.connector = connector_cls(bootstrap_server)
        self._unique_service = unique_service
        self.producer = self.connector.producer()
        self._service_id = str(uuid.uuid4())
        self._user = getpass.getuser()
        self._hostname = socket.gethostname()
        self._service_info_thread = None
        self._service_info_event = threading.Event()
        self._services_info = {}
        self._initialize_logger()
        self._check_services()
        self._status = BECStatus.BUSY
        self._start_update_service_info()

    def _check_services(self) -> None:
        if not self._unique_service:
            return

        timeout_time = 8
        elapsed_time = 0
        sleep_time = 0.5
        while True:
            self._update_existing_services()
            try:
                for service_name, msg in self._services_info.items():
                    if service_name == self.__class__.__name__:
                        raise RuntimeError(
                            f"Another instance of {self.__class__.__name__} launched by user {msg.content['info']['user']} is already running on {msg.content['info']['hostname']}"
                        )
                break
            except RuntimeError as service_error:
                if elapsed_time > timeout_time:
                    raise RuntimeError from service_error
                elapsed_time += sleep_time
                time.sleep(sleep_time)

    def _initialize_logger(self) -> None:
        bec_logger.configure(
            self.bootstrap_server, self._connector_cls, service_name=self.__class__.__name__
        )

    def _update_existing_services(self):
        services = [
            service.decode().split(":", maxsplit=1)[0]
            for service in self.producer.keys(MessageEndpoints.service_status("*"))
        ]
        msgs = [BECMessage.StatusMessage.loads(self.producer.get(service)) for service in services]
        self._services_info = {msg.content["name"]: msg for msg in msgs}

    def _update_service_info(self):
        while not self._service_info_event.is_set():
            logger.trace("Updating service info")
            self._send_service_status()
            time.sleep(3)

    def _send_service_status(self):
        self.producer.set_and_publish(
            topic=MessageEndpoints.service_status(self._service_id),
            msg=BECMessage.StatusMessage(
                name=self.__class__.__name__,
                status=self.status,
                info={"user": self._user, "hostname": self._hostname, "timestamp": time.time()},
            ).dumps(),
            expire=6,
        )

    @property
    def status(self) -> BECStatus:
        """get the current BECService status"""
        return self._status

    @status.setter
    def status(self, val: BECStatus):
        self._status = val
        self._send_service_status()

    def _start_update_service_info(self):
        self._service_info_thread = threading.Thread(target=self._update_service_info, daemon=True)
        self._service_info_thread.start()

    def set_global_var(self, name: str, val: Any) -> None:
        """Set a global variable through Redis

        Args:
            name (str): Name of the variable
            val (Any): Value of the variable

        """
        self.producer.set(
            MessageEndpoints.global_vars(name), BECMessage.VariableMessage(value=val).dumps()
        )

    def get_global_var(self, name: str) -> Any:
        """Get a global variable from Redis

        Args:
            name (str): Name of the variable

        Returns:
            Any: Value of the variable
        """
        msg = BECMessage.VariableMessage.loads(
            self.producer.get(MessageEndpoints.global_vars(name))
        )
        if msg:
            return msg.content.get("value")
        return None

    def delete_global_var(self, name: str) -> None:
        """Delete a global variable from Redis

        Args:
            name (str): Name of the variable

        """
        self.producer.delete(MessageEndpoints.global_vars(name) + ":val")

    def shutdown(self):
        """shutdown the BECService"""
        self._service_info_event.set()
        if self._service_info_thread:
            self._service_info_thread.join()

    @property
    def service_status(self):
        self._update_existing_services()
        return self._services_info

    def wait_for_service(self, name, status=BECStatus.RUNNING):
        pass
