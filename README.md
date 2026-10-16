# 神仙道无头协议自动化工具 (SXD Bot)

基于逆向工程还原的二进制协议长连接，使用 Python 3.10+ 实现的独立无头自动化框架。

---

## 1. 架构特性

- **纯无头独立运行 (Headless)**：脱离微端 Flash 容器界面，使用真实 TCP Socket 交互，内存占用低（<30MB）。
- **全自动 Web 登录 (Auto Web Auth)**：内置 3 步 Web 认证链，自动通过官方接口获取最新动态网关与有效会话令牌。
- **全功能日常挂机流水线 (Comprehensive Routine Automation)**：
  - **福利签到**：每日签到与七日登录福利自动领取；
  - **招财神符**：免费招财神符自动领取（严格零元宝安全红线）；
  - **帮派祭神**：白檀香神像祈福（声望+100，零元宝）；
  - **吉星高照**：RollCake 状态与境界点同步巡检；
  - **仙府药园**：土地状态精准同步，仙草生长维护；
  - **摘仙桃与神龙**：一键摘取高阶仙桃斩获巨额升级经验，神龙日常喂养；
  - **猎命系统**：NPC 状态同步，一键卖出厄运灰命变现，一键拾取命格入背包；
  - **西天取经**：每日阵营俸禄领取与使者护送启程；
  - **仙履奇缘**：每日奇遇智能答题，内置体力/声望最优收益选项匹配；
  - **背包整理**：主背包智能归纳分类，低级杂物变卖变现，防爆仓掉落丢失。
- **副本与战斗自动化 (Battle Automation)**：
  - **每日精英副本**：自动挂机扫荡与快速秒完成结算；
  - **普通副本极速扫荡**：自动感知剩余体力，批量快速扫荡清空体力防溢出（严格零元宝、自动变卖低级杂物）；
  - **多人副本**：活动时段感知（每日 12:30-13:30 / 18:30-19:30）与自动组队挑战；
  - **竞技场冲榜**：挑软柿子自动挑战，收割声望与排名奖励（每日免费 15 次挑战）；
  - **世界 Boss 参战**：时段感知接入、免费阅历鼓舞战力、阵亡免费复活重返战场。
- **严格零元宝安全红线 (Zero-Ingot Guardrail)**：内核级拦截非免费消耗，坚决杜绝误花元宝资产。
- **多运行模式支持**：
  - `--once`：单次跑完日常流水线后输出美化全功能战报并自动退出（配合系统计划任务）。
  - `--daemon`：24 小时后台守护挂机，维持心跳并定期巡检。
  - `--task <name>`：按需单独执行指定模块（支持 `sport`, `boss`, `travel`, `clean`, `worship`, `farm`, `peach_pet`, `fate`, `take_bible`, `hero_mission`, `multi_mission` 等）。

---

## 2. 目录结构

```text
sxd_bot/
├── CONTEXT.md                  # 领域模型统一语言与术语表
├── docs/
│   ├── adr/                    # 架构决策记录 (0001 ~ 0007)
│   ├── protocol/               # 逆向协议二进制封包规约速查矩阵
│   ├── architecture/           # 架构模型与执行生命周期指南
│   └── tools/                  # 逆向与流量嗅探 MCP 工具链实战指南
├── config/
│   ├── config.example.json     # 配置文件模板
│   └── config.json             # 真实本地凭据 (Git 已自动忽略)
├── protocol/
│   ├── frame.py                # 滑动窗口分帧与 zlib 判定状态机
│   ├── packet.py               # Flash ByteArray 读写器与 BasePacket
│   ├── builder.py              # 流式 PacketBuilder
│   └── messages/               # 强类型数据包契约 (player.py, heartbeat.py)
├── network/
│   ├── client.py               # 异步 TCP Socket 长连接与串行请求队列
│   └── web_auth.py             # 3 步全自动 Web 登录与网关提取
├── core/
│   ├── context.py              # GameContext 集中式状态池 (含等级、财富、场景)
│   └── events.py               # EventBus 事件广播总线
├── tasks/
│   ├── base.py                 # BaseTask 抽象基类与 TaskResult
│   ├── scheduler.py            # 任务调度器 (支持单次流与后台周期)
│   ├── routine/                # 日常福利与挂机任务
│   │   ├── login.py            # 登录初始化与前置握手
│   │   ├── heartbeat.py        # 3 秒活性对齐心跳保活
│   │   ├── signin.py           # 每日签到与七日登录
│   │   ├── money_tree.py       # 免费招财神符 (严格零元宝)
│   │   ├── worship.py          # 帮派白檀香祭神 (声望+100, 零元宝)
│   │   ├── lucky_star.py       # 吉星高照 (RollCake) 状态与境界点同步
│   │   ├── farm.py             # 仙府药园土地状态同步与生长维护
│   │   ├── peach_pet.py        # 摘仙桃 (巨额经验) 与神龙喂养
│   │   ├── fate.py             # 猎命系统状态同步与灰命变现/拾取
│   │   ├── take_bible.py       # 西天取经与阵营俸禄
│   │   ├── travel_event.py     # 仙履奇缘智能答题
│   │   ├── item_clean.py       # 背包智能整理与杂物变现
│   │   └── online_gift.py      # 在线礼包巡检
│   └── battle/                 # 副本与战斗自动化
│       ├── hero_mission.py     # 每日精英副本挂机扫荡与秒完成
│       ├── normal_mission.py   # 普通副本自动极速扫荡与体力清空
│       ├── multi_mission.py    # 多人副本活动时段感知与自动组队挑战
│       ├── super_sport.py      # 竞技场自动挑软柿子挑战冲榜
│       └── world_boss.py       # 世界 Boss 定时参战与鼓舞
├── tests/
│   └── test_codec.py           # 编解码单元测试套件
├── main.py                     # CLI 主启动入口 (支持 UTF-8 控制台美化战报)
└── requirements.txt
```

---

## 3. 常用运行命令

### 3.1 单次日常福利一键巡检 (默认推荐)
```powershell
python main.py -c config/config.json --once
```

### 3.2 24 小时常驻后台守护挂机
```powershell
python main.py -c config/config.json --daemon
```

### 3.3 单独执行指定模块
```powershell
# 竞技场挑软柿子自动冲榜
python main.py -t sport

# 世界 Boss 定时参战与鼓舞
python main.py -t boss

# 仙府药园
python main.py -t farm

# 帮派祭神 (白檀香)
python main.py -t worship

# 摘仙桃与神龙培养
python main.py -t peach_pet

# 猎命系统
python main.py -t fate

# 精英副本扫荡
python main.py -t hero_mission

# 普通副本极速扫荡 (清空剩余体力)
python main.py -t sweep

# 多人副本
python main.py -t multi_mission
```

---

## 4. 架构与领域文档导航

- **统一语言与领域术语**：[CONTEXT.md](./CONTEXT.md)
- **架构决策记录 (ADR)**：
  - [0001 无头原生 TCP 长连接架构](./docs/adr/0001-headless-tcp-socket-architecture.md)
  - [0002 自适应 3 步 Web 鉴权凭据换取机制](./docs/adr/0002-adaptive-web-auth-credential-exchange.md)
  - [0003 协议封包滑动窗口分帧与编解码状态机](./docs/adr/0003-binary-packet-framing-and-codec.md)
  - [0004 零元宝安全熔断机制与前置卫语句跳过策略](./docs/adr/0004-zero-ingot-guardrail-and-fail-fast-skipping.md)
  - [0005 统一事件总线与双模任务调度器](./docs/adr/0005-unified-eventbus-and-dual-mode-scheduler.md)
  - [0006 Agent-Native MCP 逆向与流量嗅探工具链](./docs/adr/0006-agent-native-mcp-reverse-toolchain.md)
  - [0007 普通副本极速扫荡与体力生命周期管理流水线](./docs/adr/0007-normal-mission-power-sweep-pipeline.md)
- **逆向协议封包速查表**：[docs/protocol/mod_action_matrix.md](./docs/protocol/mod_action_matrix.md)
- **系统架构模型与生命周期指南**：[docs/architecture/pipeline_and_lifecycle.md](./docs/architecture/pipeline_and_lifecycle.md)
- **MCP 逆向与抓包工具链指南**：[docs/tools/mcp_reverse_and_traffic.md](./docs/tools/mcp_reverse_and_traffic.md)



