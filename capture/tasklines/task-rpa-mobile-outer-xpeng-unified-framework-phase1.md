# 小鹏汽车项目通用流程框架 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-unified-framework-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-02`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-unified-framework-phase1.md`。

任务目标是将小鹏项目“调度接入层 + 参数适配层”落地为可运行最小闭环，并在不破坏稳定主链路前提下持续推进。

## 当前进展（同步摘要）

1. `T12/T13/T14/T18` 已完成，覆盖参数适配、ping 任务、养号映射、适配层单测。
2. 进入实现优先阶段，待推进 `T11/T19/T15/T16/T17`。
3. 当前活动任务线仍为该任务（见项目内 `task-index.md` 的 `active_task_id`）。

## 下一步

1. 优先推进 `T11`（调度接入层最小落地）。
2. 小步推进 `T19`（`app.py` 渐进重构）并保持评审节奏。
3. 跟进 `T15/T16` 完成回调映射与回归验证清单。
