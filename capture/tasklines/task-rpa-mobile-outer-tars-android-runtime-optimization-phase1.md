# 塔斯 App Android 子模块运行时轮询与上报优化 Phase 1

- taskline_id: `rpa-mobile/outer/tars-android-runtime-optimization-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-24 17:00 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-tars-android-runtime-optimization-phase1.md`。

该任务线用于沉淀塔斯 App Android 运行时相关的轮询、门户任务下拉与上报、运行态窗口治理，以及低内存现场诊断能力，避免把 `xp-wx1-simplified` 业务稳定基线与 Android runtime 改造混在同一条任务线内。

## 当前同步结论（摘要）

1. `WorkReportThread` 当前轮询基线为每 `1000ms` 执行一次 `doReport()`，企业版链路按 `requestRemoteJobAsync -> EngineLogManager.report -> ReportManager.report -> MemoryDiagnostics` 顺序运行。
2. 门户远程任务状态机已从早期模糊 `working` 语义，收敛为 `IDLE / TAKING / WAITING_START / STARTING / RUNNING` 五态，并分别设置超时兜底。
3. `STARTING` 明确覆盖“queue 已出队但 running 未建立”的窗口；首次运行态只有在 `reportAndWait(...)` 同步上报成功后，才正式挂载 `running item` 并进入 `RUNNING`。
4. `PortalWorkService.takeWorkToDoPortal(...)` 已补 `requestUuid` 级 `PORTAL_TAKE_TRACE` 日志，并在 `IOException` 路径上按同一个 `requestUuid` 最多请求 `3` 次，退避延迟为 `500ms / 1000ms`。
5. `RpaJobManager.reportRpaItem(...)` 当前已等待“真实上报回调结果”，而不是仅观察异步队列是否清空；同步上报单次等待 `10s`，最多重试 `3` 次。
6. 针对 `s4` 低内存被系统回收问题，Android 侧已补 `MemoryDiagnostics`、`onTrimMemory/onLowMemory`、压力突降日志与 Top 进程诊断，后续可直接复用现场日志排查。

## 下一步

1. 继续用当前 taskline 作为 Android runtime 权威路由，承接后续门户 pull/report 丢结果、轮询窗口、低内存观测和 stop 时序相关问题。
2. 若后续仍出现“门户端已消费、设备端未确认”的疑似丢单，优先围绕 `requestUuid` 幂等语义与最终结果 durable 补偿继续演进，而不是把问题再挂回业务稳定基线任务线。
3. 低内存问题下一步重点不是继续加推断文案，而是利用新增 `MEM_DIAG` 日志抓到更多真实现场，确认是否需要进一步做运行期内存收敛。

## Progress Log

- 2026-03-24 17:00 +0800 已把 Android runtime 相关工作正式路由回本任务线：同步门户 `takeWork/report` 逻辑文档，按真实代码回填五态状态机、`STARTING` 窗口、首次同步上报与同 `requestUuid` 网络重试；同时补齐 `s4` 低内存诊断代码已落地的文档记录
- 2026-03-24 12:00 +0800 已落地两项关键代码改造：`b4cba7ed6b595316a4943d57f571800277e7707e` 为门户 `takeWork` 增加同请求幂等重试与 `PORTAL_TAKE_TRACE`；`ed4656c44bd1c9ecbb16dfa400107c2f8ae93eef` 新增 `MemoryDiagnostics`、`onTrimMemory/onLowMemory` 与压力突降日志
- 2026-03-13 00:18 +0800 已新建塔斯 App Android 子模块运行时优化任务线，记录 `s1` 高频轮询日志问题、10 秒窗口证据、源码根因与推荐修复路径，供后续 AI 直接续做
