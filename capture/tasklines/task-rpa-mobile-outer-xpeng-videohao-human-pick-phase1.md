# 小鹏视频号人类拾取与实现策略确认 Phase 1

- taskline_id: `rpa-mobile/outer/xpeng-videohao-human-pick-phase1`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `done`
- updated_at: `2026-04-16 18:56 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-videohao-human-pick-phase1.md`。

该任务线聚焦“视频号域高不确定元素的人类拾取闭环 + selector 草案 + 实现策略冻结”，并与主线框架任务解耦并行推进。

## 当前进展（同步摘要）

1. 已接入视频号主要 actType：`11/12/13/14/15/21/31/32/41/51`。
2. `21` 正式代码稳定性已补强：`collect_tasks.py` 把首个搜索结果等待从 `8000ms` 提升到 `20000ms`，用于降低入口态抖动。
3. `s2` 上已完成正式 `project/app.py` 的 `21` 成功复跑，同一正式任务手动 stop 后，平台 `execution_status/logs` 已统一返回“手动停止”语义。
4. mock readiness、`adb reverse` 诊断树与 PC-hosted mock -> loopback mock 切换条件已固定进文档，后续复跑不再需要重复摸索环境。
5. 当前剩余主问题已收缩为：`21/12` 评论链路阶段信号不足，以及 `31/32/41/51` 的正式回归样例待补。
6. `xp-wx1` 导航层已完成单一路径收口：删除 `project/navigator/` 历史目录，流程/测试统一直连 `project/platform_navigators/wechat_navigator.py`，并补充回归检查防止旧 import 回流。
7. 视频号采集 DTO 已在正式 `xp-wx1` 统一收口：`collect_tasks.py` 改为通过 `project/shared_contracts/collect_dto.py` 构造 `ArticleData / CommentData / AccountData`，避免 21/31/32/41 各自漂移。
8. `s2` 真机探针已验证视频号回调口径：`articleData/commentData` 现直接挂在 `actResultList` 对应 act，且 `snapshot` 返回完整 OSS 可访问 URL。

## 下一步

> 2026-04-16 路由收口：本任务线已归档。视频号 DTO/callback/snapshot 与主要 selector 策略已完成；后续视频号稳定性问题走 `rpa-mobile/outer/xpeng-stable-baseline`，图片评论新能力走 `rpa-mobile/outer/xpeng-image-comment-human-test-phase1`。

1. Backbone：继续基于当前正式代码回归 `21/31/32/41/51`，重点看真实业务数据、评论阶段信号与页面态漂移。
2. Backbone：后续 stop/复跑默认沿用正式 `project/app.py` + 已升级运行时，不再切回临时入口验证。
3. Delta：PC-hosted mock 不满足 readiness 时直接回到环境排查；连续失败且 PC 无访问日志时切 loopback mock。
4. Delta：shared DTO contract 已稳定后，视频号侧后续新增字段默认先改共享模块，再回到具体 task 实现补行为。

## Progress Log
- 2026-03-11 19:20 +0800 已同步视频号采集 DTO shared contract、callback `actResultList` 结构与完整快照 URL 口径；`s2` 真机探针 `http_pkg_20260311_190143_080525_f77ec1e4` 已验证 `articleData/commentData + snapshot` 对客可见
- 2026-03-10 15:10 +0800 已完成 `xp-wx1` 历史 `project/navigator/` 清理，确认重复来源为迁移期本地导航器与平台导出导航器并存，并补文档/测试防止旧 import 回流
- 2026-03-09 16:59 +0800 已同步正式 `21` 成功复跑、同任务 stop 复测、`21` 稳定性补强与 mock SOP 文档
- 2026-03-09 12:30 +0800 已同步 `21` 的 PC-hosted mock 成功闭环、评论迭代 stop 阻塞与 `s2` stop 运行时版本不一致结论
- 2026-03-04 16:42:53 +0800 任务线正式启动：完成路由切换、Hub 回写、认领与写锁登记（步骤 1-3）
- 2026-03-04 16:50:40 +0800 规则调整：冻结 app.py，新增 videohao 模块目录与占位/任务清单测试骨架
- 2026-03-04 17:25:32 +0800 新增 selector 映射层 `videohao/selectors.py` 与测试入口，支持 picker 草稿回填
- 2026-03-04 17:49:00 +0800 继续视频号任务线：补齐 `PICK_TASKS` 状态同步能力；尝试进入 picker 失败（塔斯 App 未检测到）
- 2026-03-04 17:50:00 +0800 阶段校验：`check_rpa_device_test_convention.py` 通过
- 2026-03-06 澄清冻结：视频号筛选链路移除 `searchType`；并定位 picker 需支持独立 window 切换后才能拾取筛选面板
- 2026-03-06 17:25 +0800 运行时适配：关键词筛选执行改为真实点击链路，补 `detectAllWindow()` 支持独立 window 面板，并在返回前自动关闭筛选面板恢复上游页面状态
- 2026-03-06 17:30 +0800 真机结论：在 `s1` 上从微信首页导航进入视频号搜索结果页并完成筛选链路验证，可继续推进剩余视频号点位与完整流程联调
- 2026-03-06 19:05 +0800 主线接入与真机 smoke：`21/31/32/41` 已接入主线；`s1` 首轮真机 smoke 暴露作者主页导航超时与筛选面板/搜索结果列表判定问题
- 2026-03-06 23:10 +0800 互动任务闭环：`12/13` 已补齐日粒度发布时间匹配与视频号域参数忽略口径，`s1` 真机 smoke（点赞/盖楼）双通过
- 2026-03-08 15:40 +0800 `s2` 已完成视频号 `1x actType=13` 与 `11+13+14` 主线 loopback mock 闭环；当前进入“补 `1x` 样例 -> 恢复 `21/3x`”阶段
