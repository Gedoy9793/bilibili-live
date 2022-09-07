import json
from typing import Dict

import requests

from ..events.eventData import LoginUser


def getUserInfo(cookies: Dict[str, str]):
    res = requests.get("https://api.bilibili.com/x/web-interface/nav", cookies=cookies)

    data = json.loads(res.text).get("data")

    return LoginUser(uid=data.get("mid"), uname=data.get("uname"), uface=data.get("face"), cookies=cookies)
