import io
import json

import qrcode
import requests

from ..events.eventData import QRCode


def generateLoginQRCode():
    data = requests.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-mini").text
    data = json.loads(data).get("data")

    code = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L)

    code.add_data(data.get("url"))

    stream = io.StringIO()

    code.print_ascii(stream)

    return QRCode(key=data.get("qrcode_key"), link=data.get("url"), code_string=stream.getvalue())
