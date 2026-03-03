# CCOS 一体化重构设计（全量升级版）

日期：2026-03-03  
状态：待审核  
适用范围：`/Users/zhuxiaowei` 下个人中枢与已纳管项目  
升级策略：不兼容旧命名、旧脚本、旧入口，直接全量切换

---

## 0. 本文定位与更新增量

本文是新的主设计文档，用于取代“KCOS/PCOS 并存语义”的旧方案。  
旧文档保留用于追溯，不作为后续执行基线：

- `meta/ccos-unified-protocol.md`
- `meta/unified-system-redesign-2026_03_03.md`

本次增量（相对旧文档）：

1. 统一命名从候选改为已定稿：`CCOS`。
2. 目录命名全量切换：`pcos` 与 `KCOS` 语义全部升级为 `ccos` 与 `CCOS`。
3. 不做兼容包装，不保留旧脚本转调层。
4. 明确“平台负责通用 Agent，CCOS 只保留治理内核”。
5. 补足“人类认知增益”原则，确保不因治理收敛而损失认知资产化目标。
6. 提供 `ccosctl` 命令规格草案（可直接进入实现评审）。

本轮确认后的执行增量（2026-03-03 第二次更新）：

1. `game_service` 从“延后迁移”调整为“立即纳入联邦治理”。
2. `~` 目录下历史 `KCOS` 内容迁移入中枢并统一到 `CCOS` 语义。
3. 新增使用手册：`/Users/zhuxiaowei/ccos/USAGE.md`。
4. 全量迁移前完成备份归档：`/Users/zhuxiaowei/ccos_migration_backups/20260303_161540`。

---

## 1. 目标与非目标

### 1.1 目标

1. 建立单一心智模型：人和 AI 只理解 `CCOS` 一套体系。
2. 保持项目自治：项目实现与项目知识在项目目录内完成。
3. 建立中枢治理：跨项目任务路由、索引、日报在中枢统一可审计。
4. 保留认知复利：支持人类长期阅读、记忆、复盘、抽象能力提升。
5. 降低 AI 困惑：消除多入口同义、多规则重复、多命名并存。

### 1.2 非目标

1. 不重造通用 Agent 平台能力（执行引擎、通用记忆、通用工具连接）。
2. 不把中枢变成“第二项目仓”。
3. 不追求一次性完美抽象，保留小步演进能力。

---

## 2. 命名与目录全量升级

### 2.1 统一命名

- 系统名称：`CCOS`（Cognitive Collaboration Operating System）
- 中枢层：`CCOS Hub`
- 项目层：`CCOS Node`

### 2.2 目录重命名（目标态）

1. 中枢根目录：`~/pcos` -> `~/ccos`
2. 项目协议目录：`<repo>/KCOS` -> `<repo>/CCOS`
3. 中枢联邦索引：`machine/federation/kcos-index-federated.json` -> `machine/federation/ccos-index-federated.json`
4. 中枢联邦脚本：`aggregate_kcos_index.py` -> `aggregate_ccos_index.py`
5. 统一协议文档：`meta/kcos-pcos-unified-protocol.md` -> `meta/ccos-unified-protocol.md`

说明：本方案明确不维护旧路径兼容别名。

---

## 3. 核心设计原则（防止知识漂移）

### 3.1 平台与系统边界

1. 平台层（Codex/Cursor/Claude Code/Copilot）负责：
   - 通用 Agent 执行
   - 通用上下文/记忆能力
   - 通用工具连接（含 MCP）
2. CCOS 负责：
   - 跨项目治理内核
   - 项目与任务路由标准
   - 人类认知资产沉淀结构
   - 审计与复盘闭环

### 3.2 人类认知增益原则（必须保留）

1. 人机双轨：人类可读层与机器可读层分离，不互相污染。
2. 认知复利优先：知识应从事实逐步升维到模式与原则。
3. 防能力退化：文档必须支持人类独立阅读，不依赖模型上下文。
4. 原始语境保真：`capture` 不做过度结构化改写。
5. Git 可追溯：关键知识与决策必须可 diff、可回滚、可审计。

### 3.3 单一规则源原则

1. 规则正文唯一源放在 `~/ccos/meta/**`。
2. `AGENTS.md` 只做仓库适配差异与执行边界。
3. Skills 只做工作流方法与产出契约。
4. 若出现冲突，以“更严格且符合 `meta` 规则源”的版本为准。

---

## 4. 人类友好目录架构（保留 Logseq/Obsidian 场景）

### 4.1 分层不变，命名升级

```text
~/ccos
├── capture/        # L0 原始认知流（Logseq优先）
├── assets/         # L1 人类知识资产（Obsidian/Markdown优先）
├── machine/        # L2 机器结构（index/schema/graph/registry）
├── workflows/      # 协作流程
└── meta/           # L3 元认知与系统规则源
```

### 4.2 对 Logseq 的处理

1. `capture/` 继续作为 Logseq 读取与写入主入口。
2. `capture/tasklines/` 保留中枢任务线，强调跨项目背景、状态、确认项。
3. `capture/journals/` 保留日报与当天执行语境，不与项目业务文档混写。

### 4.3 对 Obsidian 的处理

1. `assets/` 继续作为长期认知资产阅读层（Obsidian 友好）。
2. 不新增强耦合 Obsidian 专有格式为系统前提，避免工具锁定。
3. 如需增强视图能力，只添加可选配置，不改变目录语义。

### 4.4 是否冗余的判断结论

1. `capture` 必要：承载 L0 原始认知流，防止“只剩结构、失去语境”。
2. `assets` 必要：承载 L1 长期可读资产，服务人类记忆与抽象能力。
3. `machine` 必要：承载 L2 自动化结构，避免反向污染人类文档。
4. 冗余不在目录分层，而在“多命名和多入口脚本”。

### 4.5 去重优化策略（建议纳入执行规范）

1. 单写入口原则：
   - 原始记录只写 `capture/**`
   - 抽象沉淀只写 `assets/**`
   - 机器索引只写 `machine/**`
2. 跨层关联用链接，不复制正文：
   - `assets` 引用 `capture` 来源路径
   - `machine` 引用 `assets` 与 `capture` 的 canonical path
3. 每日流程固定为：
   - `capture/journals` 记录当天上下文
   - 从 `capture` 蒸馏到 `assets`
   - 再由 `ccosctl` 统一生成 `machine` 索引
4. Obsidian/Logseq 仅作为阅读与写作界面，不反向定义系统字段格式。

---

## 5. 联邦治理模型（CCOS Hub x CCOS Node）

### 5.1 基本职责

1. CCOS Node（项目目录）
   - 项目代码修改
   - 项目业务知识
   - 项目上下文与决策细节
2. CCOS Hub（`~/ccos`）
   - 跨项目任务线路由
   - 联邦节点注册与索引
   - 联邦日报与治理审计

### 5.2 强约束闭环

每个任务必须具备：

1. `project_id`
2. `repo_root`
3. `ccos_node`

执行规则：

1. 实现与项目细节在 `repo_root`。
2. 跨项目路由与摘要回写 `~/ccos/capture/tasklines/**`。
3. 任务完成态需通过中枢校验后才可关闭。

---

## 6. `ccosctl` 命令规格草案（V0.1）

### 6.1 设计目标

1. 一个入口覆盖 Node + Hub 治理动作。
2. CLI 命令即协议约束，不依赖提示词自觉执行。
3. 默认输出机器可读 JSON，并提供人类可读摘要。

### 6.2 全局约定

1. 命令名：`ccosctl`
2. 配置文件：`~/ccos/meta/ccos-config.yaml`
3. 返回码：
   - `0`：成功
   - `2`：参数错误
   - `3`：规则校验失败
   - `4`：任务状态冲突
   - `5`：I/O 或外部依赖错误

### 6.3 Hub 命令

1. `ccosctl hub init --root ~/ccos`
   - 初始化中枢目录标准骨架与规则源。
2. `ccosctl hub register-node --project-id --repo-root --node-id --ccos-root --scope`
   - 更新 `machine/federation/project-registry.json`。
3. `ccosctl hub sync-index --root ~/ccos`
   - 聚合各节点 `.index.json`，输出 `ccos-index-federated.json`。
4. `ccosctl hub report daily --date YYYY-MM-DD --root ~/ccos`
   - 聚合联邦日报并回写 `capture/journals/`。
5. `ccosctl hub lint --root ~/ccos`
   - 检查规则源、索引一致性、任务线字段完整性。

### 6.4 Node 命令

1. `ccosctl node init --repo-root <path> --node-id <id>`
   - 初始化 `<repo>/CCOS` 目录与基础协议。
2. `ccosctl node validate --repo-root <path> --node-id <id>`
   - 校验 Node 协议与文档质量门槛。
3. `ccosctl node sync --repo-root <path> --node-id <id>`
   - 生成 Node `.index.json`。
4. `ccosctl node status --repo-root <path>`
   - 输出 node 元信息、索引状态、阻塞项。

### 6.5 Taskline 命令

1. `ccosctl task start --project-id --repo-root --node-id --task-id --title`
   - 在 `capture/tasklines/` 写入任务卡并锁定三字段。
2. `ccosctl task checkpoint --task-id --status --summary`
   - 追加阶段状态，不改写历史记录。
3. `ccosctl task finish --task-id --result --next-actions`
   - 结束任务并触发 Hub 校验。
4. `ccosctl task close --task-id`
   - 仅在 `finish + hub lint` 成功后允许关闭。

### 6.6 强制校验点

1. 缺失三字段禁止 `task start`。
2. `repo_root` 不存在或无 `CCOS` 目录时禁止执行 Node 同步。
3. `task finish` 时若未回写 Hub 摘要则报错 `exit 4`。
4. 规则源版本不一致时禁止关闭任务。

### 6.7 关键命令参数契约（草案）

1. `ccosctl hub register-node`
   - 必选：`--project-id --repo-root --node-id --ccos-root --scope`
   - 可选：`--enabled true|false --default-branch <name> --note <text>`
   - 产物：更新 `machine/federation/project-registry.json`
2. `ccosctl hub sync-index`
   - 必选：`--root`
   - 可选：`--include-disabled --output <path>`
   - 产物：`machine/federation/ccos-index-federated.json`
3. `ccosctl node sync`
   - 必选：`--repo-root --node-id`
   - 可选：`--strict`
   - 产物：`<repo>/CCOS/.index.json`
4. `ccosctl task start`
   - 必选：`--project-id --repo-root --node-id --task-id --title`
   - 可选：`--owner-agent --priority --labels`
   - 产物：`capture/tasklines/<task-id>.md` 与 `task-index.md`
5. `ccosctl task finish`
   - 必选：`--task-id --result`
   - 可选：`--next-actions --followup-owner --followup-date`
   - 产物：任务线完成记录 + Hub 摘要回写 + 校验报告

### 6.8 并发与幂等规则

1. 任务线文件锁：
   - 对 `capture/tasklines/<task-id>.md` 使用 lockfile，避免多 Agent 覆写。
2. 幂等要求：
   - `hub sync-index`、`node sync` 可重复执行且结果稳定。
3. 冲突处理：
   - 若任务状态已终态，`checkpoint` 返回 `exit 4`，并输出当前终态快照。
4. 审计字段：
   - 所有写操作记录 `updated_at`、`updated_by`、`command`。

---

## 7. 技能与 AGENTS 的升级规范（全量模式）

### 7.1 Skills

1. 全局技能目录统一为单源，不允许项目本地副本分叉。
2. 技能文本引用 `~/ccos/meta/ccos-unified-protocol.md`。
3. 技能名中的 `kcos`/`pcos` 前缀统一升级为 `ccos`。
4. 保留“元素拾取协议”等经验证有效的能力段落，不因改名而删减能力。

### 7.2 AGENTS

1. 每个纳管仓库提供最小 `AGENTS.md` 适配层：
   - 执行入口（项目目录）
   - CCOS 回写要求（Hub 摘要）
   - 特定仓约束（测试/工具/目录边界）
2. `AGENTS.md` 不复制规则正文，只引用 `meta` 单源规则与仓库差异。

---

## 8. 实施难点与风险

### 8.1 主要难点

1. 全量重命名会影响现有脚本路径、自动化任务、硬编码文档链接。
2. 多项目批量升级时，mono 仓内外层 Node 需单独校验（例如 `rpa-mobile`）。
3. 大规模文本替换容易误改历史文档，需要明确“执行文档”和“历史记录”边界。

### 8.2 风险控制

1. 先冻结新任务入口到 `CCOS`，避免新增历史债。
2. 对每个项目执行一次“路径重写 + 索引再生成 + 任务线回归”。
3. `game_service` 已结束旧任务线，按常规节点一并纳入迁移校验。

---

## 9. 分阶段执行方案（不兼容模式）

### Phase A：中枢重命名与规则源切换

1. `~/pcos` -> `~/ccos`
2. `meta` 下发布 `ccos-unified-protocol.md` 与 `ccos-config.yaml`
3. 更新中枢 README、workflows、federation 文件命名

### Phase B：项目 Node 全量升级

1. 迁移项目 `KCOS/` -> `CCOS/`
2. 全量替换项目内脚本与文档中的 `KCOS/PCOS` 文本引用
3. 重建各 Node 索引并纳入 Hub 注册表

### Phase C：技能与 AGENTS 统一收敛

1. 全局技能改名改链为 CCOS 语义
2. 项目 AGENTS 统一引用 `~/ccos/meta/ccos-unified-protocol.md`
3. 清理本地技能副本与旧入口文档

### Phase D：`ccosctl` 落地

1. 实现 Hub/Node/Task 命令最小集
2. 把任务完成态绑定到 `ccosctl task finish + hub lint`
3. 日报与联邦索引统一从 `ccosctl` 触发

### Phase E：脚本与命名全量替换（零兼容）

1. 删除或重命名所有 `kcos_*` / `pcos_*` 脚本入口。
2. 将自动化与文档命令全部改为 `ccosctl`。
3. 对旧命名执行仓内扫描，要求剩余引用为 `0` 才允许发布。
4. 保留旧文档仅用于历史追溯，不作为执行入口。

---

## 10. 审核清单（请拍板）

1. 是否确认系统新名为 `CCOS`，并接受“目录与脚本全量重命名、零兼容层”？
2. 是否确认 `capture + assets + machine + meta` 四层全部保留，仅优化边界与命名？
3. 是否确认 `assets` 作为 Obsidian 友好层、`capture` 作为 Logseq 友好层继续长期保留？
4. 是否确认 `ccosctl` 命令集按本文 V0.1 进入实现？
5. 是否确认 `game_service` 立即纳入联邦治理（注册与节点均启用）？
