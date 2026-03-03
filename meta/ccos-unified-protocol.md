# CCOS Node x CCOS Hub 统一协议（V1）

目标：将 `CCOS Node` 与 `CCOS Hub` 融合为单一体系，消除“二选一”歧义。

## 核心原则

1. `CCOS Node` 与 `CCOS Hub` 不是替代关系，而是分层关系。
2. 每个任务必须同时使用两层，不允许只选其一。

## 分层定义

- `CCOS Node`（项目执行层）
  - 项目内知识权威源。
  - 记录项目业务逻辑、架构、决策、上下文明细。
  - 执行与改动在项目 `repo_root` 完成。

- `CCOS Hub`（中枢治理层）
  - 跨项目任务线、联邦索引、日报汇总的中枢。
  - 记录路由、摘要、跨项目可见性，不替代项目细节。
  - 中枢目录：`~/ccos`。

## 统一执行闭环（MUST）

1. 任务启动必须确定三字段：
   - `project_id`
   - `repo_root`
   - `ccos_node`
2. 执行阶段必须在 `repo_root` 进行，禁止在 `~/ccos` 直接修改项目实现代码。
3. 项目细节必须写入项目 `CCOS/**`。
4. 跨项目摘要必须回写 `~/ccos/capture/tasklines/**`。
5. 联邦索引与联邦日报由 `~/ccos` 侧脚本生成。

## 任务线命名约定（MUST）

1. Hub 任务线 `taskline_id` 统一格式：`project_id/ccos_node/task_slug`。
2. `ccos_node` 是 Node 标识，不等同于 `taskline_id`；`taskline_id` 前两段等于 `project_id/ccos_node`。
3. 任务线文档中的 `project_id`、`ccos_node` 必须与 `taskline_id` 前两段保持一致。

## 项目目录执行的中枢继承（MUST）

1. 每个 Node 的 `CCOS/protocol/p0-rules.md` 与 `CCOS/protocol/ai-playbook.md` 必须显式引用本协议：
   - `/Users/zhuxiaowei/ccos/meta/ccos-unified-protocol.md`
2. Node 协议只能补充项目执行细则，不得覆盖 Hub 治理规则。
3. `ccosctl hub lint` 必须校验 Node 协议锚点；缺失锚点时，任务不得进入完成态。
4. 即使在项目目录发起任务，仍必须满足三字段路由与 Hub 回写：
   - `project_id`
   - `repo_root`
   - `ccos_node`

## AGENTS 与 Skills 的关系

`AGENTS.md` 可以纳入本协议体系，并作为“仓库执行适配层”：

1. 本协议是全局语义源（CCOS 协议层）。
2. `AGENTS.md` 负责把全局语义落到仓库约束（入口、目录边界、工具约束）。
3. Skills 负责具体工作流与操作步骤。
4. 若 `AGENTS.md` 与 Skills 出现冲突，以“更严格且符合本协议”的规则为准，并要求修订漂移源。

## 优先级建议

1. 平台/System/Developer 强约束
2. 仓库 `AGENTS.md`
3. 触发技能 `SKILL.md`
4. 任务文档与会话上下文

> 说明：在 2-4 层中，`AGENTS` 与 Skills 均应显式引用本协议，避免漂移。
