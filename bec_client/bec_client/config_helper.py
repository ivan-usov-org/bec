from __future__ import annotations

import json
from typing import TYPE_CHECKING

import msgpack
import yaml
from bec_utils import MessageEndpoints, bec_logger

if TYPE_CHECKING:
    from .bec_client import BECClient

logger = bec_logger.logger


class ConfigHelper:
    def __init__(self, parent: BECClient) -> None:
        self.parent = parent

    def update_session_with_file(self, file_path: str, reload=True):
        """Update the current session with a yaml file from disk.

        Args:
            file_path (str): Full path to the yaml file.
            reload (bool, optional): Send a reload request to all services. Defaults to True.
        """
        config = self._load_config_from_file(file_path)
        self.parent.device_manager.send_config_request(action="set", config=config)
        if reload:
            self.parent.device_manager.send_config_request(action="reload")

    def _load_config_from_file(self, file_path: str) -> dict:
        data = {}
        if not file_path.endswith(".yaml"):
            raise NotImplementedError

        with open(file_path, "r", encoding="utf-8") as stream:
            try:
                data = yaml.safe_load(stream)
                logger.trace(
                    f"Loaded new config from disk: {json.dumps(data, sort_keys=True, indent=4)}"
                )
            except yaml.YAMLError as err:
                logger.error(f"Error while loading config from disk: {repr(err)}")

        return data

    def save_current_session(self, file_path: str):
        """Save the current session as a yaml file to disk.

        Args:
            file_path (str): Full path to the yaml file.
        """
        msg_raw = self.parent.producer.get(MessageEndpoints.device_config())
        config = msgpack.loads(msg_raw)
        out = {}
        for dev in config:
            dev.pop("id")
            dev.pop("createdAt")
            dev.pop("createdBy")
            dev.pop("sessionId")
            enabled = dev.pop("enabled")
            config = {"status": {"enabled": enabled}}

            enabled_set = dev.pop("enabled_set", None)
            if enabled_set is not None:
                config["status"]["enabled_set"] = enabled_set
            config.update(dev)
            out[dev["name"]] = config

        with open(file_path, "w") as file:
            file.write(yaml.dump(out))

        print(f"Config was written to {file_path}.")
