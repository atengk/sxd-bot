# 0016 多账号配置体系、字段精简与容器化环境变量架构

针对项目中单账号配置结构孤立、遗留大量历史调试冗余字段（如 `local_relay_port`、空 `hash_code` 等），以及缺乏多账号流水线轮询与 Docker 容器化环境变量支持的问题，本项目决定实施配置体系全面重构：精简废弃字段、顶层解耦 `settings` 与 `accounts` 列表、引入串行故障隔离调度，并全面赋能双层容器环境变量注入体系。

## Status

accepted

## Context

随着日常自动化流水线与数据查询看板建设成熟，当前运行配置（`config/config.json`）面临三大结构性瓶颈：
1. **多账号痛点**：目前顶层仅有单一的 `web_auth` 与 `static_credentials`，多号玩家必须维护多份 JSON 文件并在命令行频繁切换 `-c config/config_sub.json`，极易混淆；
2. **历史包袱累赘**：配置中遗留了早期的微端代理端口（`local_relay_host/port`）、空字符串时间戳与哈希（`hash_code/time`）、冗余的内置参数（`app: "sxd"`）与写死角色昵称（`nickname`），违背了配置的纯粹与自解释性；
3. **容器化不友好**：不支持 Docker 标准环境变量（如 `SXD_USERNAME`、`SXD_PASSWORD`）零配置文件直启，也不支持 `config.json` 中使用 `${ENV_VAR}` 占位符解析，违背了项目安全准则中的零明文机密（Zero-Secret）红线。

## Considered Options

### 1. 配置文件形态重构 (Config Structure)
- **采纳方案**：顶层分离为全局通用运行配置 `settings`（如 `heartbeat_interval_sec`）与多账号实体列表 `accounts: [...]`。
  每个账号实体包含：
  - `alias` (str): 账号别名（默认等于 `username`，用于命令行过滤与日志打印）；
  - `username` (str): 平台登录用户名；
  - `password` (str): 登录密码（支持 `${VAR}` 占位符）；
  - `server` (str): 目标区服标识（如 `s813`）；
  - `enabled` (bool): 启停开关（默认 `true`）；
  - `platform` (str, 可选): 运营平台标识（默认缺省为 `"fengwanyx"`）；
  - `server_host` / `server_port` (可选): 高级静态免密测试网关直连覆盖项。
- **平滑兼容防御**：若载入存量单账号格式（含 `web_auth` 或 `static_credentials`），自动转换为单元素 `accounts` 列表，绝不产生破坏性报错。
- **废弃字段彻底裁剪**：物理移除 `local_relay_host`、`local_relay_port`、空 `hash_code`、空 `time`、`app`、`nickname`、`player_name`。

### 2. 多账号调度与执行策略 (Execution & Concurrency)
- **采纳方案：串行队列执行 + 故障安全隔离**：
  - 在 `--once` 或 `--daemon` 模式下，按配置顺序依次执行每个 `enabled=true` 的账号；
  - 账号间冷启动间隔 2 秒，防范服务端同 IP 瞬时并发风控拦截；
  - 若某一账号认证失败或网络异常，记录错误日志后跳过，绝不阻断后续健康账号的流水线推进；
  - 提供 CLI 参数 `--account <alias/username>`，支持针对指定单账号发起调度。
- **查询模式（`--query`）适配**：
  - 默认针对第一个启用的账号执行只读查询；
  - 支持 `main.py --query assets --account <alias>` 定向查询指定账号；
  - 支持 `main.py --query assets --account all` 全量循环打印所有账号看板。

### 3. Docker 容器化环境变量体系 (Containerization & Env Injection)
- **采纳方案：双层融合体系**：
  1. **零文件单账号直启**：若未挂载 `config.json`，检测到系统环境变量 `SXD_USERNAME`、`SXD_PASSWORD`、`SXD_SERVER` 时，内存自动合成为单账号配置开箱即跑；
  2. **多账号 JSON 注入**：支持环境变量 `SXD_ACCOUNTS_JSON='[{"alias":"主号","username":"...","password":"...","server":"s813"}]'` 跨容器注入；
  3. **配置文件占位符替换**：`config.json` 中支持任意 `${VAR_NAME}` 或 `${VAR_NAME:-default}` 动态展开，彻底杜绝明文密码落盘提交。

## Consequences

- **极致精简**：配置文件行数缩减 50% 以上，无任何无用冗余参数；
- **全自动多账号轮询**：真正实现“配置一份文件，托管全家桶角色”，无需编写外部 Shell 轮询脚本；
- **云原生就绪**：完美支持 Docker/K8s 容器化部署，凭据通过环境变量安全注入；
- **100% 向后兼容**：旧版配置文件与单账号工作流零改动直接可用。
