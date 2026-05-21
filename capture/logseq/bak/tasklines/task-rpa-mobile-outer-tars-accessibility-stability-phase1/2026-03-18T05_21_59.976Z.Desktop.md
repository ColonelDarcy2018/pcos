# 塔斯 App 无障碍稳定性与自动重连优化 Phase 1

- taskline_id: `rpa-mobile/outer/tars-accessibility-stability-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `planned`
- updated_at: `2026-03-12 12:26 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-tars-accessibility-stability-phase1.md`。

项目内知识基线：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/business-logic/tars-accessibility-stability-logic.md`。

该任务线用于沉淀“塔斯 App 无障碍服务稳定性与自动重连”方案，目标是在不依赖 adb/root 的前提下，尽量自动恢复“设置已授权但服务未实际绑定”的异常态；若命中系统边界导致无法独立恢复，则进入一致性断开态并提示用户手动修复。

## 当前同步结论（摘要）

1. 已冻结关键结论：仅靠塔斯 App 自身、且不借助 adb/root，无法承诺“系统显示已授权时一定能 100% 自动重新绑定无障碍服务”；真实 bind/unbind 生命周期仍由 Android 系统管理。
2. 已冻结推荐方案：显式拆分 `accessibilitySettingEnabled`、`accessibilityServiceBound`、`accessibilityServiceHealthy` 三类状态，并把元素拾取、悬浮窗、脚本执行、平台预热统一接入“先自愈、后人工修复”的状态机。
3. 已冻结兜底方案：当多轮自愈失败时，App 必须进入一致性断开态；若服务实例仍存活，可评估先调用 `disableSelf()` 再引导用户重授权；若实例已为空，则只能清空 App 可用态并引导用户手动修复系统权限。
4. 已同步预热约束：文件读取权限、获取应用列表权限、开发者模式、悬浮窗权限与悬浮窗显示状态仍纳入统一 gate；其中“悬浮窗打开前先确认悬浮窗权限”在现有代码中已具备基础实现。
5. 已记录真实故障证据：`s2` 在 `2026-03-12 11:38` 左右出现 `captureCurrentWindow: service = null`，但系统设置仍显示塔斯无障碍已授权；到 `11:39`-`11:40` 之间重新授权后才恢复 `onServiceConnected()`。

## 下一步

1. 先按 `ACC-01/ACC-02` 冻结状态模型与自愈状态机，避免先改入口导致语义再次分叉。
2. 再按 `ACC-03/ACC-04` 统一接入 `SettingsHandler`、`RpaEngine`、`ElementHandler`、`FloatyWindowHandler`，并补齐一致性断开态。
3. 最后执行 `ACC-05/ACC-06`，把预热 gate 与真机验收矩阵统一收口，确保后续 AI 能直接照文档推进实现与验证。

## Progress Log
- 2026-03-12 12:26 +0800 已创建塔斯 App 无障碍稳定性与自动重连任务线，并同步项目内任务文档、知识基线与状态机图；冻结“app-only 不能保证 100% 自动重绑，但必须做到双态建模、自愈优先、一致性断开态兜底”的实现方向
