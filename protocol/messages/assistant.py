"""神仙道小助手与每日活跃度模块数据契约 (Mod 52: Mod_Assistant_Base)

定义小助手日常矩阵查询、活跃度宝箱阶段状态与反序列化强类型契约模型。
严格落实 [SAFE_READ] 只读安全红线。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


class AssistantConstants:
    """Mod_Assistant_Base 官方业务常量"""

    SUCCESS = 0             # 成功 / 宝箱可领取
    NOT_ENOUGH_VIP = 1      # VIP等级不足
    NOT_ENOUGH_NUM = 2      # 活跃度未达标
    PACK_FULL = 3           # 背包已满
    HAVE_DONE = 4           # 已领取
    FAILED = 5              # 领取失败
    FISHHOOK_LIMIT = 6      # 鱼钩上限
    FIND_IMMORTAL_LIMIT = 7 # 寻仙上限


@dataclass
class AssistantDailyRawItem:
    """单项日常条目底层数据结构

    @author Ateng
    @since 2026-10-16
    """

    item_id: int = 0
    completed_count: int = 0
    quota_list: List[int] = field(default_factory=list)


@dataclass
class AssistantLivenessRawBox:
    """活跃度宝箱阶段底层数据结构

    @author Ateng
    @since 2026-10-16
    """

    box_id: int = 0
    required_liveness: int = 0
    status: int = 0


@dataclass
class AssistantInfoReq(BasePacket):
    """查询小助手日常面板全量信息请求 (Mod 52, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=52, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "AssistantInfoReq":
        return cls()


@dataclass
class AssistantInfoResp(BasePacket):
    """小助手日常面板全量信息响应 (Mod 52, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    items: List[AssistantDailyRawItem] = field(default_factory=list)
    boxes: List[AssistantLivenessRawBox] = field(default_factory=list)
    raw_payload: bytes = b""

    def __init__(
        self,
        items: Optional[List[AssistantDailyRawItem]] = None,
        boxes: Optional[List[AssistantLivenessRawBox]] = None,
        raw_payload: bytes = b"",
    ) -> None:
        super().__init__(mod=52, act=0)
        self.items = items or []
        self.boxes = boxes or []
        self.raw_payload = raw_payload

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 1. 写入日常玩法条目列表 (field_0)
        writer.write_uint16(len(self.items))
        for it in self.items:
            writer.write_int32(it.item_id)
            writer.write_int32(it.completed_count)
            writer.write_uint16(len(it.quota_list))
            for q in it.quota_list:
                writer.write_int32(q)

        # 2. 写入活跃度宝箱列表 (field_1)
        writer.write_uint16(len(self.boxes))
        for bx in self.boxes:
            writer.write_int32(bx.box_id)
            writer.write_int32(bx.required_liveness)
            writer.write_int32(bx.status)

        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "AssistantInfoResp":
        reader = ByteArrayReader(data)
        items: List[AssistantDailyRawItem] = []
        boxes: List[AssistantLivenessRawBox] = []

        try:
            # 1. 解析日常玩法条目列表 (field_0)
            if reader.remaining >= 2:
                item_count = reader.read_uint16()
                for _ in range(item_count):
                    if reader.remaining < 8:
                        break
                    item_id = reader.read_int32()
                    completed_count = reader.read_int32()
                    quota_list: List[int] = []
                    if reader.remaining >= 2:
                        sub_len = reader.read_uint16()
                        for _ in range(sub_len):
                            if reader.remaining >= 4:
                                quota_list.append(reader.read_int32())
                    items.append(
                        AssistantDailyRawItem(
                            item_id=item_id,
                            completed_count=completed_count,
                            quota_list=quota_list,
                        )
                    )

            # 2. 解析活跃度宝箱阶段列表 (field_1)
            if reader.remaining >= 2:
                box_count = reader.read_uint16()
                for _ in range(box_count):
                    if reader.remaining < 12:
                        break
                    box_id = reader.read_int32()
                    req_live = reader.read_int32()
                    status = reader.read_int32()
                    boxes.append(
                        AssistantLivenessRawBox(
                            box_id=box_id,
                            required_liveness=req_live,
                            status=status,
                        )
                    )
        except Exception:
            pass

        return cls(items=items, boxes=boxes, raw_payload=data)
