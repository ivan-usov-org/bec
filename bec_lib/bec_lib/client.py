from __future__ import print_function

import builtins
import importlib
import inspect
import subprocess
from typing import List

from rich.console import Console
from rich.table import Table

from bec_lib.alarm_handler import AlarmHandler
from bec_lib.callback_handler import CallbackHandler
from bec_lib.core import (
    Alarms,
    BECService,
    ConfigHelper,
    MessageEndpoints,
    ServiceConfig,
    bec_logger,
)
from bec_lib.core.connector import ConnectorBase
from bec_lib.core.logbook_connector import LogbookConnector
from bec_lib.core.redis_connector import RedisConnector
from bec_lib.devicemanager_client import DMClient
from bec_lib.scan_manager import ScanManager
from bec_lib.scans import Scans
from bec_lib.user_scripts_mixin import UserScriptsMixin

logger = bec_logger.logger

DEFAULT_CONFIG = {
    "redis": {"host": "localhost", "port": 6379},
    "mongodb": {"host": "localhost", "port": 27017},
    "scibec": {"host": "localhost", "port": 3030, "beamline": "MyBeamline"},
    "config": {
        "file_writer": {"plugin": "default_NeXus_format", "base_path": "./"},
        "scilog": {"env_file": "./"},
    },
}


class BECClient(BECService, UserScriptsMixin):
    def __init__(self, forced=False) -> None:
        pass

    def __new__(cls, forced=False):
        if not hasattr(cls, "_client") or forced:
            cls._client = super(BECClient, cls).__new__(cls)
            cls._initialized = False
        return cls._client

    def __repr__(self) -> str:
        return "BECClient\n\nTo get a list of available commands, type `bec.show_all_commands()`"

    def initialize(self, config: ServiceConfig = None, connector_cls: ConnectorBase = None):
        """initialize the BEC client"""
        if not config:
            config = ServiceConfig(**DEFAULT_CONFIG)

        if not connector_cls:
            connector_cls = RedisConnector
        super().__init__(config, connector_cls)
        self._configure_logger()
        # pylint: disable=attribute-defined-outside-init
        self.device_manager = None
        self.scibec_url = config.scibec
        self.queue = None
        self.alarm_handler = None
        self._load_scans()
        self._hli_funcs = {}
        self._initialized = True
        self.config = None
        builtins.bec = self
        self.metadata = {}
        # self.logbook = LogbookConnector(self.connector)
        self._update_username()
        self.history = None
        self.callbacks = CallbackHandler()
        self.live_updates = None

    @property
    def username(self) -> str:
        """get the current username"""
        return self._username

    @property
    def active_account(self) -> str:
        """get the currently active target (e)account"""
        return self.producer.get(MessageEndpoints.account())

    def start(self):
        """start the client"""
        if not self._initialized:
            logger.warning(
                "Client has not been initialized with 'client.initialize(config, connector_cls)'. Trying to initialize with default values."
            )
            self.initialize()

        logger.info("Starting new client")
        self._start_device_manager()
        self._start_scan_queue()
        self._start_alarm_handler()

        self.load_all_user_scripts()
        self.config = ConfigHelper(self.connector)
        self.history = self.queue.queue_storage.storage

    def alarms(self, severity=Alarms.WARNING):
        """get the next alarm with at least the specified severity"""
        if self.alarm_handler is None:
            yield []
        yield from self.alarm_handler.get_alarm(severity=severity)

    def show_all_alarms(self, severity=Alarms.WARNING):
        """print all unhandled alarms"""
        alarms = self.alarm_handler.get_unhandled_alarms(severity=severity)
        for alarm in alarms:
            print(alarm)

    def clear_all_alarms(self):
        """remove all alarms from stack"""
        self.alarm_handler.clear()

    @property
    def pre_scan_hooks(self):
        """currently stored pre-scan hooks"""
        return self.producer.lrange(MessageEndpoints.pre_scan_macros(), 0, -1)

    @pre_scan_hooks.setter
    def pre_scan_hooks(self, hooks: List):
        self.producer.delete(MessageEndpoints.pre_scan_macros())
        for hook in hooks:
            self.producer.lpush(MessageEndpoints.pre_scan_macros(), hook)

    def _load_scans(self):
        self.scans = Scans(self)
        builtins.scans = self.scans

    def load_high_level_interface(self, module_name):
        mod = importlib.import_module(f"bec_client.high_level_interfaces.{module_name}")
        members = inspect.getmembers(mod)
        funcs = {name: func for name, func in members if not name.startswith("__")}
        self._hli_funcs = funcs
        builtins.__dict__.update(funcs)

    def _update_username(self):
        self._username = (
            subprocess.run("whoami", shell=True, stdout=subprocess.PIPE)
            .stdout.decode()
            .split("\n")[0]
        )

    def _start_scan_queue(self):
        self.queue = ScanManager(self.connector)

    def _configure_logger(self):
        bec_logger.logger.remove()
        bec_logger.add_file_log(bec_logger.LOGLEVEL.INFO)
        bec_logger.add_sys_stderr(bec_logger.LOGLEVEL.SUCCESS)

    def _start_device_manager(self):
        logger.info("Starting device manager")
        self.device_manager = DMClient(self)
        self.device_manager.initialize(self.bootstrap_server)
        builtins.dev = self.device_manager.devices

    def _start_alarm_handler(self):
        logger.info("Starting alarm listener")
        self.alarm_handler = AlarmHandler(self.connector)
        self.alarm_handler.start()

    def shutdown(self):
        """shutdown the client and all its components"""
        super().shutdown()
        self.device_manager.shutdown()
        self.queue.shutdown()
        self.alarm_handler.shutdown()
        print("done")

    def _print_available_commands(self, title: str, data: tuple) -> None:
        console = Console()
        table = Table(title=title)
        table.add_column("Name", justify="center")
        table.add_column("Description", justify="center")
        for name, descr in data:
            table.add_row(name, descr)
        console.print(table)

    def _print_user_script_commands(self) -> None:
        data = self._get_user_script_commands()
        self._print_available_commands("User scripts", data)

    def _get_user_script_commands(self) -> list:
        avail_commands = []
        for name, val in self._scripts.items():
            descr = self._get_description_from_doc_string(val["cls"].__doc__)
            avail_commands.append((name, descr))
        return avail_commands

    def _get_scan_commands(self) -> list:
        avail_commands = []
        for name, scan in self.scans._available_scans.items():
            descr = self._get_description_from_doc_string(scan.scan_info["doc"])
            avail_commands.append((name, descr))
        return avail_commands

    def _print_scan_commands(self) -> None:
        data = self._get_scan_commands()
        self._print_available_commands("Scans", data)

    def show_all_commands(self):
        self._print_user_script_commands()
        self._print_scan_commands()

    @staticmethod
    def _get_description_from_doc_string(doc_string: str) -> str:
        if not doc_string:
            return ""
        return doc_string.strip().split("\n")[0]
