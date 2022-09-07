import json

import requests

from bilibili_live.events.eventData import QRCodeStatus


def pullScanCodeStatus(qrcode_key: str):
    res = requests.get(
        "https://passport.bilibili.com/x/passport-login/web/qrcode/poll",
        params={"qrcode_key": qrcode_key, "source": "main_mini"},
    )

    data = json.loads(res.text).get("data")
    code = data.get("code")

    if code == QRCodeStatus.QRCodeStatusCodeEnum.CHECKED:
        return QRCodeStatus(code=code, cookies=res.cookies.get_dict())
    else:
        return QRCodeStatus(code=code)
