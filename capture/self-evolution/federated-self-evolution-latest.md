# AI Self-Evolution Scan Report

- generated_at: `2026-04-22 19:31:08 +0800`
- mode: `federated`
- hub_root: `/Users/zhuxiaowei/ccos`
- sources: `6`
- files_scanned: `198`

## Scan Scope

| project_id | node_id | repo_root | ccos_root |
| --- | --- | --- | --- |
| `void` | `default` | `/Users/zhuxiaowei/apps/void` | `/Users/zhuxiaowei/apps/void/CCOS` |
| `rpa-mobile` | `outer` | `/Users/zhuxiaowei/apps/rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS` |
| `wanling-tower` | `default` | `/Users/zhuxiaowei/apps/game_demo/wanling-tower` | `/Users/zhuxiaowei/apps/game_demo/wanling-tower/CCOS` |
| `myth-td-prototype` | `default` | `/Users/zhuxiaowei/apps/game_demo/myth-td-prototype` | `/Users/zhuxiaowei/apps/game_demo/myth-td-prototype/CCOS` |
| `game_service` | `default` | `/Users/zhuxiaowei/game_service` | `/Users/zhuxiaowei/game_service/CCOS` |
| `ccos` | `default` | `/Users/zhuxiaowei/ccos` | `/Users/zhuxiaowei/ccos/CCOS` |

## Candidate Summary

| signal_id | title | matches | project_count | proposed_artifact | proposed_landing |
| --- | --- | --- | --- | --- | --- |
| `workflow-stage-template` | 软件工程阶段模板 | 172 | 5 | `workflow-pack` | `scenario workflow packs: clarify -> PRD -> design -> build -> verify -> release` |
| `automation-heartbeat` | 持续推进 / 自动唤醒 / heartbeat | 63 | 3 | `workflow` | `Workflow V2 + Codex thread automation` |
| `review-ledger-promotion` | 自动审查 / review ledger / 规则候选 | 40 | 3 | `review` | `review ledger + reviewer module + verify checks` |
| `rule-promotion` | 澄清事项升格为规则或公理 | 40 | 2 | `rule` | `AGENTS.md / CCOS/protocol/p0-rules.md / review ledger` |
| `skill-promotion` | 重复需求沉淀为技能 | 24 | 2 | `skill` | `~/.codex/skills + requirement-pool state update` |
| `known-solution-research` | 已知方案 / 开源项目 / 成熟产品调研前置 | 8 | 2 | `skill` | `global skill: solution-landscape-research` |

## Recommended Immediate Promotions

1. `workflow-stage-template` -> scenario workflow packs: clarify -> PRD -> design -> build -> verify -> release
   - reason: 不同开发场景需要固定阶段包，而不是每轮临时重新组织流程。
   - current_evidence: 172 matched lines across 5 project(s)
1. `automation-heartbeat` -> Workflow V2 + Codex thread automation
   - reason: 重复出现的“继续推进直到 blocker”需求应沉淀为调度能力。
   - current_evidence: 63 matched lines across 3 project(s)
1. `review-ledger-promotion` -> review ledger + reviewer module + verify checks
   - reason: 先记录可审计证据，再决定要不要升级为规则、hook 或 skill。
   - current_evidence: 40 matched lines across 3 project(s)

## Detailed Evidence

### workflow-stage-template - 软件工程阶段模板

- proposed_artifact: `workflow-pack`
- proposed_landing: `scenario workflow packs: clarify -> PRD -> design -> build -> verify -> release`
- why: 不同开发场景需要固定阶段包，而不是每轮临时重新组织流程。

| project_id | file | line | keyword | excerpt |
| --- | --- | --- | --- | --- |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `42` | `验收` | 9. 完成该切片的本地验证与自动化验收： |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `45` | `验收` | - 新增自动化验收脚本：`scripts/mobile_rpa_harness/verify_standard_flow_scaffold.ts` |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `84` | `验收` | 4. 把当前脚手架验收脚本接入 `Workflow V1` 的固定 exit criteria。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `82` | `验收` | 2. 里程碑验收 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `123` | `验收` | 2. 到达里程碑节点，需要人类验收 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `6` | `PRD` | related: ["../mobile-rpa-ide/mobile-rpa-single-device-projection-cloud-mvp-report-v1.md", "../../business-logic/mobile-rpa-studio-prd-v1.md", "../../../protocol/multi-ai-collaboration.md", "../../../../VOID_CODEBASE_GUID |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `35` | `验收` | 2. **最有效的模式是人类掌舵，不是人类消失。** 人类负责任务拆解、验收标准、风险判断、架构决策和最终放行；AI 负责计划草拟、代码生成、验证迭代、文档和首轮 review。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `157` | `验收` | 1. 定义任务与验收。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `174` | `验收` | H["人类掌舵者<br/>目标 / 优先级 / 验收 / 放行"] --> P["任务卡 / 验收卡<br/>Issue-style brief + PLAN.md"] |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `232` | `验收` | - 验收命令 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `261` | `里程碑` | 3. 顶层公理的升格，仍然应由人类在里程碑节点确认。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `370` | `验收` | - 用 issue 风格写清目标、范围、验收 |

_Truncated: showing 12 of 172 matched lines._

### automation-heartbeat - 持续推进 / 自动唤醒 / heartbeat

- proposed_artifact: `workflow`
- proposed_landing: `Workflow V2 + Codex thread automation`
- why: 重复出现的“继续推进直到 blocker”需求应沉淀为调度能力。

| project_id | file | line | keyword | excerpt |
| --- | --- | --- | --- | --- |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/current-task.md` | `30` | `heartbeat` | - 在首轮扫描稳定后再评估是否进入 `V2` heartbeat 半自动方案 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/session-20260422-1.md` | `14` | `持续推进` | 4. 补建本仓 `CCOS/context/` 任务路由文件，便于后续持续推进。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/session-20260422-1.md` | `31` | `heartbeat` | - 再决定是否进入 `V2` heartbeat 半自动方案 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/session-20260422-2.md` | `33` | `heartbeat` | - `automation-heartbeat` |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/session-20260422-2.md` | `43` | `heartbeat` | 3. reviewer 固定产物与 IDE 交互 smoke 完成后，再进入 `Workflow V2` heartbeat 半自动。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `15` | `controller loop` | - controller loop |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `64` | `controller loop` | 2. `controller loop` 还停留在方案层。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `66` | `heartbeat` | 4. 还未进入 `V2` 的 heartbeat 半自动验证。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `85` | `heartbeat` | 5. 若流程稳定，再进入 `V2` 半自动 heartbeat 方案。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/README.md` | `19` | `持续推进` | - [`ai-dev-harness/README.md`](./ai-dev-harness/README.md)：研发模式 / harness 项目入口，聚焦控制平面、自动审查、持续推进与规则升格。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/README.md` | `18` | `持续推进` | - [`mobile-rpa-ai-harness-engineering-pilot-v1.md`](./mobile-rpa-ai-harness-engineering-pilot-v1.md)：当前研发模式试点方案，明确 harness、自动审查、规则升格、持续推进和 `Hermes-agent` 借鉴边界。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `154` | `heartbeat` | 1. thread heartbeat / automation 唤醒 |

_Truncated: showing 12 of 63 matched lines._

### review-ledger-promotion - 自动审查 / review ledger / 规则候选

- proposed_artifact: `review`
- proposed_landing: `review ledger + reviewer module + verify checks`
- why: 先记录可审计证据，再决定要不要升级为规则、hook 或 skill。

| project_id | file | line | keyword | excerpt |
| --- | --- | --- | --- | --- |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/current-task.md` | `18` | `review ledger` | - 上游同步脚本、镜像能力清单、`AGENTS.md`、`review ledger` 模板 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/current-task.md` | `28` | `人类审核` | - 运行 `void + rpa-mobile` 联邦扫描并冻结第一轮人类审核结论 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `29` | `review ledger` | 4. 新增研发模式主文档与 `review ledger` 模板。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/README.md` | `19` | `自动审查` | - [`ai-dev-harness/README.md`](./ai-dev-harness/README.md)：研发模式 / harness 项目入口，聚焦控制平面、自动审查、持续推进与规则升格。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/README.md` | `18` | `自动审查` | - [`mobile-rpa-ai-harness-engineering-pilot-v1.md`](./mobile-rpa-ai-harness-engineering-pilot-v1.md)：当前研发模式试点方案，明确 harness、自动审查、规则升格、持续推进和 `Hermes-agent` 借鉴边界。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `74` | `候选规则` | 2. 区分必须修复问题、残余风险、候选规则升格项 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `75` | `review ledger` | 3. 将重复问题沉淀到 `review ledger` 格式 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `84` | `规则升格` | 4. 顶层规则升格批准 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `126` | `候选规则` | 5. 发现候选规则需要升格到顶层规则 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `27` | `自动审查` | \| V1.1 \| 2026-04-21 \| 增补自动审查、公理规则升格、自进化记忆、Codex 并行协作工作群、连续运行 controller loop、`Hermes-agent` 借鉴边界与 `rpa-mobile` 现有设计映射 \| |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `50` | `自动审查` | 5. **自动审查是首批应优先落地的能力。** 当前成熟做法不是“一个万能审查模型”，而是“规则层 + hooks + reviewer agent + human gate”的组合。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `66` | `自动审查` | \| reviewer agent / policy hook \| Claude Code 已支持 command hook 与 agent hook；OpenAI 则把持续 review 和后台 refactor task 作为日常机制 \| 当前项目应增加一个“自动审查层”，先按顶层公理与风险清单做机器首审，再决定是否交人 \| |

_Truncated: showing 12 of 40 matched lines._

### rule-promotion - 澄清事项升格为规则或公理

- proposed_artifact: `rule`
- proposed_landing: `AGENTS.md / CCOS/protocol/p0-rules.md / review ledger`
- why: 反复澄清的边界不应继续靠人肉口头重复。

| project_id | file | line | keyword | excerpt |
| --- | --- | --- | --- | --- |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `22` | `单一事实源` | 1. 新增根级与局部 `AGENTS.md`，固化项目边界与来源项目单一事实源。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/context/task-void-ai-dev-harness-mobile-rpa-pilot.md` | `74` | `物理隔离` | 4. 产品主线与研发模式文档必须持续物理隔离。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/README.md` | `19` | `规则升格` | - [`ai-dev-harness/README.md`](./ai-dev-harness/README.md)：研发模式 / harness 项目入口，聚焦控制平面、自动审查、持续推进与规则升格。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/README.md` | `14` | `物理隔离` | 存放“AI 主开发、人类掌舵”研发模式及其控制平面设计文档。当前目录与产品试点文档物理隔离，避免混淆“研发方法”与“交付产品”。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/README.md` | `18` | `规则升格` | - [`mobile-rpa-ai-harness-engineering-pilot-v1.md`](./mobile-rpa-ai-harness-engineering-pilot-v1.md)：当前研发模式试点方案，明确 harness、自动审查、规则升格、持续推进和 `Hermes-agent` 借鉴边界。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `74` | `规则升格` | 2. 区分必须修复问题、残余风险、候选规则升格项 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `84` | `规则升格` | 4. 顶层规则升格批准 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/ai-dev-harness-workflow-v1.md` | `126` | `顶层规则` | 5. 发现候选规则需要升格到顶层规则 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `27` | `规则升格` | \| V1.1 \| 2026-04-21 \| 增补自动审查、公理规则升格、自进化记忆、Codex 并行协作工作群、连续运行 controller loop、`Hermes-agent` 借鉴边界与 `rpa-mobile` 现有设计映射 \| |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `66` | `公理` | \| reviewer agent / policy hook \| Claude Code 已支持 command hook 与 agent hook；OpenAI 则把持续 review 和后台 refactor task 作为日常机制 \| 当前项目应增加一个“自动审查层”，先按顶层公理与风险清单做机器首审，再决定是否交人 \| |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `67` | `规则升格` | \| 规则升格 / memory promotion \| OpenAI 强调把仓库知识当成 system of record，而不是超长 prompt；当前主流实践都在把重复经验升格为 repo 规则、skill 或 hook \| 当前项目应把反复出现的人类 review 意见沉淀成 `AGENTS.md`、规则清单、skill 或脚本检查，而不是继续堆聊天提示词 \| |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `106` | `规则升格` | \| 规则升格 \| 将经验沉淀为 memory 与 skill，并形成 closed learning loop \| 建立 `review ledger -> 候选规则 -> 人类批准 -> AGENTS/hook/verify` 的升格链路 \| |

_Truncated: showing 12 of 40 matched lines._

### skill-promotion - 重复需求沉淀为技能

- proposed_artifact: `skill`
- proposed_landing: `~/.codex/skills + requirement-pool state update`
- why: 高频、机械、可复用的指令应从会话口语升格为技能。

| project_id | file | line | keyword | excerpt |
| --- | --- | --- | --- | --- |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `108` | `共享技能目录` | \| 共享技能目录 \| 支持 `external_dirs` 扫描外部共享 skill 目录 \| 后续可把团队共用 skill 目录从当前仓外置，供多个 AI 工具共用 \| |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `5` | `技能草案` | tags: [需求池, 技能草案, 长期优化, 收尾, 治理] |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `17` | `技能草案` | 1. 可复用技能草案。 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `41` | `做成技能` | 1. 当用户明确提出“收尾总结 / 沉淀坑点 / 做成技能 / 先记进需求池”时，优先回写本文。 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `49` | `收尾技能` | \| `POOL-SKILL-001` \| 收尾技能（任务线/文档/提交收口） \| `skill` \| `implemented` \| `xpeng-stable-baseline` 多轮“同步文档任务线 / 提交代码 / 检查未完成项”场景 \| 继续在真实收尾场景中观察是否需要拆分 session/taskline sync 子流程 \| |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `50` | `收尾技能` | \| `POOL-SKILL-002` \| 受控自进化技能（先并入收尾阶段的升级候选子流程） \| `skill` \| `proposed` \| 2026-04-22 多轮“总结重复纠偏、拓宽排查思路、先查成熟方案再沉淀技能/规则”的连续要求，以及现有 `ccos-self-evolution` 与 `收尾技能` 的组合使用空档 \| 先冻结一版“收尾后自进化扫描”方案：扫描 durable assets、吸收人工反证、补外部成熟方案调研、输 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `72` | `收尾技能` | ### 5.1 `POOL-SKILL-001` 收尾技能（任务线/文档/提交收口） |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `76` | `收尾技能` | - landed_path: `/Users/zhuxiaowei/.codex/skills/收尾技能` |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `83` | `收尾技能` | 1. 已于 `2026-04-16` 落地为可复用技能：`/Users/zhuxiaowei/.codex/skills/收尾技能/SKILL.md` |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `84` | `收尾技能` | 2. 已同步最小 UI 元数据：`/Users/zhuxiaowei/.codex/skills/收尾技能/agents/openai.yaml` |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1427` | `收尾技能` | - `/Users/zhuxiaowei/.codex/skills/收尾技能/SKILL.md` |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1436` | `收尾技能` | 当前仓内已经有一个可用的 `ccos-self-evolution` 技能雏形，也有一个成熟的 `收尾技能`。但两者之间仍有明显空档： |

_Truncated: showing 12 of 24 matched lines._

### known-solution-research - 已知方案 / 开源项目 / 成熟产品调研前置

- proposed_artifact: `skill`
- proposed_landing: `global skill: solution-landscape-research`
- why: 把“先查现成方案再设计/实现”固化为标准研发前置动作。

| project_id | file | line | keyword | excerpt |
| --- | --- | --- | --- | --- |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `307` | `官方文档` | 3. 涉及线上资料时，优先官方文档和官方博客。 |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `647` | `best practices` | 8. OpenAI, **Evaluation best practices** |
| `void` | `/Users/zhuxiaowei/apps/void/CCOS/knowledge/architecture/ai-dev-harness/mobile-rpa-ai-harness-engineering-pilot-v1.md` | `661` | `best practices` | 15. Cursor, **Best practices for coding with agents**, 2026-01-09 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1432` | `开源项目` | - 自进化思路应吸收会话里“总结、沉淀、拓宽排查维度”的方法，也参考现有成熟 AI 产品、开源项目和研究路线 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1490` | `开源项目` | - 当用户明确提出“参考市面上、网络上已有自进化产品/开源项目/研究方案”时，必须先查官方文档和一手资料。 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1504` | `官方文档` | - 当升级项涉及“新技能设计 / 自进化机制 / 长期记忆 / 反思闭环”时，补查官方文档和一手论文。 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1547` | `官方文档` | 1. 基于官方文档和一手论文，补一份“持久记忆 / 反思 / 技能化”的对照笔记。 |
| `rpa-mobile` | `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/patterns/requirement-pool-v1.md` | `1566` | `官方文档` | 5. 若引用外部方案，必须优先官方文档和一手论文，并标清哪些是“借鉴点”，哪些不是当前已实现能力。 |

## Human Review Decisions

| signal_id | decision | landing | notes |
| --- | --- | --- | --- |
| `workflow-stage-template` | `todo` | `scenario workflow packs: clarify -> PRD -> design -> build -> verify -> release` | human approves / rejects / freezes |
| `automation-heartbeat` | `todo` | `Workflow V2 + Codex thread automation` | human approves / rejects / freezes |
| `review-ledger-promotion` | `todo` | `review ledger + reviewer module + verify checks` | human approves / rejects / freezes |
| `rule-promotion` | `todo` | `AGENTS.md / CCOS/protocol/p0-rules.md / review ledger` | human approves / rejects / freezes |
| `skill-promotion` | `todo` | `~/.codex/skills + requirement-pool state update` | human approves / rejects / freezes |
| `known-solution-research` | `todo` | `global skill: solution-landscape-research` | human approves / rejects / freezes |

## Notes

1. V1 scans persisted CCOS assets only. It does not claim to read all raw vendor chat transcripts.
2. Promotion remains human-gated. The scanner only produces candidate evidence.
3. If a signal keeps recurring, promote it into one of: `AGENTS.md`, `p0-rules`, a reusable skill, or a workflow pack.
