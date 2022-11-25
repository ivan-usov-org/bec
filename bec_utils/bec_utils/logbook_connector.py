from bec_utils import bec_logger

logger = bec_logger.logger


class LogbookConnector:
    def __init__(self, url="https://scilog.qa.psi.ch/api/v1") -> None:
        self.url = url
        self.connected = False
        self._scilog_module = None
        self._connect()
        self.logbook = None

    def _connect(self):
        try:
            import scilog

            token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzNmNiNTA5ZjQ5ZTJlNDRjMWNiNWUxYSIsIm5hbWUiOiJLbGF1cyBXYWtvbmlnIiwicm9sZXMiOlsicDE2NDE0IiwicDE5NzQ1IiwicDE3NjQ4IiwicDE4NTMzIiwicDE3MzM4IiwicDE4OTg1IiwicDE3NTQ4IiwicDE4MDM4IiwicDE3MzAxIiwicDE0OTY4IiwicDE3MDMyIiwicDE3OTYxIiwicDE5NTUxIiwicDE3OTY0IiwicDE3NjMzIiwicDE2NDA2IiwicDE4MjQ3IiwicDE3OTY1IiwicDE5NDc4IiwicDE3OTY4IiwicDE0NzAyIiwicDE2NDAzIiwicDE3MzA2IiwicDE2ODc2IiwicDE4MTQ0IiwicDE4MTg1IiwicDE4MDQxIiwiYS0zNTQ1NSIsInAxNzMxMSIsImEtMzU0ODciLCJwMTc5NzAiLCJwMTgzOTkiLCJwMTc5NzIiLCJwMTc2NDIiLCJwMTY3OTEiLCJwMTYxMzUiLCJwMTczMTUiLCJwMTY1ODYiLCJwMTgxMDAiLCJwMTYyOTgiLCJwMTc0MTMiLCJwMTY2NDgiLCJwMTcwNTAiLCJwMTY2NDciLCJwMTc4MjgiLCJwMTY2NDQiLCJwMTc4NjUiLCJwMTgyMDEiLCJwMTY2NDMiLCJwMTY4MTIiLCJwMTgyNDkiLCJwMTc4MjQiLCJwMTY2MDIiLCJwMjAyMTYiLCJwMTk3MzAiLCJwMTcyODAiLCJwMTc3OTkiLCJwMjA1ODgiLCJwMTg0NjciLCJwMTc4NTgiLCJwMTY2MTYiLCJwMTYyNzMiLCJwMTg3NjUiLCJwMTk1MjAiLCJwMTczNzEiLCJhbnktYXV0aGVudGljYXRlZC11c2VyIiwia2xhdXMud2Frb25pZ0Bwc2kuY2giXSwiZW1haWwiOiJrbGF1cy53YWtvbmlnQHBzaS5jaCIsImlhdCI6MTY2OTA0MTU3NCwiZXhwIjoxNjcwMjUxNTc0fQ.6hiLzlYptqp0clTcx4A37C_5Hi9xxel2Dw3fu6QJtrs"
            self._scilog_module = scilog
            self.log = self._scilog_module.SciLog(self.url, options={"token": token})
            logbooks = self.log.get_logbooks(ownerGroup="p20588")
            if len(logbooks) > 1:
                raise NotImplementedError
            self.log.select_logbook(logbooks[0])
            self.connected = True

        except ImportError:
            logger.warning("The logbook cannot be used as the import of scilog failed.")

    def send_msg(self, msg: str):
        self.log.send_message(f"<p>{msg}</p>")

    def login(self):
        pass
