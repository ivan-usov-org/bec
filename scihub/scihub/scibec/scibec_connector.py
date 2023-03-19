from __future__ import annotations

from typing import TYPE_CHECKING

import msgpack
from bec_utils import BECMessage, MessageEndpoints, ServiceConfig, bec_logger
from bec_utils.connector import ConnectorBase
from requests import ConnectionError

from .config_handler import ConfigHandler
from .scibec import SciBec, SciBecError

if TYPE_CHECKING:
    from scihub import SciHub

logger = bec_logger.logger


class SciBecConnector:
    def __init__(self, scihub: SciHub, connector: ConnectorBase) -> None:
        self.scihub = scihub
        self.connector = connector
        self.producer = connector.producer()
        self.scibec = None
        self.scibec_info = {}
        self.connect_to_scibec()
        self.update_session()
        self.config_handler = ConfigHandler(self, connector)

        self._config_request_handler = None
        self._start_config_request_handler()

    @property
    def config(self):
        """get the current service config"""
        return self.scihub.config

    def get_current_session(self):
        if not self.scibec or not self.scibec_info.get("beamline"):
            return None
        self.scibec_info["activeSession"] = self.scibec.get_session_by_id(
            self.scibec_info["beamline"]["activeSession"], include_devices=True
        )
        return self.scibec_info["activeSession"]

    def update_session(self):
        session = self.get_current_session()
        if session:
            self.set_redis_config(session[0]["devices"])

    def set_redis_config(self, config):
        self.producer.set(MessageEndpoints.device_config(), msgpack.dumps(config))

    def _start_config_request_handler(self) -> None:
        self._config_request_handler = self.connector.consumer(
            MessageEndpoints.device_config_request(),
            cb=self._device_config_request_callback,
            parent=self,
        )
        self._config_request_handler.start()

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received request: {msg}")
        parent.config_handler.parse_config_request(msg)

    def connect_to_scibec(self):
        scibec_host = self.scihub.config.scibec
        if not self.scihub.config.scibec:
            return
        try:
            beamline = self.scihub.config.config["scibec"].get("beamline")
            if not beamline:
                logger.warning(f"Cannot connect to SciBec without a beamline specified.")
                return
            logger.info(f"Connecting to SciBec on {scibec_host}")
            self.scibec = SciBec()
            self.scibec.url = scibec_host
            beamline_info = self.scibec.get_beamline(beamline)
            self.scibec_info["beamline"] = beamline_info
            if not beamline_info:
                logger.warning(f"Could not find a beamline with the name {beamline}")
                return
        except (ConnectionError, SciBecError) as exc:
            self.scibec = None
            return
