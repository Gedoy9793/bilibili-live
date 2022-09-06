from events.eventData import FansMedal, User


def convert(data):
    return User(
        uid=data.get("uid"),
        uname=data.get("uname"),
        fans_medal=FansMedal(
            name=data.get("fans_medal").get("medal_name"), level=data.get("fans_medal").get("medal_level")
        )
        if data.get("medal_info")
        else None,
        guard_level=0,
    )
