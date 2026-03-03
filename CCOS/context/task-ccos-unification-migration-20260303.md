# 任务：CCOS 全量迁移与文档同步（2026-03-03）

- task_id: `ccos-unification-migration-20260303`
- status: `done`
- priority: `P0`
- owner_agent: `codex-gpt5`
- updated_at: `2026-03-03 17:35 +08:00`

## 目标

1. 统一命名到 `CCOS`，完成中枢与项目目录迁移。
2. 清理旧入口脚本与联邦索引命名，统一到 `ccos_*`。
3. 将本轮迁移过程纳入 CCOS 任务线并完成文档同步。

## 本次完成

1. 目录迁移
   - `~/pcos` -> `~/ccos`
   - `apps/pcos` 入口迁移为 `apps/ccos`（软链）
   - `~/KCOS` 与项目 `KCOS` 全量迁移为 `CCOS`
2. 脚本迁移
   - `kcos_p0.py` -> `ccos_p0.py`
   - `aggregate_kcos_index.py` -> `aggregate_ccos_index.py`
   - `kcos-index-federated.json` -> `ccos-index-federated.json`
3. 联邦治理
   - `game_service` 已启用并纳入联邦注册
   - 联邦聚合结果：`projects=4 nodes=4 indexed=4`
4. 文档补充
   - 新增 `~/ccos/USAGE.md`
   - 设计文档与协议文档完成 CCOS 化增量更新
5. 备份与回溯
   - 迁移前备份路径：`/Users/zhuxiaowei/ccos_migration_backups/20260303_161540`
6. `ccosctl` 落地
   - 新增统一入口：`~/ccos/scripts/ccosctl`
   - 新增 `hub` / `node` / `task` 子命令最小可用集
   - `node` 命令兼容不同仓库 `ccos_p0.py` 参数差异
7. 协议锚点强约束
   - 为 4 个项目 `CCOS/protocol/p0-rules.md` 与 `ai-playbook.md` 增加 Node -> Hub 元协议锚点
   - `ccosctl hub lint` 新增锚点校验，缺失即失败
8. 联邦治理回归
   - 补齐缺失任务线文档：`capture/tasklines/task-rpa-mobile-outer-remote-control.md`
   - 当前校验结果：`hub lint` 为 `errors=0 warnings=0`

## 关键决策

1. 不保留旧命名兼容层，直接采用 CCOS 新入口。
2. 保留旧文档用于追溯，但执行入口统一到 CCOS 文档与脚本。
3. 任务线记录采用 Node（`CCOS/context`）+ Hub（`capture/tasklines`）双写策略。

## 后续动作

1. 进入日报能力升级：实现“Commit-First，Diff-Fallback”。
2. 将日报入口并入 `ccosctl`（替代分散脚本入口）。
3. 对历史文档库做分批归档标识（执行态/历史态）以降低检索噪音。
