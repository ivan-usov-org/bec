from __future__ import annotations

import asyncio
import collections
import time
from typing import TYPE_CHECKING

from bec_utils.bec_errors import ScanInterruption

from .live_table import LiveUpdatesTable
from .move_device import LiveUpdatesReadbackProgressbar
from .utils import ScanRequestMixin, check_alarms

if TYPE_CHECKING:
    from bec_client import BECClient


class CallbackManager:
    def __init__(self, client: BECClient) -> None:
        self.client = client
        self._interrupted_request = None
        self._active_callback = None
        self._processed_instructions = 0
        self._active_request = None
        self._user_callback = None
        self._request_block_index = collections.defaultdict(lambda: 0)
        self._request_block_id = None

    def _process_report_instructions(self, report_instructions: list) -> None:
        scan_type = self._active_request.content["scan_type"]
        if scan_type in ["open_scan_def", "close_scan_def"]:
            self._process_instruction({"table_wait": 0})
            return
        if scan_type == "close_scan_group":
            return

        if not report_instructions:
            return

        remaining_report_instructions = report_instructions[self._processed_instructions :]
        if not remaining_report_instructions:
            return

        for instr in remaining_report_instructions:
            self._process_instruction(instr)
            self._processed_instructions += 1

    def _process_instruction(self, instr: dict):
        scan_report_type = list(instr.keys())[0]
        scan_def_id = self.client.scans._scan_def_id
        if scan_def_id is None:
            if scan_report_type == "readback":
                asyncio.run(
                    LiveUpdatesReadbackProgressbar(
                        self.client,
                        report_instruction=instr,
                        request=self._active_request,
                        callbacks=self._user_callback,
                    ).run()
                )
            elif scan_report_type == "table_wait":
                asyncio.run(
                    LiveUpdatesTable(
                        self.client,
                        report_instruction=instr,
                        request=self._active_request,
                        callbacks=self._user_callback,
                    ).run()
                )
        else:
            if self._active_callback:
                if scan_report_type == "readback":
                    asyncio.run(
                        LiveUpdatesReadbackProgressbar(
                            self.client,
                            report_instruction=instr,
                            request=self._active_request,
                            callbacks=self._user_callback,
                        ).run()
                    )
                else:
                    asyncio.run(
                        self._active_callback.resume(
                            request=self._active_request,
                            report_instruction=instr,
                            callbacks=self._user_callback,
                        )
                    )

                return

            self._active_callback = LiveUpdatesTable(
                self.client,
                report_instruction=instr,
                request=self._active_request,
                callbacks=self._user_callback,
            )
            asyncio.run(self._active_callback.run())

    def process_request(self, request, scan_report_type, callbacks):
        # pylint: disable=protected-access
        try:
            with self.client._sighandler:
                # pylint: disable=protected-access
                self._active_request = request
                self._user_callback = callbacks

                scan_request = ScanRequestMixin(self.client, request.metadata["RID"])
                asyncio.run(scan_request.wait())

                # get the corresponding queue item
                while not scan_request.request_storage.storage[-1].queue:
                    time.sleep(0.01)

                queue = scan_request.request_storage.storage[-1].queue
                self._request_block_id = req_id = self._active_request.metadata.get("RID")

                report_instructions = []
                req_block = {}
                while queue.status not in ["COMPLETED", "ABORTED", "HALTED"]:
                    check_alarms(self.client)
                    if not queue.request_blocks:
                        continue
                    available_blocks = [
                        req_block
                        for req_block in queue.request_blocks
                        if req_block["RID"] == request.metadata["RID"]
                    ]
                    req_block = available_blocks[self._request_block_index[req_id]]
                    if req_block["content"]["scan_type"] == "open_scan_def":
                        break

                    report_instructions = req_block["report_instructions"]
                    if not report_instructions:
                        continue
                    self._process_report_instructions(report_instructions)

                    complete_rbl = len(available_blocks) == self._request_block_index[req_id] + 1
                    if self._active_callback and complete_rbl:
                        break

                    if not queue.active_request_block:
                        break

                report_instructions = req_block.get("report_instructions", [])
                self._process_report_instructions(report_instructions)

            self._reset()

        except ScanInterruption as scan_interr:
            self._interrupted_request = (request, scan_report_type)
            raise scan_interr

    def _reset(self):
        self._interrupted_request = None

        self._user_callback = None
        self._processed_instructions = 0
        scan_closed = self._active_request.content["scan_type"] == "close_scan_def"
        self._active_request = None

        if self.client.scans._scan_def_id and not scan_closed:
            self._request_block_index[self._request_block_id] += 1
            return

        if scan_closed:
            self._active_callback = None

    def continue_request(self):
        if not self._interrupted_request:
            return
        self.process_request(*self._interrupted_request)
