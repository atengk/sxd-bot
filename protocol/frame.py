"""神仙道二进制网络传输协议分帧器与粘包解包状态机

管理 TCP 流式字节流缓存，依据 4 字节大端长度前缀与 RFC 1950 zlib 头部魔数切分逻辑封包，具备坏帧滑动自愈容错能力。

@author Ateng
@since 2026-10-15
"""

import logging
import struct
import zlib
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

# RFC 1950 zlib 头部常见签名 (0x78 0x9c, 0x78 0x01, 0x78 0xda, 0x78 0x5e)
ZLIB_MAGIC_PREFIX = b"\x78"
ZLIB_SECOND_BYTES = {0x01, 0x5E, 0x9C, 0xDA}


class FrameFSM:
    """基于滑动窗口的 TCP 二进制分帧状态机

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, max_buffer_size: int = 10 * 1024 * 1024) -> None:
        """初始化滑动窗口状态机

        Args:
            max_buffer_size: 内部字节流缓存上限，防止内存泄露。
        """
        self._buffer = bytearray()
        self._max_buffer_size = max_buffer_size

    def feed(self, data: bytes) -> None:
        """向状态机推入新收到的 TCP 原始字节碎片

        Args:
            data: 套接字接收到的原始字节数组。
        """
        if not data:
            return
        self._buffer.extend(data)
        if len(self._buffer) > self._max_buffer_size:
            logger.warning("分帧缓冲区超出限制 %d 字节，执行强制截断", self._max_buffer_size)
            del self._buffer[:-self._max_buffer_size]

    def extract_frames(self) -> List[Tuple[bytes, bool]]:
        """从当前缓冲区中尝试提取出所有已就绪的逻辑封包

        Returns:
            元组列表，每项为 (解压后的有效载荷 payload_bytes, 是否经过 zlib 压缩 is_compressed)。
        """
        frames: List[Tuple[bytes, bool]] = []

        while len(self._buffer) >= 4:
            payload_len = struct.unpack(">I", self._buffer[:4])[0]

            # 1. 过滤 0 长度心跳或空载荷
            if payload_len == 0:
                del self._buffer[:4]
                continue

            # 2. 检查是否为异常超长包 (单包上限设置为 2MB 防御)
            if payload_len > 2 * 1024 * 1024:
                logger.warning("检测到异常超大帧声明: %d 字节，触发前向滑动对齐", payload_len)
                del self._buffer[:1]
                continue

            # 3. 半包检查：等待剩余字节完全到达
            total_frame_len = 4 + payload_len
            if len(self._buffer) < total_frame_len:
                break

            # 4. 提取完整单帧载荷
            raw_payload = bytes(self._buffer[4:total_frame_len])
            del self._buffer[:total_frame_len]

            # 5. 校验并解压 zlib 载荷
            is_zlib = (
                len(raw_payload) >= 2
                and raw_payload[0:1] == ZLIB_MAGIC_PREFIX
                and raw_payload[1] in ZLIB_SECOND_BYTES
            )

            if is_zlib:
                try:
                    decompressed = zlib.decompress(raw_payload)
                    frames.append((decompressed, True))
                except Exception as exc:
                    logger.error("zlib 载荷解压失败，丢弃该异常帧: %s", exc)
            else:
                frames.append((raw_payload, False))

        return frames

    @property
    def buffer_size(self) -> int:
        """获取当前未消费的挂起字节数"""
        return len(self._buffer)

    def clear(self) -> None:
        """清空内部缓冲区状态"""
        self._buffer.clear()
