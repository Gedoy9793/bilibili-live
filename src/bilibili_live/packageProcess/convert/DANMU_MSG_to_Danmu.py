from typing import Tuple

from ...events.eventData import Danmu, FansMedal, User


def convert(data) -> Tuple[User, int]:
    return Danmu(
        user=User(
            uname=data[2][1],
            uid=data[2][0],
            fans_medal=FansMedal(
                name=data[3][1], 
                level=data[3][0], 
                target_uid=data[3][3], 
                guard_level=data[3][10]
            ) if bool(data[3]) else None
        ),
        msg=data[1],
    ), int(data[0][4] / 1000)
