from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from bec_utils.bec_errors import ScanInterruption

from .live_table import LiveUpdatesTable
from .move_device import LiveUpdatesReadbackProgressbar

if TYPE_CHECKING:
    from bec_client import BECClient


class CallbackManager:
    def __init__(self, client: BECClient) -> None:
        self.client = client
        self._interrupted_request = None

    def process_request(self, request, scan_report_type):
        # pylint: disable=protected-access
        try:
            with self.client._sighandler:
                if scan_report_type == "readback":
                    asyncio.run(
                        LiveUpdatesReadbackProgressbar(
                            self.client,
                            request,
                        ).run()
                    )
                elif scan_report_type == "table":
                    # pylint: disable=protected-access
                    scan_def_id = self.client.scans._scan_def_id

                    if scan_def_id is None or request.content["scan_type"] == "close_scan_def":
                        asyncio.run(LiveUpdatesTable(self.client, request).run())
            self._interrupted_request = None
        except ScanInterruption as scan_interr:
            self._interrupted_request = (request, scan_report_type)
            raise ScanInterruption from scan_interr

    def continue_request(self):
        if not self._interrupted_request:
            return
        self.process_request(*self._interrupted_request)
