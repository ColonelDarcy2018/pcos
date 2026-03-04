# Agent Focus Router

> 每个 agent 的焦点任务路由表。并发模式下以本文件替代 `current-task.md`。

| agent_id | focus_task_id | latest_session | status | updated_at | note |
|---|---|---|---|---|---|
| `agent-codex-main` | `ccos-dedup-daily-automation-v1` | `CCOS/context/session-20260303-04.md` | `active` | 2026-03-04 21:25 +0800 | 持续推进去冗余与任务线并发治理改造 |

## 规则

1. 一条记录只对应一个 `agent_id`。
2. 切换任务时必须同步更新本文件与 `task-index.md`。
3. agent 空闲时可将 `status` 标记为 `idle`，并清空 `focus_task_id`。
