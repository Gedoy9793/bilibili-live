import json

import requests

from bilibili_live.events.eventData import RoomInfo


def getRoomInfo(short_id: int):
    data = json.loads(
        requests.get(
            "https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom", params={"room_id": short_id}
        ).text
    )
    return RoomInfo(
        room_id=data.get("data").get("room_info").get("room_id"),
        short_id=short_id,
        title=data.get("data").get("room_info").get("title"),
        cover_image=data.get("data").get("room_info").get("cover"),
        area_id=data.get("data").get("room_info").get("area_id"),
        area_name=data.get("data").get("room_info").get("area_name"),
        parent_area_id=data.get("data").get("room_info").get("parent_area_id"),
        parent_area_name=data.get("data").get("room_info").get("parent_area_name"),
        live_status=data.get("data").get("room_info").get("live_status"),
        live_start_time=data.get("data").get("room_info").get("live_start_time"),
    )
