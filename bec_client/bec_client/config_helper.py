from __future__ import annotations

from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from .bec_client import BECClient


class ConfigHelper:
    def __init__(self, parent: BECClient) -> None:
        self.parent = parent

    def update_session_with_file(self, file_path: str, reload=True):
        """Update the current session with a yaml file from disk.

        Args:
            file_path (str): Full path to the yaml file.
            reload (bool, optional): Send a reload request to all services. Defaults to True.
        """
        dm = self.parent.device_manager
        dm.scibec.update_session_with_file(file_path)
        if reload:
            dm.send_config_request(action="reload")

    def save_current_session(self, file_path: str):
        """Save the current session as a yaml file to disk.

        Args:
            file_path (str): Full path to the yaml file.
        """
        scibec = self.parent.device_manager.scibec
        beamlines = scibec.get_beamlines()
        if not beamlines:
            print("No config available.")
            return
        if len(beamlines) > 1:
            print("More than one beamline available.")
            return

        beamline = beamlines[0]
        if not beamline.get("activeSession"):
            print("No active session.")
            return
        session = scibec.get_session_by_id(beamline["activeSession"], include_devices=True)
        devices = session[0].get("devices")
        if not devices:
            print("No devices found for the current session.")
            return
        out = {}
        for dev in devices:
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
