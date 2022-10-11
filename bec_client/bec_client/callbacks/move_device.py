import numpy as np
from bec_client.progressbar import DeviceProgressBar
from bec_utils import BECMessage, DeviceManagerBase, MessageEndpoints

from .utils import check_alarms


class ReadbackDataMixin:
    def __init__(self, device_manager: DeviceManagerBase, devices) -> None:
        self.device_manager = device_manager
        self.devices = devices

    def get_device_values(self):
        """get the current device values"""
        return [
            self.device_manager.devices[dev].read(cached=True, use_readback=True).get("value")
            for dev in self.devices
        ]

    def get_request_done_msgs(self):
        """get all request-done messages"""
        pipe = self.device_manager.producer.pipeline()
        for dev in self.devices:
            self.device_manager.producer.get(MessageEndpoints.device_req_status(dev), pipe)
        return pipe.execute()

    def wait_for_RID(self, request):
        """wait for the readback's metadata to match the request ID"""
        while True:
            msgs = [
                BECMessage.DeviceMessage.loads(
                    self.device_manager.producer.get(MessageEndpoints.device_readback(dev))
                )
                for dev in self.devices
            ]
            if all(msg.metadata.get("RID") == request.metadata["RID"] for msg in msgs if msg):
                break
            check_alarms(self.device_manager.parent)


async def live_updates_readback_progressbar(
    device_manager: DeviceManagerBase, request: BECMessage.ScanQueueMessage
) -> None:
    """Live feedback on motor movements using a progressbar.

    Args:
        dm (DeviceManagerBase): devicemanager
        request (ScanQueueMessage): request that should be monitored

    """

    devices = list(request.content["parameter"]["args"].keys())

    data_source = ReadbackDataMixin(device_manager, devices)
    data_source.wait_for_RID(request)

    start_values = data_source.get_device_values()
    target_values = [x for xs in request.content["parameter"]["args"].values() for x in xs]
    if request.content["parameter"]["kwargs"].get("relative"):
        target_values = np.asarray(target_values) + np.asarray(start_values)

    with DeviceProgressBar(
        devices, start_values=start_values, target_values=target_values
    ) as progress:
        req_done = False
        while not progress.finished or not req_done:
            check_alarms(device_manager.parent)

            values = data_source.get_device_values()
            progress.update(values=values)

            req_done_msgs = data_source.get_request_done_msgs()
            msgs = [BECMessage.DeviceReqStatusMessage.loads(msg) for msg in req_done_msgs]
            request_ids = [
                msg.metadata["RID"] if (msg and msg.metadata.get("RID")) else None for msg in msgs
            ]
            if set(request_ids) != set([request.metadata["RID"]]):
                await progress.sleep()
                continue

            req_done = True
            for dev, msg in zip(devices, msgs):
                if not msg:
                    continue
                if msg.content.get("success", False):
                    progress.set_finished(dev)
