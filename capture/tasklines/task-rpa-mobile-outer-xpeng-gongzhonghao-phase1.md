# 小鹏公众号任务实现 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-gongzhonghao-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-04`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-gongzhonghao-phase1.md`。

该任务线聚焦公众号域一期最小可执行链路（指定链接入口、账号类型约束、D11 采链接边界），并保持与视频号及主线框架解耦。

## 当前进展（同步摘要）

1. 已完成任务线启动步骤 1-3：Node 路由切换、Hub 路由回写、行动计划审阅稿落盘。
2. Node 并发路由已迁移为 `task-index + agent-focus`，不再依赖 `current-task` 单指针。
3. `STEP-4` 已落地：`project/gongzhonghao/` 独立目录、一期参数契约、`actType=41` 适配层映射与对应测试已补齐。
4. 操作原则已冻结：`app.py` 保持稳定基线不改，公众号落地实现统一下沉 `project/gongzhonghao/` 独立目录，便于单测与解耦迭代。

## 下一步

1. 回写 Node 任务索引与认领状态，切回该任务线持续推进 `GZH-04~GZH-07`。
2. 进入 D11 边界定义、回调模板与真机验证清单收敛。
3. 阶段收口前执行 `python3 CCOS/scripts/check_rpa_device_test_convention.py`。

## Progress Log

- 2026-03-04 17:33:45 +0800 任务线启动：完成 Node/Hub 路由同步与行动计划审阅稿落盘，待用户审核后执行。
- 2026-03-04 17:38:00 +0800 用户新增“app.py 冻结 + 独立目录模块化实现”原则，已同步 Node/Hub 任务线文档。
- 2026-03-04 20:15:00 +0800 并发路由迁移：Node 侧改为 `task-index + agent-focus`；`STEP-4` 代码与测试产出已完成。
