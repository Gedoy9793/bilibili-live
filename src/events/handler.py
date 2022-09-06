from ..proto.proto import BilibiliLivePackage, BilibiliProtoException
from .eventData import Danmu, Gift, SuperChat, User


class BilibiliLiveEventHandler:
    def __init__(self, observer):
        self.observer = observer

    def onPackage(self, package: BilibiliLivePackage):
        """收到任意包"""

    def onAuth(self, package: BilibiliLivePackage):
        """校验已通过"""

    def onDanmu(self, package: BilibiliLivePackage, data: Danmu):
        """收到弹幕事件"""

    def onGift(self, package: BilibiliLivePackage, data: Gift):
        """收到礼物事件，银瓜子礼物或金瓜子礼物都会触发"""

    def onSilverGift(self, package: BilibiliLivePackage, data: Gift):
        """收到银瓜子礼物事件"""

    def onGoldGift(self, package: BilibiliLivePackage, data: Gift):
        """收到金瓜子礼物事件"""

    def onInteractWord(self, package: BilibiliLivePackage, data: User):
        """收到底部消息，包括进入直播间、关注主播等"""

    def onFollow(self, package: BilibiliLivePackage, data: User):
        """用户关注主播"""

    def onShare(self, package: BilibiliLivePackage, data: User):
        """用户分享了直播间"""

    def onUserEntry(self, package: BilibiliLivePackage, data: User):
        """用户进入直播间，包括舰长和未上舰用户"""

    def onSuperChat(self, package: BilibiliLivePackage, data: SuperChat):
        """收到醒目留言，包括日语留言"""

    def onUnpackExceprion(self, package: BilibiliLivePackage, exception: BilibiliProtoException):
        """解包消息过程出现异常"""

    def onException(self, exception: Exception):
        """出现异常"""

    def onNotProcessPackage(self, package: BilibiliLivePackage):
        """未处理的包"""
