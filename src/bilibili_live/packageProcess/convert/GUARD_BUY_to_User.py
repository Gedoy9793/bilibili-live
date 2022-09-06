from ...events.eventData import User


def convert(data):
    return User(
        uid=data.get("uid"),
        uname=data.get("username"),
        guard_level=3,
    ), data.get("start_time")
