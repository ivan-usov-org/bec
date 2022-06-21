import bec_utils.BECMessage as KMessage

import koss.scans as ks


class ScanAssembler:
    """
    ScanAssembler receives scan messages and translates the scan message into device instructions.
    """

    def __init__(self, *, parent):
        self.parent = parent
        self.dm = self.parent.dm
        self.connector = self.parent.connector
        self._scans = dict()
        self._load_scans()

    def _load_scans(self):
        self._scans = self.parent.scan_dict

    def _unpack_scan(self, msg: KMessage.ScanQueueMessage):
        scan = msg.content.get("scan_type")
        scan_cls = getattr(ks, self._scans[scan]["class"])

        print(f"Preparing instructions of request of type {scan} / {scan_cls}")

        return scan_cls(
            devicemanager=self.dm,
            parameter=msg.content.get("parameter"),
            metadata=msg.metadata,
        )

    def assemble_device_instructions(self, msg):
        return self._unpack_scan(msg)
