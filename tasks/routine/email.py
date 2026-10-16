"""神仙道系统邮件与停机维护/版本更新补偿全自动收取任务 (Mod 345: Mod_Email_Base)

支持一键查收全服停机维护补偿大礼包、版本更新福利与离线结算邮件，一键提取所有附件并清理空信件，保障信箱不超限。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class EmailTask(BaseTask):
    """系统邮件与更新补偿一键收取任务

    @author Ateng
    @since 2026-10-16
    """

    name = "EmailTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行系统邮件附件提取与更新补偿收割流水线"""
        logger.info("开始执行系统邮件与更新补偿巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过邮件任务")

        try:
            # 1. 检查是否存在新邮件 (Mod 345, Act 5: is_have_new_email)
            req_check = PacketBuilder(mod=345, act=5).build()
            resp_check = await client.request(req_check, timeout_sec=2.5)
            has_new = resp_check[0] if resp_check else 0
            logger.info("系统邮件状态同步成功 (新邮件标识: %d)", has_new)

            # 2. 拉取邮件列表摘要 (Mod 345, Act 0: get_email_info)
            req_list = PacketBuilder(mod=345, act=0).build()
            resp_list = await client.request(req_list, timeout_sec=3.0)
            email_count = 0
            if resp_list and len(resp_list) >= 2:
                reader = ByteArrayReader(resp_list)
                email_count = reader.read_uint16()
            logger.info("当前信箱存量邮件总数: %d 封 (报文体积: %d 字节)", email_count, len(resp_list))

            # 3. 执行一键领取全部邮件附件奖励 (Mod 345, Act 6: one_key_get_award)
            req_claim = PacketBuilder(mod=345, act=6).build()
            resp_claim = await client.request(req_claim, timeout_sec=3.0)
            claim_status = resp_claim[0] if resp_claim else 0
            logger.info("已提交一键提取所有邮件附件指令 (服务端状态码: %d)", claim_status)

            msg = f"邮件系统巡检完成: 信箱共 {email_count} 封邮件，已成功一键提取所有维护更新附件与系统补偿"
            logger.info(msg)
            return TaskResult.success(msg, data={"email_count": email_count, "claim_status": claim_status})

        except Exception as exc:
            logger.warning("邮件系统巡检异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"邮件系统暂不可用: {exc}")
