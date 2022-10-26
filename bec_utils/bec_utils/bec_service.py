import getpass
import socket
import threading
import time
import uuid
from typing import Any

from rich.console import Console
from rich.table import Table

from . import BECMessage
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
        self._initialize_logger()
        self._check_services()
        self._start_update_service_info()

    def _check_services(self) -> None:
        if not self._unique_service:
            return

        timeout_time = 8
        elapsed_time = 0
        sleep_time = 0.5
        while True:
            services = [
                service.decode().split(":", maxsplit=1)[0]
                for service in self.producer.keys(MessageEndpoints.service_status("*"))
            ]
            msgs = [
                BECMessage.StatusMessage.loads(self.producer.get(service)) for service in services
            ]
            try:
                for msg in msgs:
                    if msg.content["name"] == self.__class__.__name__:
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

    def _update_service_info(self):
        while not self._service_info_event.is_set():
            logger.trace("Updating service info")
            self.producer.set_and_publish(
                topic=MessageEndpoints.service_status(self._service_id),
                msg=BECMessage.StatusMessage(
                    name=self.__class__.__name__,
                    status=BECMessage.BECStatus.RUNNING,
                    info={"user": self._user, "hostname": self._hostname, "timestamp": time.time()},
                ).dumps(),
                expire=6,
            )
            time.sleep(3)

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

    @property
    def global_vars(self):
        """Get all available global variables"""
        available_keys = self.producer.keys(MessageEndpoints.global_vars("*"))

        def get_endpoint_from_topic(topic: str) -> str:
            return topic.decode().split(MessageEndpoints.global_vars(""))[-1].split(":val")[0]

        endpoints = [get_endpoint_from_topic(k) for k in available_keys]

        console = Console()
        table = Table(title="Global variables")
        table.add_column("Variable", justify="center")
        table.add_column("Content", justify="center")
        for endpoint in endpoints:
            var = str(self.get_global_var(endpoint))
            if len(var) > 20:
                var = var[0:10] + "..., " + var[-10:]
            table.add_row(endpoint, var)
        console.print(table)

    def shutdown(self):
        """shutdown the BECService"""
        self._service_info_event.set()
        if self._service_info_thread:
            self._service_info_thread.join()
