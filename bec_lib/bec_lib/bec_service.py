"""
This module provides the BECService class, which is the base class for all BEC services.
"""

from __future__ import annotations

import getpass
import socket
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

import psutil
from rich.console import Console
from rich.table import Table

from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.service_config import ServiceConfig
from bec_lib.utils.import_utils import lazy_import, lazy_import_from

if TYPE_CHECKING:
    from bec_lib.connector import ConnectorBase

# TODO: put back normal imports when Pydantic gets faster
messages = lazy_import("bec_lib.messages")
BECStatus = lazy_import_from("bec_lib.messages", ("BECStatus",))


logger = bec_logger.logger

SERVICE_CONFIG = None


class BECService:
    def __init__(
        self,
        config: str | ServiceConfig,
        connector_cls: ConnectorBase,
        unique_service=False,
        wait_for_server=False,
        name: str | None = None,
    ) -> None:
        super().__init__()
        self._name = name if name else self.__class__.__name__
        self._import_config(config)
        self._connector_cls = connector_cls
        self.connector = connector_cls(self.bootstrap_server)
        self._unique_service = unique_service
        self.wait_for_server = wait_for_server
        self.__service_id = str(uuid.uuid4())
        self._user = getpass.getuser()
        self._hostname = socket.gethostname()
        self._service_info_thread = None
        self._service_info_event = threading.Event()
        self._metrics_emitter_thread = None
        self._metrics_emitter_event = threading.Event()
        self._services_info = {}
        self._services_metric = {}
        self._initialize_logger()
        self._check_services()
        self._status = BECStatus.BUSY
        self._start_update_service_info()
        self._start_metrics_emitter()
        self._wait_for_server()

    @property
    def _service_name(self):
        return self._name if self._unique_service else f"{self._name}/{self._service_id}"

    @property
    def _service_id(self):
        return self.__service_id

    def _import_config(self, config: str | ServiceConfig) -> None:
        if isinstance(config, str):
            self._service_config = ServiceConfig(config_path=config)
        elif isinstance(config, ServiceConfig):
            self._service_config = config
        else:
            raise TypeError("config must be of type str or ServiceConfig")
        global SERVICE_CONFIG
        SERVICE_CONFIG = self._service_config
        self.bootstrap_server = self._service_config.redis

    def _check_services(self, timeout_time=8, sleep_time=0.5) -> None:
        if not self._unique_service:
            return
        elapsed_time = 0
        while self._run_service_check(timeout_time, elapsed_time):
            elapsed_time += sleep_time
            time.sleep(sleep_time)

    def _run_service_check(self, timeout_time: float, elapsed_time: float) -> bool:
        self._update_existing_services()
        try:
            for service_name, msg in self._services_info.items():
                if service_name == self.__class__.__name__:
                    raise RuntimeError(
                        f"Another instance of {self.__class__.__name__} launched by user"
                        f" {msg.content['info']['user']} is already running on"
                        f" {msg.content['info']['hostname']}"
                    )
            return False
        except RuntimeError as service_error:
            if elapsed_time > timeout_time:
                raise RuntimeError from service_error
        return True

    def _initialize_logger(self) -> None:
        bec_logger.configure(
            self.bootstrap_server,
            self._connector_cls,
            service_name=self._name,
            service_config=self._service_config.config["service_config"],
        )

    def _update_existing_services(self):
        service_keys = self.connector.keys(MessageEndpoints.service_status("*"))
        if not service_keys:
            return
        # service keys are in the form of: "internal/services/status/4b9d1af8-44ed-4f3a-8787-ef9f958f59b"
        services = []
        for service_key in service_keys:
            _, _, service_id = service_key.decode().rpartition("/")
            services.append(service_id)
        msgs = [
            self.connector.get(MessageEndpoints.service_status(service)) for service in services
        ]
        self._services_info = {msg.content["name"]: msg for msg in msgs if msg is not None}
        msgs = [self.connector.get(MessageEndpoints.metrics(service)) for service in services]
        self._services_metric = {msg.content["name"]: msg for msg in msgs if msg is not None}

    def _update_service_info(self):
        while not self._service_info_event.is_set():
            logger.trace("Updating service info")
            try:
                self._send_service_status()
            except Exception:
                # exception is not explicitely specified,
                # because it depends on the underlying connector
                pass
            self._service_info_event.wait(timeout=3)

    def _send_service_status(self):
        self.connector.set_and_publish(
            topic=MessageEndpoints.service_status(self._service_id),
            msg=messages.StatusMessage(
                name=self._service_name,
                status=self.status,
                info={"user": self._user, "hostname": self._hostname, "timestamp": time.time()},
            ),
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
        self._service_info_thread = threading.Thread(
            target=self._update_service_info, daemon=True, name="update_service_info"
        )
        self._service_info_thread.start()

    def _start_metrics_emitter(self):
        self._metrics_emitter_thread = threading.Thread(
            target=self._get_metrics, daemon=True, name="metrics_emitter"
        )
        self._metrics_emitter_thread.start()

    def _get_metrics(self):
        proc = psutil.Process()
        while not self._metrics_emitter_event.is_set():
            res = proc.as_dict(
                attrs=[
                    "name",
                    "num_threads",
                    "pid",
                    "cpu_percent",
                    "memory_info",
                    "cmdline",
                    "cpu_times",
                    "create_time",
                    "memory_percent",
                ]
            )

            data = asdict(
                ServiceMetric(
                    process_name=res["name"],
                    username=self._user,
                    hostname=self._hostname,
                    cpu_percent=res["cpu_percent"],
                    cpu_times=res["cpu_times"].user,
                    cmdline=res["cmdline"],
                    num_threads=res["num_threads"],
                    pid=res["pid"],
                    memory_in_mb=res["memory_info"].rss / 1024 / 1024,
                    memory_used_percent=res["memory_percent"],
                    create_time=res["create_time"],
                )
            )
            msg = messages.ServiceMetricMessage(name=self._service_name, metrics=data)
            try:
                self.connector.set_and_publish(MessageEndpoints.metrics(self._service_id), msg)
            except Exception:
                # exception is not explicitely specified,
                # because it depends on the underlying connector
                pass
            self._metrics_emitter_event.wait(timeout=1)

    def set_global_var(self, name: str, val: Any) -> None:
        """Set a global variable through Redis

        Args:
            name (str): Name of the variable
            val (Any): Value of the variable

        """
        self.connector.set(MessageEndpoints.global_vars(name), messages.VariableMessage(value=val))

    def get_global_var(self, name: str) -> Any:
        """Get a global variable from Redis

        Args:
            name (str): Name of the variable

        Returns:
            Any: Value of the variable
        """
        msg = self.connector.get(MessageEndpoints.global_vars(name))
        if msg:
            return msg.content.get("value")
        return None

    def delete_global_var(self, name: str) -> None:
        """Delete a global variable from Redis

        Args:
            name (str): Name of the variable

        """
        self.connector.delete(MessageEndpoints.global_vars(name))

    def show_global_vars(self) -> str:
        """Get all available global variables"""
        # sadly, this cannot be a property as it causes side effects with IPython's tab completion
        available_keys = self.connector.keys(MessageEndpoints.global_vars("*"))

        def get_endpoint_from_topic(topic: str) -> str:
            return topic.decode().split(MessageEndpoints.global_vars("").endpoint)[-1]

        endpoints = [get_endpoint_from_topic(k) for k in available_keys]

        console = Console()
        table = Table(title="Global variables")
        table.add_column("Variable", justify="center")
        table.add_column("Content", justify="center")
        for endpoint in endpoints:
            var = str(self.get_global_var(endpoint))
            if len(var) > 40:
                var = var[0:20] + "..., " + var[-20:]
            table.add_row(endpoint, var)
        with console.capture() as capture:
            console.print(table)
        out = capture.get()
        logger.info(out)
        print(out)

    def shutdown(self):
        """shutdown the BECService"""
        try:
            self.connector.shutdown()
            self._service_info_event.set()
            if self._service_info_thread:
                self._service_info_thread.join()
            self._metrics_emitter_event.set()
            if self._metrics_emitter_thread:
                self._metrics_emitter_thread.join()
        except AttributeError:
            print("Failed to shutdown BECService.")

    @property
    def service_status(self):
        """get the status of active services"""
        self._update_existing_services()
        return self._services_info

    def wait_for_service(self, name, status=None):
        if status is None:
            status = BECStatus.RUNNING
        logger.info(f"Waiting for {name}.")
        while True:
            service_status_msg = self.service_status.get(name)
            if service_status_msg is not None:
                service_status = BECStatus(service_status_msg.content["status"])
                if service_status == status:
                    break
            time.sleep(0.05)
        logger.success(f"{name} is running.")

    def _wait_for_server(self):
        if not self.wait_for_server:
            return
        try:
            self.wait_for_service("ScanServer", BECStatus.RUNNING)
            self.wait_for_service("ScanBundler", BECStatus.RUNNING)
            self.wait_for_service("DeviceServer", BECStatus.RUNNING)
            self.wait_for_service("SciHub", BECStatus.RUNNING)
            logger.success("All BEC services are running.")
        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt received. Stopped waiting for BEC services.")


@dataclass
class ServiceMetric:
    """Container for keeping performance metrics."""

    pid: int
    cmdline: list
    process_name: str
    username: str
    hostname: str
    cpu_percent: float
    cpu_times: dict
    num_threads: int
    memory_in_mb: float
    memory_used_percent: float
    create_time: float
