from events.eventData import Danmu, Gift


class BilibiliLiveEventHandler:
    def onDanmu(self, data: Danmu):
        ...

    def onGift(self, data: Gift):
        ...

    def onSilverGift(self, data: Gift):
        ...

    def onGoldGift(self, data: Gift):
        ...