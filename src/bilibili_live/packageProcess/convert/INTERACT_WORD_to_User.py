from ...events.eventData import FansMedal, User


def convert(data):
    return User(
        uid=data.get("uid"),
        uname=data.get("uname"),
        fans_medal=FansMedal(
            name=data.get("fans_medal").get("medal_name"), 
            level=data.get("fans_medal").get("medal_level"),
            target_uid=data.get("fans_medal").get("target_id"),
            guard_level=data.get("fans_medal").get("guard_level")
        )
        if data.get("medal_info")
        else None,

        guard_level=0
        if data.get("msg_type") == 1
        else None,
    ), data.get("timestamp")
