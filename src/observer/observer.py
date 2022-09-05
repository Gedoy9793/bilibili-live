import asyncio
import json
from observer.packageProcess.packageProcessor import PackageProcessor
import websockets

from events.handler import BilibiliLiveEventHandler
from proto.proto import BilibiliProto, BilibiliProtoException
from utils.danmuInfo import DanmuInfo
from utils.roomInfo import RoomInfo

class Observer:
    def schedule(self, handler, short_id):
        self.handler: BilibiliLiveEventHandler = handler
        self.processor: PackageProcessor = PackageProcessor(self.handler)

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
                self.handler.onUnpackExceprion(e)
                continue
            for package in packages:
                self.processor.process(package)