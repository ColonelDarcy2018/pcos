# CCOS P0 公共约束（规则权威源）

本文件定义 CCOS P0 的公共约束，供所有技能和知识文档统一引用。

## 0. Hub 元协议锚点

### MUST
- 本文档继承中枢元协议：`../../meta/ccos-unified-protocol.md`。

## 1. 资产分区

### MUST
- 将 `CCOS/knowledge/**` 视为知识权威源（Single Source of Truth）。
- 将 `CCOS/.index.json`、`CCOS/.ccos/**` 视为机器派生资产。
- 禁止手工编辑 `CCOS/.index.json`。

### SHOULD
- 优先将人类可读决策写入 `knowledge/` 或 `context/`，再由脚本派生索引。

## 2. 目录与结构

### MUST
- 保持以下目录存在：
  - `CCOS/context/`
  - `CCOS/knowledge/`
  - `CCOS/templates/`
  - `CCOS/assets/`
  - `CCOS/scripts/`
  - `CCOS/.ccos/`
- `CCOS/knowledge/` 的每个一级子目录必须包含 `README.md`。

## 3. 链接规范

### MUST
- 仅使用相对路径链接项目内文件。
- 禁止使用绝对路径链接（如 `file:///...`、`/Users/...`、`C:\...`）。

### SHOULD
- 链接目标应存在；不存在时尽快修复。

## 4. CCOS-Index 元数据

### SHOULD（P0 当前级别）
- 知识文档建议包含 `CCOS-Index` front matter。
- `id`、`domain`、`tags`、`related`、`created`、`updated` 建议完整填写。

### MUST
- 若填写了 `CCOS-Index.id`，必须保证在知识库内唯一。

## 5. 命令约束

### MUST
- 在新增/修改知识文档后，至少执行一次：

```bash
python3 CCOS/scripts/ccos_p0.py sync
```

### SHOULD
- 在大批量调整前先执行 `validate`，降低返工。

## 6. 规则级别映射（与当前脚本行为对齐）

| 规则 | 级别 | 当前脚本行为 |
|------|------|--------------|
| 必需目录缺失 | error | `validate` 失败 |
| `knowledge/*/README.md` 缺失 | error | `validate` 失败 |
| `CCOS-Index.id` 重复 | error | `validate` 失败 |
| 绝对路径链接 | error | `validate` 失败 |
| `CCOS-Index` 缺失 | warning | `validate` 通过但告警 |
| `CCOS-Index.id` 缺失 | warning | `validate` 通过但告警 |
| 链接目标不存在 | warning | `validate` 通过但告警 |
| `related` 引用缺失 | warning | `validate` 通过但告警 |

> 注：上述等级是 P0 当前约定。若未来引入 strict 模式，可将部分 warning 升级为 error。

## 7. 上下文连续性（会话状态）

### MUST
- 当用户明确提出“保存当前状态/生成会话摘要/下次继续/续做上次任务”时，必须更新：
  - `CCOS/context/current-task.md`
  - `CCOS/context/task-index.md`
  - `CCOS/context/task-{任务ID}.md`（受影响任务）
  - `CCOS/context/session-{YYYYMMDD}-{n}.md`
  - `CCOS/context/session-latest.md`

### SHOULD
- 对于跨轮次、长链路的研发任务，在阶段性里程碑结束时同步一次 `current-task.md`，降低上下文断层风险。

## 8. 多任务并行模式

### MUST
- 当存在 2 条及以上任务线时，`current-task.md` 仅作为“活动任务路由器”，不承载单任务完整正文。
- 每条任务线必须独立维护 `CCOS/context/task-{任务ID}.md`，禁止用新任务内容覆盖旧任务文件。
- 任务切换时必须同步更新：
  - `CCOS/context/current-task.md`（active_task）
  - `CCOS/context/task-index.md`（状态与优先级）
  - `CCOS/context/session-latest.md`（最近会话指针）

### SHOULD
- 对“等待用户决策”的任务，保留明确的 `待确认问题`，便于后续快速恢复。
- `task-index.md` 建议包含：`task_id`、`状态`、`优先级`、`任务文档`、`最新会话`。

## 9. 多 AI 协作防冲突

> 详细流程见：`CCOS/protocol/multi-ai-collaboration.md`

### MUST
- 多 AI 并行时，每个 AI 必须使用唯一 `agent_id`，并登记到 `CCOS/context/agent-registry.md`。
- 开工前必须在 `CCOS/context/task-index.md` 完成任务认领（`owner_agent`、`lease_until`、`working_branch`、`lock_scope`）。
- 修改文件前必须在 `CCOS/context/file-locks.md` 申请 `write` 锁；锁冲突时不得继续写入同一文件。
- 若发生抢占、锁超时接管、合并冲突，必须记录到 `CCOS/context/conflict-log.md`。

### SHOULD
- 建议采用“一任务一分支”策略（`task/<task_id>/<agent_id>`）。
- 建议每 5-15 分钟更新一次租约心跳，降低误接管。
