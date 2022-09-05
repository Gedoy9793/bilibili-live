from dataclasses import dataclass
import json
import struct
from typing import List
import zlib
import brotli

class BilibiliProtoException(Exception):
    ...

@dataclass
class BilibiliPackage:
    cmd: str
    data: dict = None


class BilibiliProto:
    OP_HEARTBEAT = 2
    OP_AUTH = 7

    def __init__(self):
        self.packetLen = 0
        self.headerLen = 16
        self.ver = 1
        self.op = self.OP_HEARTBEAT
        self.seq = 1
        self.body = ''
        self.maxBody = 4096
 
    def pack(self):
        self.packetLen = len(self.body) + self.headerLen
        buf = struct.pack('>i', self.packetLen)
        buf += struct.pack('>h', self.headerLen)
        buf += struct.pack('>h', self.ver)
        buf += struct.pack('>i', self.op)
        buf += struct.pack('>i', self.seq)
        buf += self.body.encode()
        return buf
 
    @classmethod
    def unpack(cls, buf):
        unpacked: List[BilibiliPackage] = []
        cls()._unpack(buf, unpacked)
        return unpacked

    def _unpack(self, buf, unpacked):
        if len(buf) < self.headerLen:
            raise BilibiliProtoException("包头不够")
        self.packetLen = struct.unpack('>i', buf[0:4])[0]
        self.headerLen = struct.unpack('>h', buf[4:6])[0]
        self.ver = struct.unpack('>h', buf[6:8])[0]
        self.op = struct.unpack('>i', buf[8:12])[0]
        self.seq = struct.unpack('>i', buf[12:16])[0]
        if self.packetLen < 0 or self.packetLen > self.maxBody:
            raise BilibiliProtoException("包体长不对", "self.packetLen:", self.packetLen,
                  " self.maxBody:", self.maxBody)
        bodyLen = self.packetLen - self.headerLen
        if bodyLen <= 0:
            return
        self.body = buf[16:self.packetLen]
        if self.ver == 0:
            # 获取到实际数据
            pkg = json.loads(self.body.decode('utf-8'))
            cmd = pkg.get('cmd', 'UNKNOWN')
            if cmd == 'DANMU_MSG':
                data = pkg.get('info')
            elif pkg.get('data'):
                data = pkg.get('data')
            else:
                data = pkg

            unpacked.append(BilibiliPackage(cmd, data))
        elif self.ver == 1:
            # 心跳包回复
            if self.op == 3:
                unpacked.append(BilibiliPackage("OP_HEARTBEAT_REPLY"))
            elif self.op == 8:
                unpacked.append(BilibiliPackage("OP_AUTH_REPLY"))

        elif self.ver == 2 or self.ver == 3:
            if self.ver == 2:
                # zlib解压
                self.body = zlib.decompress(self.body)
            elif self.ver == 3:
                # brotli解压
                self.body = brotli.decompress(self.body)
            bodyLen = len(self.body)
            offset = 0
            while offset < bodyLen:
                cmdSize = struct.unpack('>i', self.body[offset:offset+4])[0]
                if offset + cmdSize > bodyLen:
                    return
                newProto = BilibiliProto()
                newProto._unpack(self.body[offset: offset+cmdSize], unpacked)
                offset += cmdSize
        else:
            return