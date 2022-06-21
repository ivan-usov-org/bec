import asyncio
import logging
import threading
import time

import bec_utils.BECMessage as KMessage
import msgpack
import numpy as np
from bec_utils import Alarms, DeviceManagerBase, DeviceStatus, MessageEndpoints
from bec_utils.connector import ConsumerConnector

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
    if len(bk.alarms) > 0:
        for alarm in bk.alarms:
            if alarm.severity > Alarms.WARNING:
                raise alarm


async def live_updates_readback(
    dm: DeviceManagerBase, move_args: dict, consumer: ConsumerConnector
) -> None:
    """Live feedback on motor movements.

    Args:
        dm (DeviceManagerBase): devicemanager
        move_args (dict): arguments passed to the move command
        consumer (ConsumerConnector): active consumer

    """
    start = time.time()
    dm.parent._set_busy()
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
                msg = KMessage.DeviceMessage.loads(msg.value).content["signals"]
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
                    if val is not None:
                        val = msgpack.loads(val)
                        # print(val.get("timestamp") - start)
                        # print(dev_values)
                        # print(DeviceStatus(val.get("status")))
                        if DeviceStatus(val.get("status")) == DeviceStatus.IDLE:
                            if all(
                                np.isclose(
                                    dev_values[ind], list(move_args.values())[ind], atol=0.05
                                )
                            ):
                                if not stop[ind].is_set():
                                    set_event_delayed(stop[ind], 0.2)
                check_alarms(dm.parent)
                await asyncio.sleep(0.1)
                # else:

                #     if all(
                #         np.isclose(dev_values[ind], list(move_args.values())[ind])
                #     ):
                #         if not stop[ind].is_set:
                #             set_event_delayed(stop[ind], 0.2)
            print_device_positions()

    print("\n")
    dm.parent._set_idle()


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


async def live_updates_table(bk, request):
    acq_header = "seq. num"
    pause_requested = False
    scan_devices = request.content["parameter"]["args"].keys()
    primary_devices = bk.devicemanager.devices.primary_devices(
        [bk.devicemanager.devices[dev] for dev in scan_devices]
    )
    primary_devices = primary_devices[0 : min(15, len(primary_devices)) - 1]
    devices = [dev.name for dev in primary_devices]
    dev_values = [0 for dev in devices]

    RID = request.metadata["RID"]

    scan_queue_requests = bk.queue.scan_queue_requests

    scan_queue_request = await wait_for_scan_request(scan_queue_requests, RID)

    await wait_for_scan_request_decision(scan_queue_request)
    check_alarms(bk)
    if not scan_queue_request.decision_pending:
        while scan_queue_request.accepted is None:
            await asyncio.sleep(0.01)
        if scan_queue_request.accepted[0] == True:
            # scanID = scan_queue_request.scanID

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
                elif queue_pos > 0:
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
            print(f"Starting scan {scan_number}.")

            header = [acq_header]
            header.extend(devices)
            t = PrettyTable(header, padding=12)
            print(t.get_header_lines())

            point_id = 0
            while True:
                check_alarms(bk)
                point_data = queue_item.data.get(point_id)
                if point_data:
                    point_id += 1
                    if point_id % 100 == 0:
                        print(t.get_header_lines())
                    for ind, dev in enumerate(devices):
                        dev_values[ind] = point_data[dev][dev].get("value")
                    print(t.get_row(point_id, *dev_values))
                else:
                    logger.debug("waiting for new data point")
                    await asyncio.sleep(0.1)
                queue_pos = bk.queue.get_queue_position(scanID)
                if queue_item.num_points is not None and scanID not in queue_item._open_scan_defs:
                    if point_id == queue_item.num_points:
                        break
                    elif point_id > queue_item.num_points:
                        raise RuntimeError("Received more points than expected.")
                # if queue_pos is None:
                #     print(t.get_row_separator())
                #     print(t.get_header_separator())
                #     break
            if queue_pos is None:
                print(t.get_footer(f"Scan {scan_number} finished. Scan ID {scanID}."))
        else:
            raise ScanRequestError("Scan was rejected by the server.")
