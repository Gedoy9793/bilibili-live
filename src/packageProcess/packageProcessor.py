from ..events.handler import BilibiliLiveEventHandler
from .convert import (
    DANMU_MSG_to_Danmu,
    ENTRY_EFFECT_to_User,
    INTERACT_WORD_to_User,
    SEND_GIFT_to_Gift,
    SUPER_CHAT_MESSAGE_JPN_to_SuperChat,
    SUPER_CHAT_MESSAGE_to_SuperChat,
)


class PackageProcessor:
    def __init__(self, handler: BilibiliLiveEventHandler):
        self.handler = handler

    def process(self, package):
        # ====================心跳包===================
        if package.cmd == "OP_AUTH_REPLY":
            # wss连接鉴权通过
            self.handler.onAuth(package)

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
        elif package.cmd == "ONLINE_RANK_TOP3":
            ...
        elif package.cmd == "HOT_RANK_SETTLEMENT":
            ...

        # ================基础互动消息===================
        elif package.cmd == "DANMU_MSG":
            # 收到弹幕
            danmu = DANMU_MSG_to_Danmu.convert(package.data)
            self.handler.onDanmu(package, danmu)

        elif package.cmd == "INTERACT_WORD":
            # 下方互动文字
            user = INTERACT_WORD_to_User.convert(package.data)
            self.handler.onInteractWord(package, user)
            if package.data.get("msg_type") == 1:
                # 用户进入直播间
                self.handler.onUserEntry(package, user)
            elif package.data.get("msg_type") == 2:
                # 用户关注主播
                self.handler.onFollow(package, user)
            elif package.data.get("msg_type") == 3:
                # 用户分享直播间
                self.handler.onShare(package, user)
            else:
                self.handler.onNotProcessPackage(package)

        elif package.cmd == "SEND_GIFT":
            # 发送礼物
            gift = SEND_GIFT_to_Gift.convert(package.data)
            self.handler.onGift(package, gift)
            if gift.coin_type == "gold":
                self.handler.onGoldGift(package, gift)
            elif gift.coin_type == "silver":
                self.handler.onSilverGift(package, gift)

        elif package.cmd == "SUPER_CHAT_MESSAGE":
            # 醒目留言
            superChat = SUPER_CHAT_MESSAGE_to_SuperChat.convert(package.data)
            self.handler.onSuperChat(package, superChat)

        elif package.cmd == "SUPER_CHAT_MESSAGE_JPN":
            # 日语醒目留言
            superChat = SUPER_CHAT_MESSAGE_JPN_to_SuperChat.convert(package.data)
            self.handler.onSuperChat(package, superChat)

        elif package.cmd == "COMBO_SEND":
            # 连击礼物
            ...

        elif package.cmd == "ENTRY_EFFECT":
            # 用户进场特效
            user = ENTRY_EFFECT_to_User.convert(package.data)
            self.handler.onUserEntry(package, user)

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
        elif package.cmd == "LIVE_MULTI_VIEW_CHANGE":
            ...
        else:
            print(package)
