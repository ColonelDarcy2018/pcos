# 小鹏稳定基线任务线

- taskline_id: `rpa-mobile/outer/xpeng-stable-baseline`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-20 02:08 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-stable-baseline.md`。

该任务线用于沉淀小鹏相关“稳定基线”改造项，避免零散审查结论散落在会话里。当前已冻结的首个待办，是 `xp-wx1-simplified` 删除旧结果兼容层、只保留 XP callback 与 mock 返回链路的实现方案。

## 当前待办（同步摘要）

1. `SB-01`：删除 `xp-wx1-simplified/project/result_body.py`，移除视频号执行结果的旧 `status/task_type/result_data` 包装层。
2. `SB-02`：移除 `execution.py` 中的 `resultData/legacyResult` 中间层，内部结果直接收口到 `actResultList[*]`。
3. `SB-03`：让 `reporting.py` 的 callback 与 mock seed 都直接消费同一份 `actResultList[*].accountData/articleData/commentData`。
4. `SB-04`：同步 `case.yaml`、`README.md` 与测试，确保后续 AI 可直接按冻结方案落地。
5. `SB-05`：修复 `actType=21` 的 `articleData.pubTime/pubTimeStr` 换算错误，避免出现 `1773225188` 这类与真实发布时间不一致的时间戳。
6. `SB-06`：优化 `actType=21` 默认筛选条件；当条件为“不限/范围不限”等默认值时跳过筛选交互。
7. `SB-07`：修复 `actType=21` 筛选后的结果页刷新等待；筛选生效后需等待页面刷新完成，再继续点击视频卡片。
8. `SB-08`：把 simplified 新引入的 `project/shared_contracts/collect_dto.py` 等 shared DTO contract 代码拍平，去掉不符合当前项目风格的额外共享层级。
9. `SB-09`：把 simplified 的设计思想正式沉淀成文档/守则，作为后续重构和代码评审的判断基线。
10. `SB-10`：补齐 `3x` 任务在创作者页内搜索视频标题、点击首个结果并进入播放页的真实链路。
11. `SB-11`：增强 AI 自动化标准测试链路，记录每次执行对应的 XP callback body，并把 `task_payload.callbackUrl` 收口为本地 mock override；仅本地地址可直接回调 mock，非本地地址不再兼容为 override。元数据固定从 `examples/mobile-rpa-cases/cases/common_mock_callback_service/` 目录读取。
12. `SB-12`：在其他需求全部完成后，按最新 AI 标准测试链路文档做一轮统一完整回归；为提效允许跳过 `51`，回归取数固定看 `examples/mobile-rpa-cases/cases/common_mock_callback_service/`，并默认优先复用已冻结的 `爱吃波客 / sphkEaNwwJj1TZH` 稳定基线。
13. `SB-13`：持续维护 dispatch-integration `14-20` 子文档里的稳定基线样例；当前每个子文档都已补 1 条 `爱吃波客` 定向 case，后续补跑时只追加执行残差，不删除原 `小鹏汽车` 样例。
14. `SB-14`：统一 `1x/3x` 的 creator 级规划口径；同一创作者分组内若只有 `1` 个 act，则保持 `single plan`；若存在多个 act，则走 creator 级 `combo plan`。命中策略上，单 act 默认“创作者页搜索优先、失败后迭代兜底”，combo 默认按视频流迭代匹配。
15. `SB-15`：统一“采完即停 / act 做完即退 / task 做完即结束”的退出口径；该规则同样覆盖采集类任务，pending groups 清空后不再继续执行 `iter_video(...)`。
16. `SB-16`：统一关键成功截图策略；失败/异常截图继续放通用框架，非采集 act 与 `51` 养号动作在核心动作完成后通知执行层统一截图，当前统一延迟 `2s` 再拍，并保留“接成功判定” TODO。
17. `SB-17`：新增一份 dispatch-integration 标准风格的回归测试用例文档，覆盖采集类采完即停、`1x/3x` 单目标搜索/多目标迭代、关键成功截图与 `51` 成功截图；当前落盘路径为 `CCOS/knowledge/business-logic/xpeng-project/dispatch-integration/25-视频号退出时机与关键成功截图回归测试用例-v1.md`。
18. `SB-18`：补齐未命中目标视频/评论的细节失败提示；视频侧需区分“标题不匹配”与“标题命中但发布时间不匹配”，评论侧需区分“评论文本不匹配”与“评论作者不匹配”，并在最终失败信息中附有限样例与已扫描计数。当前先冻结方案，不在本轮实现。
19. `SB-19`：执行层内部收口 `single/combo` 两套入口；后续按任务族收口为两个内部核心执行器，分别覆盖 `1x` 与 `3x`，`single/combo` 仅保留为 planning 与 act 结果绑定元数据。当前方案已冻结，尚未实现。

## 下一步

1. 认领本任务线后，优先在 `xp-wx1-simplified` 内按“设计守则冻结 -> 结果链拍平 -> `21` 修复 -> `3x` 链路补齐 -> callback body 记录增强 -> 最终完整回归”的顺序推进；不要先动 `xp-wx1` 正式版。
2. 实施期间保持已稳定的 callback/STS/OSS/signature/retry 链路不变，避免把“结果结构收口”与“网络稳定性改造”混成一轮。
3. 若后续要继续收口公众号或正式版，再基于该任务线新增子需求，不直接覆盖当前冻结方案。
4. 若补跑 AI 标准链路或 OpenAPI 文档样例，默认先从 `41 -> 21 -> 3x -> 1x` 的 `爱吃波客` 稳定基线取数，再决定是否回切 `小鹏汽车` 对照样本。

## Progress Log
- 2026-03-20 02:08 +0800 已把“内部收口重构”方案同步进任务线：当前只修复了 `1x/3x` planning 层的单 act / combo 规划语义，并新增统一 family 选路 helper；executor 内部 `single/combo` 统一执行器方案已冻结为 `SB-19`，明确后续按 `1x/3x` 两个族级核心执行器推进，当前暂未实现
- 2026-03-19 11:09 +0800 已完成 `task_payload.callbackUrl` 规则收口：本地 `127.0.0.1/localhost` 时 simplified 直接回调 mock、不再双发 XP 正式 callback；未传时继续走正式 XP callback；显式非本地地址按参数错误处理。相关代码、测试、mock README、标准链路与回归用例文档已同步，且本地回归与 `check_rpa_device_test_convention.py` 已通过
- 2026-03-17 23:17 +0800 已把“未命中目标视频/评论细节失败提示”的后续方案冻结到稳定基线任务线：视频侧拟补标题/发布时间两类诊断采样，评论侧拟补文本/作者两类失配摘要；当前先记任务，不在本轮实现
- 2026-03-13 00:15 +0800 已继续收 `execution.py` 的 plan 内 act 结果更新样板：新增同级小 helper 统一“标记 act 成功/失败并同步 executed_ids/failed_ids”，减少 `_execute_single_plan(...)` 中重复的状态写回样板，并补 `test_execution_snapshot.py` 保护
- 2026-03-13 00:06 +0800 已继续收 `planning.py` 的 creator/combo 计划样板：新增轻量 `item_payload/source`、creator combo payload 初始化与 `use_author_home_search` 统一收尾，减少 `1x/3x` 组合计划的重复组装代码，并补 `test_planning.py` 保护作者与最大 loop count 口径
- 2026-03-12 21:10 +0800 已继续收 `planning.py` 的 creator/combo 计划样板：补了轻量 `item_payload/source`、combo payload 初始化和 `use_author_home_search` 统一收尾 helper，减少 `1x/3x` 组合计划重复组装代码，并补 `test_planning.py` 保护作者与最大 loop count 口径
- 2026-03-12 21:03 +0800 已继续推进 `app.py` 薄入口化：`task_type` 提取、内部失败码映射、手动停止文案等入口共识已继续下沉到 `xp-wx1-simplified/project/dispatch_common.py`，`app.py` 不再依赖 `execution.py` 私有 helper，并补了 `test_dispatch_common.py/test_entry.py` 保护
- 2026-03-12 20:46 +0800 已补一轮结构收口与平台同步：`xp-wx1-simplified/project/dispatch_common.py` 收口 `unwrap/attemptsId/stopping/snapshot split` 共识，`execution.py/reporting.py/param_adapter.py/planning.py` 已开始复用；同时开发平台 `wechat_navigator_sdk.py` 已同步“创作者主页首个视频只允许在头部 anchor parent 作用域内等待 RecyclerView，禁止全页 fallback”这一稳定规则，并补了保护测试
- 2026-03-12 20:10 +0800 已将 `SB-14 ~ SB-17` 同步进稳定基线任务线：creator 级 combo 规划、采完即停退出口径、关键成功截图 2s 延迟方案以及配套人工回归测试文档已开始落地
- 2026-03-12 16:27 +0800 已把 `爱吃波客 / sphkEaNwwJj1TZH` 冻结为当前文档级稳定基线：dispatch-integration `14-20` 子文档各新增 1 条定向 case，后续只做残差追加并保留原 `小鹏汽车` 样例
- 2026-03-11 21:55 +0800 已创建小鹏稳定基线任务线，并冻结 `xp-wx1-simplified` 删除 `result_body.py` / `legacyResult` / `resultData`、统一 callback 与 mock 数据源的实施方案，供后续 AI 直接认领实现
- 2026-03-11 22:02 +0800 已追加两项 `actType=21` 稳定性待办：修复 `articleData.pubTime/pubTimeStr` 时间换算，以及在“不限/范围不限”等默认条件下跳过筛选交互
- 2026-03-11 22:06 +0800 已追加 `SB-07`：`actType=21` 点击筛选条件后需等待结果页刷新完成，再继续点击视频卡片；页面刷新较慢，不能沿用当前短等待
- 2026-03-11 22:11 +0800 已追加 `SB-08`：simplified 新提交的 shared DTO contract 模块后续也要拍平，保持项目继续符合“少分层、易维护”的设计风格
- 2026-03-11 22:16 +0800 已追加 `SB-09`：需把 simplified 的设计思想正式沉淀成文档/守则，作为后续重构与代码评审的判断基线
- 2026-03-11 22:36 +0800 已追加 `SB-10`：补齐 `3x` 任务在创作者页内搜索标题、点击首个结果并进入视频播放页的真实链路，并记录了具体 selector / 等待 / 点击实现方式
- 2026-03-11 22:42 +0800 已追加 `SB-11`：基于 AI 自动化标准测试链路文档，后续需新增每次执行对应的 XP callback body 记录，并调整流程回调逻辑为“真实 XP callback body 单一来源；若传 mock url，则 mock 与正式链路共用同一份 body”
- 2026-03-11 22:49 +0800 已追加 `SB-12`：当前任务线其他需求全部完成后，再按最新 AI 标准链路文档做统一完整回归；为提效允许跳过 `51`，并补了一版推荐开发顺序供后续审核
- 2026-03-11 22:53 +0800 已补充元数据取数口径：后续 AI 在查看 callback body / seed / 执行回归证据时，固定从 `examples/mobile-rpa-cases/cases/common_mock_callback_service/` 目录读取
