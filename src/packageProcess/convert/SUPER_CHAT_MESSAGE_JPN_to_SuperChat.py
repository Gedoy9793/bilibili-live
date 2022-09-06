from events.eventData import FansMedal, SuperChat, User


def convert(data):
    return SuperChat(
        user=User(
            uid=data.get("uid"),
            uname=data.get("user_info").get("uname"),
            uface=data.get("user_info").get("face"),
            fans_medal=FansMedal(
                name=data.get("medal_info").get("medal_name"), level=data.get("medal_info").get("medal_level")
            )
            if data.get("medal_info")
            else None,
            guard_level=data.get("user_info").get("guard_level"),
        ),
        timestamp=data.get("start_time"),
        msg_id=data.get("id"),
        msg=data.get("message"),
        price=data.get("price"),
        time=data.get("time"),
        msg_jpn=data.get("message_jpn"),
    )
