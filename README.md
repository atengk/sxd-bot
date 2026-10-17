# 神仙道无头协议自动化工具 (SXD Bot)

<p align="center">
  <a href="https://github.com/atengk/sxd-bot/releases"><img src="https://img.shields.io/github/v/release/atengk/sxd-bot?style=flat-square&color=2563eb" alt="GitHub Release"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://github.com/atengk/sxd-bot/pkgs/container/sxd-bot"><img src="https://img.shields.io/badge/docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker Ready"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="License"></a>
</p>

<p align="center">
  基于逆向二进制长连接协议的现代化神仙道无头自动化工具与 Web 控制台。<br/>
  脱离 Flash 微端容器与模拟点击，内存占用极低（&lt;35MB），内置 35+ 项全功能日常福利收割、战斗极速扫荡与常驻自愈守护引擎。
</p>

---

## 🌟 核心特性

- **纯无头二进制长连接 (Headless Socket)**：直接与官方 TCP 网关进行 Flash AMF/ByteArray 数据包交互，零 UI 渲染开销，支持 7×24 小时低资源耗用挂机。
- **Web 控制台与自愈守护双模引擎 (Web & Daemon)**：内置基于 FastAPI + Element Plus 的响应式单页仪表盘，支持实时日志 SSE 流式推送、多账号纳管与态势感知看板。
- **全方位安全门禁 (Security Gate)**：
  - **访问口令门禁 (Web Token Gate)**：支持通过命令行 `--token`、环境变量 `SXD_WEB_TOKEN` 或设置面板配置访问密码，敏感接口与操作全量拦截校验。
  - **严格零元宝安全红线 (Zero-Ingot Guardrail)**：内核级拦截非免费游戏消耗，杜绝任何误花元宝资产行为。
  - **玩家自登顶号瞬态避让 (Evade Circuit Breaker)**：检测到客户端顶号时毫秒级切断连接并挂起托管，严格服从玩家端内最高操作权。
- **全功能日常与战斗自动化流水线 (Comprehensive Routine)**：
  - **日常福利**：每日签到、免费招财神符、帮派白檀香祭神、吉星高照 (RollCake)、仙府药园维护、仙桃与神龙、猎命系统（厄运灰命变卖/拾取）、西天取经、仙履奇缘智能答题、仙道问灵、周末狂欢双转盘、停服维护大礼包自动领取。
  - **战斗与扫荡**：每日精英副本秒完成结算、普通副本体力极速清空（严格零元宝）、多人副本时段感知组队、竞技场挑选软柿子冲榜、世界 Boss 阅历鼓舞参战。
  - **背包自理**：免排自理管道，自动开箱、丹药使用、杂物变现防爆仓。

---

## ⚡ 快速开始 (Docker 生产部署)

推荐使用 Docker Compose 在 Linux 服务器（如 `/data/sxd-bot`）上一键部署：

### 1. 编写 `docker-compose.yml`

```yaml
services:
  sxd-bot:
    image: registry.cn-chengdu.aliyuncs.com/atengk/sxd-bot:latest
    container_name: sxd-bot-server
    restart: unless-stopped
    ports:
      - "18000:8000"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./data:/app/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
      - SXD_MODE=web
      - SXD_HOST=0.0.0.0
      - SXD_PORT=8000
      # 可选：设置 Web 控制台访问密码 (留空则免密进入)
      - SXD_WEB_TOKEN=${SXD_WEB_TOKEN:-}
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://127.0.0.1:8000/api/health || exit 1"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"
```

### 2. 启动与更新服务

```bash
# 启动容器服务
docker compose up -d

# 一键滚动更新至最新版本 (自带镜像缓存清理)
docker compose pull && docker compose up -d --remove-orphans && docker image prune -f
```

启动完成后，访问 `http://<服务器IP>:18000` 即可进入 Web 控制台。

---

## 🖥️ 本地 CLI 运行指南

### 1. 环境准备

```bash
# 克隆代码库
git clone https://github.com/atengk/sxd-bot.git
cd sxd-bot

# 安装运行依赖
pip install -r requirements.txt
```

### 2. 常用运行模式

```bash
# 1. 启动 Web 控制台与自愈挂机调度服务 (推荐)
python main.py web --host 0.0.0.0 --port 8000

# 带口令门禁启动 Web 控制台
python main.py web --token YOUR_SECRET_TOKEN

# 2. 单次跑完日常福利流水线后自动退出 (配合系统计划任务)
python main.py --config config/config.json --once

# 3. 24 小时后台纯无头常驻挂机模式
python main.py --config config/config.json --daemon

# 4. 单独执行指定模块任务 (如竞技场、世界Boss、药园)
python main.py -t sport         # 竞技场自动冲榜
python main.py -t boss          # 世界 Boss 定时参战与鼓舞
python main.py -t sweep         # 普通副本快速扫荡清空体力
python main.py -t farm          # 仙府药园种植与采摘
python main.py -t worship       # 帮派祭神 (白檀香)
```

---

## 📂 目录结构与架构

```text
sxd_bot/
├── .github/
│   ├── workflows/              # GitHub Actions 二元流水线 (ci.yml / release.yml)
│   ├── ISSUE_TEMPLATE/         # 规范化缺陷反馈与特性建议模板
│   └── PULL_REQUEST_TEMPLATE.md
├── config/
│   ├── config.example.json     # 本地配置文件模板
│   └── config.json             # 真实本地凭据 (Git 自动忽略)
├── core/
│   ├── context.py              # GameContext 集中式状态池 (等级/资产/背包/场景)
│   ├── events.py               # EventBus 事件广播与分发总线
│   └── config.py               # 账号与应用全局配置管理
├── protocol/
│   ├── frame.py                # 滑动窗口分帧与 zlib 解压状态机
│   ├── packet.py               # Flash ByteArray 读写器与 BasePacket
│   └── messages/               # 强类型数据包契约 (player.py, heartbeat.py)
├── network/
│   ├── client.py               # 异步 TCP Socket 长连接与请求队列
│   └── web_auth.py             # 3 步全自动 Web 登录与网关提取
├── tasks/
│   ├── routine/                # 每日福利与挂机任务 (签到/招财/药园/仙桃/问灵等)
│   ├── battle/                 # 副本与战斗自动化 (精英副本/扫荡/竞技场/世界Boss)
│   └── scheduler.py            # 双模任务调度器
├── storage/
│   ├── config_db.py            # SQLite 账号配置与运行设置持久化
│   └── player_db.py            # 角色资产与背包快照持久化
├── web/
│   ├── app.py                  # FastAPI 主接入应用与鉴权中间件
│   ├── session_manager.py      # 多账号长连接常驻自愈调度引擎
│   ├── routes/                 # RESTful API 路由 (账号/任务/事件流/遥测)
│   └── static/                 # Element Plus 前端响应式单页
├── scripts/
│   ├── commit.sh               # Conventional Commits 规范提交助手
│   ├── release.sh              # 统合发版防呆与版本自增脚本
│   └── update.sh               # 生产服务器一键滚动更新脚本
├── Dockerfile                  # 生产级 Python 3.11-slim 极简多阶段构建
├── docker-compose.yml          # 生产部署编排定义
├── pyproject.toml              # 标准 Python 项目与工具链元数据
└── CONTEXT.md                  # 领域模型统一语言与术语规约
```

---

## 📖 架构决策记录 (ADR)

本项目严格采用领域驱动与架构决策记录（Architecture Decision Records）追踪核心设计演进，详见 [`docs/adr/`](./docs/adr/)：

- [ADR 0001: 无头原生 TCP 长连接架构](./docs/adr/0001-headless-tcp-socket-architecture.md)
- [ADR 0002: 自适应 3 步 Web 鉴权凭据换取机制](./docs/adr/0002-adaptive-web-auth-credential-exchange.md)
- [ADR 0003: 协议封包滑动窗口分帧与编解码状态机](./docs/adr/0003-binary-packet-framing-and-codec.md)
- [ADR 0004: 零元宝安全熔断机制与前置卫语句跳过策略](./docs/adr/0004-zero-ingot-guardrail-and-fail-fast-skipping.md)
- [ADR 0005: 统一事件总线与双模任务调度器](./docs/adr/0005-unified-eventbus-and-dual-mode-scheduler.md)
- [ADR 0021: 真实 Socket 引擎与一体化双主题控制台设计](./docs/adr/0021-real-socket-engine-and-cohesive-dual-theme-redesign.md)
- [ADR 0022: 常驻自愈守护引擎与多租户存储隔离](./docs/adr/0022-continuous-autonomous-daemon-and-storage-isolation.md)
- [ADR 0034: 工业级开源模版集成、容器化与生产服务器部署架构](./docs/adr/0034-oss-template-integration-containerization-and-server-deployment.md)

---

## 🤝 参与贡献

欢迎任何形式的贡献与建议！提交代码前请仔细阅读 [贡献指南 (CONTRIBUTING.md)](./CONTRIBUTING.md) 并遵循 Conventional Commits 规范。

---

## 📄 开源许可证

本项目基于 [Apache License 2.0](./LICENSE) 协议开源。
