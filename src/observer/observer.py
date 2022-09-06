import asyncio
import json
from threading import Thread

import websockets

from events.handler import BilibiliLiveEventHandler
from observer.packageProcess.packageProcessor import PackageProcessor
from proto.proto import BilibiliProto, BilibiliProtoException
from utils.danmuInfo import DanmuInfo
from utils.roomInfo import RoomInfo


class Observer:
    def schedule(self, handler, short_id):
        self.handler: BilibiliLiveEventHandler = handler

        self.room_info = RoomInfo(short_id)
        self.danmu_info = DanmuInfo(self.room_info.room_id)
        self.host = self.danmu_info.host_list[0]

        self.processor: PackageProcessor = PackageProcessor(self.handler, danmu_info=self.danmu_info)

    def start(self):
        self.main_task = None

        def live_thread():
            async def main():
                self.main_task = asyncio.create_task(self.start_asyncio())

            asyncio.run(main())

        self.thread = Thread(target=live_thread)
        self.thread.start()

    def stop(self):
        self.main_task.cancel()

    async def start_asyncio(self):
        self.websocket = await websockets.connect(f"wss://{self.host.host}:{self.host.wss_port}/sub")
        auth_proto = BilibiliProto()
        auth_proto.body = json.dumps(
            {
                "uid": 0,
                "roomid": self.room_info.room_id,
                "protover": 3,
                "platform": "web",
                "type": 2,
                "key": self.danmu_info.token,
            }
        )
        auth_proto.op = BilibiliProto.OP_AUTH
        await self.websocket.send(auth_proto.pack())
        await asyncio.wait([self._heart(), self._recv()], return_when=asyncio.FIRST_EXCEPTION)

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
