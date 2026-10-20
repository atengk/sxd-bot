"""神仙道出站安全防火墙与元宝零消耗防御守卫

在出站网络层 (Egress) 构筑物理防线，对所有即将写入 TCP Socket 的数据包进行深度拦截与校验。
严禁自动化任务在未经显式授权的情况下向服务端发送任何可能扣除元宝 (Ingot) 的高危操作。

@author Ateng
@since 2026-10-20
"""

import logging
from typing import Dict, Tuple
from protocol.packet import BasePacket

logger = logging.getLogger(__name__)


class IngotSecurityException(PermissionError):
    """元宝高危操作安全拦截异常

    当出站数据包命中高危元宝操作黑名单且未获得显式授权时抛出。

    @author Ateng
    @since 2026-10-20
    """

    def __init__(self, message: str, mod: int, act: int, action_name: str) -> None:
        super().__init__(message)
        self.mod = mod
        self.act = act
        self.action_name = action_name


class IngotFirewall:
    """出站元宝安全防火墙

    集中管理高危元宝操作协议黑名单与动态载荷规则，
    在出站网络帧进入底层传输层前进行物理阻断。

    @author Ateng
    @since 2026-10-20
    """

    # 无条件高危元宝指令字典: (mod, act) -> 行为语义描述
    HAZARDOUS_INGOT_ACTIONS: Dict[Tuple[int, int], str] = {
        # Mod 0: 角色
        (0, 5): "元宝购买体力",
        # Mod 2: 物品/背包
        (2, 54): "元宝开启背包格子",
        # Mod 13: 药园/招财
        (13, 3): "仙府药园元宝开垦红土地",
        (13, 8): "仙府药园元宝清除CD",
        (13, 25): "仙府药园元宝招财神符",
        # Mod 20: 角色
        (20, 4): "元宝购买体力",
        # Mod 21: 仙履奇缘
        (21, 3): "仙履奇缘元宝清除CD",
        # Mod 22: 命格
        (22, 5): "元宝开启命格背包格子",
        (22, 10): "元宝召唤姜子牙",
        # Mod 24: 世界Boss
        (24, 6): "世界Boss元宝浴火重生",
        # Mod 28: 竞技场
        (28, 3): "竞技场元宝清除CD",
        (28, 4): "竞技场元宝购买挑战次数",
        # Mod 30: 西天取经
        (30, 7): "西天取经元宝购买保护",
        (30, 8): "西天取经元宝刷新使者",
        (30, 11): "西天取经元宝加速",
        (30, 13): "西天取经元宝召唤如来",
        (30, 14): "西天取经元宝加速",
        (30, 17): "西天取经元宝清除CD",
        (30, 18): "西天取经元宝购买祝福",
        # Mod 38: 吉星高照
        (38, 3): "吉星高照元宝重掷",
        # Mod 40: 摘仙桃
        (40, 2): "仙桃元宝购买猴子",
        (40, 6): "仙桃召唤白猿(100元宝)",
        # Mod 41: 帮派祭神
        (41, 2): "帮派祭神元宝上香",
    }

    @classmethod
    def check_egress(cls, packet: BasePacket, allow_ingot: bool = False) -> Tuple[bool, str, str]:
        """检查出站数据包是否存在元宝消耗风险并执行防御拦截判定

        Args:
            packet: 待发送数据包实例。
            allow_ingot: 是否获得显式授权消耗元宝 (默认 False)。

        Returns:
            Tuple[is_safe, action_name, reason]:
            - is_safe: 是否允许发送至套接字 (True=放行, False=拦截)。
            - action_name: 动作语义名称。
            - reason: 拦截或放行的详细原因说明。
        """
        mod = packet.mod
        act = packet.act
        key = (mod, act)

        # 检查是否具备显式授权标志
        packet_allowed = getattr(packet, "allow_ingot", False)
        effective_allow = allow_ingot or packet_allowed

        # 1. 命中无条件元宝指令黑名单
        if key in cls.HAZARDOUS_INGOT_ACTIONS:
            action_name = cls.HAZARDOUS_INGOT_ACTIONS[key]
            if not effective_allow:
                reason = f"出站防火墙拦截高危元宝操作: {action_name} [Mod={mod}, Act={act}] 未获显式授权 (allow_ingot=False)"
                return False, action_name, reason
            return True, action_name, "显式授权元宝操作"

        # 2. 载荷条件检查 (针对兼有铜钱与元宝双模态的混合指令)
        payload = packet.encode_payload() if hasattr(packet, "encode_payload") else b""

        # Mod 41, Act 1: 帮派祭神 (1=白檀香/铜钱, 2=苏合香/100元宝, 3=天木香/1000元宝)
        if mod == 41 and act == 1:
            if len(payload) >= 4:
                incense_type = int.from_bytes(payload[:4], "big")
                if incense_type in (2, 3):
                    action_name = f"帮派祭神元宝上香(档位={incense_type})"
                    if not effective_allow:
                        reason = f"出站防火墙拦截高危元宝操作: {action_name} [Mod=41, Act=1] 未获显式授权"
                        return False, action_name, reason

        # Mod 48, Act 2: 神龙培养 (0=普通/铜钱, 1/2=元宝培养)
        if mod == 48 and act == 2:
            if len(payload) >= 1:
                feed_type = payload[0]
                if feed_type != 0:
                    action_name = f"神龙元宝培养(feed_type={feed_type})"
                    if not effective_allow:
                        reason = f"出站防火墙拦截高危元宝操作: {action_name} [Mod=48, Act=2] 未获显式授权"
                        return False, action_name, reason

        # Mod 24, Act 7: 世界Boss鼓舞 (1=阅历鼓舞, 2=元宝鼓舞)
        if mod == 24 and act == 7:
            if len(payload) >= 1:
                inspire_type = payload[0]
                if inspire_type != 1:
                    action_name = f"世界Boss元宝鼓舞(inspire_type={inspire_type})"
                    if not effective_allow:
                        reason = f"出站防火墙拦截高危元宝操作: {action_name} [Mod=24, Act=7] 未获显式授权"
                        return False, action_name, reason

        return True, "常规安全操作", "放行"
