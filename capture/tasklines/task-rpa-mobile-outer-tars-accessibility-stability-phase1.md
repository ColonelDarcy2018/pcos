# 塔斯 App 无障碍稳定性与自动重连优化 Phase 1

- taskline_id: `rpa-mobile/outer/tars-accessibility-stability-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `paused`
- updated_at: `2026-04-16 18:56 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-tars-accessibility-stability-phase1.md`。

项目内知识基线：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/business-logic/tars-accessibility-stability-logic.md`。

该任务线用于沉淀“塔斯 App 无障碍服务稳定性与自动重连”方案，目标是在不依赖 adb/root 的前提下，尽量自动恢复“设置已授权但服务未实际绑定”的异常态；若命中系统边界导致无法独立恢复，则进入一致性断开态并提示用户手动修复。

## 当前同步结论（摘要）

1. 已完成 `ACC-01` Android 落地：`AccessibilityService`、`AccessibilityServiceTool`、`SettingsHandler`、`RpaPyJob`、`RpaEngine` 等关键入口已统一使用 setting/bound/healthy 三态。
2. `readyForRpa` 与平台预热已切到真实无障碍健康态；“系统设置已勾选”不再单独代表可执行态，且平台状态已补充 `manualRepairRequired`、`healthReason` 与最近连接/事件/root 时间。
3. 已完成关键入口错误码收口：当前能明确区分“无障碍未授权”和“已授权但未运行”，避免再次把两类问题混为一谈。
4. 已完成定向验证：`android` 子仓执行 `./gradlew :app:compileOriginDebugJavaWithJavac` 成功。
5. 已记录外部阻塞：仓库约定检查失败点来自既有测试文件 `examples/mobile-rpa-cases/cases/xp-wx1-simplified/project/tests/test_videohao_executor.py` 缺少 `main(zbot, *args, **kwargs)`，非本任务改动引入，仍需单独处理。

## 下一步

> 2026-04-16 路由收口：`ACC-01` 已完成，`ACC-02` 自愈状态机尚未排期，本任务线暂停。后续需要实现 watchdog/自愈状态机时再恢复。

1. 下一步优先推进 `ACC-02`：补齐短窗口恢复、退避重试、健康心跳与 watchdog。
2. 然后推进 `ACC-03/ACC-04`：把剩余入口统一接入状态机，并补齐一致性断开态与人工修复提示。
3. 最后执行 `ACC-05/ACC-06`：统一预热 gate、日志 tag 与真机验收矩阵。

## Progress Log
- 2026-03-12 12:26 +0800 已创建塔斯 App 无障碍稳定性与自动重连任务线，并同步项目内任务文档、知识基线与状态机图；冻结“app-only 不能保证 100% 自动重绑，但必须做到双态建模、自愈优先、一致性断开态兜底”的实现方向
- 2026-03-18 13:20 +0800 已完成 `ACC-01` Android 实现并同步任务线：无障碍状态已拆成 setting/bound/healthy，平台态与关键入口已切到真实运行态；`android` 子仓 `originDebug` 编译通过，仓库约定检查仅剩外部既有测试文件阻塞
