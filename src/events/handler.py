from events.eventData import Danmu, Gift, SuperChat, User
from proto.proto import BilibiliLivePackage, BilibiliProtoException
from utils.danmuInfo import DanmuInfo


class BilibiliLiveEventHandler:
    def onAuth(self, data: DanmuInfo):
        """校验已通过"""

    def onDanmu(self, data: Danmu):
        """收到弹幕事件"""

    def onGift(self, data: Gift):
        """收到礼物事件，银瓜子礼物或金瓜子礼物都会触发"""

    def onSilverGift(self, data: Gift):
        """收到银瓜子礼物事件"""

    def onGoldGift(self, data: Gift):
        """收到金瓜子礼物事件"""

    def onInteractWord(self, data: User):
        """收到底部消息，包括进入直播间、关注主播等"""

    def onUserEntry(self, data: User):
        """用户进入直播间，包括舰长和未上舰用户"""

    def onSuperChat(self, data: SuperChat):
        """收到醒目留言，包括日语留言"""

    def onUnpackExceprion(self, exception: BilibiliProtoException):
        """解包消息过程出现异常"""

    def onNotProcessPackage(self, package: BilibiliLivePackage):
        """未处理的包"""
