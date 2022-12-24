from ..events.eventData import Event
from ..events.handler import BilibiliLiveEventHandler
from .convert import (
    DANMU_MSG_to_Danmu,
    ENTRY_EFFECT_to_User,
    GUARD_BUY_to_User,
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
            self.handler.onAuth(Event(package))

        elif package.cmd == "OP_HEARTBEAT_REPLY":
            # 收到心跳包
            self.handler.onHeartRecv()

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
            danmu, timestamp = DANMU_MSG_to_Danmu.convert(package.data)
            self.handler.onDanmu(Event(package, data=danmu, timestamp=timestamp))

        elif package.cmd == "INTERACT_WORD":
            # 下方互动文字
            user, timestamp = INTERACT_WORD_to_User.convert(package.data)
            self.handler.onInteractWord(Event(package, data=user, timestamp=timestamp))
            if package.data.get("msg_type") == 1:
                # 用户进入直播间
                self.handler.onUserEntry(Event(package, data=user, timestamp=timestamp))
            elif package.data.get("msg_type") == 2:
                # 用户关注主播
                self.handler.onFollow(Event(package, user, timestamp=timestamp))
            elif package.data.get("msg_type") == 3:
                # 用户分享直播间
                self.handler.onShare(Event(package, user, timestamp=timestamp))
            else:
                self.handler.onNotProcessPackage(Event(package))

        elif package.cmd == "SEND_GIFT":
            # 发送礼物
            gift, timestamp = SEND_GIFT_to_Gift.convert(package.data)
            self.handler.onGift(Event(package, gift, timestamp))
            if gift.coin_type == "gold":
                self.handler.onGoldGift(Event(package, gift, timestamp))
            elif gift.coin_type == "silver":
                self.handler.onSilverGift(Event(package, gift, timestamp))

        elif package.cmd == "SUPER_CHAT_MESSAGE":
            # 醒目留言
            superChat, timestamp = SUPER_CHAT_MESSAGE_to_SuperChat.convert(package.data)
            self.handler.onSuperChat(Event(package, superChat, timestamp))

        elif package.cmd == "SUPER_CHAT_MESSAGE_JPN":
            # 日语醒目留言
            superChat, timestamp = SUPER_CHAT_MESSAGE_JPN_to_SuperChat.convert(package.data)
            self.handler.onSuperChat(Event(package, superChat, timestamp))

        elif package.cmd == "SUPER_CHAT_MESSAGE_DELETE":
            # 撤回SC {'ids': [4985011]}
            ...

        elif package.cmd == "COMBO_SEND":
            # 连击礼物
            ...

        elif package.cmd == "ENTRY_EFFECT":
            # 用户进场特效
            user, timestamp = ENTRY_EFFECT_to_User.convert(package.data)
            self.handler.onUserEntry(Event(package, data=user, timestamp=timestamp))

        elif package.cmd == "USER_TOAST_MSG":
            ...

        elif package.cmd == "GUARD_BUY":
            # 上舰
            user, timestamp = GUARD_BUY_to_User.convert(package.data)
            self.handler.onGuardBuy(Event(package, user, timestamp))

        elif package.cmd == "DANMU_AGGREGATION":
            # 集合弹幕 示例：{'activity_identity': '5742069', 'activity_source': 2, 'aggregation_cycle': 1, 'aggregation_icon': 'https://i0.hdslb.com/bfs/live/024f7473753c7cc993413e05c69e8b960086e68f.png', 'aggregation_num': 10, 'dmscore': 144, 'msg': '老板大气！点点红包抽礼物', 'show_rows': 1, 'show_time': 2, 'timestamp': 1662465700}
            ...

        # =====================直播间状态消息==================
        elif package.cmd == "WATCHED_CHANGE":
            # 观看人数更新
            ...

        elif package.cmd == "LIKE_INFO_V3_UPDAT":
            ...

        elif package.cmd == "ROOM_REAL_TIME_MESSAGE_UPDATE":
            # 房间实时信息更新(粉丝数)
            ...

        elif package.cmd == "ROOM_BLOCK_MSG":
            # 禁言
            ...

        elif package.cmd == "PREPARING":
            # 下播
            self.handler.onLiveEnd(Event(package))

        elif package.cmd == "LIVE":
            # 开播 {'cmd': 'LIVE', 'live_key': '276197252200243670', 'voice_background': '', 'sub_session_key': '276197252200243670sub_time:1662465528', 'live_platform': 'pc', 'live_model': 0, 'roomid': 22389206}
            # TODO
            ...

        elif package.cmd == "ROOM_CHANGE":
            # 房间信息变化，示例：{'title': '和小小约联动我爱记歌词~', 'area_id': 371, 'parent_area_id': 9, 'area_name': '虚拟主播', 'parent_area_name': '虚拟主播', 'live_key': '0', 'sub_session_key': ''}
            # TODO
            ...

        elif package.cmd == "POPULARITY_RED_POCKET_NEW":
            # 红包 {'lot_id': 5742069, 'start_time': 1662465687, 'current_time': 1662465687, 'wait_num': 0, 'uname': 'ルキロキ视频存放处', 'uid': 2357943, 'action': '送出', 'num': 1, 'gift_name': '红包', 'gift_id': 13000, 'price': 100, 'name_color': '', 'medal_info': {'target_id': 1359949418, 'special': '', 'icon_id': 0, 'anchor_uname': '', 'anchor_roomid': 0, 'medal_level': 26, 'medal_name': '口袋蛋', 'medal_color': 398668, 'medal_color_start': 398668, 'medal_color_end': 6850801, 'medal_color_border': 6809855, 'is_lighted': 1, 'guard_level': 3}}
            ...

        elif package.cmd == "POPULARITY_RED_POCKET_START":
            # 红包开始 {'lot_id': 5742069, 'sender_uid': 2357943, 'sender_name': 'ルキロキ视频存放处', 'sender_face': 'http://i0.hdslb.com/bfs/face/5065331fe4771c632eefd08a03830388c3daf24f.jpg', 'join_requirement': 1, 'danmu': '老板大气！点点红包抽礼物', 'current_time': 1662465688, 'start_time': 1662465687, 'end_time': 1662465867, 'last_time': 180, 'remove_time': 1662465882, 'replace_time': 1662465877, 'lot_status': 1, 'h5_url': 'https://live.bilibili.com/p/html/live-app-red-envelope/popularity.html?is_live_half_webview=1&hybrid_half_ui=1,5,100p,100p,000000,0,50,0,0,1;2,5,100p,100p,000000,0,50,0,0,1;3,5,100p,100p,000000,0,50,0,0,1;4,5,100p,100p,000000,0,50,0,0,1;5,5,100p,100p,000000,0,50,0,0,1;6,5,100p,100p,000000,0,50,0,0,1;7,5,100p,100p,000000,0,50,0,0,1;8,5,100p,100p,000000,0,50,0,0,1&hybrid_rotate_d=1&hybrid_biz=popularityRedPacket&lotteryId=5742069', 'user_status': 2, 'awards': [{'gift_id': 31213, 'gift_name': '这个好诶', 'gift_pic': 'https://s1.hdslb.com/bfs/live/bb6c11dcc365b3d8287569f08b8b0d0f2e1a3ef8.png', 'num': 3}, {'gift_id': 31212, 'gift_name': '打call', 'gift_pic': 'https://s1.hdslb.com/bfs/live/f75291a0e267425c41e1ce31b5ffd6bfedc6f0b6.png', 'num': 8}, {'gift_id': 31214, 'gift_name': '牛哇', 'gift_pic': 'https://s1.hdslb.com/bfs/live/b8a38b4bd3be120becddfb92650786f00dffad48.png', 'num': 10}], 'lot_config_id': 4, 'total_price': 8000, 'wait_num': 0}
            ...

        elif package.cmd == "POPULARITY_RED_POCKET_WINNER_LIST":
            # 红包结束 {'lot_id': 5742069, 'total_num': 21, 'winner_info': [[8262573, '逸帆帆帆', 3110409, 31213], [383895892, '二奈yuk', 3111968, 31213], [687482615, '碾鱼_出海', 3095370, 31213], [402323599, '龙之圣堂武士', 3103793, 31212], [86178261, '西宮宵子', 3099443, 31212], [12376405, 'slience-8', 3095372, 31212], [2146239736, '符栗', 3128041, 31212], [30650198, '幻想乡丶绅士', 3127576, 31212], [106276499, '丨吴笙丶', 3096814, 31212], [1115373338, '梦者无言', 3127577, 31212], [221708240, '我有一只傻黑猫', 3129049, 31212], [1232472106, '米诺是个低分狗', 3128042, 31214], [223907057, '幻月初憶', 3085711, 31214], [2932836, '合咕', 3128043, 31214], [4485665, 'orangemon', 3095371, 31214], [341096812, '冲鸭玩具推销员', 3111966, 31214], [842512, '兔突猛进biubiubiu', 3111967, 31214], [15457334, '别念我_名字', 3082656, 31214], [183812660, '神里流-万-叶天帝', 3129050, 31214], [11074391, '-_Asuna_-', 3099444, 31214], [27953214, '凌裫', 3082657, 31214]], 'awards': {'31212': {'award_type': 1, 'award_name': '打call', 'award_pic': 'https://s1.hdslb.com/bfs/live/f75291a0e267425c41e1ce31b5ffd6bfedc6f0b6.png', 'award_big_pic': 'https://i0.hdslb.com/bfs/live/9e6521c57f24c7149c054d265818d4b82059f2ef.png', 'award_price': 500}, '31213': {'award_type': 1, 'award_name': '这个好诶', 'award_pic': 'https://s1.hdslb.com/bfs/live/bb6c11dcc365b3d8287569f08b8b0d0f2e1a3ef8.png', 'award_big_pic': 'https://i0.hdslb.com/bfs/live/dafd2e9e5c3086377124a9328e840cd21a3f6847.png', 'award_price': 1000}, '31214': {'award_type': 1, 'award_name': '牛哇', 'award_pic': 'https://s1.hdslb.com/bfs/live/b8a38b4bd3be120becddfb92650786f00dffad48.png', 'award_big_pic': 'https://i0.hdslb.com/bfs/live/3b74c117b4f265edcea261bc5608a58d3a7c300a.png', 'award_price': 100}}, 'version': 1}
            ...

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
            ...
