from __future__ import annotations

import time
from math import inf
from typing import TYPE_CHECKING

from bec_lib import messages
from bec_lib.bec_errors import ScanAbortion
from bec_lib.endpoints import MessageEndpoints

if TYPE_CHECKING:
    from bec_lib.client import BECClient
    from bec_lib.queue_items import QueueItem


class ScanReport:
    """Scan Report class that provides a convenient way to access the status of a scan request."""

    def __init__(self) -> None:
        self._client = None
        self.request = None
        self._queue_item = None

    @classmethod
    def from_request(
        cls, request: messages.ScanQueueMessage, client: BECClient = None
    ) -> ScanReport:
        """
        Create a ScanReport from a request

        Args:
            request (messages.ScanQueueMessage): request to create the report from
            client (BECClient, optional): BECClient instance. Defaults to None.

        Returns:
            ScanReport: ScanReport instance
        """
        scan_report = cls()
        scan_report._client = client

        client.queue.request_storage.update_with_request(request)
        scan_report.request = client.queue.request_storage.find_request_by_ID(
            request.metadata["RID"]
        )
        return scan_report

    @property
    def scan(self):
        """get the scan item"""
        return self.request.scan

    @property
    def status(self):
        """returns the current status of the request"""
        scan_type = self.request.request.content["scan_type"]
        status = self.queue_item.status
        if scan_type == "mv" and status == "COMPLETED":
            return "COMPLETED" if self._get_mv_status() else "RUNNING"
        return self.queue_item.status

    @property
    def queue_item(self):
        """get the queue item"""
        if not self._queue_item:
            self._queue_item = self._get_queue_item(timeout=10)
        return self._queue_item

    def _get_queue_item(self, timeout=None) -> QueueItem:
        """
        get the queue item from the queue storage

        Args:
            timeout (float, optional): timeout in seconds. Defaults to None.
        """
        timeout = timeout if timeout is not None else inf
        queue_item = None
        elapsed_time = 0
        sleep_time = 0.1
        while not queue_item:
            queue_item = self._client.queue.queue_storage.find_queue_item_by_requestID(
                self.request.requestID
            )
            elapsed_time += sleep_time
            time.sleep(sleep_time)
            if elapsed_time > timeout:
                raise TimeoutError
        return queue_item

    def _get_mv_status(self) -> bool:
        """get the status of a move request"""
        motors = list(self.request.request.content["parameter"]["args"].keys())
        request_status = self._client.device_manager.connector.lrange(
            MessageEndpoints.device_req_status_container(self.request.requestID), 0, -1
        )
        if len(request_status) == len(motors):
            return True
        return False

    def wait(self, timeout: float = None) -> ScanReport:
        """
        wait for the request to complete

        Args:
            timeout (float, optional): timeout in seconds. Defaults to None.

        Raises:
            TimeoutError: if the timeout is reached

        Returns:
            ScanReport: ScanReport instance
        """
        sleep_time = 0.1
        scan_type = self.request.request.content["scan_type"]
        try:
            if scan_type == "mv":
                self._wait_move(timeout, sleep_time)
            else:
                self._wait_scan(timeout, sleep_time)
        except KeyboardInterrupt as exc:
            self._client.queue.request_scan_abortion()
            raise ScanAbortion("Aborted by user.") from exc

        return self

    def _check_timeout(self, timeout: float = None, elapsed_time: float = 0) -> None:
        """
        check if the timeout is reached

        Args:
            timeout (float, optional): timeout in seconds. Defaults to None.
            elapsed_time (float, optional): elapsed time in seconds. Defaults to 0.

        """
        if timeout is None:
            return
        if elapsed_time > timeout:
            raise TimeoutError(
                f"Timeout reached while waiting for request to complete. Timeout: {timeout} s."
            )

    def _wait_move(self, timeout: float = None, sleep_time: float = 0.1) -> None:
        """
        wait for a move request to complete

        Args:
            timeout (float, optional): timeout in seconds. Defaults to None.
            sleep_time (float, optional): sleep time in seconds. Defaults to 0.1.

        """
        elapsed_time = 0
        while True:
            if self._get_mv_status():
                break
            self._client.alarm_handler.raise_alarms()
            time.sleep(sleep_time)
            elapsed_time += sleep_time
            self._check_timeout(timeout, elapsed_time)

    def _wait_scan(self, timeout: float = None, sleep_time: float = 0.1) -> None:
        """
        wait for a scan request to complete

        Args:
            timeout (float, optional): timeout in seconds. Defaults to None.
            sleep_time (float, optional): sleep time in seconds. Defaults to 0.1.
        """
        elapsed_time = 0
        while True:
            if self.status == "COMPLETED":
                break
            if self.status == "STOPPED":
                raise ScanAbortion
            self._client.callbacks.poll()
            time.sleep(sleep_time)
            elapsed_time += sleep_time
            self._check_timeout(timeout, elapsed_time)

    def __str__(self) -> str:
        separator = "--" * 10
        details = f"\tStatus: {self.status}\n"
        if self.scan:
            details += self.scan.describe()
        return f"ScanReport:\n{separator}\n{details}"
