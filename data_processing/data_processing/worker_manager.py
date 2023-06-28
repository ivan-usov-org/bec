from __future__ import annotations

import multiprocessing as mp

from bec_lib.core import BECMessage, MessageEndpoints, bec_logger
from bec_lib.core.redis_connector import RedisConnector

from .stream_processor import LmfitProcessor

logger = bec_logger.logger


class DAPWorkerManager:
    """Data processing worker manager class."""

    def __init__(self, connector: RedisConnector):
        self.connector = connector
        self.producer = connector.producer()
        self._workers = {}
        self._config = {}
        self._update_config()
        self._start_config_consumer()

    def _update_config(self):
        """Get config from redis."""
        logger.debug("Getting config from redis")
        msg = self.producer.get(MessageEndpoints.dap_config())
        if not msg:
            return
        self.update_config(BECMessage.DAPConfigMessage.loads(msg))

    def _start_config_consumer(self):
        """Get config from redis."""
        logger.debug("Starting config consumer")
        self.consumer = self.connector.consumer(
            MessageEndpoints.dap_config(), cb=self._set_config, parent=self
        )
        self.consumer.start()

    @staticmethod
    def _set_config(msg: BECMessage.BECMessage, parent: DAPWorkerManager) -> None:
        """Set config to the parent."""
        msg = BECMessage.DAPConfigMessage.loads(msg.value)
        if not msg:
            return
        parent.update_config(msg)

    def update_config(self, msg: BECMessage.DAPConfigMessage):
        """Update the config."""
        logger.debug(f"Updating config: {msg.content}")
        if not msg.content["config"]:
            return
        self._config = msg.content["config"]
        for worker_config in self._config["workers"]:
            # Check if the worker is already running and start it if not
            if worker_config["id"] not in self._workers:
                self._start_worker(worker_config)
                continue

            # Check if the config has changed
            if self._workers[worker_config["id"]]["config"] == worker_config["config"]:
                logger.debug(f"Worker config has not changed: {worker_config['id']}")
                continue

            # If the config has changed, terminate the worker and start a new one
            logger.debug(f"Restarting worker: {worker_config['id']}")
            self._workers[worker_config["id"]]["worker"].terminate()
            self._start_worker(worker_config)

        # Check if any workers need to be removed
        for worker_id in list(self._workers):
            if worker_id not in [worker["id"] for worker in self._config["workers"]]:
                logger.debug(f"Removing worker: {worker_id}")
                self._workers[worker_id]["worker"].terminate()
                del self._workers[worker_id]

    def _start_worker(self, config: dict):
        """Start a worker."""
        logger.debug(f"Starting worker: {config}")

        self._workers[config["id"]] = {
            "worker": self.run_worker(config["config"]),
            "config": config["config"],
        }

    def shutdown(self):
        for worker in self._workers:
            worker.shutdown()

    @staticmethod
    def run_worker(config: dict) -> mp.Process:
        """Run the worker."""
        worker = mp.Process(
            target=LmfitProcessor.run,
            kwargs={"config": config, "connector_host": ["localhost:6379"]},
            daemon=True,
        )
        worker.start()
        return worker
