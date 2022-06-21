import logging
import threading

import IPython
from bluekafka_utils.connector import ConnectorBase
from IPython.terminal.prompts import Prompts, Token

from .alarm_handler import AlarmHandler
from .devicemanager_client import DMClient
from .scan_queue import ScanQueue
from .scans import Scans
from .signals import SigintHandler

logger = logging.getLogger(__name__)


class BKClient:
    def __init__(self, bootstrap_server: list, Connector: ConnectorBase, scibec_url: str):
        """Bluekafka Client

        Args:
            bootstrap_server (list): bootstrap server adress
            Connector (ConnectorBase): connector class

        Returns:
            _type_: _description_
        """
        self.devicemanager = None
        self.bootstrap_server = bootstrap_server
        self.scibec_url = scibec_url
        self.connector = Connector(bootstrap_server)
        self.producer = self.connector.producer()
        self._sighandler = SigintHandler(self)
        self._ip = None
        self._alarm_handler = None
        self._load_scans()

    def start(self):
        logger.info("Starting new client")
        self._start_devicemanager()
        self._start_exit_handler()
        self._configure_prompt()
        self._start_scan_queue()
        self._start_alarm_handler()

    @property
    def alarms(self):
        if self._alarm_handler is None:
            return []
        else:
            return self._alarm_handler.get_unhandled_alarms()

    def _load_scans(self):
        self.scans = Scans(self)

    def _start_scan_queue(self):
        self.queue = ScanQueue(self)

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
        self._alarm_handler = AlarmHandler(self.connector)
        self._alarm_handler.start()

    def shutdown(self):
        logger.info("Shutting down device manager")
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
