# 任务索引（Task Index）

- updated_at: 2026-03-04 21:25 +0800

## 路由说明

1. 本文件是任务级事实源，不维护全局 `active_task_id`。
2. agent 当前执行焦点请查看 `CCOS/context/agent-focus.md`。
3. 每条任务线必须落在独立 `task-*.md`，禁止互相覆盖。

## 任务清单

| task_id | 任务名称 | 状态 | 优先级 | owner_agent | lease_until | working_branch | lock_scope | 任务文档 | 最新会话 |
|---|---|---|---|---|---|---|---|---|---|
| `ccos-unification-migration-20260303` | CCOS 全量迁移与文档同步 | `completed` | `P0` | `unassigned` | - | - | - | `CCOS/context/task-ccos-unification-migration-20260303.md` | `CCOS/context/session-20260303-04.md` |
| `remote-codex-control` | 手机跨网络远程控制 PC Codex 任务 | `in_progress` | `P0` | `unassigned` | - | - | - | `CCOS/context/task-remote-codex-control.md` | `CCOS/context/session-20260303-03.md` |
| `ccos-dedup-daily-automation-v1` | CCOS 去冗余改造与自动日报闭环 V1 | `in_progress` | `P0` | `agent-codex-main` | `2026-03-11 23:59 +0800` | `main` | `CCOS/context/*.md, capture/tasklines/*.md, meta/ccos-unified-protocol.md` | `CCOS/context/task-ccos-dedup-daily-automation-v1.md` | `CCOS/context/session-20260303-04.md` |

## 使用规则

1. 开工前必须在本文件完成任务认领（`owner_agent/lease_until/working_branch/lock_scope`）。
2. 任务切换时至少同步：`task-index.md`、`agent-focus.md`、`agent-registry.md`、对应 `task-*.md`。
3. 多任务并行且用户未指定任务线时，先展示候选任务线并等待用户选择。
