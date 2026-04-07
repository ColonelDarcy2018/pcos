# 塔斯 App commander 弱网重试与结果补偿加固

- taskline_id: `rpa-mobile/outer/tars-commander-retry-hardening`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `active`
- updated_at: `2026-04-08 00:08 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内知识基线：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/business-logic/tars-commander-runtime-logic.md`。

本轮 Android 代码提交：
1. `android` 子仓 `9e24e3825eb0baa50fc7e09dffe8e2974b40423b`（`fix(android): harden commander retry stability`）。
2. `android` 子仓 `a2cdd1e0`（`fix(android): harden commander recovery stability`）。

该任务线用于沉淀塔斯 App commander 主链路在弱网下的下载重试、首次运行态/结束态 durable 补偿、进程重启后的 commander 恢复、调试切链和真机证据，避免后续再把“运营平台回报丢失”“包下载失败”“切换 origin/portal 串用鉴权”“杀进程后 commander 会话丢失”等问题散落到更泛的 runtime 任务线里。

## 当前同步结论（摘要）

1. commander 主链路已新增 `PREPARING_PACKAGE` 状态，包准备不再继续占用 `TAKING` 的短超时窗口。
2. `PackageManager` 已补“包详情查询 + zip 下载”有限重试、流式写盘和损坏缓存 zip 可读性校验。
3. 首次 `RUNNING` 与最终结束态同步上报现在都支持 timeout 后继续有限重试；达到上限后会落 `PersistentReportStore` durable 队列，等待后续 replay。
4. `HttpServer` 已新增 `/api/platform_commander_state` 与 `/api/platform_commander_configure`，便于开发平台或真机直接切换 commander 环境并核对设备端真实配置。
5. `CommandManager` 已修复 Portal/Origin 登录切换时的 `AuthService` 单例串用问题；`origin` 上报路径也已把非法非数字 `jobId` 归类为非重试错误，不再进入补偿队列。
6. `CommanderRuntimeStore + BotService START_STICKY + WorkReportThread` 已补齐 commander 会话恢复底座：`developMode`、远程任务状态、关键 `ReportItem` 会落盘；进程重启后能恢复轮询，现场对不上时会补一条 `APP_PROCESS_RESTARTED` 失败态而不是静默丢状态。
7. `ApiRequest` 已拆分 `CONTROL` 与 `DOWNLOAD` 两套 `OkHttpClient` profile；Portal 包缓存也已补 `packagePath/packageMd5/packageSize` sidecar 校验，避免命中过期或错包。
8. 异步心跳和 engine log 现在都具备 durable 回放：普通异步上报默认会落 `PersistentReportStore`，日志批次会落 `PersistentEngineLogStore` 并在后续轮询 replay。
9. 通用包默认口径仍以 `origin` flavor 的通用 `originRelease` 为主，除非特别指定不切 `portal` 包。
10. `s2 / WKDAUGWGEA75KRCM` 已安装通用 `originRelease 2.1.4`（`buildTime=260407_2239`），并完成 release 安装预热、commander 状态查询与杀进程后恢复回归。

## 真机验证证据

1. 包下载重试场景：
   `jobId=93001`、`packageId=93002`，首个下载请求强制 `HTTP 500`，第二次改为 `20s` 慢流成功；最终 `package_attempts=2`，任务成功，且 `PREPARING_PACKAGE` 期间无重复 `takeWork`。
2. 首次运行态 durable 补偿：
   `jobId=93021`，`status=1` 同步上报连续 timeout `3` 次；设备日志出现 `[REPORT_PERSIST] persist ... source=first_running`，后续第 `4` 次 replay 成功，任务本地继续执行并成功结束。
3. 最终结果 durable 补偿：
   `jobId=93041`，`status=5` 同步上报连续 timeout `3` 次；设备日志出现 `[REPORT_PERSIST] persist ... source=final_status`，后续第 `4` 次 replay 成功，服务端最终状态被补齐。
4. 非法 `jobId` 非重试兜底：
   `jobId=bad-id-2` 未产生 pending 文件；日志明确输出“判定为非重试错误，不进入补偿队列”，且上报路径不再抛异常。
5. release 安装与预热：
   `s2` 已覆盖安装通用 `originRelease 2.1.4`，设备确认 `tars_app_version=2.1.4`、`tars_build_time=260407_2239`，开发平台返回 `prepared=true`。
6. 杀进程后的 commander 恢复：
   对 App 执行 `force-stop` 后重新拉起，再查询 `/api/platform_commander_state`，设备端返回 `devModeEnabled=true`、`currentUserPresent=true`、`remoteControl=true`、`remoteWorkStatusName=IDLE`、`persistedRemoteWorkPending=false`；说明 commander 会话与本地开关可以恢复。
7. 重启后设备预热闭环：
   首次重启后 `platform_state` 一度显示 `accessibilityServiceHealthy=false`、`floatingWindowShowing=false`；随后执行平台预热后恢复为 `readyForRpa=true`，证明“极端杀进程”场景下仍需要预热链路兜底，但恢复路径已打通。

## 下一步

1. 继续补齐“脚本执行上下文级”的恢复能力；当前已能恢复 commander 会话与安全收尾，但还不能让运行中的 Python 任务真正断点续跑。
2. 在 `CONTROL / DOWNLOAD` 客户端拆分的基础上，继续把重试退避和 jitter 做 profile 级细分，避免两类流量仍沿用同一套线性 backoff。
3. 扩展非重试错误分类，把参数非法、资源不存在、流程包元数据非法等终态进一步收口成 `origin/portal` 共用的统一错误码策略。
4. 评估是否要给 commander debug 状态接口增加 durable pending 数量、最近 replay 时间和最近失败原因，降低真机排障门槛。

## Progress Log

- 2026-04-07 16:22 +0800 `android` 子仓已提交 `9e24e3825eb0baa50fc7e09dffe8e2974b40423b`：补齐 commander 包下载重试、首次运行态/结束态 durable 补偿、debug commander 配置接口、鉴权单例隔离与非法 `jobId` 非重试兜底；对应 `originDebug` 单测与 `s2` 真机回归已完成
- 2026-04-07 16:26 +0800 已同步项目知识与跨项目任务线，冻结本轮 `s2` 真机证据、提交号和剩余稳定性隐患，后续可直接沿本任务线继续做“进程重启恢复范围 + timeout/重试参数拆分 + 非重试错误码收口”
- 2026-04-08 00:08 +0800 `android` 子仓已提交 `a2cdd1e0`：补齐 commander 会话恢复与安全收尾底座（`CommanderRuntimeStore`、`BotService START_STICKY`、持久化 `developMode`）、拆分 `CONTROL / DOWNLOAD` 网络客户端、为异步心跳与 engine log 增加 durable replay、为 Portal 包缓存补 `md5/size/packagePath` 校验，并在 `s2` 通用 `originRelease 2.1.4` 上完成安装预热、状态查询与杀进程恢复回归
