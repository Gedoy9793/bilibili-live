from ...events.eventData import FansMedal, Gift, User


def convert(data):
    return Gift(
        user=User(
            uid=data.get("uid"),
            uname=data.get("uname"),
            uface=data.get("face"),
            fans_medal=FansMedal(
                name=data.get("medal_info").get("medal_name"), 
                level=data.get("medal_info").get("medal_level"),
                target_uid=data.get("medal_info").get("target_id"),
                target_live_id=data.get("medal_info").get("anchor_roomid"),
                guard_level=data.get("medal_info").get("guard_level")
            )
            if data.get("medal_info")
            else None,
            guard_level=data.get("guard_level"),
        ),
        gift_id=data.get("giftId"),
        gift_name=data.get("giftName"),
        gift_num=data.get("num"),
        price=data.get("price"),
        coin_type=data.get("coin_type"),
    ), data.get("timestamp")
