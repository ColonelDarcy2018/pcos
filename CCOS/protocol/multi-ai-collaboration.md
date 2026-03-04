# CCOS Multi-AI Collaboration Protocol

本协议用于“多 AI 同时推进多条任务线”场景，目标是降低并发冲突、重复劳动和上下文漂移。

## 1. 角色与标识

每个 AI 会话必须有唯一 `agent_id`（示例：`agent-codex-a`），并登记到：

- `CCOS/context/agent-registry.md`

建议字段：

- `agent_id`
- `task_id`
- `status`（active/idle/blocked）
- `working_branch`
- `lease_until`
- `last_heartbeat`

并发路由要求（MUST）：

1. 同步维护 `CCOS/context/agent-focus.md`，以 `agent_id -> focus_task_id` 做路由。
2. 不使用 `current-task.md` 作为并发场景的全局单指针路由源。

## 2. 任务认领（Task Claim）

开始执行前必须先认领任务，在 `CCOS/context/task-index.md` 更新：

- `owner_agent`
- `lease_until`
- `working_branch`
- `lock_scope`（计划要改的文件范围）

认领规则：

1. 已被其他 agent 认领且租约未过期，不得抢占。
2. 仅允许用户明确指令覆盖认领关系。
3. 租约过期可由其他 agent 接管，并记录接管原因。
4. `task-index.md` 禁止维护全局 `active_task_id`，仅维护任务清单与 owner/lease。

## 3. 文件锁（File Lock）

在修改代码前，先写入 `CCOS/context/file-locks.md`。

每条锁记录建议包含：

- `path`
- `agent_id`
- `task_id`
- `lock_type`（read/write）
- `locked_at`
- `lease_until`
- `note`

格式约束（MUST）：

1. 一条记录只允许一个 `path`；禁止把多个路径拼在单行里。
2. 目录路径与文件路径都可加锁，但目录锁必须写清子树边界（例如 `project/videohao/`）。

规则：

1. `write` 锁互斥；存在有效 `write` 锁时其他 agent 不能写同一文件。
2. `read` 锁可共享，但不阻塞 `write` 锁申请检查。
3. 锁超时后可被接管，接管必须记录在 `CCOS/context/conflict-log.md`。

## 4. 心跳与续租（Heartbeat）

执行中应周期更新：

- `agent-registry.md` 的 `last_heartbeat`
- `task-index.md` 的 `lease_until`
- `agent-focus.md` 的 `updated_at`（当焦点任务切换时）

建议心跳间隔：5-15 分钟。超过租约时间未续租视为可接管。

## 5. 冲突处理（Conflict Handling）

发生冲突时记录到：

- `CCOS/context/conflict-log.md`

建议字段：

- `time`
- `task_id`
- `file`
- `agent_a` / `agent_b`
- `conflict_type`
- `resolution`
- `resolved_by`

冲突优先级：

1. 用户明确指令
2. 任务 owner（有效租约内）
3. 最近一次成功提交者

## 6. 分支策略（Git）

建议一任务一分支：

- `task/<task_id>/<agent_id>`

禁止多个 agent 直接并发写同一分支同一文件而无锁记录。

## 7. 结束与释放

任务阶段结束后必须：

1. 释放 `file-locks.md` 中对应锁。
2. 更新 `task-index.md` 任务状态与 owner。
3. 更新 `agent-focus.md`（标记 `idle` 或切换到新任务）。
4. 在 `session-latest.md` 记录当前可接手入口（兼容模式，可选）。
