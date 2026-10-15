"""神仙道动态流式封包构造器

用于快速拼装与原型验证任意模块与动作的二进制指令，支持链式调用与类型化输出。

@author Ateng
@since 2026-10-15
"""

import struct
from typing import Optional
from protocol.packet import ByteArrayWriter, BasePacket


class DynamicPacket(BasePacket):
    """基于动态字节载荷的通用数据包

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, mod: int, act: int, payload: bytes) -> None:
        super().__init__(mod, act)
        self.payload = payload

    def encode_payload(self) -> bytes:
        return self.payload


class PacketBuilder:
    """流式封包构造器

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, mod: int, act: int) -> None:
        """初始化构造器

        Args:
            mod: 模块 ID。
            act: 动作 ID。
        """
        self.mod = mod
        self.act = act
        self._writer = ByteArrayWriter()

    def write_int8(self, value: int) -> "PacketBuilder":
        self._writer.write_int8(value)
        return self

    def write_uint8(self, value: int) -> "PacketBuilder":
        self._writer.write_uint8(value)
        return self

    def write_int16(self, value: int) -> "PacketBuilder":
        self._writer.write_int16(value)
        return self

    def write_uint16(self, value: int) -> "PacketBuilder":
        self._writer.write_uint16(value)
        return self

    def write_int32(self, value: int) -> "PacketBuilder":
        self._writer.write_int32(value)
        return self

    def write_uint32(self, value: int) -> "PacketBuilder":
        self._writer.write_uint32(value)
        return self

    def write_int64(self, value: int) -> "PacketBuilder":
        self._writer.write_int64(value)
        return self

    def write_utf(self, value: str) -> "PacketBuilder":
        self._writer.write_utf(value)
        return self

    def write_bytes(self, value: bytes) -> "PacketBuilder":
        self._writer.write_bytes(value)
        return self

    def build(self) -> DynamicPacket:
        """完成组装并生成 DynamicPacket 实例"""
        return DynamicPacket(self.mod, self.act, self._writer.to_bytes())

    def to_network_frame(self) -> bytes:
        """直接生成可向套接字发送的完整网络传输帧"""
        return self.build().to_network_frame()
