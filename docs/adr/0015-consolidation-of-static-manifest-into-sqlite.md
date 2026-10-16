# 0015 静态协议元数据与逆向资产收归 SQLite 数据库架构

针对项目中分散在 Git 版本控制中的超大协议元数据 JSON 文件（`protocol/manifest/all_modules_manifest.json`，9.06 MB）以及逆向调试资产清单（`config/reverse_assets.json`），本项目决定将其全面收归并预置于标准 SQLite 协议元数据库（`data/protocol_manifest.db`），由 Git 直接纳管轻量二进制数据库文件，并物理清理原分散 JSON 文件，实现项目净瘦身与秒级代码生成。

## Status

accepted

## Context

在早期的逆向工程与协议还原阶段，全量 880 模块、8,719 个 Action 与 13,765 个常量的元数据以单一大文件 JSON 形式保存（体积达 9.06 MB）。尽管在 [ADR 0010](./0010-sqlite-storage-and-state-persistence.md) 中已引入了基于 SQLite 的 `ProtocolDatabase` 与 `ProtocolRepository`，但：
1. **冷启动与文件冗余**：此前架构设计为“首次冷启动时从 9MB JSON 热转储入 SQLite”，导致开发机与生产环境克隆代码后存在 0.3~0.5s 的解析与写入延迟，且代码仓库中长期保留着 9MB 的庞大冗余 JSON；
2. **多源数据分散**：逆向调试产物索引 `config/reverse_assets.json` 作为独立静态数据孤立存在于 `config/` 目录；
3. **依赖解耦未彻底**：代码生成器 `scripts/protocol_codegen.py` 与部分单测仍直接打开并解析 9MB JSON，破坏了“存储层统一门面”的分层原则。

## Considered Options

- **选项 1：预置只读 SQLite 库直接由 Git 纳管 + `tb_metadata` 通用扩展 + 依赖代码全面重构 (采纳)**：
  - **直接纳管**：在 `.gitignore` 中解除对 `data/protocol_manifest.db` 的忽略，直接提交已 VACUUM 优化后的轻量只读数据库（约 4MB，Git pack 打包后仅约 1.2MB），相比 9MB JSON 显著节约传输带宽与磁盘空间；
  - **统一数据模型**：在 SQLite 库中扩展 `tb_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)` 表，将 `reverse_assets` 与 `manifest_metadata` 统一入库；
  - **严格自检防线**：`ProtocolDatabase` 剥离任何 JSON 依赖，若数据库文件不存在直接抛出明确的 `FileNotFoundError`；
  - **仓储层按需驱动**：重构 `scripts/protocol_codegen.py` 与单测，改由 `ProtocolRepository` 执行按需点查（`get_module`、`get_actions_by_module`、`get_constants_by_module`），彻底告别单一大字典反序列化；
  - **清理原文件**：物理删除 `protocol/manifest/all_modules_manifest.json` 与 `config/reverse_assets.json`。
- **选项 2：保留 JSON 并仅在代码中忽略**：
  - 无法达到给项目瘦身的目标，Git 历史与克隆成本持续居高不下。
- **选项 3：提交 SQL 压缩文本种子**：
  - 启动时仍需要运行时解压执行 SQL DDL/DML，未能达成“零延迟、开箱即用”的最佳体验。

## Consequences

- **代码库显著瘦身**：成功剔除 9.06 MB 的巨型 JSON 冗余文件，代码库架构更加轻巧敏捷；
- **真正的零冷启动延迟**：所有依赖静态元数据的功能（CLI 工具、代码生成、协议查询）无需任何预热，毫秒级即启即查；
- **分层与职责统一**：所有静态元数据访问均收口至 `storage/protocol_db.py`，外部代码不再有随意 `open()` 静态数据文件的破坏行为；
- **100% 向后兼容与单测健康**：全量单元测试对齐新仓储查询协议，135+ 项单测全绿。
