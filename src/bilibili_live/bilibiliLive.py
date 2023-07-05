import asyncio
import json
import sys
import logging
from queue import Queue
from threading import Thread

import websockets

from . import api

from .events import Event
from .events.handler import BilibiliLiveEventHandler
from .packageProcess.exceptions import PackageConvertException
from .packageProcess.packageProcessor import PackageProcessor
from .proto.proto import BilibiliProto, BilibiliProtoException

_bilibiliLive = {}


logger = logging.getLogger("bilibili-live")


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
                    ptype, package = self.package_queue.get()
                    try:
                        if ptype == "package":
                            try:
                                self.handler.onPackage(Event(package=package))
                                self.processor.process(package)
                            except BilibiliProtoException:
                                self.package_queue.put(
                                    ("exception_with_package", Event(package=package, data=sys.exc_info())))
                        elif ptype == "exception_with_package":
                            self.handler.onUnpackException(package)
                        elif ptype == "heart":
                            self.handler.onHeart()
                    except Exception:
                        self.package_queue.put(("exception", sys.exc_info()))

                    try:
                        if ptype == "exception":
                            self.handler.onException(package)
                    except Exception as e:
                        logger.error(f"error when handle another error: {e}")

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
                self.host = api.getBestHost(self.danmu_info.host_list)
                logger.info(f"connecting to {self.host}")
                self.websocket = await websockets.connect(f"wss://{self.host.host}:{self.host.wss_port}/sub")
                await self._auth()
                self.connected.set()
                logger.info(f"connected to {self.host}")
            except ConnectionRefusedError:
                api.decuteHostScore(self.host)
                logger.error("connection refused, reconnecting")
                await asyncio.sleep(1)
            except Exception:
                self.package_queue.put(("exception", sys.exc_info()))

    async def _auth(self):
        auth_proto = BilibiliProto()
        auth_proto.body = json.dumps(
            {
                "uid": self.room_info.room_owner_uid or 0,
                "roomid": self.room_info.room_id,
                "protover": 3,
                "platform": "web",
                "type": 2,
                "key": self.danmu_info.token,
            }
        )
        auth_proto.op = BilibiliProto.OP_AUTH
        await self.websocket.send(auth_proto.pack())
        logger.info("send auth package")

    async def _heart(self):
        while True:
            try:
                await self.connected.wait()
                await self.websocket.send(BilibiliProto().pack())
                logger.info("send heart package")
                self.package_queue.put(("heart", None))
                await asyncio.sleep(self.heart_time)
            except websockets.exceptions.ConnectionClosedError:
                logger.error("connection closed at heart, reconnecting")
                api.decuteHostScore(self.host)
                await asyncio.sleep(1)
                self.connected.clear()
            except Exception:
                self.package_queue.put(("exception", sys.exc_info()))

    async def _recv(self):
        while True:
            try:
                await self.connected.wait()
                recv = await self.websocket.recv()
                packages = BilibiliProto.unpack(recv)
                for package in packages:
                    self.package_queue.put(("package", package))
            except websockets.exceptions.ConnectionClosedError:
                api.decuteHostScore(self.host)
                self.connected.clear()
                logger.error("connection closed at recv, reconnecting")
            except BilibiliProtoException:
                self.package_queue.put(("exception_with_package", Event(package, data=sys.exc_info())))
            except PackageConvertException:
                self.package_queue.put(("exception_with_package", Event(package, data=sys.exc_info())))
            except Exception:
                self.package_queue.put(("exception", sys.exc_info()))
