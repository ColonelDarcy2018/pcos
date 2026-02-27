# PCOS（Personal Cognitive Operating System）

这是一个可版本控制、可回滚、可扩展的个人认知基础设施目录。它把日常思考与长期资产分离，并为未来自动化预留机器可读层。

PCOS 的定位是一个**认知进化系统**：结构的目的在于支持知识从经验到抽象的演化与复利，而不是把内容“分到正确的分类里”。

## 目标

- **低门槛落地**：先能用，再逐步增强
- **人机双轨**：人类可读（Markdown）与机器可读（JSON/Schema/Index）并行演进
- **Git 即真理**：所有沉淀可 diff、可审计、可回滚
- **插件化扩展**：高级能力以独立模块/脚本加入，避免强耦合

## 目录说明

- `capture/`：原始捕获（建议作为 Logseq 图谱根目录；这里是“收件箱”）
- `assets/`：长期认知资产（人类层，允许自然书写与演化）
  - `evidence/`：事实与经验（案例、复盘、决策记录、实验与观察）
  - `patterns/`：可复用模式（方法、模型、策略、技巧、结构）
  - `principles/`：稳定原则（世界模型、系统哲学、方法论生成规则）
  - 设计说明见：`assets/README.md`
- `machine/`：机器可读结构（索引/Schema/图谱/提示词/Agent 定义）
  - `schema/`：JSON Schema（约束 machine 数据格式）
  - `graph/`：关系图谱（可选；后续可由脚本生成/维护）
  - `prompts/`：可复用提示词（可选；用于蒸馏/归档/总结等）
  - `agents/`：自动化 Agent 定义（可选；保持可插拔）
- `workflows/`：人机协作流程（如何从 capture 产出 assets + machine）
- `meta/`：系统原则与宪法（不作为日常沉淀入口，用于约束长期演进方式）

## 基本使用方式（V1 极简）

1. **捕获**：把所有临时想法、信息、未验证结论先写入 `capture/`，不要急着结构化。
2. **蒸馏**：按 `workflows/distill.md` 将有价值内容沉淀到 `assets/`，同时更新 `machine/` 索引。
3. **复用**：优先从 `assets/` 取用，而不是重复造轮子；重要决策写入 `assets/evidence/decisions/`。

## 日报闭环（Git -> Capture -> 提交）

为保证每天工作与想法都形成可追踪沉淀，PCOS 增加了项目化日报技能：

- 技能位置：`assets/patterns/skills/git-daily-report/`
- 核心约束：日报严格基于 `git diff HEAD`（不混入已提交历史）
- 固定产物：`今日完成`、`明日任务`、`工时`
- 回写位置：`capture/journals/YYYY_MM_DD.md` 的 `- 日报` 区块
- 收尾动作：回写后提交全部文档并推送，形成当日演化快照

推荐执行命令：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --sync
```

该闭环与 `workflows/distill.md` 互补：日报用于“当天收敛”，蒸馏用于“长期升维”。

## 演进原则（如何长期维护）

- **先手工、后自动化**：流程稳定后再加脚本/Agent；自动化产物尽量可重建。
- **不改写原始捕获**：`capture/` 保持原始语境；资产以新增/提炼为主。
- **小步提交**：每次提交聚焦一个主题，便于回滚与审计。
- **新能力以“插件”加入**：新增目录/脚本前先写清输入/输出与回归方式。

更多原则见：`meta/constitution.md`；meta 与三层资产结构的语义映射见：`meta/cognitive-mapping.md`。
