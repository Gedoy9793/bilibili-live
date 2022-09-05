import asyncio
import json
import websockets
from events.eventData import Danmu, Gift

from src.events.handler import BilibiliLiveEventHandler
from src.proto.proto import BilibiliProto, BilibiliProtoException
from src.utils.danmuInfo import DanmuInfo
from src.utils.roomInfo import RoomInfo

class Observer:
    def schedule(self, handler, short_id):
        self.handler: BilibiliLiveEventHandler = handler

        self.room_info = RoomInfo(short_id)

        self.danmu_info = DanmuInfo(self.room_info.room_id)
        self.host = self.danmu_info.host_list[0]

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.start_asyncio())

    async def start_asyncio(self):
        self.websocket = await websockets.connect(f"wss://{self.host.host}:{self.host.wss_port}/sub")
        auth_proto = BilibiliProto()
        auth_proto.body = json.dumps({
            "uid": 0,
            "roomid": self.room_info.room_id,
            "protover": 3,
            "platform": "web",
            "type": 2,
            "key": self.danmu_info.token
        })
        auth_proto.op = BilibiliProto.OP_AUTH
        await self.websocket.send(auth_proto.pack())
        await asyncio.wait([self._heart(), self._recv()])

    async def _heart(self):
        while True:
            await self.websocket.send(BilibiliProto().pack())
            await asyncio.sleep(30)

    async def _recv(self):
        while True:
            recv = await self.websocket.recv()
            try:
                packages = BilibiliProto.unpack(recv)
            except BilibiliProtoException as e:
                print(e)
                continue
            for package in packages:
                if package.cmd == "STOP_LIVE_ROOM_LIST":
                    # 直播结束时显示的推荐房间列表
                    continue
                elif package.cmd == "OP_AUTH_REPLY":
                    # wss连接鉴权通过
                    continue
                elif package.cmd == "OP_HEARTBEAT_REPLY":
                    # 收到心跳包
                    continue
                elif package.cmd == "ONLINE_RANK_V2":
                    # 高能榜数据
                    continue
                elif package.cmd == "ONLINE_RANK_COUNT":
                    # 高能榜数据更新
                    continue
                elif package.cmd == "LIVE_INTERACTIVE_GAME":
                    continue
                elif package.cmd == "DANMU_MSG":
                    # 收到弹幕
                    danmu = Danmu.load(package.data)
                    self.handler.onDanmu(danmu)
                elif package.cmd == "ENTRY_EFFECT":
                    # 进入特效(舰长进入直播间)
                    continue
                elif package.cmd == "INTERACT_WORD":
                    # 进入直播间
                    continue
                elif package.cmd == "WATCHED_CHANGE":
                    # 观看人数更新
                    continue
                elif package.cmd == "HOT_RANK_CHANGED":
                    # 主播实时活动排名
                    continue
                elif package.cmd == "HOT_RANK_CHANGED_V2":
                    # 主播实时活动排名
                    continue
                elif package.cmd == "SEND_GIFT":
                    # 发送礼物
                    gift = Gift.load(package.data)
                    self.handler.onGift(gift)
                    if gift.coin_type == "gold":
                        self.handler.onGoldGift(gift)
                    elif gift.coin_type == "silver":
                        self.handler.onSilverGift(gift)
                elif package.cmd == "ROOM_REAL_TIME_MESSAGE_UPDATE":
                    # 房间实时信息更新(粉丝数)
                    continue
                elif package.cmd == "WIDGET_BANNER":
                    continue
                elif package.cmd == "NOTICE_MSG":
                    # 直播间通知
                    continue
                elif package.cmd == "ROOM_BLOCK_MSG":
                    # 禁言
                    continue
                elif package.cmd == "PREPARING":
                    # 下播
                    continue
                elif package.cmd == "LIVE":
                    # 开播
                    continue
                elif package.cmd == "SUPER_CHAT_MESSAGE":
                    # 醒目留言
                    continue
                elif package.cmd == "SUPER_CHAT_MESSAGE_JPN":
                    # 日语醒目留言
                    continue
                elif package.cmd == "HOT_ROOM_NOTIFY":
                    continue
                elif package.cmd == "COMMON_NOTICE_DANMAKU":
                    continue
                else:
                    print(package)
                    