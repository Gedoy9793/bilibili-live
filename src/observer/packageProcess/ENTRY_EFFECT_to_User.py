import re
from events.eventData import User
from .exceptions import PackageConvertException


def convert(data):
    try:
        matched = re.match(r'欢迎(舰长|提督|总督) <%(.*)%> 进入直播间', data.get('copy_writing')).groups()
    except AttributeError:
        raise PackageConvertException()
    if matched[0] == "舰长":
        guard_level = 1
    elif matched[1] == "提督":
        guard_level = 2
    elif matched[1] == "总督":
        guard_level = 3
    else:
        raise PackageConvertException()
    return User(
        uid=data.get('uid'),
        uface=data.get('face'),
        uname=matched[1],
        guard_level=guard_level
    )