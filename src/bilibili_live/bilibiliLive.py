import asyncio
import json
from threading import Thread

import websockets

from bilibili_live import api

from .events import Event
from .events.handler import BilibiliLiveEventHandler
from .packageProcess.exceptions import PackageConvertException
from .packageProcess.packageProcessor import PackageProcessor
from .proto.proto import BilibiliProto, BilibiliProtoException

_bilibiliLive = {}

class BilibiliLive:
    connected: asyncio.Event
    loop: asyncio.AbstractEventLoop
    main_task: asyncio.Task

    def __new__(cls, name='defaule'):
        if name in _bilibiliLive:
            return _bilibiliLive[name]
        else:
            obj = object.__new__(cls)
            _bilibiliLive[name] = obj
            return obj

    def __init__(self):
        def live_thread():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            async def main():
                self.connected = asyncio.Event(loop=self.loop)
                self.main_task = asyncio.create_task(self._start())
                await self.main_task

            self.loop.run_until_complete(main())
            if self.main_task._exception is not None:
                self.handler.onException(self.main_task._exception)
                raise self.main_task._exception

        self.thread = Thread(target=live_thread)
        self.thread.setDaemon(True)

    def schedule(self, handler, short_id):
        self.handler: BilibiliLiveEventHandler = handler(self)
        self.processor: PackageProcessor = PackageProcessor(self.handler)

        self.room_info = api.getRoomInfo(short_id)
        self.danmu_info = api.getDanmuServerInfo(self.room_info.room_id)
        self.host = self.danmu_info.host_list[0]

    def start(self):
        self.thread.start()
        return self.thread

    def stop(self):
        self.main_task.cancel()

    async def _start(self):
        await self._connect()
        await asyncio.wait([self._heart(), self._recv()])

    async def _connect(self):
        while True:
            try:
                self.websocket = await websockets.connect(f"wss://{self.host.host}:{self.host.wss_port}/sub")
                await self._auth()
                self.connected.set()
                return
            except ConnectionRefusedError:
                await asyncio.sleep(1)

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
                await self.connected.wait()
                recv = await self.websocket.recv()
                packages = BilibiliProto.unpack(recv)
                for package in packages:
                    self.handler.onPackage(package)
                    self.processor.process(package)
            except websockets.exceptions.ConnectionClosedError:
                self.connected.clear()
                await self._connect()
            except BilibiliProtoException as e:
                self.handler.onException(e)
                self.handler.onUnpackExceprion(Event(package, data=e))
            except PackageConvertException as e:
                self.handler.onUnpackExceprion(Event(package, data=e))
            except Exception as e:
                self.handler.onException(e)
                ...
