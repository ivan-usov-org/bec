from __future__ import annotations

import os
import traceback
from typing import TYPE_CHECKING

import bec_utils
import msgpack
from bec_utils import BECMessage as BMessage
from bec_utils import BECStatus, DeviceConfigError, MessageEndpoints, bec_logger

from .scibec_validator import SciBecValidator

if TYPE_CHECKING:
    from devicemanager import DeviceManagerDS

logger = bec_logger.logger

dir_path = os.path.abspath(os.path.join(os.path.dirname(bec_utils.__file__), "../../scibec/"))


class ConfigHandler:
    def __init__(self, device_manager: DeviceManagerDS) -> None:
        self.device_manager = device_manager
        self.validator = SciBecValidator(os.path.join(dir_path, "openapi_schema.json"))

    def send_config(self, msg: BMessage.DeviceConfigMessage) -> None:
        """broadcast a new config"""
        self.device_manager.producer.send(MessageEndpoints.device_config_update(), msg.dumps())

    def parse_config_request(self, msg: BMessage.DeviceConfigMessage) -> None:
        """Processes a config request. If successful, it emits a config reply

        Args:
            msg (BMessage.DeviceConfigMessage): Config request

        """
        try:
            self.device_manager.check_request_validity(msg)
            if msg.content["action"] == "update":
                self._update_config(msg)
            if msg.content["action"] == "reload":
                self._reload_config(msg)

        except DeviceConfigError as dev_conf_error:
            content = traceback.format_exc()
            self.device_manager.send_config_request_reply(
                accepted=False, error_msg=content, metadata=msg.metadata
            )
