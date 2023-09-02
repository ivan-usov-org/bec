import asyncio

from bec_lib.core import BECMessage, MessageEndpoints, bec_logger

from bec_client.progressbar import ScanProgressBar

from .live_table import LiveUpdatesTable

logger = bec_logger.logger


class LiveUpdatesScanProgress(LiveUpdatesTable):
    async def core(self):
        req_ID = self.scan_queue_request.requestID
        while True:
            request_block = [
                req for req in self.scan_item.queue.request_blocks if req["RID"] == req_ID
            ][0]
            if not request_block["is_scan"]:
                break
            if request_block["report_instructions"]:
                break
            self.check_alarms()

        await self._run_scan_progress_update(self.report_instruction["scan_progress"])

    async def _run_scan_progress_update(self, device_names: str):
        with ScanProgressBar(
            scan_number=self.scan_item.scan_number, clear_on_exit=False
        ) as progressbar:
            while True:
                self.check_alarms()
                status = self.bec.producer.get(MessageEndpoints.device_progress(device_names[0]))
                if not status:
                    logger.debug("waiting for new data point")
                    await asyncio.sleep(0.1)
                    continue
                status = BECMessage.DeviceStatusMessage.loads(status)
                if status.metadata["scanID"] != self.scan_item.scanID:
                    logger.debug("waiting for new data point")
                    await asyncio.sleep(0.1)
                    continue

                point_id = status.content["status"].get("value")
                if point_id is None:
                    logger.debug("waiting for new data point")
                    await asyncio.sleep(0.1)
                    continue

                max_value = status.content["status"].get("max_value")
                if max_value and max_value != progressbar.max_points:
                    progressbar.max_points = max_value

                progressbar.update(point_id)
                # process sync callbacks
                self.bec.callbacks.poll()
                self.scan_item.poll_callbacks()

                if point_id == max_value:
                    break

    async def process_request(self):
        if self.request.content["scan_type"] == "close_scan_def":
            await self.wait_for_scan_item_to_finish()
            return

        await self.wait_for_request_acceptance()
        await asyncio.wait_for(self.update_scan_item(), timeout=15)
        await self.wait_for_scan_to_start()

        print(f"\nStarting scan {self.scan_item.scan_number}.")

        await self.core()

    async def run(self):
        if self.request.content["scan_type"] == "open_scan_def":
            await self.wait_for_request_acceptance()
            return
        await self.process_request()
        await self.wait_for_scan_item_to_finish()
