from __future__ import annotations

import asyncio
import threading
import time
from typing import TYPE_CHECKING

import msgpack
import numpy as np
from bec_utils import (
    Alarms,
    BECMessage,
    DeviceManagerBase,
    DeviceStatus,
    MessageEndpoints,
    bec_logger,
)
from bec_utils.connector import ConsumerConnector

from bec_client.request_items import RequestItem, RequestStorage
from bec_client.scan_items import ScanItem, ScanStorage

from .prettytable import PrettyTable
from .progressbar import DeviceProgressBar, ScanProgressBar

if TYPE_CHECKING:
    from .bec_client import BKClient

logger = bec_logger.logger


class ScanRequestError(Exception):
    pass


def set_event_delayed(event: threading.Event, delay: int) -> None:
    """Set event with a delay

    Args:
        event (threading.Event): event that should be set
        delay (int): delay time in seconds

    """

    def call_set():
        time.sleep(delay)
        event.set()

    thread = threading.Thread(target=call_set, daemon=True)
    thread.start()


def check_alarms(bec):
    for alarm in bec.alarms(severity=Alarms.MINOR):
        # print(alarm)
        raise alarm


async def live_updates_readback_progressbar(
    device_manager: DeviceManagerBase, request: BECMessage.ScanQueueMessage
) -> None:
    """Live feedback on motor movements using a progressbar.

    Args:
        dm (DeviceManagerBase): devicemanager
        request (ScanQueueMessage): request that should be monitored

    """
    devices = list(request.content["parameter"]["args"].keys())
    target_values = [x for xs in request.content["parameter"]["args"].values() for x in xs]

    def get_device_values():
        return [
            device_manager.devices[dev].read(cached=True, use_readback=True).get("value")
            for dev in devices
        ]

    while True:
        msgs = [
            BECMessage.DeviceMessage.loads(
                device_manager.producer.get(MessageEndpoints.device_readback(dev))
            )
            for dev in devices
        ]
        if all(msg.metadata.get("RID") == request.metadata["RID"] for msg in msgs):
            break
        check_alarms(device_manager.parent)
    start_values = get_device_values()
    with DeviceProgressBar(
        devices=devices, start_values=start_values, target_values=target_values
    ) as progress:
        req_done = False
        while not progress.finished or not req_done:
            check_alarms(device_manager.parent)

            pipe = device_manager.producer.pipeline()
            for dev in devices:
                device_manager.producer.get(MessageEndpoints.device_req_status(dev), pipe)
            req_done_msgs = pipe.execute()

            values = get_device_values()
            progress.update(values=values)

            msgs = [BECMessage.DeviceReqStatusMessage.loads(msg) for msg in req_done_msgs]
            request_ids = [msg.metadata["RID"] if msg else None for msg in msgs]
            if set(request_ids) != set([request.metadata["RID"]]):
                await progress.sleep()
                continue

            req_done = True
            for dev, msg in zip(devices, msgs):
                if not msg:
                    continue
                if msg.content.get("success", False):
                    progress.set_finished(dev)


async def live_updates_readback(
    dm: DeviceManagerBase, move_args: dict, consumer: ConsumerConnector
) -> None:
    """Live feedback on motor movements.

    Args:
        dm (DeviceManagerBase): devicemanager
        move_args (dict): arguments passed to the move command
        consumer (ConsumerConnector): active consumer

    """

    devices = move_args.keys()
    print("  ", "\t".join(f"{dev}" for dev in devices))
    stop = [threading.Event() for dev in devices]
    dev_values = [
        dm.devices[dev].read(cached=True, use_readback=True).get("value") for dev in devices
    ]

    def print_device_positions():
        print(
            "  ",
            "\t".join(f"{dev:0.3f}" for dev in dev_values),
            end="\r",
            flush=True,
        )

    print_device_positions()
    if not all(np.isclose(dev_values, list(move_args.values()))[0]):
        while not all(stop_dev.is_set() for stop_dev in stop):
            msg = consumer.poll_messages()
            if msg is not None:
                msg = BECMessage.DeviceMessage.loads(msg.value).content["signals"]
                for ind, dev in enumerate(devices):
                    if dev in msg:
                        dev_values[ind] = msg[dev].get("value")
            else:
                dev_values = [
                    dm.devices[dev].read(cached=True, use_readback=True).get("value")
                    for dev in devices
                ]
                for ind, dev in enumerate(devices):
                    val = dm.parent.producer.get(MessageEndpoints.device_status(dev))
                    if not val:
                        continue
                    val = msgpack.loads(val)

                    if DeviceStatus(val.get("status")) != DeviceStatus.IDLE:
                        continue

                    tolerance = dm.devices[dev].config["deviceConfig"].get("tolerance", 0.5)
                    is_close = all(
                        np.isclose(dev_values[ind], list(move_args.values())[ind], atol=tolerance)
                    )
                    if not is_close:
                        continue
                    if not stop[ind].is_set():
                        set_event_delayed(stop[ind], 0.2)
                check_alarms(dm.parent)
                await asyncio.sleep(0.1)
            print_device_positions()

    print("\n")


async def wait_for_scan_request(requests: RequestStorage, RID: str) -> RequestItem:
    logger.debug("Waiting for request ID")
    start = time.time()
    while requests.find_request_by_ID(RID) is None:
        await asyncio.sleep(0.1)
    logger.debug(f"Waiting for request ID finished after {time.time()-start} s.")
    return requests.find_request_by_ID(RID)


async def wait_for_scan_request_decision(scan_queue_request):
    logger.debug("Waiting for decision")
    start = time.time()
    while scan_queue_request.decision_pending:
        await asyncio.sleep(0.1)
    logger.debug(f"Waiting for decision finished after {time.time()-start} s.")


def sort_devices(devices, scan_devices) -> list:
    for scan_dev in list(scan_devices)[::-1]:
        devices.remove(scan_dev)
        devices.insert(0, scan_dev)
    return devices


def get_devices_from_request(device_manager, request) -> list:
    scan_devices = request.content["parameter"]["args"].keys()
    primary_devices = device_manager.devices.primary_devices(
        [device_manager.devices[dev] for dev in scan_devices]
    )
    devices = [dev.name for dev in primary_devices]
    devices = sort_devices(devices, scan_devices)
    devices = devices[0 : min(10, len(devices)) - 1]

    return devices


async def get_scan_item(bec: BKClient, request_item: RequestItem) -> ScanItem:
    timeout_time = 15
    sleep_time = 0.1
    consumed_time = 0
    while request_item.scan is None:
        check_alarms(bec)
        await asyncio.sleep(sleep_time)
        consumed_time += sleep_time
        if consumed_time > timeout_time:
            raise TimeoutError("Reached timeout while waiting for scan data.")
    return request_item.scan


def get_devices(device_manager, request, scan_msg):
    if scan_msg.metadata["scan_type"] == "step":
        return get_devices_from_request(device_manager=device_manager, request=request)
    if scan_msg.metadata["scan_type"] == "fly":
        devices = list(scan_msg.content["data"].keys())
        return devices[0 : min(10, len(devices)) - 1]


async def wait_for_scan_to_start(bec, scan_item: ScanItem):
    while True:
        queue_pos = scan_item.queue.queue_position
        check_alarms(bec)
        if scan_item.status == "closed":
            break
        if queue_pos is None:
            logger.debug(f"Could not find queue entry for scanID {scan_item.scanID}")
            continue
        if queue_pos == 0:
            break
        print(
            f"Scan is enqueued and is waiting for execution. Current position in queue: {queue_pos + 1}.",
            end="\r",
            flush=True,
        )
        await asyncio.sleep(0.1)


async def wait_for_scan_item_to_finish(bec, scan_item):
    while not scan_item.end_time or scan_item.queue.queue_position is not None:
        check_alarms(bec)
        await asyncio.sleep(0.1)


async def live_updates_table(bec: BKClient, request: BECMessage.ScanQueueMessage):
    """Live updates for scans using a table and a scan progess bar.

    Args:
        bec (BKClient): client instance
        request (BECMessage.ScanQueueMessage): The scan request that should be monitored

    Raises:
        TimeoutError: Raised if no queue item is added before reaching a predefined timeout.
        RuntimeError: Raised if more points than requested are returned.
        ScanRequestError: Raised if the scan was rejected by the server.
    """

    RID = request.metadata["RID"]

    request_storage = bec.queue.request_storage

    scan_queue_request = await wait_for_scan_request(request_storage, RID)

    await wait_for_scan_request_decision(scan_queue_request)
    check_alarms(bec)

    while scan_queue_request.accepted is None:
        await asyncio.sleep(0.01)

    if not scan_queue_request.accepted[0]:
        raise ScanRequestError(
            f"Scan was rejected by the server: {scan_queue_request.response.content.get('message')}"
        )

    # get device names
    devices = get_devices_from_request(device_manager=bec.devicemanager, request=request)
    dev_values = [0 for dev in devices]

    # get queue item
    # queue_item = await get_queue_item(bec=bec, RID=RID)

    # block_id = queue_item.queue_info.get_block_id(RID)

    # scanID = queue_item.queue_info.scanID[block_id]
    # scan_number = queue_item.queue_info.scan_number[block_id]
    scan_item = await get_scan_item(bec=bec, request_item=scan_queue_request)

    await wait_for_scan_to_start(bec, scan_item)

    print(f"\nStarting scan {scan_item.scan_number}.")

    with ScanProgressBar(scan_number=scan_item.scan_number, clear_on_exit=True) as progressbar:
        point_id = 0
        table = None
        while True:
            check_alarms(bec)
            point_data = scan_item.data.get(point_id)
            if scan_item.num_points:
                progressbar.max_points = scan_item.num_points

            progressbar.update(point_id)
            if point_data:
                if not table:
                    devices = get_devices(bec.devicemanager, request, point_data)
                    dev_values = [0 for dev in devices]
                    header = ["seq. num"]
                    header.extend(devices)
                    table = PrettyTable(header, padding=12)
                    print(table.get_header_lines())

                point_id += 1
                if point_id % 100 == 0:
                    print(table.get_header_lines())
                for ind, dev in enumerate(devices):
                    signal = point_data.content["data"][dev].get(dev)
                    dev_values[ind] = signal.get("value") if signal else -999
                print(table.get_row(point_id, *dev_values))
                progressbar.update(point_id)
            else:
                logger.debug("waiting for new data point")
                await asyncio.sleep(0.1)

            if not scan_item.num_points:
                continue
            if scan_item.scanID in scan_item.open_scan_defs:
                continue

            if point_id == scan_item.num_points:
                break
            if point_id > scan_item.num_points:
                raise RuntimeError("Received more points than expected.")

        await wait_for_scan_item_to_finish(bec, scan_item=scan_item)

        elapsed_time = scan_item.end_time - scan_item.start_time
        print(
            table.get_footer(
                f"Scan {scan_item.scan_number} finished. Scan ID {scan_item.scanID}. Elapsed time: {elapsed_time:.2f} s"
            )
        )
