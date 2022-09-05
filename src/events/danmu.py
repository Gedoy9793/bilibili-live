
from dataclasses import dataclass


@dataclass
class Danmu:
    # 用户名
    uname: str
    uid: int
    uface: str
    timestamp: int
    room_id: int
    msg: str
    msg_id: str
    guard_level: int
    fans_medal_wearing_status: bool
    fans_medal_name: str
    fans_medal_level: int