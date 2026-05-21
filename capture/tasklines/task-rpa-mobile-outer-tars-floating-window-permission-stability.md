# 塔斯 App 悬浮窗权限漂移与预热治理

- taskline_id: `rpa-mobile/outer/tars-floating-window-permission-stability`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `planned`
- updated_at: `2026-04-16 18:56 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-tars-floating-window-permission-stability.md`。

该任务线用于沉淀 `s2` 设备“塔斯悬浮窗丢失，但权限页与‘我的’页面仍显示已开启”的问题排查结论与后续治理方向，目标是先冻结证据链、时间线和建议方案，待后续确认需要实现时再进入开发。

## 当前同步结论（摘要）

1. `s2` 当前异常不是“贴边隐藏”，也不是“悬浮窗对象根本没有创建”；真实问题是系统对 `SYSTEM_ALERT_WINDOW` 的 `AppOps` 已变成 `ignore`，导致窗口实例仍在，但展示被系统可见性策略拦掉。
2. 最近一次明确拒绝悬浮窗的时间点是 `2026-04-07 09:47:03 +0800`；最近一段已知允许窗口是从 `2026-04-03 17:53:45 +0800` 开始，持续 `1d5h4m54s`，在 `2026-04-04 22:58:40 +0800` 左右结束。
3. 塔斯 App 当前对“悬浮窗已开启”的判断存在假阳性：`FloatingPermission.canDrawOverlays(...)` 与 `FloatyWindowManger.isCircularMenuShowing()` 可以继续返回“开启/显示中”，但这并不等价于系统仍允许真正渲染到屏幕上。
4. 当前 `rpa-dev-platform` 的预热确实存在“用 ADB `appops` 兜底临时修复悬浮窗权限”的路径；这能修复当下状态，但在 MIUI / HyperOS 上不是持久保证，可能再次被系统治理。
5. 当前已先并行落一条低风险误触缓解：`RUNNING/NONE_SESSION_RUNNING` 时悬浮按钮的单击/抬手不再展开菜单，只保留长按展开入口，减少流程运行中误触对真机回归的干扰。
6. 上述缓解不改视频号迭代器滑动逻辑，也不改变 `READY` 等非运行态的短按行为；任务结束后状态机自动离开运行态，短按展开会随之恢复。

## 下一步

> 2026-04-16 路由收口：现场证据与方案已冻结，权限漂移主治理暂未启动，保持 `planned`。

1. 若后续决定实现，优先把“手动授权为默认路径、`AppOps` 真实态为权限事实源、渲染就绪校验为显示事实源”作为统一设计前提。
2. 平台预热后续应补“执行前/回到前台后的漂移复检”，避免只依赖一次性预热结论。
3. ADB `appops` 兜底应从默认策略降级为显式 opt-in，仅在明确接受临时修复态风险时使用。
4. 继续观察“运行态短按抑制 + 长按展开”是否足以覆盖误触类问题；若后续仍有误触，再优先从悬浮窗贴边/位置策略继续治理，不回头改业务迭代器滑动逻辑。

## Progress Log

- 2026-04-07 10:59 +0800 已创建悬浮窗权限漂移任务线，并同步项目任务文档、索引和会话摘要；冻结 `s2` 现场证据、关键时间线与后续治理方向，当前维持“只建档，暂不开发”
- 2026-04-09 08:55 +0800 已落一条与权限漂移主问题解耦的运行态误触缓解：Android 悬浮按钮在 `RUNNING/NONE_SESSION_RUNNING` 时短按/抬手不再展开菜单，仅保留长按展开；实现保持 `READY` 态交互不变，也不修改视频号迭代器 `swipe/drag` 逻辑。当前长按时长沿用系统 `ViewConfiguration.getLongPressTimeout()`，任务结束后短按展开会随状态机自动恢复。
