import json
import logging
import yaml

logger = logging.getLogger(__name__)


class ServiceConfig:
    def __init__(self, config_path) -> None:
        self.config_path = config_path
        self.scibec = None
        self.redis = None
        self.mongodb = None
        self.config = None
        self._load_config()
        self._load_urls("scibec")
        self._load_urls("redis")
        self._load_urls("mongodb")

    def _load_config(self):
        if self.config_path:
            with open(self.config_path, "r") as stream:
                self.config = yaml.safe_load(stream)
                logger.info(
                    f"Loaded new config from disk: {json.dumps(self.config, sort_keys=True, indent=4)}"
                )
        else:
            raise ValueError("Config path cannot be empty")

    def _load_urls(self, entry: str):
        config = self.config.get(entry)
        if config:
            setattr(self, entry, f"{config['host']}:{config['port']}")
        else:
            raise ValueError(
                f"The provided config does not specify the url (host and port) for {entry}."
            )
