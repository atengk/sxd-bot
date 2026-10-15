# 分流标签规范 (Triage Labels)

相关 Skills 预设了 5 个标准分流角色。本文件将这些角色映射到本项目 Issue 追踪器中实际使用的标签字符串。

| mattpocock/skills 标准标签 | 本项目实际标签 | 业务含义 |
| :--- | :--- | :--- |
| `needs-triage` | `needs-triage` | 待维护者评估与分流 |
| `needs-info` | `needs-info` | 等待提报者补充更多上下文信息 |
| `ready-for-agent` | `ready-for-agent` | 需求与规范完整，可由离线 Agent 自主实现 |
| `ready-for-human` | `ready-for-human` | 逻辑复杂或涉及敏感决策，需人类工程师介入 |
| `wontfix` | `wontfix` | 确认不予处理/关闭 |

当 Skill 提及某种角色（例如“打上 AFK-ready 分流标签”）时，统一使用上表对应的标签字符串。

后续若希望调整标签命名习惯，直接编辑上表第二列即可。
