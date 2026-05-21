# RPA 开发平台多 AI 并行设备绑定与长期上下文接入 Phase 1

- taskline_id: `rpa-mobile/outer/rpa-dev-platform-multi-ai-device-binding-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-04-13`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-rpa-dev-platform-multi-ai-device-binding-phase1.md`。

该任务线聚焦两件事：

1. 让新 AI 进入 RPA 开发任务时，默认掌握平台长期上下文，而不是依赖偶然命中文档。
2. 在多设备并行、多 AI 并行场景下，要求每个 AI 会话从开始就绑定唯一设备 `device_serial`，后续操作只作用于自己的设备。

## 当前进展（同步摘要）

1. 已确认上下文分层边界：平台长期上下文是通用基线；领域上下文与会话现场上下文按任务动态装配。
2. 已确认多设备底层能力现状：当前 `DeviceManager` 已支持每设备独立本地转发端口，不再把多设备问题定义为传输层缺失。
3. 已更新平台 PRD：补入多设备并行下 AI 设备绑定与上下文分层要求。
4. 已更新规则沉淀文档：明确多设备并行时每个 AI 会话必须绑定唯一 `device_serial`。
5. 已建立 Node+Hub 双侧任务线。
6. `MDB-04` 已执行：技能入口默认加载长期平台上下文，并在多设备场景强制先绑定 `device_serial`。
7. 开发平台用户侧设备选择体验补充：优先展示设备别名，内部继续绑定 `device_serial`。
8. 插件侧已开始落实 MDB-03：去除多设备隐式默认设备回退，停止/日志/截图/分析统一先绑定设备。
9. Daemon 已新增执行证据聚合与结构化失败分析 HTTP 入口。
10. Android 端本地元素拾取已与开发模式解耦，本地读取不再依赖开发模式。
11. Daemon + Android 已补齐按唯一 `job_id` 查询执行状态与 ObjectBox 干净日志的链路，`adb logcat` 保留为补充/保底诊断路径。
12. 已确认真实运行入口在 app 侧 `HttpServer`，并完成真机回归：设备端新路由返回 JSON，daemon 侧可按 `job_id` 收到结束状态与错误/成功日志。
13. Daemon 已默认启用单实例锁；同机第二个实例会直接拒绝启动，避免插件误连旧实例和设备状态分裂。
14. 平台已新增 `/api/devices/{serial}/reconnect`，统一处理“重新探测设备 + 自动拉起塔斯 + 预热恢复”。
15. 真机执行前已不再默认信任 stale cached device；USB 拔插/换机后如果设备真实离线，会直接报“当前不在线或未连接”。
16. VSCode 插件已新增“刷新设备列表”“重新连接设备”命令；无 ready 设备、连接后塔斯未就绪、以及单设备下发失败命中 Tars 连接错误时，都会给出恢复路径。
17. `s2(WKDAUGWGEA75KRCM)` 已实测 reconnect 成功，当前恢复链路可把设备重新拉回 `ready=true`。
18. 插件 VSIX 已重新打包并安装到 VSCode，当前扩展列表可见 `your-publisher.rpa-dev-platform@0.1.0`。
19. 已补记一条高频环境残差：本机可能出现“daemon 进程仍存活并持有 lock，但 `127.0.0.1:8765` 已不再监听”的异常残留态；此时插件侧会报 `ECONNREFUSED 127.0.0.1:8765`，不能误判成设备问题。
20. `s2(WKDAUGWGEA75KRCM)` 现场已完成一次闭环排障：清理残留坏实例后，仅拉起一个新的健康 daemon，`/health` 恢复 `healthy`，`/api/devices` 重新识别到 `s2` 且 `tars_connected=true`。
21. Trae/VSCode 插件已新增 daemon 常驻状态栏与 `RPA: 管理Daemon/启动Daemon/停止Daemon/重启Daemon` 命令，并在设备面板标题区提供入口，后续人类可以直接从 UI 控制 daemon 生命周期。
22. 插件 daemon 启动逻辑已固定为“先查 `/health` -> 查 lock/pid -> 必要时清理残留坏实例 -> 启动新实例 -> 等待 `/health` 通过”，同时把 stdout/stderr 固定写入 `/tmp/rpa-dev-platform-daemon.{stdout,stderr}.log`。
23. 最新 VSIX 已重新离线打包并安装到 Trae 与 VSCode，可直接验证 daemon 管理 UI，而不需要额外手工安装脚本。

## 下一步

1. 在 Trae/VSCode 里补跑 daemon 管理 UI smoke：状态栏显示、点击管理、停止后重启、日志打开与设备树刷新是否一致。
2. 在 VSCode 里补跑“已连接 -> 拔 USB -> 换机 -> 换回 -> 刷新/重连 -> 再下发”的真实 smoke，确认插件端恢复链路闭环。
3. 继续收口插件/平台侧 MDB-03 余项，优先补“一键重连并自动重试本次下发”。
4. 基于已落地的 `job_id` 状态/日志接口与 reconnect 入口，补多设备并行下的真机隔离回归用例。
