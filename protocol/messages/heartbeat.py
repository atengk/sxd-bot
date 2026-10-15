"""神仙道心跳保活数据契约 (Mod 184, Act 4)

用于维持与远端网关的活性对齐，防止因长期无交互被断开连接。

@author Ateng
@since 2026-10-15
"""

from dataclasses import dataclass
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


@dataclass
class HeartbeatPkt(BasePacket):
    """心跳对齐封包 (Mod 184, Act 4)

    @author Ateng
    @since 2026-10-15
    """

    seq: int = 0

    def __init__(self, seq: int = 0) -> None:
        super().__init__(mod=184, act=4)
        self.seq = seq

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.seq)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "HeartbeatPkt":
        reader = ByteArrayReader(data)
        seq = reader.read_uint8() if reader.remaining >= 1 else 0
        return cls(seq=seq)
