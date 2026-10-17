# 工业级开源模版集成、容器化与生产服务器部署架构

为了规范神仙道自动化工具 (SXD Bot) 的工程治理体系，消除各端配置碎片化，并满足云原生生产环境的常驻高可用运行诉求，决定全量对齐并集成 `atengk/oss-template` 工业级开源模版底座，完成双元流水线建设、轻量级 Docker 容器化以及远程生产集群部署。

## 决策背景与核心考量

1. **工程规范治理**：项目此前缺少标准 CI 门禁、Conventional Commits 强校验以及统一 Changelog 提取链。通过引入模版的 `.cliff.toml`、`.githooks/commit-msg`、`scripts/commit.sh` 与 `scripts/release.sh`，构建从开发提交到版本发布的闭环。
2. **流水线二元设计**：遵循模版标准二元模型，集成 `ci.yml`（PR/Push 质量门禁：Ruff 代码规范检查 + Pytest 跨版本兼容性测试矩阵）与 `release.yml`（统合发版编排器：git-cliff 提取日志、GitHub Release 打包、双镜像源构建与推送）。
3. **双仓库镜像策略 (Dual Registry)**：容器镜像统一由 Actions 构建，同时推送到 GitHub Container Registry (`ghcr.io/atengk/sxd-bot`) 与阿里云容器镜像服务 (`registry.cn-chengdu.aliyuncs.com/atengk/sxd-bot`)，兼顾国际生态协作与境内服务器极速无代理拉取。
4. **容器化双模常驻架构**：基于 `python:3.11-slim` 极简多阶段镜像，主进程运行 `python main.py web --host 0.0.0.0 --port 8000`，内置 FastAPI 状态探针与自愈调度引擎，外置持久化卷解耦存储。
5. **服务器拓扑与目录规约**：生产环境部署于 `/data/sxd-bot`，通过 `docker-compose.yml` 映射宿主机端口 `18000:8000`（避开 `8080/18080`），将 SQLite 数据库与关键配置挂载至宿主机卷，并配备 `update.sh` 一键无感滚动更新脚本。

## 方案选型与权衡 (Considered Options)

- **主进程模式**：
  - *选项 A (采纳)*: `python main.py web`（Web 控制台 + 调度守护双模引擎），提供 HTTP 健康探针与可视化管控面板；
  - *选项 B (放弃)*: 纯无头终端守护 `python main.py --daemon`，缺少 HTTP 探针，无法与容器存活性探测及外部反向代理无缝联动。
- **镜像仓库选型**：
  - *选项 A (采纳)*: GHCR 与阿里云 ACR 双推策略，网络抗脆弱性高；
  - *选项 B (放弃)*: 仅推单一仓库，境内服务器直接拉取 GHCR 易受网络波动影响。
- **部署编排方式**：
  - *选项 A (采纳)*: Docker Compose 声明式管理与 `/data/sxd-bot/update.sh` 脚本化更新；
  - *选项 B (放弃)*: 原生裸命令 `docker run`，不利于日志配额限制、自动重启策略与数据卷版本化维护。
