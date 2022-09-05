from dataclasses import dataclass

@dataclass
class BaseData:
    timestamp: int
    
    @classmethod
    def load(cls, data):
        ...

@dataclass
class User:
    uid: int
    uname: str
    uface: str

@dataclass
class FansMedal:
    name: str
    level: int

@dataclass
class Danmu(BaseData):
    # 用户名
    user: User
    msg: str
    guard_level: int
    fans_medal: FansMedal

    @classmethod
    def load(cls, data):
        return cls(
            user=User(
                uname=data[2][1],
                uid=data[2][0],
                uface=""
            ),
            timestamp=data[0][4] / 1000,
            msg=data[1],
            guard_level=0,
            fans_medal=FansMedal(
                name=data[3][1],
                level=data[3][0]
            ) if bool(data[3]) else None
        )

@dataclass
class Gift(BaseData):
    user: User
    fans_medal: FansMedal
    gift_id: int
    gift_name: str
    gift_num: int
    price: int
    coin_type: str
    guard_level: int

    @classmethod
    def load(cls, data):
        return cls(
            timestamp=data.get('timestamp'),
            user=User(
                uid=data.get('uid'),
                uname=data.get('uname'),
                uface=data.get('face')
            ),
            fans_medal=FansMedal(
                name=data.get('medal_info').get('medal_name'),
                level=data.get('medal_info').get('medal_level')
            ),
            gift_id=data.get('giftId'),
            gift_name=data.get('giftName'),
            gift_num=data.get('num'),
            price=data.get('price'),
            coin_type=data.get('coin_type'),
            guard_level=data.get('guard_level')
        )