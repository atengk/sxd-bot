# 任务追踪器：GitHub Issues

本项目的 Issue 与任务规范统一记录在 GitHub Issues 中。所有操作均通过 `gh` CLI 执行。

## 常用操作约定

- **创建 Issue**：`gh issue create --title "..." --body "..."`。多行内容建议使用 Heredoc 语法。
- **查看 Issue 详情**：`gh issue view <number> --comments`，支持结合 `jq` 过滤评论并获取关联标签。
- **列出 Issue 列表**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，可搭配 `--label` 与 `--state` 过滤。
- **添加评论**：`gh issue comment <number> --body "..."`
- **添加 / 移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭 Issue**：`gh issue close <number> --comment "..."`

仓库地址通过 `git remote -v` 自动推断——在克隆仓库内执行 `gh` 命令时会自动识别。

## PR 作为分流入口

**将外部 PR 作为需求入口：否 (PRs as a request surface: no)**。*(若后续希望将外部 PR 纳入需求分流队列，可将此项改为 `yes`，`/triage` 会读取该配置。)*

当配置为 `yes` 时，PR 将沿用与 Issue 相同的标签流转状态，使用对应的 `gh pr` 命令操作：
- **查看 PR**：`gh pr view <number> --comments` 及 `gh pr diff <number>` 查看改动。
- **筛选待分流的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，仅保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的条目（排除 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论 / 打标 / 关闭**：使用 `gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 中 Issue 和 PR 共享同一个数字编号空间，若出现裸编号 `#42`，先尝试 `gh pr view 42`，失败后回退至 `gh issue view 42`。

## 当 Skill 提示 "发布到 Issue 追踪器 (publish to the issue tracker)" 时

创建一个 GitHub Issue。

## 当 Skill 提示 "获取关联 Ticket (fetch the relevant ticket)" 时

执行 `gh issue view <number> --comments`。

## 探路者操作 (Wayfinding operations)

供 `/wayfinder` 使用。**全局地图 (Map)** 为单个汇总 Issue，**子任务 Ticket** 作为其关联子项。

- **地图 Issue (Map)**：打上 `wayfinder:map` 标签的单个 Issue，记录 Notes / 既定决策 (Decisions-so-far) / 迷雾区 (Fog)。创建命令：`gh issue create --label wayfinder:map`。
- **子任务 Ticket (Child ticket)**：作为子 Issue 链接到地图 Issue（通过 `gh api` 子 Issue 端点）。若子 Issue 未开启，则在地图正文的任务清单中登记子项，并在子项正文顶部标注 `Part of #<map>`。标签格式为 `wayfinder:<type>`（如 `research`/`prototype`/`grilling`/`task`）。被认领后分配给负责开发者。
- **依赖阻塞 (Blocking)**：使用 GitHub **原生 Issue 依赖**。关联语法：`gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`（其中 `<blocker-db-id>` 为阻塞项的数字 Database ID，通过 `gh api repos/<owner>/<repo>/issues/<n> --jq .id` 获取，而非普通编号 `#n`）。若依赖特性不可用，则在正文顶部降级标注 `Blocked by: #<n>, #<n>`。当所有阻塞项关闭时视为已解除阻塞。
- **前沿任务查询 (Frontier query)**：列出地图的所有未关闭子项（`gh issue list --state open`，限定于地图的子 Issue / 任务列表），排除存在未解除阻塞项或已有负责人的条目；按地图声明顺序优先选取首项。
- **认领任务 (Claim)**：`gh issue edit <n> --add-assignee @me`。
- **完结归档 (Resolve)**：`gh issue comment <n> --body "<answer>"`，然后执行 `gh issue close <n>`，最后将决策概要与链接追加到地图的 Decisions-so-far 中。
