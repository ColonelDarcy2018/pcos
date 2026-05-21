# 塔斯 APK 打包命名与安装基线

- taskline_id: `rpa-mobile/outer/tars-apk-build-baseline`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-04-13 19:38 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

该任务线用于沉淀塔斯 App 在 `rpa-dev-platform` 中的统一 APK 打包、命名、安装、批量升级和安装后版本确认口径，避免后续 AI 再把“通用包 / Portal 包”“本地 APK 时间戳 / 设备端 buildTime”“安装成功 / 实际版本已切换成功”混为一谈。

本轮关键提交：

1. 根仓 `442556a06ab47a26a0ffa4b51b9845bdefdca8d4`：`docs(rpa-dev-platform): clarify tars apk build rules`
2. 根仓 `ebb73ee`：`feat(rpa-dev-platform): harden tars apk install validation`

项目内长期说明文档：

1. `/Users/zhuxiaowei/apps/rpa-mobile/rpa-dev-platform/docs/TARS_APK_BUILD.md`
2. `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/knowledge/business-logic/rpa-dev-platform-logic.md`

当前源码口径（2026-04-13）：

1. `/Users/zhuxiaowei/apps/rpa-mobile/android/app/build.gradle` 当前 `versionName="2.1.6"`、`versionCode=12`。
2. 本任务线中提到的 `2.1.5` release/signer 冲突结论，属于 `2026-04-09` 的历史验证样本，不应直接当作“当前设备必然仍是该状态”的事实。

## 当前同步结论（摘要）

1. 开发平台默认打的是通用 `origin` 包，不是 `Portal` 包；未特别说明时，本地联调用 `originDebug`，正式发版用通用 `originRelease Standard`。
2. `originRelease Portal` 只在明确指定“门户功能集 APK”时使用，不能因为运行时调度主线走 `ApiType.PORTAL` 就默认选择 `Portal` 构建。
3. 统一命名规则已经收敛为 `TarsAgent_<suffix>_<appVersion>_<YYYYMMDD_HHMM>.apk`，其中设备端能力握手里的 `buildTime` 使用短格式 `yyMMdd_HHmm`。
4. `build_tars_apk`、`install_tars_apk` 和插件命令已经对齐 GitLab CI 的构建口径，其他 AI 继续做 APK 相关操作时应优先复用这些入口，不要再手写零散 Gradle 命令。
5. 安装链路的默认动作已经固定为：亮屏解锁 -> `adb install -r -t -g` -> 如命中 `INSTALL_FAILED_UPDATE_INCOMPATIBLE` 则自动卸载重装 -> 拉起塔斯 -> 设备预热。
6. 安装后现在不再只看“adb install 成功”或“塔斯能拉起”，而是新增了 `version_check` 强校验：会从 APK 文件名解析目标 `appVersion/buildTime`，再用设备端 `platform_info` 返回的 `appVersion/buildTime` 做一致性确认。
7. `version_check` 的阻断场景包括：安装后未能刷新设备信息、未读到 `platform_info`、缺失设备端 `appVersion/buildTime`、或设备端版本与目标 APK 不一致；这些场景不应再当作“安装成功”。
8. `version_check` 的非阻断场景包括：APK 文件名无法解析目标版本、或本次安装流程未自动拉起塔斯；这些场景会保留 warning，但不误报成已强校验成功。
9. 单机和批量安装结果现在都会透出 `version_check`；插件提示文案也会直接展示“版本已校验为 ...”或具体失败原因，减少人工二次判断。
10. “最新版本”不能只看本地 APK 路径或最近一次构建时间，应该同时检查两层证据：本地 APK 文件名时间戳，以及设备端 `tars_app_version + tars_build_time` / `version_check.matched=true`。
11. 已冻结一份“正式 release 真机安装验证”的历史样本：`2026-04-09` 时，`v2.1.5` 正式 release APK 可从标签态成功重建；当时 `s2` 上存在 debug 签名 `2.1.5`，覆盖安装失败根因是 debug/release signer 不兼容（`INSTALL_FAILED_UPDATE_INCOMPATIBLE`），不是 release 构建流程本身失败。
12. 当前源码主线已迭代到 `2.1.6`；后续若要继续使用本任务线做发包/安装判断，必须先重新确认目标设备上的实际 `appVersion/buildTime/signer`，不能直接复用 `2.1.5` 的设备结论。

## 对其他 AI 的直接复用建议

1. 用户只说“打最新 release 包”时，默认理解为通用 `originRelease Standard`，不要默认切到 `Portal`。
2. 用户只说“安装最新 APK”时，优先复用 `install_tars_apk` 或插件安装命令，而不是直接给出裸 `adb install` 方案。
3. 看到 `version_check.matched=true` 才能高置信认为“设备已经切到目标构建”；仅有 `prepared=true` 不等于版本已切换正确。
4. 若安装结果里 `reason=apk_filename_unparseable`，说明 APK 命名没有遵循统一规则；这不是设备问题，而是无法执行安装后强校验。
5. 若安装结果里 `reason=platform_info_unavailable`，应优先判定为设备上的塔斯版本过旧或能力握手异常，而不是简单重试同一个 APK。
6. 若批量升级多台设备，应优先消费每台设备各自的 `version_check`，不要只看批量接口顶层的 `all_succeeded`。
7. 若要在已安装 debug 包的设备上做正式 release 覆盖安装验证，先检查 signer；命中 debug/release 签名不一致时，应优先判定为“设备环境阻塞”，而不是“release APK 不可用”。
8. 若用户要求继续在同一设备验证正式 release，必须先确认是否允许卸载当前 debug 包并清空本地数据/登录态。

## 任务线边界优化

1. 这条任务线只负责“构建 profile 选择、APK 命名、安装/批量升级、安装后版本确认”。
2. 若问题属于 commander 运行期下载、上报、进程重启恢复，优先转到 `tars-commander-retry-hardening` 或 `tars-weak-network-result-delivery-phase1`。
3. 若问题属于“弱网导致平台过程态丢失结果、实时 ACK 不稳、需要长时网络体检”，优先转到 `tars-weak-network-result-delivery-phase1`。

## 下一步

1. 继续评估是否要把“覆盖安装失败后自动卸载重装”的策略再产品化成对混合版本设备群更友好的单键升级工作流。
2. 若后续要支持更多构建组合，应继续复用“统一命名 + 文件名解析 + 设备端版本确认”这条闭环，避免重新出现“装的是哪个包说不清”的问题。
3. 若设备群升级场景继续扩展，可再补“安装后按 `version_check` 聚合统计失败设备”的批量运维视图。
4. 若需要完成“正式 release 真机安装验证”闭环，应先按当前源码版本 `2.1.6` 重新构建 release 包，并优先准备干净设备；若只能复用现有 debug 设备，则先走卸载影响确认，再执行正式安装与版本校验。

## Progress Log

- 2026-04-08 23:44 +0800 根仓已提交 `442556a06ab47a26a0ffa4b51b9845bdefdca8d4`：沉淀 GitLab CI 对齐的 APK 打包命名、通用 Debug/Release/Portal 口径和最新构建识别规则。
- 2026-04-09 09:06 +0800 根仓已提交 `ebb73ee`：安装链路新增 `version_check` 强校验，单机/批量安装返回体与插件 UI 均可直接透出版本确认结果。
- 2026-04-09 11:24 +0800 已补齐跨项目任务线沉淀：把“默认非 Portal、统一命名、安装后强校验、latest 识别规则”抽成可直接复用的稳定事实，供后续 AI 接力时直接参考。
- 2026-04-09 19:47 +0800 已补齐“正式 release 真机安装验证”结论：官方 `v2.1.5` release APK 可从标签态重建，但 `s2` 当前 debug 签名安装包与 release signer 不兼容，覆盖安装返回 `INSTALL_FAILED_UPDATE_INCOMPATIBLE`；继续验证需 clean device 或明确批准先卸载 debug 包。
- 2026-04-13 19:38 +0800 已按当前源码版本 `2.1.6` 重写任务线口径：明确 `2.1.5` signer 冲突仅是历史验证样本，新增任务线边界说明，并把“重新确认设备实际版本/签名后再复用旧结论”提升为默认约束。
