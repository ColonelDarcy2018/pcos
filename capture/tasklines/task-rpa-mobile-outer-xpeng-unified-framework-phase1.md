# 小鹏汽车项目通用流程框架 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-unified-framework-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-09 12:09 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-unified-framework-phase1.md`。

任务目标是将小鹏项目“调度接入层 + 参数适配层 + 回传/证据链”落地为可运行最小闭环，并在不破坏稳定主链路前提下持续推进。

## 当前进展（同步摘要）

1. `T11/T15/T16` 已进入“闭环验证 + 收口”阶段，当前主线以视频号 `1x` 与 mock 回传/证据链为优先。
2. `s2` 上已完成两条视频号 `1x` 主线 loopback mock 闭环：
   - 单 `actType=13`：`job_id=http_pkg_20260308_152546_576429_8465a405`；
   - 组合 `11+13+14`：`job_id=http_pkg_20260308_152845_744838_21ad9abf`。
3. `s2` 的 PC-hosted mock 已补回成功样例；当前建议调整为“PC-hosted mock 优先，设备 loopback 兜底”。
4. `s1` 上已用正式 `app.py` 入口再次下发视频号 `actType=13`，并明确当前外部 `scanLimit` 会映射为 `comment_count`，未显式传入时 `video_count` 默认取 `10`。
5. 已新增 `human_test/videohao_act13_like_probe.py` 单文件探针，用于绕开主线直接验证正式 `task_like_data` 链路，支持外部 act13 / 内部 `dianzan` / kwargs 三种入参口径。
6. 已按分层原则完成通用沉淀：selector 唯一性校验、列表容器根节点判定、`project/human_test/**` 单文件 probe 规范，以及 util sdk 新增“数量/唯一性” helper；项目文档仅保留视频号 `21` 时序与评论页 `depth(6)` 等专属残差。
7. 当前剩余主收口项已收缩为：combo act 细粒度缓存更新、通用分组策略抽象，以及 `21/3x` 的后续真机闭环。

## 下一步

1. Backbone：基于当前 `s2 + mock` 基线继续补齐视频号 `1x` 其余单 act 的主线样例与证据。
2. Backbone：再恢复 `21/3x` 真机闭环与组合执行验证。
3. Delta：等待用户审核本轮分层沉淀；若通过，再继续把阶段信号、评论进度缓存等能力沉淀到开发平台与主线回调契约。

## Progress Log
- 2026-03-03 19:22:39 2026-03-03: T19第二刀完成（author_route_navigation + test_author_route_navigation），app.py转兼容封装；下一步T19第三刀
- 2026-03-03 19:29:27 2026-03-03: 将 CCOS/context 核心路由文件纳入 Git 管理，补充 p0-rules/ai-playbook 约束
- 2026-03-04 10:05:15 2026-03-04: execute_flow_package 自动导出默认落到 project_root 上级 tmp/，并补充 cases/*/tmp 忽略规则与API说明
- 2026-03-08 15:40 +0800 `s2` 已完成视频号 `1x actType=13` 与 `11+13+14` 主线 loopback mock 闭环；PC-hosted mock 网络卡点已归类为非业务阻塞
- 2026-03-08 18:24 +0800 新增 `human_test/videohao_act13_like_probe.py`，并同步 `act13` 参数映射、`21` 筛选面板与评论迭代器的近期真机排障结论
- 2026-03-09 12:09 +0800 已完成 selector/单文件 probe/评论容器唯一性规则的分层沉淀；项目文档仅保留视频号专属残差，待用户审核
