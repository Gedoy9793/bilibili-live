from events.eventData import Danmu, FansMedal, User


def convert(data):
    return Danmu(
        user=User(
            uname=data[2][1],
            uid=data[2][0],
            fans_medal=FansMedal(name=data[3][1], level=data[3][0]) if bool(data[3]) else None,
        ),
        timestamp=data[0][4] / 1000,
        msg=data[1],
    )
