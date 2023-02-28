import json

import yaml

from .logger import bec_logger

logger = bec_logger.logger


class ServiceConfig:
    def __init__(
        self,
        config_path: str = None,
        scibec: dict = None,
        redis: dict = None,
        mongodb: dict = None,
        config: dict = None,
    ) -> None:
        self.config_path = config_path
        self.config = {}
        self._load_config()
        if self.config:
            self._load_urls("scibec")
            self._load_urls("redis")
            self._load_urls("mongodb")

        self._update_config(config=config, scibec=scibec, redis=redis, mongodb=mongodb)

        self.service_config = self.config.get("service_config")

    def _update_config(self, **kwargs):
        for key, val in kwargs.items():
            if not val:
                continue
            self.config[key] = val

    def _load_config(self):
        if not self.config_path:
            return
        with open(self.config_path, "r") as stream:
            self.config = yaml.safe_load(stream)
            logger.info(
                f"Loaded new config from disk: {json.dumps(self.config, sort_keys=True, indent=4)}"
            )

    def _load_urls(self, entry: str):
        config = self.config.get(entry)
        if not config:
            raise ValueError(
                f"The provided config does not specify the url (host and port) for {entry}."
            )
        return f"{config['host']}:{config['port']}"

    @property
    def scibec(self):
        return self._load_urls("scibec")

    @property
    def redis(self):
        return self._load_urls("redis")

    @property
    def mongodb(self):
        return self._load_urls("mongodb")
