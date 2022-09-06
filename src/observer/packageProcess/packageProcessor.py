from events.handler import BilibiliLiveEventHandler

from .convert import (
    DANMU_MSG_to_Danmu,
    ENTRY_EFFECT_to_User,
    INTERACT_WORD_to_User,
    SEND_GIFT_to_Gift,
    SUPER_CHAT_MESSAGE_JPN_to_SuperChat,
)
from .exceptions import PackageConvertException


class PackageProcessor:
    def __init__(self, handler):
        self.handler: BilibiliLiveEventHandler = handler

    def process(self, package):
        # ====================心跳包===================
        if package.cmd == "OP_AUTH_REPLY":
            # wss连接鉴权通过
            ...
        elif package.cmd == "OP_HEARTBEAT_REPLY":
            # 收到心跳包
            ...

        # ====================打榜相关=================
        elif package.cmd == "STOP_LIVE_ROOM_LIST":
            # 直播结束时显示的推荐房间列表
            ...
        elif package.cmd == "ONLINE_RANK_V2":
            # 高能榜数据
            ...
        elif package.cmd == "ONLINE_RANK_COUNT":
            # 高能榜数据更新
            ...
        elif package.cmd == "LIVE_INTERACTIVE_GAME":
            ...
        elif package.cmd == "HOT_RANK_CHANGED":
            # 主播实时活动排名
            ...
        elif package.cmd == "HOT_RANK_CHANGED_V2":
            # 主播实时活动排名
            ...
        elif package.cmd == "HOT_RANK_SETTLEMENT_V2":
            ...

        # ================基础互动消息===================
        elif package.cmd == "DANMU_MSG":
            # 收到弹幕
            danmu = DANMU_MSG_to_Danmu.convert(package.data)
            self.handler.onDanmu(danmu)

        elif package.cmd == "INTERACT_WORD":
            # 下方互动文字
            user = INTERACT_WORD_to_User.convert(package.data)
            self.handler.onInteractWord(user)
            if package.data.get("msg_type") == 1:
                # 用户进入直播间
                self.handler.onUserEntry(user)
            else:
                print(package)

        elif package.cmd == "SEND_GIFT":
            # 发送礼物
            gift = SEND_GIFT_to_Gift.convert(package.data)
            self.handler.onGift(gift)
            if gift.coin_type == "gold":
                self.handler.onGoldGift(gift)
            elif gift.coin_type == "silver":
                self.handler.onSilverGift(gift)

        elif package.cmd == "SUPER_CHAT_MESSAGE":
            # 醒目留言
            # 似乎醒目留言事件和日语醒目留言事件会同时出现，所以只处理下面那个好了
            ...

        elif package.cmd == "SUPER_CHAT_MESSAGE_JPN":
            # 日语醒目留言
            superChat = SUPER_CHAT_MESSAGE_JPN_to_SuperChat.convert(package.data)
            self.handler.onSuperChat(superChat)

        elif package.cmd == "COMBO_SEND":
            # 连击礼物
            ...

        elif package.cmd == "ENTRY_EFFECT":
            # 用户进入特效(舰长进入直播间)
            try:
                user = ENTRY_EFFECT_to_User.convert(package.data)
                self.handler.onUserEntry(user)
            except PackageConvertException:
                print(package)

        # =====================直播间状态消息==================
        elif package.cmd == "WATCHED_CHANGE":
            # 观看人数更新
            ...

        elif package.cmd == "ROOM_REAL_TIME_MESSAGE_UPDATE":
            # 房间实时信息更新(粉丝数)
            ...

        elif package.cmd == "ROOM_BLOCK_MSG":
            # 禁言
            ...

        elif package.cmd == "PREPARING":
            # 下播
            print(package)

        elif package.cmd == "LIVE":
            # 开播
            print(package)

        # ===================全局消息====================
        elif package.cmd == "HOT_ROOM_NOTIFY":
            ...
        elif package.cmd == "NOTICE_MSG":
            # 直播间通知
            ...
        elif package.cmd == "WIDGET_BANNER":
            ...
        elif package.cmd == "COMMON_NOTICE_DANMAKU":
            ...

        else:
            print(package)
