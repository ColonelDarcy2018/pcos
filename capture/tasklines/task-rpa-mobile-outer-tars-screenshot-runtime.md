# 塔斯 App 截图链路重构与真机验证（Origin）

- taskline_id: `rpa-mobile/outer/tars-screenshot-runtime`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `done`
- updated_at: `2026-03-04`
- updated_by: `codex(agent-codex-main)`
- related_commits:
  - `apps/rpa-mobile/android`: `aa1b92ee`
  - `apps/rpa-mobile`: `cdead5b`

## 背景

该任务线用于落实“塔斯 App 截图能力”边界修正与 Android 14 问题修复，并按用户要求完成真机端完整链路验证：

1. 截图并获取截图地址
2. 保存全图到塔斯目录
3. 从全图裁剪小图
4. 保存裁剪图到塔斯内部目录
5. 通过日志与设备文件系统双重校验结果

## 完成项（同步摘要）

1. 运行边界纠偏：
   - 明确主改造目标为塔斯 App Android 模块，不以 `rpa-dev-platform` 的 ADB/MCP 截图作为主链路。
   - 明确 `android/uiautomator/src/main/python/packages/*/py/exports.py` 为旧兼容层，不作为主入口。
2. Android 侧能力改造：
   - 新增统一截图入口 `Mobile.CaptureScreenshot(...)`（AUTO/SYSTEM/SHELL/PROJECTION）。
   - 原 `Mobile.ScreenShot(...)` 收敛到 AUTO，兼容存量调用。
   - `ScreenshotObserver` 回调改为优先返回应用本地副本路径。
   - `Image.screenshot()` / `Image.load()` 补齐失败判定与 `Cursor` 安全处理。
   - `zbot` 新增 `captureScreenshot/capture_screenshot/captureExceptionScreenshot`。
3. 约束沉淀：
   - 在项目知识库新增截图运行基线文档并挂到索引，固化“强约束 + 验证口径 + Origin 打包口径”。

## 验证证据

1. 构建与安装：
   - 执行 `android/gradlew -p android :app:installOriginDebug` 成功。
   - 设备安装包为 `com.aiindeed.mobileagent`（Origin 默认版）。
2. 真机脚本完整链路验证：
   - `job_id`: `mcpjob_20260304_202054_564251_cf7b112f`
   - 日志关键结果：
     - `capture_path=/storage/emulated/0/Android/data/com.aiindeed.mobileagent/files/rpa/storage/shot_flow/full_capture.png`
     - `internal_full_path=/storage/emulated/0/Android/data/com.aiindeed.mobileagent/files/rpa/storage/shot_flow_internal_full.png, saved=True`
     - `internal_crop_path=/storage/emulated/0/Android/data/com.aiindeed.mobileagent/files/rpa/storage/shot_flow_internal_crop.png, saved=True`
     - `crop_rect=[480, 1140, 120, 120]`
3. 设备文件系统二次核验：
   - 三个文件路径均存在且可读（全图、内部全图、内部裁剪图）。

## 下一步

1. 在业务流程/异常上报路径中统一切换到 `zbot.captureScreenshot(...)`。
2. 将截图路径纳入上报 payload，统一错误快照结构（异常类型、截图路径、任务上下文）。
3. 若后续新增截图能力，继续遵循“主链路非 ADB、完整链路验证、Origin 调试口径”三项约束。
