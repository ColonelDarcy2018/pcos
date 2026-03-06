# 小鹏视频号人类拾取与实现策略确认 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-videohao-human-pick-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-06`
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
7. 视频号关键词采集筛选口径已冻结：视频号只处理 `range/sort/videoLength`，`searchType` 仅属于公众号任务筛选逻辑。
8. 新阻塞已定位：微信筛选面板可能以独立 `window` 打开，现有 picker 默认只抓 active window，需要补 `window_index` 切换能力。

## 下一步

1. 将 picker `window_index` / `list_picker_windows` 能力部署到塔斯 App 与 daemon。
2. 在 `s1` 上重新打开视频号筛选面板，先枚举窗口并切到目标窗口后继续 `VHP-04` picker 闭环。
3. 每项 selector 草稿回填后执行 `sync_pick_tasks_markdown`，持续更新 `PICK_TASKS.md`。
4. 阶段收口时执行 `python3 CCOS/scripts/check_rpa_device_test_convention.py`。

## Progress Log

- 2026-03-04 16:42:53 +0800 任务线正式启动：完成路由切换、Hub 回写、认领与写锁登记（步骤 1-3）
- 2026-03-04 16:50:40 +0800 规则调整：冻结 app.py，新增 videohao 模块目录与占位/任务清单测试骨架
- 2026-03-04 17:25:32 +0800 新增 selector 映射层 `videohao/selectors.py` 与测试入口，支持 picker 草稿回填
- 2026-03-04 17:49:00 +0800 继续视频号任务线：补齐 `PICK_TASKS` 状态同步能力；尝试进入 picker 失败（塔斯 App 未检测到）
- 2026-03-04 17:50:00 +0800 阶段校验：`check_rpa_device_test_convention.py` 通过
- 2026-03-06 澄清冻结：视频号筛选链路移除 `searchType`；并定位 picker 需支持独立 window 切换后才能拾取筛选面板
- 2026-03-06 17:25 +0800 运行时适配：关键词筛选执行改为真实点击链路，补 `detectAllWindow()` 支持独立 window 面板，并在返回前自动关闭筛选面板恢复上游页面状态
- 2026-03-06 17:30 +0800 真机结论：在 `s1` 上从微信首页导航进入视频号搜索结果页并完成筛选链路验证，可继续推进剩余视频号点位与完整流程联调

