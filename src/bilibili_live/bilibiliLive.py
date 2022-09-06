import asyncio
import json
from threading import Thread

import websockets

from .events import Event
from .events.handler import BilibiliLiveEventHandler
from .packageProcess.exceptions import PackageConvertException
from .packageProcess.packageProcessor import PackageProcessor
from .proto.proto import BilibiliProto, BilibiliProtoException
from .utils.danmuInfo import DanmuInfo
from .utils.roomInfo import RoomInfo


class BilibiliLive:
    def schedule(self, handler, short_id):
        self.handler: BilibiliLiveEventHandler = handler(self)
        self.processor: PackageProcessor = PackageProcessor(self.handler)

        self.room_info = RoomInfo(short_id)
        self.danmu_info = DanmuInfo(self.room_info.room_id)
        self.host = self.danmu_info.host_list[0]

    def start(self):
        self.main_task: asyncio.Task = None

        def live_thread():
            async def main():
                self.main_task = asyncio.create_task(self.connect())
                await self.main_task

            asyncio.run(main())
            if self.main_task._exception is not None:
                self.handler.onException(self.main_task._exception)

        self.thread = Thread(target=live_thread)
        self.thread.setDaemon(True)
        self.thread.start()
        return self.thread

    def stop(self):
        self.main_task.cancel()

    async def connect(self):
        self.websocket = await websockets.connect(f"wss://{self.host.host}:{self.host.wss_port}/sub")
        await self._auth()
        await asyncio.wait([self._heart(), self._recv()])

    async def _auth(self):
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

    async def _heart(self):
        while True:
            try:
                await self.websocket.send(BilibiliProto().pack())
                await asyncio.sleep(30)
            except Exception as e:
                self.handler.onException(e)

    async def _recv(self):
        while True:
            try:
                recv = await self.websocket.recv()
                packages = BilibiliProto.unpack(recv)
                for package in packages:
                    self.handler.onPackage(package)
                    self.processor.process(package)
            except BilibiliProtoException as e:
                self.handler.onException(e)
                self.handler.onUnpackExceprion(Event(package, data=e))
            except PackageConvertException as e:
                self.handler.onUnpackExceprion(Event(package, data=e))
            except Exception as e:
                self.handler.onException(e)
                ...
