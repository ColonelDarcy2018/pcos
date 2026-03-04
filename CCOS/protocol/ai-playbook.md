# CCOS AI Playbook（会话操作清单）

本文件是 AI 在 CCOS 下执行任务的标准操作清单。

## 0) Node -> Hub 读取顺序（强制）

### MUST
- 即使在项目目录执行，也必须先确认 Hub 元协议：`/Users/zhuxiaowei/ccos/meta/ccos-unified-protocol.md`。
- 本地 `CCOS/protocol/*` 仅是节点执行细则；跨项目治理、任务线与联邦索引规则以 Hub 元协议为准。
- 当任务涉及跨项目路由或状态沉淀时，必须回写 `~/ccos/capture/tasklines/**`。


## 1) 会话开始

### MUST
- 读取 `CCOS/knowledge/README.md` 作为知识入口。
- 若是多 AI 并行场景，读取 `CCOS/protocol/multi-ai-collaboration.md`。

### SHOULD
- 若用户明确要求恢复上下文，读取：
  - `CCOS/context/task-index.md`
  - `CCOS/context/agent-focus.md`（按当前 `agent_id` 解析焦点任务）
  - `CCOS/context/task-{focus_task_id}.md`（若可解析）
  - `CCOS/context/session-latest.md`（兼容模式，可选）

## 2) 执行中

### SHOULD
- 按问题类型选择知识域：
  - 业务流程：`knowledge/business-logic/`
  - 架构方案：`knowledge/architecture/`
  - 决策记录：`knowledge/decisions/`
  - 可复用模式：`knowledge/patterns/`
  - 脚本案例规范：`knowledge/rpa/`
- 优先链接现有知识，避免重复内联长文本。
- 默认采用“残差式增量迭代”：保留已验证主干，仅修改本次需求相关差异，避免无关改写。
- 信息不明确时，先向用户提澄清问题。
- 若 `task-index.md` 存在多条可推进任务且用户未指定任务线，先询问用户本轮推进哪条任务线。

### MUST（多 AI 并行）
- 先在 `task-index.md` 认领任务，再开始执行。
- 修改代码文件前先更新 `CCOS/context/file-locks.md` 申请 `write` 锁。
- 若检测到锁冲突或租约冲突，暂停写入并记录到 `CCOS/context/conflict-log.md`。

## 3) 会话结束

### MUST
- 当用户明确提出“保存当前状态/生成会话摘要/下次继续/续做上次任务”时，必须更新：
  - `CCOS/context/task-index.md`
  - `CCOS/context/agent-focus.md`
  - `CCOS/context/agent-registry.md`（多 AI 并行时）
  - `CCOS/context/file-locks.md`（有锁操作时）
  - `CCOS/context/conflict-log.md`（发生冲突时）
  - `CCOS/context/task-{任务ID}.md`（受影响任务）
  - `CCOS/context/session-{YYYYMMDD}-{n}.md`
  - `CCOS/context/session-latest.md`（兼容模式，可选）
- 核心任务路由文件（`task-index/agent-focus/task-*.md/session-latest(可选)/agent-registry/file-locks/conflict-log`）必须保持可提交状态，不得长期仅存在本地未追踪副本。

### SHOULD
- 对于跨轮次、长链路研发任务，在关键里程碑后同步一次 `task-index.md` 与 `agent-focus.md`，避免会话中断后丢失进度。

### MUST
- 若新增/修改了知识文档，执行：

```bash
python3 CCOS/scripts/ccos_p0.py sync
```

## 4) 输出约定（建议）

- 给出“当前状态 + 证据 + 下一步”。
- 若存在多方案，默认先给成熟基线，再给更优备选与权衡理由。
- 明确标注需要用户确认的决策点。
