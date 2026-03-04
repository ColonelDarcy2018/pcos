# File Locks

> 文件写锁登记。修改代码前先加锁，完成后及时释放。

## Active Locks

| path | lock_type | agent_id | task_id | locked_at | lease_until | note |
|---|---|---|---|---|---|---|
| `CCOS/context/task-index.md` | `write` | `agent-codex-main` | `ccos-dedup-daily-automation-v1` | `2026-03-04 21:25 +0800` | `2026-03-11 23:59 +0800` | 任务索引迁移 |
| `CCOS/context/agent-focus.md` | `write` | `agent-codex-main` | `ccos-dedup-daily-automation-v1` | `2026-03-04 21:25 +0800` | `2026-03-11 23:59 +0800` | agent 路由迁移 |
| `CCOS/protocol/p0-rules.md` | `write` | `agent-codex-main` | `ccos-dedup-daily-automation-v1` | `2026-03-04 21:25 +0800` | `2026-03-11 23:59 +0800` | P0 并发规则迁移 |
