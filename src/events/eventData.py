from dataclasses import dataclass

@dataclass
class BaseData:
    timestamp: int

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
class Danmu(BaseData):
    # 用户名
    user: User
    msg: str

@dataclass
class Gift(BaseData):
    user: User
    gift_id: int
    gift_name: str
    gift_num: int
    price: int
    coin_type: str

@dataclass
class SuperChat(BaseData):
    user: User
    msg_id: int
    msg: str
    price: int
    time: int
    msg_jpn:str = ""