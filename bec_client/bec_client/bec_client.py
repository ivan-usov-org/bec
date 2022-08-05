import threading
from typing import List, Tuple

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


class BKClient(BECService):
    def __init__(self, bootstrap_server: list, connector_cls: ConnectorBase, scibec_url: str):
        """bec Client

        Args:
            bootstrap_server (list): bootstrap server adress
            Connector (ConnectorBase): connector class

        Returns:
            _type_: _description_
        """
        super().__init__(bootstrap_server, connector_cls)
        self.devicemanager = None
        self.scibec_url = scibec_url
        self._sighandler = SigintHandler(self)
        self._ip = None
        self.queue = None
        self.alarm_handler = None
        self._load_scans()

    def start(self):
        logger.info("Starting new client")
        self._start_devicemanager()
        self._start_exit_handler()
        self._configure_prompt()
        self._start_scan_queue()
        self._start_alarm_handler()

    def alarms(self, severity=Alarms.WARNING):
        if self.alarm_handler is None:
            return []
        yield from self.alarm_handler.get_alarm(severity=severity)

    def show_all_alarms(self, severity=Alarms.WARNING):
        alarms = self.alarm_handler.get_unhandled_alarms(severity=severity)
        for alarm in alarms:
            print(alarm)

    def clear_all_alarms(self):
        self.alarm_handler.clear()

    @property
    def pre_scan_hooks(self):
        return self.producer.lrange(MessageEndpoints.pre_scan_macros(), 0, -1)

    @pre_scan_hooks.setter
    def pre_scan_hooks(self, hooks: List):
        self.producer.delete(MessageEndpoints.pre_scan_macros())
        for hook in hooks:
            self.producer.lpush(MessageEndpoints.pre_scan_macros(), hook)

    def _load_scans(self):
        self.scans = Scans(self)

    def _start_scan_queue(self):
        self.queue = ScanManager(self.connector)

    def _set_ipython_prompt_scan_number(self, scan_number: int):
        if self._ip:
            self._ip.prompts.scan_number = scan_number + 1

    def _configure_prompt(self):
        self._ip = IPython.get_ipython()
        if self._ip is not None:
            self._ip.prompts = BKClientPrompt(self._ip, "demo")

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
        monitor = threading.Thread(target=self._exit_thread)
        monitor.daemon = True
        monitor.start()

    def _start_devicemanager(self):
        logger.info("Starting device manager")
        self.devicemanager = DMClient(self, self.scibec_url)
        self.devicemanager.initialize(self.bootstrap_server)

    def _start_alarm_handler(self):
        logger.info("Starting alarm listener")
        self.alarm_handler = AlarmHandler(self.connector)
        self.alarm_handler.start()

    def shutdown(self):
        # logger.info("Shutting down device manager")
        self.devicemanager.shutdown()

    def _exit_thread(self):
        main_thread = threading.main_thread()
        main_thread.join()
        self.shutdown()


class BKClientPrompt(Prompts):
    def __init__(self, ip, username, status=0):
        self._username = username
        self.status = status
        self.scan_number = 0
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
            (Token.PromptNum, str(self.scan_number)),
            (Token.Prompt, "] "),
            (Token.Prompt, "❯❯ "),
        ]

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
