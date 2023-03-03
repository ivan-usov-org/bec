import json

import jsonschema

# import ophyd
# import ophyd.sim as ops
# import ophyd_devices as opd


class SciBecValidator:
    def __init__(self, schema_path: str) -> None:
        self.schema = self._load_schema(schema_path)
        self.device_schema = self.schema["components"]["schemas"]["Device"]

    def _load_schema(self, schema_path) -> dict:
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            content = schema_file.read()
            schema_content = json.loads(content)
        return schema_content

    def validate_device(self, device):
        jsonschema.validate(device, schema=self.device_schema)

    def validate_device_patch(self, config):
        properties = {k: v for k, v in self.device_schema["properties"].items() if k in config}
        schema = {"properties": properties, "required": []}
        jsonschema.validate(config, schema=schema)

    # def assert_device_name_is_consistent(self, config) -> None:
    #     """ensure that the device name matches the name of the deviceConfig"""
    #     for dev, conf in config.items():
    #         if conf["deviceConfig"]["name"] != dev:
    #             raise ValueError(f"{dev}")

    # def check_signals(self, config) -> None:
    #     """run checks on EpicsSignals"""
    #     for dev, conf in config.items():
    #         dev_class = self._get_device_class(conf["deviceClass"])
    #         if issubclass(dev_class, ophyd.EpicsMotor):
    #             if "prefix" not in conf["deviceConfig"]:
    #                 msg_suffix = ""
    #                 if "read_pv" in conf["deviceConfig"]:
    #                     msg_suffix = "Maybe a typo? The device specifies a read_pv instead."
    #                 raise ValueError(f"{dev}: does not specify the prefix. {msg_suffix}")
    #         if not issubclass(dev_class, ophyd.signal.EpicsSignalBase):
    #             for anc, name, item in dev_class.walk_components():
    #                 if not issubclass(item.cls, ophyd.signal.EpicsSignalBase):
    #                     continue
    #                 if not item.is_signal:
    #                     continue
    #                 if not item.kind < ophyd.Kind.normal:
    #                     continue
    #                 # check if auto_monitor is in kwargs
    #                 self._has_auto_monitor(f"{dev}/{name}", item.kwargs)
    #             continue
    #         self._has_auto_monitor(dev, conf["deviceConfig"])
    #         if "read_pv" not in conf["deviceConfig"]:
    #             raise ValueError(f"{dev}: does not specify the read_pv")

    # @staticmethod
    # def _has_auto_monitor(name: str, config: dict) -> None:
    #     if "auto_monitor" not in config:
    #         print(f"WARNING: Device {name} is configured without auto monitor.")

    # def _get_device_class(self, dev_type):
    #     module = None
    #     if hasattr(ophyd, dev_type):
    #         module = ophyd
    #     elif hasattr(opd, dev_type):
    #         module = opd
    #     elif hasattr(ops, dev_type):
    #         module = ops
    #     else:
    #         TypeError(f"Unknown device class {dev_type}")
    #     return getattr(module, dev_type)

    # def validate_schema(self, config) -> None:
    #     """validate the device config against the json schema"""
    #     db_config = self._translate_to_db_config(config)
    #     for dev_name, device in db_config.items():
    #         try:
    #             jsonschema.validate(device, schema=self.schema)
    #         except jsonschema.ValidationError as exc:
    #             raise jsonschema.ValidationError(f"Failed to validate {dev_name}.") from exc

    # @staticmethod
    # def _translate_to_db_config(config) -> dict:
    #     db_config = config.copy()
    #     for name, device in db_config.items():
    #         device["enabled"] = device["status"]["enabled"]
    #         if device["status"].get("enabled_set"):
    #             device["enabled_set"] = device["status"].get("enabled_set")
    #         device.pop("status")
    #         device["name"] = name
    #     return db_config
