from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

import numpy as np
from bec_client.prettytable import PrettyTable
from bec_client.progressbar import ScanProgressBar
from bec_client.request_items import RequestItem
from bec_utils import BECMessage, bec_logger

from .utils import ScanRequestError, check_alarms

if TYPE_CHECKING:
    from bec_client.bec_client import BKClient

logger = bec_logger.logger


class ScanRequestMixin:
    def __init__(self, bec: BKClient, RID: str) -> None:
        self.bec = bec
        self.request_storage = self.bec.queue.request_storage
        self.RID = RID
        self.scan_queue_request = None

    async def _wait_for_scan_request(self) -> RequestItem:
        """wait for scan queuest"""
        logger.debug("Waiting for request ID")
        start = time.time()
        while self.request_storage.find_request_by_ID(self.RID) is None:
            await asyncio.sleep(0.1)
        logger.debug(f"Waiting for request ID finished after {time.time()-start} s.")
        return self.request_storage.find_request_by_ID(self.RID)

    async def _wait_for_scan_request_decision(self):
        """wait for a scan queuest decision"""
        logger.debug("Waiting for decision")
        start = time.time()
        while self.scan_queue_request.decision_pending:
            await asyncio.sleep(0.1)
        logger.debug(f"Waiting for decision finished after {time.time()-start} s.")

    async def wait(self):
        """wait for the request acceptance"""
        self.scan_queue_request = await self._wait_for_scan_request()

        await self._wait_for_scan_request_decision()
        check_alarms(self.bec)

        while self.scan_queue_request.accepted is None:
            await asyncio.sleep(0.01)

        if not self.scan_queue_request.accepted[0]:
            raise ScanRequestError(
                f"Scan was rejected by the server: {self.scan_queue_request.response.content.get('message')}"
            )


def sort_devices(devices, scan_devices) -> list:
    """sort the devices to ensure that the table starts with scan motors"""
    for scan_dev in list(scan_devices)[::-1]:
        devices.remove(scan_dev)
        devices.insert(0, scan_dev)
    return devices


class LiveUpdatesTable:
    """Live updates for scans using a table and a scan progess bar.

    Args:
        bec (BKClient): client instance
        request (BECMessage.ScanQueueMessage): The scan request that should be monitored

    Raises:
        TimeoutError: Raised if no queue item is added before reaching a predefined timeout.
        RuntimeError: Raised if more points than requested are returned.
        ScanRequestError: Raised if the scan was rejected by the server.
    """

    def __init__(self, bec: BKClient, request: BECMessage.ScanQueueMessage) -> None:
        self.bec = bec
        self.request = request
        self.RID = request.metadata["RID"]
        self.scan_queue_request = None
        self.scan_item = None
        self.dev_values = None
        self.point_data = None

    async def wait_for_request_acceptance(self):
        scan_request = ScanRequestMixin(self.bec, self.RID)
        await scan_request.wait()

        self.scan_queue_request = scan_request.scan_queue_request

    async def wait_for_scan_to_start(self):
        """wait until the scan starts"""
        while True:
            queue_pos = self.scan_item.queue.queue_position
            self.check_alarms()
            if self.scan_item.status == "closed":
                break
            if queue_pos is None:
                logger.debug(f"Could not find queue entry for scanID {self.scan_item.scanID}")
                continue
            if queue_pos == 0:
                break
            print(
                f"Scan is enqueued and is waiting for execution. Current position in queue: {queue_pos + 1}.",
                end="\r",
                flush=True,
            )
            await asyncio.sleep(0.1)

    async def wait_for_scan_item_to_finish(self):
        """wait for scan completion"""
        while not self.scan_item.end_time or self.scan_item.queue.queue_position is not None:
            self.check_alarms()
            await asyncio.sleep(0.1)

    def check_alarms(self):
        check_alarms(self.bec)

    @property
    def devices(self):
        """get the devices for the callback"""
        if self.point_data.metadata["scan_type"] == "step":
            return self.get_devices_from_request()
        if self.point_data.metadata["scan_type"] == "fly":
            devices = list(self.point_data.content["data"].keys())
            return devices[0 : min(10, len(devices)) - 1]
        return None

    def get_devices_from_request(self) -> list:
        """extract interesting devices from a scan request"""
        device_manager = self.bec.device_manager
        scan_devices = self.request.content["parameter"]["args"].keys()
        primary_devices = device_manager.devices.primary_devices(
            [device_manager.devices[dev] for dev in scan_devices]
        )
        devices = [dev.name for dev in primary_devices]
        devices = sort_devices(devices, scan_devices)
        devices = devices[0 : min(10, len(devices)) - 1]

        return devices

    def _prepare_table(self) -> PrettyTable:
        header = ["seq. num"]
        header.extend(self.devices)
        return PrettyTable(header, padding=12)

    async def update_scan_item(self):
        """get the current scan item"""
        while self.scan_queue_request.scan is None:
            self.check_alarms()
            await asyncio.sleep(0.1)
        self.scan_item = self.scan_queue_request.scan

    async def core(self):
        print(f"\nStarting scan {self.scan_item.scan_number}.")
        with ScanProgressBar(
            scan_number=self.scan_item.scan_number, clear_on_exit=True
        ) as progressbar:
            point_id = 0
            table = None
            while True:
                self.check_alarms()
                self.point_data = self.scan_item.data.get(point_id)
                if self.scan_item.num_points:
                    progressbar.max_points = self.scan_item.num_points

                progressbar.update(point_id)
                if self.point_data:
                    if not table:
                        self.dev_values = list(np.zeros_like(self.devices))
                        table = self._prepare_table()
                        print(table.get_header_lines())

                    point_id += 1
                    if point_id % 100 == 0:
                        print(table.get_header_lines())
                    for ind, dev in enumerate(self.devices):
                        signal = self.point_data.content["data"][dev].get(dev)
                        self.dev_values[ind] = signal.get("value") if signal else -999
                    print(table.get_row(point_id, *self.dev_values))
                    progressbar.update(point_id)
                else:
                    logger.debug("waiting for new data point")
                    await asyncio.sleep(0.1)

                if not self.scan_item.num_points:
                    continue
                if self.scan_item.open_scan_defs:
                    continue

                if point_id == self.scan_item.num_points:
                    break
                if point_id > self.scan_item.num_points:
                    raise RuntimeError("Received more points than expected.")

            await self.wait_for_scan_item_to_finish()

            elapsed_time = self.scan_item.end_time - self.scan_item.start_time
            print(
                table.get_footer(
                    f"Scan {self.scan_item.scan_number} finished. Scan ID {self.scan_item.scanID}. Elapsed time: {elapsed_time:.2f} s"
                )
            )

    async def run(self):
        await self.wait_for_request_acceptance()
        await asyncio.wait_for(self.update_scan_item(), timeout=15)
        await self.wait_for_scan_to_start()
        await self.core()
