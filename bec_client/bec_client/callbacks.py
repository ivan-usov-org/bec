import asyncio
import logging
import threading
import time

import bec_utils.BECMessage as BMessage
import msgpack
import numpy as np
from bec_utils import Alarms, DeviceManagerBase, DeviceStatus, MessageEndpoints
from bec_utils.connector import ConsumerConnector

from bec_client.progressbar import DeviceProgressBar, ScanProgressBar

from .prettytable import PrettyTable

logger = logging.getLogger("client_callback")


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


def check_alarms(bk):
    for alarm in bk.alarms(severity=Alarms.MINOR):
        print(alarm)
        raise alarm


async def live_updates_readback_progressbar(
    dm: DeviceManagerBase, request: BMessage.ScanQueueMessage
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
            dm.devices[dev].read(cached=True, use_readback=True).get("value") for dev in devices
        ]

    start_values = get_device_values()
    with DeviceProgressBar(
        devices=devices, start_values=start_values, target_values=target_values
    ) as progress:
        while not progress.finished:
            check_alarms(dm.parent)
            values = get_device_values()
            progress.update(values=values)

            pipe = dm.producer.pipeline()
            for dev in devices:
                dm.producer.get(MessageEndpoints.device_req_status(dev), pipe)
            req_done_msgs = pipe.execute()

            for dev, msg in zip(devices, req_done_msgs):
                msg = BMessage.DeviceReqStatusMessage.loads(msg)
                if not msg:
                    continue
                if not msg.metadata["RID"] == request.metadata["RID"]:
                    continue
                if msg.content.get("success", False):
                    progress.set_finished(dev)

            await progress.sleep()


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
                msg = BMessage.DeviceMessage.loads(msg.value).content["signals"]
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


async def wait_for_scan_request(requests, RID):
    logger.debug("Waiting for request ID")
    start = time.time()
    while requests.get(RID) is None:
        await asyncio.sleep(0.1)
    logger.debug(f"Waiting for request ID finished after {time.time()-start} s.")
    return requests.get(RID)


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
    print(devices)
    return devices


async def live_updates_table(bk, request):
    acq_header = "seq. num"
    scan_devices = request.content["parameter"]["args"].keys()
    primary_devices = bk.devicemanager.devices.primary_devices(
        [bk.devicemanager.devices[dev] for dev in scan_devices]
    )

    RID = request.metadata["RID"]

    scan_queue_requests = bk.queue.scan_queue_requests

    scan_queue_request = await wait_for_scan_request(scan_queue_requests, RID)

    await wait_for_scan_request_decision(scan_queue_request)
    check_alarms(bk)
    if not scan_queue_request.decision_pending:
        while scan_queue_request.accepted is None:
            await asyncio.sleep(0.01)
        if scan_queue_request.accepted[0]:

            devices = [dev.name for dev in primary_devices]
            devices = sort_devices(devices, scan_devices)
            devices = devices[0 : min(10, len(devices)) - 1]
            dev_values = [0 for dev in devices]

            queue_item = bk.queue.find_scan(RID=RID)
            timeout_time = 15
            sleep_time = 0.1
            consumed_time = 0
            while queue_item is None:
                check_alarms(bk)
                await asyncio.sleep(sleep_time)
                consumed_time += sleep_time
                if consumed_time > timeout_time:
                    raise TimeoutError("Reached timeout while waiting for scan data.")
                queue_item = bk.queue.find_scan(RID=RID)

            block_id = queue_item.queueInfo.get_block_id(RID)

            scanID = queue_item.queueInfo.scanID[block_id]
            scan_number = queue_item.queueInfo.scan_number[block_id]
            while True:
                queue_pos = bk.queue.get_queue_position(scanID)
                if queue_pos is None:
                    break
                if queue_pos > 0:
                    print(
                        f"Scan is enqueued and is waiting for execution. Current position in queue: {queue_pos + 1}.",
                        end="\r",
                        flush=True,
                    )
                    await asyncio.sleep(0.1)
                else:
                    break
            if queue_pos is None:
                print(f"Could not find queue entry for scanID {scanID}")
                if bk.queue.find_scan(RID) is None:
                    return
            while len(queue_item.status) == 0:
                await asyncio.sleep(0.1)
            print(f"Starting scan {scan_number}.")

            header = [acq_header]
            header.extend(devices)
            table = PrettyTable(header, padding=12)
            print(table.get_header_lines())

            with ScanProgressBar(scan_number=scan_number, clear_on_exit=True) as progressbar:
                point_id = 0
                while True:
                    check_alarms(bk)
                    point_data = queue_item.data.get(point_id)
                    if queue_item.num_points:
                        progressbar.max_points = queue_item.num_points - 1

                    progressbar.update(point_id)
                    if point_data:
                        point_id += 1
                        if point_id % 100 == 0:
                            print(table.get_header_lines())
                        for ind, dev in enumerate(devices):
                            dev_values[ind] = point_data[dev][dev].get("value")
                        print(table.get_row(point_id, *dev_values))
                        progressbar.update(point_id)
                    else:
                        logger.debug("waiting for new data point")
                        await asyncio.sleep(0.1)

                    if (
                        queue_item.num_points is not None
                        and scanID not in queue_item.open_scan_defs
                    ):
                        if point_id == queue_item.num_points:
                            break
                        if point_id > queue_item.num_points:
                            raise RuntimeError("Received more points than expected.")

                queue_pos = bk.queue.get_queue_position(scanID)
                if queue_pos is None:
                    print(
                        table.get_footer(
                            f"Scan {scan_number} finished. Scan ID {scanID}. Elapsed time: {queue_item.end_time-queue_item.start_time:.2f} s"
                        )
                    )
        else:
            raise ScanRequestError(
                f"Scan was rejected by the server: {scan_queue_request.response.content.get('message')}"
            )
