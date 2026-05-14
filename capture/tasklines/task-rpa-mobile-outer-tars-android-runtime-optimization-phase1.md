# 塔斯 App Android 子模块运行时轮询与上报优化 Phase 1

- taskline_id: `rpa-mobile/outer/tars-android-runtime-optimization-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-05-14 21:34 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-tars-android-runtime-optimization-phase1.md`。

该任务线用于沉淀塔斯 App Android 运行时相关的轮询、门户任务下拉与上报、运行态窗口治理，以及低内存现场诊断能力，避免把 `xp-wx1-simplified` 业务稳定基线与 Android runtime 改造混在同一条任务线内。

## 当前同步结论（2026-05-14 21:34 +0800）

1. “Android 运行时超时后强杀”现已正式路由到本任务线承接；`xpeng-stable-baseline` 仅保留历史评审结论，不再承担实现。
2. 流程级配置 contract 已冻结：
   - 正式 key：顶层 `inputParam.runtime_timeout_ms`
   - 兼容读取短期允许 `runtimeTimeoutMs` 与 `task_payload.runtime_timeout_ms/runtimeTimeoutMs`
   - 长期文档与平台口径只保留 `runtime_timeout_ms`
3. 设备级 fallback 已冻结：App 设置页新增“默认流程超时”，仅在本次流程未显式下发 `runtime_timeout_ms` 时生效。
4. 运行时行为已冻结：
   - 任务进入 `RUNNING` 后启动绝对墙钟 watchdog
   - heartbeat 不刷新 timeout deadline
   - 到期先 soft stop，再给短宽限期；仍不退出则升级为进程级 kill
   - timeout 最终态必须与 manual stop 分离，并优先持久化 timeout 结果，避免重启后只剩通用 `APP_PROCESS_RESTARTED`
5. 下一轮实现优先级已前移：`CommandWork / RpaJobManager / RpaItem / ScheduleException / Pref / SettingsHandler / SettingsModule / NewSetting.tsx` 是本轮冻结的主改造落点。

## 当前同步结论（摘要）

1. `WorkReportThread` 当前轮询基线为每 `1000ms` 执行一次 `doReport()`，企业版链路按 `requestRemoteJobAsync -> EngineLogManager.report -> ReportManager.report -> MemoryDiagnostics` 顺序运行。
2. 门户远程任务状态机已从早期模糊 `working` 语义，收敛为 `IDLE / TAKING / WAITING_START / STARTING / RUNNING` 五态，并分别设置超时兜底。
3. `STARTING` 明确覆盖“queue 已出队但 running 未建立”的窗口；首次运行态只有在 `reportAndWait(...)` 同步上报成功后，才正式挂载 `running item` 并进入 `RUNNING`。
4. `PortalWorkService.takeWorkToDoPortal(...)` 已补 `requestUuid` 级 `PORTAL_TAKE_TRACE` 日志，并在 `IOException` 路径上按同一个 `requestUuid` 最多请求 `3` 次，退避延迟为 `500ms / 1000ms`。
5. `RpaJobManager.reportRpaItem(...)` 当前已等待“真实上报回调结果”，而不是仅观察异步队列是否清空；同步上报单次等待 `10s`，最多重试 `3` 次。
6. 针对 `s4` 低内存被系统回收问题，Android 侧已补 `MemoryDiagnostics`、`onTrimMemory/onLowMemory`、压力突降日志与 Top 进程诊断，后续可直接复用现场日志排查。
7. `2026-03-26` 新确认一个 tracing 口径：小鹏门户/运营平台里的 `job_id(jobUuid)` 可以表示“可重复运行的门户任务”，不保证单次运行唯一；单次实例应优先靠 `workUuid`、`workExecuteUuid`、`job_log_id`、`start_time` 区分。
8. 针对上面这条口径，daemon 已收口 `by_start_time` 的错误回退逻辑：当设备端已命中具体运行但该运行日志为空时，不再按复用的 `job_id` 二次查询，避免串到同一门户任务的另一轮运行。
9. 设备 `114` 最近三次核查运行（`13:29:08`、`13:30:39`、`13:49:08`）均为成功；其中 `13:30:39` 的空结果已确认是“文章没有评论”。
10. 同一批次成功运行窗口里看到的非致命异常噪音已完成第二轮收敛：
    - 明确属于 app/runtime 治理：`BotIMEService` 未知输入法 ID、`currentPageInfo` 解析链路 null-safe 缺失
    - 由上面问题诱发的外部伴生噪音：搜狗输入法 `InvocationTargetException`
    - 现阶段不再直接归为塔斯自有问题：`CalledFromWrongThreadException`，因为当前 `114` 设备最新命中栈位于微信进程 `ViewRootImpl(29204)`，同窗日志对应 `com.tencent.mm` 页面而非塔斯进程 `rpa-mobile(29387)`
    - 暂按外部 SDK / ROM 噪音观测：`AppMeasurement is not initialized`、`MBrainLocalService SecurityException`
11. 针对“小鹏门户 `job_id(jobUuid)` 可复用、平台 `job_id` 又被拿来当本地执行句柄”的长期混淆，本轮已把下一轮可直接实施的 runtime 重构方案写入主 taskline：核心方向不是全量把 `job_id` 替换成 `workUuid`，而是拆成 `execution_id` 与 `portalJobUuid/workUuid/workExecuteUuid` 两组语义。
12. `2026-03-27` 在 `114 / SC7P95SKY5GIHE8T` 最新日志里又收敛出一类确定性自有噪音：塔斯进程 `32268` 的 `Slow main thread`。其中一条已有明确类名证据：
    - `W/Looper PerfMonitor doFrame ... c=com.aiindeed.mobileagent.app.handler.SettingsHandler$$ExternalSyntheticLambda0`
    - 对应 `SettingsHandler.reopenFloatingWindowAndWait()` 在主线程执行“若已显示则先 hide，再 show CircularMenu”的浮窗重建 lambda
    - 同窗日志可见多层 `Window{... com.aiindeed.mobileagent}` overlay 的 draw/remove、focus 切换与 token 回收，说明这类慢帧与浮窗恢复/预热路径直接相关，而不是纯系统误报
13. 同日已落一小步噪音收敛：`android` 子仓已提交 `d6ab5cbe` `fix(android): harden current page info parsing`；`AgentHandler` 的 `currentPageInfo` 解析已改成 null-safe 字段读取，去掉单独 `NullPointerException` 噪音分支。
14. `2026-04-14` 已完成一轮与本任务线直接相关的 `s2` release 真机回归：`android` 子仓提交 `826369b8` 已修复 `UiSelectorHandler` 高亮等待无超时的问题，`s2 / WKDAUGWGEA75KRCM` 上的 `UiObject.click()` 与 `clickVisible()` 已验证不再把任务吊死；但同机对照也确认“overlay 在场 + 原始坐标点击”仍会影响命中结果，因此运行态后续必须继续拆分“节点点击预览”和“像素点点击”两条链路。

## 本轮实施方案（可直接排期）

1. Phase 0 先做术语收口：把 daemon/MCP/插件里的本地运行句柄明确命名为 `execution_id`，legacy `job_id` 只保留兼容别名；日志统一同时打印 `executionId/portalJobUuid/workUuid/workExecuteUuid`。
2. Phase 1 从 `PortalWorkService -> RpaItem` 入口开始拆语义：新增 `portalJobUuid` 字段，塔斯内部运行主键改为 `workExecuteUuid > workUuid > jobUuid` 的优先级；过渡期 `RpaItem.jobId` 继续承载 runtime `executionId`，避免一次性改穿全链路。
3. Phase 2 升级 `JobLog/ObjectBox/BaseHttpServer`：日志与查询接口补 `executionId/portalJobUuid/workUuid/workExecuteUuid`，并禁止 `by_start_time` 命中后再退回按复用门户 `jobUuid` 取“最近一条”。
4. Phase 3 改 stop/report/runtime lookup：塔斯内部 `stopJob/getLatestExecution` 统一按 `executionId` 解析；门户“要求停止”时优先按 `workExecuteUuid/workUuid` 定位实例。
5. Phase 4 做 daemon/MCP/插件兼容升级：返回体新增 `execution_id`、`portal_job_uuid`、`work_uuid`、`work_execute_uuid`、`job_log_id`，旧调用方继续可用。
6. 回归门禁最少覆盖 3 条：同一门户 `jobUuid` 连跑 2 次日志不串、停止其中一轮不误杀另一轮、旧版 MCP/插件不改调用也能查到这次运行。

## 下一步

1. 继续用当前 taskline 作为 Android runtime 权威路由，承接后续门户 pull/report 丢结果、轮询窗口、低内存观测和 stop 时序相关问题。
2. 若后续仍出现“门户端已消费、设备端未确认”的疑似丢单，优先围绕 `requestUuid` 幂等语义与最终结果 durable 补偿继续演进，而不是把问题再挂回业务稳定基线任务线。
3. 低内存问题下一步重点不是继续加推断文案，而是利用新增 `MEM_DIAG` 日志抓到更多真实现场，确认是否需要进一步做运行期内存收敛。
4. Android runtime 下一轮实现优先级建议：
   - 先开 Phase 0/1，把门户 `jobUuid` 从塔斯内部运行主键职责里拆出来
   - 修 `ScriptRuntime.getClip()`，停止强切未注册的 `BotIMEService`
   - 补全 `currentPageInfo` 的分级降噪，确认缺字段/空页面不再升级成 NPE 或 RuntimeException
   - 继续收口高亮预览链路：节点动作可保留短 preview，但像素点/坐标点击默认不要与 overlay 并发
   - 优化浮窗恢复/预热路径，避免 `SettingsHandler.reopenFloatingWindowAndWait()` 在主线程反复执行 `hideCircularMenu() + showCircularMenu()`
   - `CalledFromWrongThreadException` 先补“进程名/PID/自家类名”采样口径；在抓到塔斯进程栈之前，不再把它当成塔斯自有 crash
5. 若后续要继续提升按开始时间的可观测性，设备端查询接口与 daemon 本地历史索引都应继续向“实例级标识”收敛，避免 `status/jobLogId` 再按复用 `job_id` 取最新值。

## Progress Log

- 2026-04-14 15:24 +0800 已同步本轮高亮预览治理结论：`s2 / WKDAUGWGEA75KRCM` 已安装 `v2.1.6 / buildTime=260414_1347` release 包；`UiObject.click()` 回归任务 `mcpjob_20260414_142631_243258_36371db4` 与 `clickVisible()` 回归任务 `mcpjob_20260414_142714_077947_2f5dc27a` 均成功从 `MiuiSettings` 进入 `Settings$WifiSettingsActivity`，确认“动画等待无超时导致任务卡死”主问题已修住。与此同时，同坐标对照证明残余风险仍在：裸 `automator.click` 基线任务 `mcpjob_20260414_143113_310422_70b220b3` 可在 `160ms` 内成功进页，但 `showNodeHighlightAnimation(bounds) + 原始坐标点击` 任务 `mcpjob_20260414_142931_828374_6fac7d93` 虽然 `raw_click_result=true`、`animation_result=true`，页面仍停留在 `MiuiSettings`。后续运行态必须继续做“节点点击预览 / 像素点点击禁 overlay”分流，而不能把当前 `FLAG_NOT_TOUCHABLE` 误记成完全安全。
- 2026-03-27 16:25 +0800 已继续推进 runtime 噪音任务线：在 114 设备最新日志里确认 `Slow main thread` 至少有一条自有来源是 `SettingsHandler.reopenFloatingWindowAndWait()` 的主线程浮窗重建 lambda；同步落地 `android` 子仓提交 `d6ab5cbe`，开始收敛 `currentPageInfo` 缺字段导致的噪音
- 2026-03-26 16:25 +0800 已同步第二轮 runtime 方案与噪音收敛结论：把门户 `job_id` 语义拆分方案沉淀为可直接迭代的四阶段改造路径；同时修正 `CalledFromWrongThreadException` 归类，当前证据显示它发生在微信进程而非塔斯进程，故从“塔斯自有异常”降级为“目标 App/系统 Accessibility 噪音待继续观察”；仍维持 `BotIMEService` 与 `currentPageInfo` 为 app/runtime 优先治理项
- 2026-03-24 17:00 +0800 已把 Android runtime 相关工作正式路由回本任务线：同步门户 `takeWork/report` 逻辑文档，按真实代码回填五态状态机、`STARTING` 窗口、首次同步上报与同 `requestUuid` 网络重试；同时补齐 `s4` 低内存诊断代码已落地的文档记录
- 2026-03-26 14:52 +0800 已同步本轮结论：提交 `768d563742de3a4960736ddad6c9406b4dbb953b` 收口 daemon 的 start-time tracing 串日志问题；补记门户 `job_id/jobUuid` 可复用、单次运行优先看 `workUuid/start_time/job_log_id` 的排障口径；同时把 114 设备非致命异常噪音按 app 自有问题与外部/ROM 噪音完成首轮分层
- 2026-03-24 12:00 +0800 已落地两项关键代码改造：`b4cba7ed6b595316a4943d57f571800277e7707e` 为门户 `takeWork` 增加同请求幂等重试与 `PORTAL_TAKE_TRACE`；`ed4656c44bd1c9ecbb16dfa400107c2f8ae93eef` 新增 `MemoryDiagnostics`、`onTrimMemory/onLowMemory` 与压力突降日志
- 2026-03-13 00:18 +0800 已新建塔斯 App Android 子模块运行时优化任务线，记录 `s1` 高频轮询日志问题、10 秒窗口证据、源码根因与推荐修复路径，供后续 AI 直接续做
