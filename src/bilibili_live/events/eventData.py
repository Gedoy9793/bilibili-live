import json
from dataclasses import dataclass
from enum import IntEnum
from time import time
from types import TracebackType
from typing import Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from typing_extensions import TypeAlias

from ..proto.proto import BilibiliLivePackage

_EventData = TypeVar("_EventData")

_ExcInfo: TypeAlias = Tuple[Type[BaseException], BaseException, TracebackType]
OptExcInfo: TypeAlias = Union[_ExcInfo, Tuple[None, None, None]]


@dataclass
class Event(Generic[_EventData]):
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = int(time())

    package: BilibiliLivePackage
    data: _EventData = None
    timestamp: int = None


@dataclass
class FansMedal:
    name: str
    level: int
    target_live_id: int
    target_uid: int
    guard_level: int


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


@dataclass
class Room:
    title: str
    area_id: int
    area_name: str
    parent_area_id: int
    parent_area_name: str


@dataclass
class RoomInfo:
    room_id: int
    short_id: int
    room_owner_uid: int
    title: str
    cover_image: str  # 封面
    area_id: int
    area_name: str
    parent_area_id: int
    parent_area_name: str
    live_status: int  # 0:未开播 1:正在开播
    live_start_time: int  # 开播时间


@dataclass
class HostInfo:
    host: str
    port: int
    wss_port: int
    ws_port: int
    score: int = 100


@dataclass
class DanmuServerInfo:
    token: str
    host_list: List[HostInfo]


@dataclass
class LoginUser:
    uid: int
    uname: str
    uface: str
    cookies: Dict[str, str]

    @classmethod
    def loads(cls, s: str):
        data = json.loads(s)
        return cls(uid=data.get("uid"), uname=data.get("uname"), uface=data.get("uface"), cookies=data.get("cookies"))

    def dumps(self):
        return json.dumps(self)


@dataclass
class QRCode:
    key: str
    link: str
    code_string: str


@dataclass
class QRCodeStatus:
    class QRCodeStatusCodeEnum(IntEnum):
        OUT_OF_DATA = 86038
        WAITING = 86101
        SCANED = 86090
        CHECKED = 0

    code: int
    """
    86038: 已失效
    86101: 未扫码
    86090: 扫码未确认
    0: 已扫码
    """
    cookies: Optional[Dict[str, str]] = None
