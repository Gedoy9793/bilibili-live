from events.eventData import Danmu, Gift, SuperChat, User
from proto.proto import BilibiliProtoException


class BilibiliLiveEventHandler:
    def onDanmu(self, data: Danmu):
        ...

    def onGift(self, data: Gift):
        ...

    def onSilverGift(self, data: Gift):
        ...

    def onGoldGift(self, data: Gift):
        ...

    def onInteractWord(self, data: User):
        ...

    def onUserEntry(self, data: User):
        ...

    def onSuperChat(self, data: SuperChat):
        ...

    def onUnpackExceprion(self, exception: BilibiliProtoException):
        ...