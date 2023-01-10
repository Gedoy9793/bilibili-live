import asyncio
import json
from queue import Queue
from threading import Thread

import websockets

from bilibili_live import api

from .events import Event
from .events.handler import BilibiliLiveEventHandler
from .packageProcess.exceptions import PackageConvertException
from .packageProcess.packageProcessor import PackageProcessor
from .proto.proto import BilibiliLivePackage, BilibiliProto, BilibiliProtoException

_bilibiliLive = {}


class BilibiliLive:
    connected: asyncio.Event
    stop_sig: asyncio.Event

    package_queue: Queue

    def __new__(cls, name="defaule"):
        if name in _bilibiliLive:
            return _bilibiliLive[name]
        else:
            obj = object.__new__(cls)
            _bilibiliLive[name] = obj
            return obj

    def __init__(self):
        def live_thread_run():
            def handle_thread_run():
                while True:
                    package = self.package_queue.get()
                    try:
                        if isinstance(package, BilibiliLivePackage):
                            try:
                                self.handler.onPackage(Event(package=package))
                                self.processor.process(package)
                            except BilibiliProtoException as e:
                                self.package_queue.put(Event(package=package, data=e))
                            except Exception as e:
                                self.package_queue.put(e)
                        elif isinstance(package, Event):
                            self.handler.onUnpackException(package)
                        elif package == "heart":
                            self.handler.onHeart()
                    except Exception as e:
                        self.package_queue.put(e)

                    try:
                        if isinstance(package, Exception):
                            self.handler.onException(package)
                    except Exception:
                        ...

            handle_thread = Thread(target=handle_thread_run)
            handle_thread.setDaemon(True)

            self.loop = asyncio.new_event_loop()
            self.connected = asyncio.Event(loop=self.loop)
            self.stop_sig = asyncio.Event(loop=self.loop)
            self.package_queue = Queue()

            handle_thread.start()
            self.loop.run_until_complete(self._start())

        self.live_thread = Thread(target=live_thread_run)
        self.live_thread.setDaemon(True)

    def schedule(self, handler, short_id, heart_time=30):
        self.handler: BilibiliLiveEventHandler = handler(self)
        self.processor: PackageProcessor = PackageProcessor(self.handler)

        self.room_info = api.getRoomInfo(short_id)
        self.danmu_info = api.getDanmuServerInfo(self.room_info.room_id)
        self.host = self.danmu_info.host_list[0]

        self.heart_time = heart_time

    def start(self):
        self.live_thread.start()
        return self.live_thread

    def stop(self):
        self.stop_sig.set()

    async def _check_stop(self):
        await self.stop_sig.wait()

    async def _start(self):
        await asyncio.wait(
            [self._connect(), self._heart(), self._recv(), self._check_stop()], return_when=asyncio.FIRST_COMPLETED
        )

    async def _connect(self):
        while True:
            if self.connected.is_set():
                await asyncio.sleep(1)
                continue
            try:
                self.websocket = await websockets.connect(f"wss://{self.host.host}:{self.host.wss_port}/sub")
                await self._auth()
                self.connected.set()
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
                await self.connected.wait()
                await self.websocket.send(BilibiliProto().pack())
                self.package_queue.put("heart")
                await asyncio.sleep(self.heart_time)
            except websockets.exceptions.ConnectionClosedError as e:
                self.package_queue.put(e)
                await asyncio.sleep(1)
                self.connected.clear()
            except Exception as e:
                self.package_queue.put(e)

    async def _recv(self):
        while True:
            try:
                await self.connected.wait()
                recv = await self.websocket.recv()
                packages = BilibiliProto.unpack(recv)
                for package in packages:
                    self.package_queue.put(package)
            except websockets.exceptions.ConnectionClosedError as e:
                self.package_queue.put(e)
                self.connected.clear()
            except BilibiliProtoException as e:
                self.package_queue.put(Event(package, data=e))
            except PackageConvertException as e:
                self.package_queue.put(Event(package, data=e))
            except Exception as e:
                self.package_queue.put(e)
                ...
