"""Flash ByteArray 范式二进制序列化读写器与基础数据包抽象

封装大端字节序读写、writeUTF/readUTF 字符串契约与基础封包模型。

@author Ateng
@since 2026-10-15
"""

import json
import struct
from typing import Any, Optional


class ByteArrayReader:
    """Flash 规范大端序二进制流式读取器

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, data: bytes) -> None:
        """初始化读取器

        Args:
            data: 待解析的二进制载荷字节。
        """
        self._data = data
        self._offset = 0

    @property
    def remaining(self) -> int:
        """剩余可读字节数"""
        return max(0, len(self._data) - self._offset)

    def read_int8(self) -> int:
        """读取单字节带符号整数"""
        self._check_bounds(1)
        val = struct.unpack(">b", self._data[self._offset : self._offset + 1])[0]
        self._offset += 1
        return val

    def read_uint8(self) -> int:
        """读取单字节无符号整数"""
        self._check_bounds(1)
        val = struct.unpack(">B", self._data[self._offset : self._offset + 1])[0]
        self._offset += 1
        return val

    def read_int16(self) -> int:
        """读取 16 位大端带符号整数"""
        self._check_bounds(2)
        val = struct.unpack(">h", self._data[self._offset : self._offset + 2])[0]
        self._offset += 2
        return val

    def read_uint16(self) -> int:
        """读取 16 位大端无符号整数"""
        self._check_bounds(2)
        val = struct.unpack(">H", self._data[self._offset : self._offset + 2])[0]
        self._offset += 2
        return val

    def read_int32(self) -> int:
        """读取 32 位大端带符号整数"""
        self._check_bounds(4)
        val = struct.unpack(">i", self._data[self._offset : self._offset + 4])[0]
        self._offset += 4
        return val

    def read_uint32(self) -> int:
        """读取 32 位大端无符号整数"""
        self._check_bounds(4)
        val = struct.unpack(">I", self._data[self._offset : self._offset + 4])[0]
        self._offset += 4
        return val

    def read_int64(self) -> int:
        """读取 64 位大端带符号长整数"""
        self._check_bounds(8)
        val = struct.unpack(">q", self._data[self._offset : self._offset + 8])[0]
        self._offset += 8
        return val

    def read_bool(self) -> bool:
        """读取单字节布尔值 (BooleanUtil)"""
        return self.read_uint8() != 0

    def read_float(self) -> float:
        """读取 32 位大端 IEEE 754 浮点数 (FloatUtil)"""
        self._check_bounds(4)
        val = struct.unpack(">f", self._data[self._offset : self._offset + 4])[0]
        self._offset += 4
        return val

    def read_double(self) -> float:
        """读取 64 位大端 IEEE 754 双精度浮点数 (DoubleUtil)"""
        self._check_bounds(8)
        val = struct.unpack(">d", self._data[self._offset : self._offset + 8])[0]
        self._offset += 8
        return val

    def read_utf(self) -> str:
        """读取 Flash 标准 writeUTF 格式字符串 (16位大端长度 + UTF-8 字节)

        Returns:
            解码后的字符串。
        """
        length = self.read_uint16()
        if length == 0:
            return ""
        self._check_bounds(length)
        raw_bytes = self._data[self._offset : self._offset + length]
        self._offset += length
        return raw_bytes.decode("utf-8", errors="replace")

    def read_json(self) -> Any:
        """读取 writeUTF 编码的 JSON 结构并自动反序列化 (JSONUtil)"""
        text = self.read_utf()
        if not text:
            return None
        return json.loads(text)

    def read_bytes(self, length: Optional[int] = None) -> bytes:
        """读取指定长度的原始字节序列 (若未指定则读至末尾)"""
        if length is None:
            length = self.remaining
        self._check_bounds(length)
        chunk = self._data[self._offset : self._offset + length]
        self._offset += length
        return chunk

    def _check_bounds(self, size: int) -> None:
        """边界校验"""
        if self._offset + size > len(self._data):
            raise IndexError(
                f"二进制读取越界: 需读取 {size} 字节，剩余可用 {self.remaining} 字节 (总长 {len(self._data)})"
            )


class ByteArrayWriter:
    """Flash 规范大端序二进制流式写入器

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self) -> None:
        """初始化写入器"""
        self._buffer = bytearray()

    def write_int8(self, value: int) -> "ByteArrayWriter":
        """写入单字节带符号整数"""
        self._buffer.extend(struct.pack(">b", value))
        return self

    def write_uint8(self, value: int) -> "ByteArrayWriter":
        """写入单字节无符号整数"""
        self._buffer.extend(struct.pack(">B", value))
        return self

    def write_int16(self, value: int) -> "ByteArrayWriter":
        """写入 16 位大端带符号整数"""
        self._buffer.extend(struct.pack(">h", value))
        return self

    def write_uint16(self, value: int) -> "ByteArrayWriter":
        """写入 16 位大端无符号整数"""
        self._buffer.extend(struct.pack(">H", value))
        return self

    def write_int32(self, value: int) -> "ByteArrayWriter":
        """写入 32 位大端带符号整数"""
        self._buffer.extend(struct.pack(">i", value))
        return self

    def write_uint32(self, value: int) -> "ByteArrayWriter":
        """写入 32 位大端无符号整数"""
        self._buffer.extend(struct.pack(">I", value))
        return self

    def write_int64(self, value: int) -> "ByteArrayWriter":
        """写入 64 位大端带符号长整数"""
        self._buffer.extend(struct.pack(">q", value))
        return self

    def write_bool(self, value: bool) -> "ByteArrayWriter":
        """写入单字节布尔值 (BooleanUtil)"""
        self._buffer.append(1 if value else 0)
        return self

    def write_float(self, value: float) -> "ByteArrayWriter":
        """写入 32 位大端 IEEE 754 浮点数 (FloatUtil)"""
        self._buffer.extend(struct.pack(">f", value))
        return self

    def write_double(self, value: float) -> "ByteArrayWriter":
        """写入 64 位大端 IEEE 754 双精度浮点数 (DoubleUtil)"""
        self._buffer.extend(struct.pack(">d", value))
        return self

    def write_utf(self, value: str) -> "ByteArrayWriter":
        """写入 Flash 标准 writeUTF 格式字符串 (16位大端长度 + UTF-8 字节)"""
        raw_bytes = value.encode("utf-8")
        if len(raw_bytes) > 0xFFFF:
            raise ValueError(f"字符串超出 Flash writeUTF 最大限制 (65535 字节): {len(raw_bytes)}")
        self.write_uint16(len(raw_bytes))
        self._buffer.extend(raw_bytes)
        return self

    def write_json(self, value: Any) -> "ByteArrayWriter":
        """将结构序列化为 JSON 字符串并通过 writeUTF 写入 (JSONUtil)"""
        text = json.dumps(value, ensure_ascii=False)
        return self.write_utf(text)

    def write_bytes(self, value: bytes) -> "ByteArrayWriter":
        """追加原始二进制切片"""
        self._buffer.extend(value)
        return self

    def to_bytes(self) -> bytes:
        """获取当前写入的全部原始字节"""
        return bytes(self._buffer)


class BasePacket:
    """神仙道业务协议基础封包模型

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, mod: int, act: int) -> None:
        """初始化基础协议头

        Args:
            mod: 模块编号 (uint16)。
            act: 动作编号 (uint16)。
        """
        self.mod = mod
        self.act = act

    def encode_payload(self) -> bytes:
        """编码业务载荷数据 (子类覆盖实现)"""
        return b""

    def to_network_frame(self) -> bytes:
        """将完整数据包打包为包含 4 字节长度头的网络传输帧

        Returns:
            [4 字节总长] + [2 字节 Mod] + [2 字节 Act] + [业务载荷]
        """
        payload = self.encode_payload()
        total_body = struct.pack(">HH", self.mod, self.act) + payload
        length_prefix = struct.pack(">I", len(total_body))
        return length_prefix + total_body
