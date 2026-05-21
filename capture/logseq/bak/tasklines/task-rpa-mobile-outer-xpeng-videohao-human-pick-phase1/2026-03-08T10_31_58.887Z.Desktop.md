# 小鹏视频号人类拾取与实现策略确认 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-videohao-human-pick-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-04`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-videohao-human-pick-phase1.md`。

该任务线聚焦“视频号域高不确定元素的人类拾取闭环 + selector 草案 + 实现策略冻结”，并与主线框架任务解耦并行推进。

## 当前进展（同步摘要）

1. 已完成任务线启动步骤 1-3：Node 路由切换、Hub 路由回写、任务认领与写锁登记。
2. Node 并发路由已迁移为 `task-index + agent-focus`，不再依赖 `current-task` 单指针。
3. 任务状态从“规划中”切换为“进行中（已认领）”，并已按用户指令切回该任务线继续推进。
4. `VHP-01~VHP-03` 已落地：human-pick 占位、selector 映射层、`PICK_TASKS.md` 基线已具备。
5. 本轮新增 `VHP-05` 能力：`PICK_TASKS.md` 可根据 selector 回填状态自动同步（`待拾取/已回填`）。
6. `VHP-04` 真机拾取当前阻塞：设备可连但塔斯 App 未检测到（`tars_connected=false`）。

## 下一步

1. 在设备上启动塔斯 App，恢复 `tars_connected=true`。
2. 继续 `VHP-04` picker 闭环：`start_element_picker -> get_latest_picked_element -> generate_selector_from_picked_element`。
3. 每项 selector 草稿回填后执行 `sync_pick_tasks_markdown`，持续更新 `PICK_TASKS.md`。
4. 阶段收口时执行 `python3 CCOS/scripts/check_rpa_device_test_convention.py`。

## Progress Log

- 2026-03-04 16:42:53 +0800 任务线正式启动：完成路由切换、Hub 回写、认领与写锁登记（步骤 1-3）
- 2026-03-04 16:50:40 +0800 规则调整：冻结 app.py，新增 videohao 模块目录与占位/任务清单测试骨架
- 2026-03-04 17:25:32 +0800 新增 selector 映射层 `videohao/selectors.py` 与测试入口，支持 picker 草稿回填
- 2026-03-04 17:49:00 +0800 继续视频号任务线：补齐 `PICK_TASKS` 状态同步能力；尝试进入 picker 失败（塔斯 App 未检测到）
- 2026-03-04 17:50:00 +0800 阶段校验：`check_rpa_device_test_convention.py` 通过
