# 任务线中枢（Logseq 友好）

本目录用于维护跨项目任务线，面向人类读写与会话恢复。

## 使用定位

- 记录跨项目任务背景、目标、状态和待确认问题。
- 作为 AI 协作的中枢入口，不承载项目级业务逻辑细节。
- 项目细节仍保留在各项目 `CCOS` 内。

## 文件约定

- `task-index.md`：任务线总览与路由。
- `task-*.md`：单条任务线详情。

## 命名与路由约定（统一口径）

1. `taskline_id` 统一格式：`project_id/ccos_node/task_slug`。
2. `ccos_node` 仅表示节点标识（例如 `default`、`outer`）。
3. `project_id/ccos_node` 组成 Node 路由键；`taskline_id` 是在该键下的任务线标识。
4. 任务文档头部的 `project_id`、`ccos_node` 必须与 `taskline_id` 前两段一致。

## 与 machine/federation 的关系

- `capture/tasklines`：人类可读、可在 Logseq 中自然编辑。
- `machine/federation`：机器可读、用于脚本聚合和自动化执行。

建议做法：任务状态先写在 `tasklines`，再由脚本读取注册表/索引生成联邦日报。

## 并发路由约束（2026-03-04 更新）

1. Hub 侧不维护 Node 的单一活动任务指针。
2. Node 并发路由以 `task-index + agent-focus` 为准，Hub 仅消费任务线状态摘要。
