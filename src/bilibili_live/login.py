from threading import Event, Thread

from bilibili_live.events.eventData import LoginUser

from . import api


class LoginServerEventHandle:
    def outOfData(self):
        """二维码已过期"""

    def scaned(self):
        """二维码已扫描待确认"""

    def logined(self, user: LoginUser):
        """已登录"""


class LoginServer:
    def __init__(self) -> None:
        self.stop_pull = Event()
        self.thread = Thread(target=self._poll)

    def _poll(self):
        while True:
            self.stop_pull.wait(2)
            if self.stop_pull.is_set():
                return
            self.res = api.pullScanCodeStatus(self.loginQRCode.key)
            if self.res.code == self.res.QRCodeStatusCodeEnum.CHECKED:
                self.user = api.getUserInfo(self.res.cookies)
                self.handle.logined(self.user)
                return
            elif self.res.code == self.res.QRCodeStatusCodeEnum.OUT_OF_DATA:
                self.handle.outOfData()
                return
            elif self.res.code == self.res.QRCodeStatusCodeEnum.SCANED:
                self.handle.scaned()

    def stopScan(self):
        self.stop_pull.set()

    def setHandle(self, handle: LoginServerEventHandle):
        self.handle = handle

    def getQRCode(self):
        self.loginQRCode = api.generateLoginQRCode()
        if not self.thread.is_alive():
            self.thread = Thread(target=self._poll)
            self.thread.setDaemon(True)
            self.stop_pull.clear()
            self.thread.start()
        return self.loginQRCode
