from dataclasses import dataclass
from time import time
from typing import Generic, TypeVar

from ..proto.proto import BilibiliLivePackage

EventData = TypeVar("EventData")


@dataclass
class Event(Generic[EventData]):
    package: BilibiliLivePackage
    data: EventData = None
    timestamp: int = int(time())


@dataclass
class FansMedal:
    name: str
    level: int


@dataclass
class User:
    uid: int
    uname: str
    uface: str = None
    fans_medal: FansMedal = None
    guard_level: int = None


@dataclass
class Danmu:
    # 用户名
    user: User
    msg: str


@dataclass
class Gift:
    user: User
    gift_id: int
    gift_name: str
    gift_num: int
    price: int
    coin_type: str


@dataclass
class SuperChat:
    user: User
    msg_id: int
    msg: str
    price: int
    time: int
    msg_jpn: str = ""
