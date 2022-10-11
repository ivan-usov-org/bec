from bec_client.progressbar import DeviceProgressBar
from bec_utils import BECMessage, DeviceManagerBase, MessageEndpoints

from .utils import check_alarms


class ReadbackDataMixin:
    def __init__(self, device_manager: DeviceManagerBase, devices) -> None:
        self.device_manager = device_manager
        self.devices = devices

    def get_device_values(self):
        return [
            self.device_manager.devices[dev].read(cached=True, use_readback=True).get("value")
            for dev in self.devices
        ]

    def get_request_done_msgs(self):
        pipe = self.device_manager.producer.pipeline()
        for dev in self.devices:
            self.device_manager.producer.get(MessageEndpoints.device_req_status(dev), pipe)
        return pipe.execute()


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

    data_source = ReadbackDataMixin(device_manager, devices)

    while True:
        msgs = [
            BECMessage.DeviceMessage.loads(
                device_manager.producer.get(MessageEndpoints.device_readback(dev))
            )
            for dev in devices
        ]
        if all(msg.metadata.get("RID") == request.metadata["RID"] for msg in msgs if msg):
            break
        check_alarms(device_manager.parent)
    start_values = data_source.get_device_values()

    with DeviceProgressBar(devices, start_values, target_values) as progress:
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
