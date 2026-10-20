# 出站元宝硬拦截防火墙与双轨审计机制

在神仙道长连接自动化运行过程中，偶有任务（如偷桃系统的召唤白猿 `Mod 40 Act 6`）因契约误判发出付费指令导致元宝被扣。我们决定在底层网络客户端（`SXDClient`）建立物理级出站发包防火墙（Egress Ingot Firewall），并实施“事前拦截审计 + 事后广播差额审计”的双轨资金审计机制。凡命中高危元宝消费协议且未获显式授权的指令，底层直接抛出 `IngotSecurityException` 彻底切断发包流向；同时在资产切面与防火墙处双向沉淀 `tb_audit_log` 审计记录，确保自动化环境下元宝 100% 绝对零消耗。

## Considered Options

- **选项 1：仅在上层业务任务中修补漏洞**：仅在发现扣费任务时修改业务代码，底层保持直通。被否决，因为无法防范未来新增任务或错误协议引起的未知扣费风险。
- **选项 2：底层网络客户端硬拦截防火墙与双轨审计（采纳）**：在网络发包出口做零信任物理拦截，搭配事前阻断审计与事后状态广播校验，彻底根绝元宝偷跑。

## Consequences

- 彻底拔除 `tasks/routine/peach_pet.py` 中 `call_peach`（召唤白猿）的发包逻辑，仙桃流水线恢复纯免费运转。
- `SXDClient.send_packet` 与 `request` 在向 Socket 写入字节前必须通过 `IngotFirewall.check_packet` 校验；阻断时抛出受管异常并发布安全告警。
- `SqliteStorageSubscriber` 捕获拦截事件与 Mod 0 Act 3 元宝净减少事件，自动写入 `tb_audit_log`。
- 常驻周期巡检统一挂载 `active_task` 上下文，彻底消灭“被动收益/系统同步”的归因漂移。
