import sys
import warnings
from typing import List

from typeguard import typechecked

from bec_utils import bec_logger

logger = bec_logger.logger

try:
    import scilog
except ImportError:
    logger.warning("The logbook cannot be used as the import of scilog failed.")


class LogbookMessage:
    def __init__(self, logbook):
        self._logbook = logbook
        self._content = scilog.Paragraph()

    def add_text(self, msg: str):
        if not msg.startswith("<"):
            msg = f"<p>{msg}</p>"

        if self._content.textcontent:
            self._content.textcontent += msg
        else:
            self._content.textcontent = msg
        return self

    def add_file(self, file_path: str):
        file_info, textcontent = self._logbook.log.prepare_file_content(file_path)
        if self._content.files:
            self._content.files.append(file_info)
        else:
            self._content.files = [file_info]
        self.add_text(textcontent)
        return self

    def add_tag(self, tag: List[str]):
        if not isinstance(tag, list):
            tag = [tag]
        if self._content.tags:
            self._content.tags.extend(tag)
        else:
            self._content.tags = tag
        return self


class LogbookConnector:
    def __init__(self, url="https://scilog.qa.psi.ch/api/v1") -> None:
        self.url = url
        self.connected = False
        self._scilog_module = None
        self._connect()
        self.logbook = None

    def _connect(self):
        if "scilog" in sys.modules:
            token = "Bearer "
            self._scilog_module = scilog
            self.log = self._scilog_module.SciLog(self.url, options={"token": token})
            # FIXME the python sdk should not use the ownergroup
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                logbooks = self.log.get_logbooks(ownerGroup="p20588")
            if len(logbooks) > 1:
                raise NotImplementedError
            self.log.select_logbook(logbooks[0])
            self.connected = True

    @typechecked
    def send_message(self, msg: str):
        """Send a simple text message to the logbook

        Args:
            msg (str): Message that ought to be sent

        Example:
            >>> log.send_message("Text")

        """
        logbook_msg = LogbookMessage(self.log)
        logbook_msg.add_text(msg)
        self.send_logbook_message(logbook_msg)

    @typechecked
    def send_logbook_message(self, msg: LogbookMessage) -> None:
        payload = msg._content.to_dict(include_none=False)
        payload["linkType"] = "paragraph"
        # FIXME the python sdk should not use the ownergroup
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.log.post_snippet(**payload)

    def login(self):
        pass


if __name__ == "__main__":
    import datetime

    logbook = LogbookConnector()
    msg = LogbookMessage(logbook)
    # msg.add_text("Test").add_file("/Users/wakonig_k/Desktop/lamni_logo.png")
    msg.add_text(
        f"<p><mark class='pen-red'><strong>Beamline checks failed at {str(datetime.datetime.now())}.</strong></mark></p>"
    ).add_tag("BEC")
    logbook.send_logbook_message(msg)
