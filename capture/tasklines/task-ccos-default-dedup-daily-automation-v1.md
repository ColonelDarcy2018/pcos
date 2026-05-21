# CCOS 去冗余改造与自动日报闭环 V1

- taskline_id: `ccos/default/dedup-daily-automation-v1`
- project_id: `ccos`
- repo_root: `/Users/zhuxiaowei/ccos`
- ccos_node: `default`
- status: `in_progress`
- updated_at: `2026-04-09 11:24 +0800`

## 背景

目标是在不增加流程负担的前提下，完成 CCOS 的去冗余治理，并建立“AI 生成 + 人类审核 + 自动上报”的日报闭环。

关联知识文档：
`/Users/zhuxiaowei/ccos/CCOS/knowledge/architecture/ccos-governance-dedup-and-daily-automation-v1.md`。

## 当前阶段

1. 架构设计文档已沉淀，形成 V1 指标与边界。
2. 已建立 Hub 与 Node 双层任务路由入口。
3. `git-daily-report` 已形成单仓 Commit-First、联邦 Commit-Only 的自动化主路径。
4. 已确认“日报”至少存在两种合法口径：
   - `证据投影日报`：按单仓/联邦 commit 或 diff 直接生成，适合自动化与审计追踪。
   - `实际工作日报`：面向人类复盘，允许跨仓聚合相关 `repo_root` 的真实提交、当日 journal 与少量未提交语义，但必须显式标注为“实际工作”口径。
5. 已确认一个高频失真点：若在 Hub 只扫描 `ccos` 仓，本体项目的真实代码修复会被压缩成 `docs(taskline)` 同步提交，导致日报只看到“任务线回写”，看不到实际 bugfix。
6. 已确认联邦流程文档一度存在口径漂移：旧版 `workflows/federated-daily-report.md` 仍写“只看 diff”，而当前实现默认是 Commit-Only；后续 AI 必须以 workflow/skill/脚本三者一致口径执行。
7. 已补齐一条实现级安全规则：Diff-Fallback 只允许从文档类文件提取 `DONE/TODO/NOW/WAITING/工时`，避免代码里的 `done/todo` 变量被误判成日报语义。

## 下一步

1. 固化“证据投影日报 / 实际工作日报”双口径命名与入口，避免后续 AI 在同一请求里混用。
2. 为“实际工作日报”补一层跨仓聚合规则：优先按 taskline `repo_root` 或联邦注册表定位项目仓，再决定是否把 Hub 投影提交纳入摘要。
3. 继续实现日报草稿生成、审核门禁与自动上报链路，并把 workflow / skill / 脚本帮助文档保持单源一致。
4. 建立治理指标（漂移率、消费率、审核时长）并持续回写。

## Progress Log

- 2026-04-09 11:24 +0800 已补同步一轮“日报口径治理”上下文：确认 `ccos` 中枢里的 `docs(taskline)` 只是一层任务线投影，不能替代项目仓真实实现证据；后续若用户明确要“今日实际工作”，必须跨仓读取相关 `repo_root` 的提交 / journal / 必要 diff，而不是只扫 `ccos`。同时已把联邦日报 workflow 从旧的“diff-only”描述收口到当前默认 Commit-Only 口径，并补记 Diff-Fallback 只从文档类文件提取 `DONE/TODO/工时` 的实现级约束，避免代码变量被误判成日报语义。
