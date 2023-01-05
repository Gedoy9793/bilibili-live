from ..proto.proto import BilibiliProtoException
from .eventData import Danmu, Event, Gift, SuperChat, User


class BilibiliLiveEventHandler:
    def __init__(self, observer):
        self.observer = observer

    def onHeart(self):
        """发出心跳包"""

    def onHeartRecv(self, event: Event[None]):
        """收到心跳包"""

    def onPackage(self, event: Event[None]):
        """收到任意包"""

    def onAuth(self, event: Event[None]):
        """校验已通过"""

    def onLiveEnd(self, event: Event[None]):
        """直播结束"""

    def onDanmu(self, event: Event[Danmu]):
        """收到弹幕事件"""

    def onGift(self, event: Event[Gift]):
        """收到礼物事件，银瓜子礼物或金瓜子礼物都会触发"""

    def onSilverGift(self, event: Event[Gift]):
        """收到银瓜子礼物事件"""

    def onGoldGift(self, event: Event[Gift]):
        """收到金瓜子礼物事件"""

    def onGuardBuy(self, event: Event[User]):
        """上舰"""

    def onInteractWord(self, event: Event[User]):
        """收到底部消息，包括进入直播间、关注主播等"""

    def onFollow(self, event: Event[User]):
        """用户关注主播"""

    def onShare(self, event: Event[User]):
        """用户分享了直播间"""

    def onUserEntry(self, event: Event[User]):
        """用户进入直播间，包括舰长和未上舰用户"""

    def onSuperChat(self, event: Event[SuperChat]):
        """收到醒目留言，包括日语留言"""

    def onUnpackException(self, event: Event[BilibiliProtoException]):
        """解包消息过程出现异常"""

    def onException(self, exception: Exception):
        """出现异常"""

    def onNotProcessPackage(self, event: Event[None]):
        """未处理的包"""
