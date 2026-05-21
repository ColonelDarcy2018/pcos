# 小鹏汽车项目通用流程框架 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-unified-framework-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-09 20:12 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-unified-framework-phase1.md`。

任务目标是将小鹏项目“调度接入层 + 参数适配层 + 回传/证据链”落地为可运行最小闭环，并在不破坏稳定主链路前提下持续推进。

## 当前进展（同步摘要）

1. 安装/升级固定链路已平台化：`rpa-dev-platform` 新增 `/api/devices/{serial}/install-apk` 与 `/api/devices/{serial}/prepare`，统一收口亮屏、解锁、HTTP readiness、无障碍与悬浮按钮恢复。
2. Android 运行时已补 `/api/platform_state`、`/api/platform_prepare`，`s2` 实机升级安装后已返回 `prepared=true`。
3. `execution_status` 与 `execution_logs` 的手动停止口径已统一到 `32/手动停止/任务被手动停止`；对客回调继续保持 `50012`。
4. 新 `13-20` 测试文档矩阵已成为默认真机回归基线，`s2` 上已完成一轮按矩阵执行的 `4.1 ping / 4.4 control / 2x / 3x / 4x` 联调记录，长结果统一索引到 `21-视频号与任务控制接口新一轮真机联调运行记录索引-v1.md`。
5. 本轮真机结论已沉淀：`VH21-COMMENTS` 通过；`VH21-POSTS` 暴露筛选锚点问题；`VH21-FULL` 命中 `NoneType.child`；`VH41` activity 漂移；`VH31+32` 仍受 `HUMAN_PICK_REQUIRED` 阻塞。
6. mock readiness / SOP / 诊断树已落文档，PC-hosted mock 失败且 PC 无访问日志时可直接切 loopback mock。
7. 通用框架已新增 `actResult.snapshot`：每个 act 完成后尝试截图并上传，截图前/后固定延迟 `0.5s/2s`，combo 本地执行器优先在 act 边界回填。
8. `rpa-dev-platform` 已新增通用执行预检：执行前自动 reconnect/拉起塔斯、宿主机 URL 探活、从 `input_params` 自动提取 `localhost/127.0.0.1` 端口并执行 `adb reverse`；mock 启动与业务样本前置条件仍保留在流程域。

## 下一步

1. Backbone：继续基于已升级运行时和正式 `project/app.py` 修复 `21` 的筛选锚点 / 空节点问题，并复跑 `2x` 主链路。
2. Backbone：补齐 `41` 页面态漂移与 `31/32` human-pick 阻塞的定向修复，再按新矩阵复测。
3. Delta：将项目侧 runner / 模板接入通用执行预检参数，同时保持 mock 启动与业务样本准备继续沉淀在流程域 SOP。

## Progress Log
- 2026-03-09 20:12 +0800 已同步新测试矩阵真机结果与通用执行预检沉淀：`4.4/4.1/2x/3x/4x` 结果已入库，平台层现可自动 reconnect/拉起塔斯/host preflight/localhost adb reverse
- 2026-03-09 18:10 +0800 已同步 act 级截图字段、固定截图延迟策略与 combo observer 单测结论
- 2026-03-09 18:20 +0800 已完成 act 级截图定向验证与 CCOS 规范校验，当前可进入主仓提交；后续仅待补一条真机 mock/OSS 样例
- 2026-03-09 18:44 +0800 已从源 `.docx` 抽取 46 条视频号测试用例，并补齐 `13-20` 文档矩阵；当前未实现/需人工锁前置的场景已统一沉淀到待人工处理清单
- 2026-03-09 16:59 +0800 已同步安装升级平台化链路、stop 查询统一口径、正式 `21`/stop 复测与 mock SOP 文档
- 2026-03-09 12:30 +0800 已同步 `21` 的 PC-hosted mock 成功闭环、评论迭代 stop 阻塞与 `s2` stop 运行时版本不一致结论
- 2026-03-03 19:22:39 2026-03-03: T19第二刀完成（author_route_navigation + test_author_route_navigation），app.py转兼容封装；下一步T19第三刀
- 2026-03-03 19:29:27 2026-03-03: 将 CCOS/context 核心路由文件纳入 Git 管理，补充 p0-rules/ai-playbook 约束
- 2026-03-04 10:05:15 2026-03-04: execute_flow_package 自动导出默认落到 project_root 上级 tmp/，并补充 cases/*/tmp 忽略规则与API说明
- 2026-03-08 15:40 +0800 `s2` 已完成视频号 `1x actType=13` 与 `11+13+14` 主线 loopback mock 闭环；PC-hosted mock 网络卡点已归类为非业务阻塞
- 2026-03-08 18:24 +0800 新增 `human_test/videohao_act13_like_probe.py`，并同步 `act13` 参数映射、`21` 筛选面板与评论迭代器的近期真机排障结论
- 2026-03-09 12:09 +0800 已完成 selector/单文件 probe/评论容器唯一性规则的分层沉淀；项目文档仅保留视频号专属残差，待用户审核
