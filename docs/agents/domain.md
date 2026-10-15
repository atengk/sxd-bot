# 领域文档指南 (Domain Docs)

工程类 Skills 在探索与理解本代码库时，如何使用本项目的领域模型文档。

## 探索代码库前必读

- 根目录下的 **`CONTEXT.md`**，或者
- 根目录下的 **`CONTEXT-MAP.md`**（若存在则分别指向各子上下文的 `CONTEXT.md`，按需阅读与当前任务相关的上下文）。
- **`docs/adr/`**：阅读与当前改动领域相关的架构决策记录 (ADR)。在多上下文仓库中，还应查阅 `src/<context>/docs/adr/` 获取上下文局部的决策记录。

如果上述任何文件尚不存在，**静默继续执行**。不要主动报错，也无需在未涉及时提前创建。当通过 `/grill-with-docs` 或 `/improve-codebase-architecture` 触发 `/domain-modeling` 且具体术语或决策真正落地时，会按需延迟创建它们。

## 目录结构规范

单上下文仓库（Single-context repo，适用于绝大多数项目及本项目）：

```text
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-protocol-packet-framing.md
│   └── 0002-async-socket-event-loop.md
└── core/
```

多上下文仓库（Multi-context repo，根目录下存在 `CONTEXT-MAP.md`）：

```text
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← 系统全局决策
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← 上下文局部决策
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 统一使用术语表定义

在输出领域概念（如 Issue 标题、重构方案、技术假设、测试用例名称）时，必须严格使用 `CONTEXT.md` 中定义的标准术语，不得使用术语表已明确排除的近义词。

如果所需的领域概念尚未收录于术语表中，这是一个重要信号——要么是使用了项目未认可的自造词（需审慎重新评估），要么是领域模型存在真实空白（需记录并后续使用 `/domain-modeling` 补充）。

## 标注 ADR 冲突

若生成的方案与既有 ADR 存在冲突，必须明确高亮揭示，严禁静默覆盖：

> _与 ADR-0007 (协议分帧机制) 存在冲突——但鉴于……，建议重新评估该决策_
