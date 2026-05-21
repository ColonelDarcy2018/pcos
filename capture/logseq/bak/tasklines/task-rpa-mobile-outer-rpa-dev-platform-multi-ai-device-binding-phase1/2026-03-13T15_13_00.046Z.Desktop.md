# RPA 开发平台多 AI 并行设备绑定与长期上下文接入 Phase 1

- taskline_id: `rpa-mobile/outer/rpa-dev-platform-multi-ai-device-binding-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-08`
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

## 下一步

1. 在设备端补一个“无悬浮窗前置时的自动提示/自动拉起”优化，降低单文件 smoke 的环境门槛。
2. 继续收口插件/平台侧 MDB-03 余项，并补充用户可见入口文案。
3. 基于已落地的 `job_id` 状态/日志接口，补多设备并行下的真机隔离回归用例。
4. 规划多 AI 多设备真机并行回归用例，验证互不串台。
