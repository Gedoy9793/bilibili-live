import json
import requests


class RoomInfo:
    def __init__(self, short_id):
        data = json.loads(requests.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom", params={"room_id": short_id}).text)
        self.room_id = data.get('data').get('room_info').get('room_id')