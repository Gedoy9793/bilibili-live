import json
from typing import List

import requests

from bilibili_live.events.eventData import DanmuServerInfo, HostInfo


def getDanmuServerInfo(room_id: int):
    data = json.loads(
        requests.get(
            "https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo", params={"id": room_id, "type": 0}
        ).text
    )

    host_list = []
    for host in data.get("data").get("host_list"):
        host_list.append(HostInfo(**host))

    return DanmuServerInfo(token=data.get("data").get("token"), host_list=host_list)


def getBestHost(host_list: List[HostInfo]):
    return sorted(host_list, key=lambda host: host.score, reverse=True)[0]


def decuteHostScore(host: HostInfo):
    host.score -= 1
