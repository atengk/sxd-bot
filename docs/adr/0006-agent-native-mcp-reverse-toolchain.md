# 0006 Agent-Native MCP 逆向与流量嗅探工具链

在协议逆向与全自动挂机机器人开发中，传统的网络抓包与二进制反编译依赖开发者在外部独立桌面 GUI 软件（如 Wireshark、Fiddler、IDA Pro）与代码编辑器之间频繁切换并手工导出 Hex 文本，导致严重的上下文割裂与极高的 AI 协同摩擦；本项目决定在底层引入两套由项目作者开源的 Agent-Native Model Context Protocol (MCP) 服务端——[mcp-server-traffic-inspector](https://github.com/atengk/mcp-server-traffic-inspector)（全栈流量嗅探与链路诊断）与 [mcp-server-reverse](https://github.com/atengk/mcp-server-reverse)（二进制静态分析与反编译），使得 AI Agent 能够通过标准化工具接口直接在会话内完成 PCAP 抓包、TCP 流重组、Flash 符号搜索与控制流逆向；该决策使协议还原闭环提速数倍，并确立了可复用的自动化逆向工程 SOP。

## Status

accepted

## Considered Options

- **选项 1：Agent-Native MCP 自动化工具链（采纳）**：通过标准化 MCP 协议直接与 AI 上下文集成，支持 Agent 自主抓包、会话重组分析与符号逆向，无需跳出 IDE，实现真正的人机协作自动化。
  - 流量嗅探服务端：[https://github.com/atengk/mcp-server-traffic-inspector](https://github.com/atengk/mcp-server-traffic-inspector)
  - 逆向分析服务端：[https://github.com/atengk/mcp-server-reverse](https://github.com/atengk/mcp-server-reverse)
- **选项 2：传统外部桌面 GUI 软件配合人工手动抓包**：依赖开发者手动打开 Wireshark 或 IDA Pro 分析后，将 Hex 复制给 Agent，上下文极易断层且不可编写自动化测试。
- **选项 3：项目内部硬编码私有 Python 抓包脚本**：无法形成跨项目通用的标准化能力，且每次更换目标环境均需重复编写套接字拦截与反编译胶水代码。

## Consequences

- 显著提升逆向效率与分析精确度，成功攻克了 Mod 184 心跳特征提取、Mod 28 战报解包与 Mod 52 非法主动探针熔断诊断等关键难题；
- 开发环境需配置 MCP 运行时（如 `uvx`），工具链依赖详见实战指南 [mcp_reverse_and_traffic.md](../tools/mcp_reverse_and_traffic.md)。
