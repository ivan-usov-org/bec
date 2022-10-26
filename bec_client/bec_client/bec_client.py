import builtins
import importlib
import inspect
import threading
import time
from typing import List

import IPython
from bec_utils import Alarms, BECService, MessageEndpoints, bec_logger
from bec_utils.connector import ConnectorBase
from IPython.terminal.prompts import Prompts, Token

from bec_client.scan_manager import ScanManager

from .alarm_handler import AlarmHandler
from .devicemanager_client import DMClient
from .scans import Scans
from .signals import SigintHandler

logger = bec_logger.logger


class BECClient(BECService):
    def __init__(self, bootstrap_server: list, connector_cls: ConnectorBase, scibec_url: str):
        """bec Client

        Args:
            bootstrap_server (list): bootstrap server adress
            Connector (ConnectorBase): connector class

        Returns:
            _type_: _description_
        """
        super().__init__(bootstrap_server, connector_cls)
        self.device_manager = None
        self.scibec_url = scibec_url
        self._sighandler = SigintHandler(self)
        self._ip = None
        self.queue = None
        self.alarm_handler = None
        self._load_scans()
        self._exit_event = threading.Event()
        self._exit_handler_thread = None
        self._hli_funcs = {}

    def start(self):
        """start the client"""
        logger.info("Starting new client")
        self._start_device_manager()
        self._start_exit_handler()
        self._configure_prompt()
        self._start_scan_queue()
        self._start_alarm_handler()
        self._configure_logger()

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

    def _start_scan_queue(self):
        self.queue = ScanManager(self.connector)

    def _set_ipython_prompt_scan_number(self, scan_number: int):
        if self._ip:
            self._ip.prompts.scan_number = scan_number + 1

    def _configure_prompt(self):
        self._ip = IPython.get_ipython()
        if self._ip is not None:
            self._ip.prompts = BECClientPrompt(ip=self._ip, client=self, username="demo")

    def _configure_logger(self):
        bec_logger.logger.remove()
        bec_logger.add_file_log(bec_logger.LOGLEVEL.INFO)
        bec_logger.add_sys_stderr(bec_logger.LOGLEVEL.SUCCESS)

    def _set_error(self):
        if self._ip is not None:
            self._ip.prompts.status = 0

    def _set_busy(self):
        if self._ip is not None:
            self._ip.prompts.status = 1

    def _set_idle(self):
        if self._ip is not None:
            self._ip.prompts.status = 2

    def _start_exit_handler(self):
        self._exit_handler_thread = threading.Thread(target=self._exit_thread)
        self._exit_handler_thread.daemon = True
        self._exit_handler_thread.start()

    def _shutdown_exit_handler(self):
        self._exit_event.set()
        if self._exit_handler_thread:
            self._exit_handler_thread.join()

    def _start_device_manager(self):
        logger.info("Starting device manager")
        self.device_manager = DMClient(self, self.scibec_url)
        self.device_manager.initialize(self.bootstrap_server)

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
        self._shutdown_exit_handler()
        print("done")

    def _exit_thread(self):
        main_thread = threading.main_thread()
        while main_thread.is_alive() and not self._exit_event.is_set():
            time.sleep(0.1)
        if not self._exit_event.is_set():
            self.shutdown()


class BECClientPrompt(Prompts):
    def __init__(self, ip, username, client, status=0):
        self._username = username
        self.client = client
        self.status = status
        super().__init__(ip)

    def in_prompt_tokens(self, cli=None):
        if self.status == 0:
            status_led = Token.OutPromptNum
        elif self.status == 1:
            status_led = Token.PromptNum
        else:
            status_led = Token.Prompt
        return [
            (status_led, "\u2022"),
            (Token.Prompt, " " + self.username),
            (Token.Prompt, " ["),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, "/"),
            (Token.PromptNum, str(self.client.queue.next_scan_number)),
            (Token.Prompt, "] "),
            (Token.Prompt, "❯❯ "),
        ]

    @property
    def username(self):
        """current username"""
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
