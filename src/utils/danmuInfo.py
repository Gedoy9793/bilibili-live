from dataclasses import dataclass
import json
from typing import List
import requests


class DanmuInfo:
    def __init__(self, room_id):
        data = json.loads(requests.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo", params={"id": room_id, "type": 0}).text)
        self.token = data.get('data').get('token')
        self.host_list: List[HostInfo] = []
        for host in data.get('data').get('host_list'):
            self.host_list.append(HostInfo(**host))

@dataclass
class HostInfo:
    host: str
    port: int
    wss_port: int
    ws_port: int