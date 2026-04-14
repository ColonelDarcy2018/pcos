# RPA 开发平台导出流程包能力迭代

- taskline_id: `rpa-mobile/outer/rpa-dev-platform-export-iteration`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-04-14 20:30 +0800`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-rpa-dev-platform-export-iteration.md`。

该任务线聚焦“导出 + 完整流程包下发 + 自动增量调试”统一迭代，目标是形成本地调试与后续远程通道可复用的流程包能力基线，并持续收敛 AI 协同开发时的执行可观测性。

## 当前进展（同步摘要）

1. `T1` 到 `T7` 已完成，已具备 `project-only` 导出、`execute_flow_package`、`package_patch` 自动识别与回退等核心能力。
2. `T8/T9` 因远程双通道前置信息不足暂缓。
3. `T10` 已完成 v1：新增“元素拾取 -> selector 草案 -> 占位插入 -> PICK_TASKS 回写”协作链路（Android/Daemon/MCP/插件全链路打通）。
4. 已并入来自 `rpa-dev-platform-multi-ai-device-binding-phase1` 的执行可观测性残差：daemon + Android 补齐按唯一 `job_id` 查询状态与日志的链路。
5. 设备端日志收敛为“ObjectBox 干净日志优先，`adb logcat` 作为补充/保底诊断路径”。
6. 真机已验证设备端新路由返回 JSON，daemon 可按 `job_id` 拿到结束状态与失败/成功日志。
7. 当前进入 `T10` v2 收口阶段：继续处理环境前置提示、多设备隔离回归与协作协议细化。
8. Node 并发路由已迁移为 `task-index + agent-focus`，后续认领/切换按新口径执行。
9. 新增并完成两项高优先级需求：`export_flow_package` 默认导出目录统一收口到案例根 `output/`，插件导出对话框默认定位到该目录；新增 `project/test/**` 本地测试目录约定，并在流程包导出时自动忽略。
10. 已完成“历史执行日志查询”扩展：Android/ObjectBox 新增最近一次运行日志与按开始时间查询日志接口，daemon 改为优先走设备端历史记录并在不可用时回退本地索引；Trae 扩展新增对应 UI 命令。
11. 已冻结“正式流程包是否忽略测试目录”的兼容方案：当前默认行为保持不变，只自动忽略 `project/test/**`；`project/tests/**` 不默认忽略，若后续需要“正式导出不带 `project/tests/**`”，应新增显式开关/profile（建议 `exclude_project_tests`），默认关闭。
12. 已补一轮开发平台微信导航器 SDK 模板同步：
   - `rpa-dev-platform/daemon/core/wechat_navigator_sdk.py` 已重新对齐项目侧 `platform_navigators/wechat_navigator.py` 的最新口径，补上“作者主页空白页最多重试 2 次”和“搜索结果明确无相关结果时直接判目标未命中”两段逻辑；
   - 同时修复 `render_wechat_navigator_module(...)` 在导出作者主页重试日志时会因 `next_retry_count` 被模板层提前插值而触发 `NameError` 的问题；
   - 平台侧回归 `PYTHONPATH=/Users/zhuxiaowei/apps/rpa-mobile/rpa-dev-platform/daemon python3 rpa-dev-platform/daemon/tests/test_wechat_navigator_sdk.py` 已通过，且继续保持“导出 SDK 与项目导航器快照一致”的校验。

## 下一步

1. 补一次真机回归：覆盖“最近一次运行日志”“按开始时间查询日志”“命中运行中任务后切换实时追踪”三条用户链路。
2. 继续推进 `T10` v2：补齐悬浮按钮前置条件提示/自动拉起、拾取回填校验和 selector 优先级规则。
3. 补齐 Java 中转服务协议细节后，再重启 `T8/T9` 双通道整合。
4. 持续本地 ADB 链路回归验证，避免后续远程改造引入退化。
5. 跟进 `project/test/**` 新标准在更多案例上的迁移策略，避免与现有 `project/tests/**` 设备端测试混淆。
6. 若要支持“正式导出不带 `project/tests/**`”，按兼容方案新增显式开关/profile，并在 `entry_file=tests/**` 时做前置阻断，不改当前默认行为。
7. 后续若继续调整项目内微信导航器，必须同步检查 `wechat_navigator_sdk.py` 与 `test_wechat_navigator_sdk.py`，避免导出模板再次落后于项目实现。


## 残差更新（2026-03-11）

Backbone（保持不变）:
1. 开发平台继续以“设备端 ObjectBox 干净日志优先，`adb logcat` 兜底”作为执行可观测性主链路。
2. 插件/daemon 仍要求先绑定唯一 `device_serial`，日志、停止、截图与分析等操作都围绕该设备展开。
3. 历史 `get_execution_status` / `get_execution_logs` 按唯一 `job_id` 查询的链路保持兼容，不回退已有调用方式。

Delta（本轮新增）:
1. Android `HttpServer/BaseHttpServer` 新增 `/api/job_logs_latest` 与 `/api/job_logs_by_start_time`，并通过 ObjectBox 支持跨 daemon 重启后的历史运行日志查询。
2. daemon 新增 `get_latest_execution_logs` / `get_execution_logs_by_start_time` 的 HTTP + MCP 能力，且优先走设备端历史接口；仅当设备端能力不可用时才退回本地运行索引。
3. Trae 扩展新增“查看最近一次运行日志”“按开始时间查看日志”命令，设备树右键可直接触发，并支持命中运行中任务后切换到实时追踪。

## 残差更新（2026-04-09 19:47 +0800）

Backbone（保持不变）:
1. 当前正式/调试导出主链路仍以 `project-only` 为基础，不改变 `entry_file` 可指向 `project/` 内任意已有脚本的能力。
2. 默认自动忽略目录仍只有 `project/test/**`，继续把它视为“本地专用测试目录”。

Delta（本轮新增）:
1. 已核定 `project/tests/**` 当前不能默认忽略，因为仓内已有设备端探针通过 `entry_file=tests/**` 直接下发执行。
2. 正式导出若要进一步排除 `project/tests/**`，必须新增显式导出开关/profile（建议 `exclude_project_tests`），默认关闭。
3. 当显式排除 `project/tests/**` 时，若 `entry_file` 指向 `tests/**`，导出器应直接报错阻断，避免静默打出不可运行的流程包。
