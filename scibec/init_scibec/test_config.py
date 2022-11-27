import argparse
import json

import jsonschema
import ophyd
import ophyd.sim as ops
import ophyd_devices as opd
import yaml

DEVICE_SCHEMA = "./device_schema.json"


class DeviceConfigTest:
    def __init__(self, config: str) -> None:
        self.config = self.read_config(config)

    def read_config(self, config) -> dict:
        """load a config from disk"""
        content = None
        with open(config, "r") as file:
            file_content = file.read()
            content = yaml.safe_load(file_content)
        return content

    def assert_device_name_is_consistent(self) -> None:
        """ensure that the device name matches the name of the deviceConfig"""
        for dev, conf in self.config.items():
            if conf["deviceConfig"]["name"] != dev:
                raise ValueError(f"{dev}")

    def check_signals(self) -> None:
        """run checks on EpicsSignals"""
        for dev, conf in self.config.items():
            dev_class = self._get_device_class(conf["deviceClass"])
            if issubclass(dev_class, ophyd.EpicsMotor):
                if "prefix" not in conf["deviceConfig"]:
                    msg_suffix = ""
                    if "read_pv" in conf["deviceConfig"]:
                        msg_suffix = "Maybe a typo? The device specifies a read_pv instead."
                    raise ValueError(f"{dev}: does not specify the prefix. {msg_suffix}")
            if not issubclass(dev_class, ophyd.signal.EpicsSignalBase):
                for anc, name, item in dev_class.walk_components():
                    if not issubclass(item.cls, ophyd.signal.EpicsSignalBase):
                        continue
                    if not item.is_signal:
                        continue
                    if not item.kind < ophyd.Kind.normal:
                        continue
                    # check if auto_monitor is in kwargs
                    self._has_auto_monitor(f"{dev}/{name}", item.kwargs)
                continue
            self._has_auto_monitor(dev, conf["deviceConfig"])
            if "read_pv" not in conf["deviceConfig"]:
                raise ValueError(f"{dev}: does not specify the read_pv")

    @staticmethod
    def _has_auto_monitor(name: str, config: dict) -> None:
        if "auto_monitor" not in config:
            print(f"WARNING: Device {name} is configured without auto monitor.")

    def _get_device_class(self, dev_type):
        module = None
        if hasattr(ophyd, dev_type):
            module = ophyd
        elif hasattr(opd, dev_type):
            module = opd
        elif hasattr(ops, dev_type):
            module = ops
        else:
            TypeError(f"Unknown device class {dev_type}")
        return getattr(module, dev_type)

    def validate_schema(self) -> None:
        """validate the device config against the json schema"""
        with open(DEVICE_SCHEMA, "r") as schema_file:
            content = schema_file.read()
            schema_content = json.loads(content)
        db_config = self._translate_to_db_config(self.config)
        for dev_name, device in db_config.items():
            try:
                jsonschema.validate(device, schema=schema_content)
            except jsonschema.ValidationError as exc:
                raise jsonschema.ValidationError(f"Failed to validate {dev_name}.") from exc

    @staticmethod
    def _translate_to_db_config(config) -> dict:
        db_config = config.copy()
        for name, device in db_config.items():
            device["enabled"] = device["status"]["enabled"]
            if device["status"].get("enabled_set"):
                device["enabled_set"] = device["status"].get("enabled_set")
            device.pop("status")
            device["name"] = name
        return db_config


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--config",
        default="./test_lamni_config.yaml",
        help="path to the config file",
    )

    clargs = parser.parse_args()
    config = clargs.config

    device_config_test = DeviceConfigTest(config)
    device_config_test.assert_device_name_is_consistent()
    device_config_test.check_signals()
    device_config_test.validate_schema()
