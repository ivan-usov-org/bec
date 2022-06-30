import bec_utils.BECMessage as BMessage

import koss.scans as koss_scans


class ScanAssembler:
    """
    ScanAssembler receives scan messages and translates the scan message into device instructions.
    """

    def __init__(self, *, parent):
        self.parent = parent
        self.device_manager = self.parent.device_manager
        self.connector = self.parent.connector
        self._scans = self.parent.scan_dict #TODO should these be the same dict, or a copy?

    def assemble_device_instructions(self, msg: BMessage.ScanQueueMessage):
        scan = msg.content.get("scan_type")
        cls_name self._scans[scan]["class"]
        scan_cls = getattr(koss_scans, cls_name)

        print(f"Preparing instructions of request of type {scan} / {scan_cls}") #TODO: logging?

        return scan_cls(
            device_manager=self.device_manager,
            parameter=msg.content.get("parameter"),
            metadata=msg.metadata,
        )
