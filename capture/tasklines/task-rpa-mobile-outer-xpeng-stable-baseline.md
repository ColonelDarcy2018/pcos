# 小鹏稳定基线任务线

- taskline_id: `rpa-mobile/outer/xpeng-stable-baseline`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-04-14 20:25 +0800`
- updated_by: `codex(agent-codex-main)`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-stable-baseline.md`。

该任务线用于沉淀小鹏相关“稳定基线”改造项，避免零散审查结论散落在会话里。当前已冻结的首个待办，是 `xp-wx1-simplified` 删除旧结果兼容层、只保留 XP callback 与 mock 返回链路的实现方案。

## 当前收尾结论（2026-04-13 20:30 +0800）

1. 本轮已补齐“需求池 + 收尾治理 + 公众号云端样本认知”的同步收口：
   - 新增 `CCOS/knowledge/patterns/requirement-pool-v1.md` 作为跨任务需求池入口，并把“收尾技能（任务线/文档/提交收口）”以 `POOL-SKILL-001` 正式入池。
   - 已把三条新坑点冻结到平台规则文档：
     - 云端历史 runtime 与当前仓库代码不能混看；
     - portal engine log 中间“流程运行成功”日志不能替代最终结果体；
     - `network/page exception` 文案必须保留真实页面锚点。
2. 公众号 `workUuid=31f568a9eac85bff67f476af05c699b4` 的复盘结论已澄清：
   - 失败点仍是指定链接文章页 `profileBt` 单锚点等待超时；
   - 但该样本 runtime 实际仍是旧 `50000ms` 等待，不是当前仓库已升级到 `90000ms` 的时间切片；
   - 因此该样本更适合作为“旧基线页面未 ready / 页面加载慢”历史证据，而不是“当前修复仍无效”的结论。
3. 当前 worktree 已落一处低风险修正：`dispatch_common` 现会把 `查找元素文章链接结果页面判定 超时` 收口为 `网络加载/页面异常: 文章链接结果页面等待超时`，不再误写成“视频搜索结果页面等待超时”；脚本式测试入口与 `check_rpa_device_test_convention.py` 已通过。

## 当前补充结论（2026-04-14 10:45 +0800）

1. 已收口作者主页进片异常页的恢复策略：
   - `MMFTSSearchTabWebViewUI` 默认按“搜索链路中间态/加载态”处理，回退后优先重试原卡片 1 次；
   - 若同一候选重复命中 `MMFTSSearchTabWebViewUI`，再升级为尝试下一张卡片；
   - `AppBrandPluginUI` 继续按“页面偏航到异常分支”处理，回退后优先尝试下一张卡片。
2. 已冻结一条排障认知：`AppBrandPluginUI` / `MMFTSSearchTabWebViewUI` 的 Activity 名称真值来自设备运行时 `zbot.app.getCurrentActivityName()`；“它属于什么页面语义”是解释层，不应反过来覆盖 Activity 真值。
3. 项目侧导航器与开发平台镜像导航器已同步同一恢复口径：`examples/mobile-rpa-cases/cases/xp-wx1-simplified/project/platform_navigators/wechat_navigator.py` 与 `rpa-dev-platform/daemon/core/wechat_navigator_sdk.py` 已完成同步，案例侧单测与仓级 `check_rpa_device_test_convention.py` 已通过。
4. 本轮原计划补 `s2` 真机回归，但执行时本机 `adb` 与开发平台均未发现在线设备；该项保留为后续残差，不把“未拿到真机结论”误记为“已回归通过”。
5. 作者主页进片恢复口径已再次收窄：当前保留“`MMFTSSearchTabWebViewUI` 先完整等待 `20s` 再回退并重试原卡片 1 次”，若同一候选第二次仍命中该 Activity，则直接按 `网络加载/页面异常` 失败收口，不再切下一张卡片；`AppBrandPluginUI` 的偏航恢复策略保持不变。

## 当前补充结论（2026-04-14 16:08 +0800）

1. `workUuid=d6574f612603e20a31599f6bade78edd` 的根因边界已重新收口：
   - 云端截图明确停在微信搜索 `全部` tab，页面文案为“暂无相关结果 / 你可尝试更换搜索词”；
   - 因此这类样本不再按“脚本找不到创作者主页入口按钮”理解，也不再尝试“切 `账号` tab 重试”。
2. 项目侧导航器已按最小策略调整：
   - 若当前 Activity 仍为 `MMFTSSearchTabWebViewUI`，且页面明确命中“无相关结果”提示，则直接抛 `未找到目标创作者：<author_id>；微信搜索结果无相关结果`；
   - 不扩导航策略面，不改变既有人类已验证的“搜索命中后直接进入账号主页”主路径。
3. 失败分类已确认复用现有口径，无需新造一套：
   - `dispatch_common` 已存在内部 `target_not_found` 分类；
   - 该类样本当前对客文案统一收口为 `目标未命中: ...`，上游可按“给定参数/目标查无结果”处理；
   - 当前事实仍是它映射到对客 `failReason=31`，尚未拆出新的 public code，本轮不扩大改动面。
4. 本轮已同步撤回一次错误方向：
   - 先前短暂尝试过“`全部` 无结果时切 `账号` tab 重试主页入口”的窄兜底；
   - 经用户确认后已完整撤回，仅保留“无结果即目标未命中”这一更符合上游处理预期的收口。
5. 验证口径：
   - 导航器定向测试、`dispatch_common` 分类测试与 `python3 CCOS/scripts/check_rpa_device_test_convention.py` 已通过；
   - `s2` 补充真机探针未在观察窗口内稳定复现到与云端截图一致的空结果页，因此只把真机结果记为“未补充到新分支命中证据”，不误记为“代码无效”或“已完成真机闭环”。

## 当前补充结论（2026-04-14 20:25 +0800）

1. 创作者主页“轻触空白处，再次加载”收口已完成代码与真机双重闭环：
   - 项目导航器与开发平台镜像导航器均已冻结统一口径：命中创作者主页空白提示后，最多点击重试 `2` 次；若仍未恢复，则直接抛 `网络加载/页面异常: 创作者主页内容区空白，点击“轻触空白处，再次加载”重试 2 次后仍未恢复`。
   - 对客归类不再额外发散，继续复用现有 `network/page exception` 体系；重点是保留真实页面锚点与重试耗尽事实。
2. `s2(WKDAUGWGEA75KRCM)` 已补到有效真机证据，且区分了“强造弱网失败路径”和“恢复网络后的页面自恢复路径”：
   - 精准弱网探针 `job_id=mcppkg_20260414_191547_800077_d0995b23` 在 `19:16:56` 命中作者主页 Activity ready 后立即断网，随后依次出现 `retry=1/2`（`19:17:06`）、`retry=2/2`（`19:17:11`），最终按预期抛出上述 `网络加载/页面异常`；这证明重试分支与报错文案在真机上都已实际触发。
   - 恢复网络后，再对当前卡住页面做“只点重试、不重跑全链路”的专项探针 `job_id=mcppkg_20260414_201412_059963_cde5bfce`，日志显示 `reload_hint_before=True -> retry=1/2 -> reload_hint_after=False -> recycler_ready child_size=13`，且任务 `status=成功`；这证明当前实现能把作者主页从空白态拉回可继续处理的列表态。
3. “空白恢复后继续进片”链路也已在 `s2` 补到最小闭环：
   - 探针 `job_id=mcppkg_20260414_201637_627684_88201ab8` 从 `FinderProfileUI` 起跑，先确认作者主页列表 `child_size=13`，随后稳定进入并停留在 `FinderProfileTimeLineUI`，最终任务成功结束。
   - 这轮未观测到 `com.tencent.mm.ui.widget.dialog.x3`，因此当前可以客观记录为“作者主页空白恢复后继续进播放页已闭环”；`x3` 相关恢复守卫仍以代码与本地测试为主，本次真机记录不冒进写成“已在同轮复现并拦截”。
4. 评论区稳定性侧已同步新增两项低风险守卫：
   - `videohao/collect_runtime.py` 现会在评论迭代过程中检测 `com.tencent.mm.ui.widget.dialog.x3`，命中后自动 `back` 并记录 `[COMMENT_DIALOG_RECOVER]`；
   - 同时新增已处理评论去重 key，避免因弹窗打断后恢复迭代时重复处理同一条评论或错乱评论序号。

## 上一轮收尾结论（2026-04-09 18:20 +0800）

1. 本轮与“网络/页面异常”直接相关的代码与知识沉淀已提交完成：
   - `b6863fb fix(xpeng): classify network/page-ready failures as code 30`
   - `2cfe1c5 docs(xpeng): freeze failReason30 triage and device preflight`
2. 已冻结的可复用结论：
   - `21/3x` 里“搜索结果页未 ready / 灰底空白 / 显式网络异常”样本统一按 `failReason=30` 处理
   - 视频搜索结果页等待基线为 `95s + 5s retry`
   - 真机回归前必须先检查宿主机代理与 `platform_commander_state.currentUserPresent/loggedIn`
3. `s2(WKDAUGWGEA75KRCM)` 当前真机 blocker 已明确：流程包可能在设备侧 `RpaPyJob.onStart()` 先因 `currentUser.getUserId()` 空指针失败；这不是当前小鹏 Python 代码的直接回归结论。
4. 当前 git worktree 仍有未提交文件，但与本任务线本轮直接相关的代码和知识文档已经提交；剩余脏文件主要属于 `rpa-dev-platform`、公众号手写脚本与其他任务线。

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
20. `SB-20`：视频号非养号任务的 task 级通用风控升级；风控等级支持 `riskLevel=1/2/3`，调度标准参数固定走 `extraParams.riskLevel`，缺省按 `1`，仅对非养号视频号任务生效；在第一次进入视频号播放页后、所有 act 前执行前置风控，在所有 act 结束并回到视频播放页后、最终 callback 前执行后置风控；动作当前只保留“刷视频 / 点赞视频 / 喜欢视频”，且前后总时长需受该等级预算约束。`actType=51` 明确忽略该字段，并移除养号内部旧的前后刷视频壳；公众号任务不接入本轮通用风控。当前代码与单测已完成，待 `s2` 真机回归确认。
21. `SB-21`：冻结“小鹏任务超时自动停止”双层治理方案。推荐口径是 Android 运行时补绝对超时 watchdog，XP 业务层补 timeout 配置读取、timeout 独立文案/截图/归类与阶段缓存联动；明确 timeout stop 不能复用当前 manual stop 语义，也不能把唯一兜底建立在设备 HTTP `/api/stop` 上。
22. `SB-22`：优先修复流程侧高风险卡死漏洞，尽量在不依赖全局 watchdog 的前提下降低“任务挂住但不结束”概率。首批目标包括：视频号与导航链路里的直接 `setText(...)` 收口为可观测/可重试输入 helper；视频号补 `stage/stageProgress/lastProgressAt` 心跳；公众号旧主线补 act observer 与阶段缓存入口，并把评论/回复/链接转发等直接输入动作纳入同一包装层。

## 下一步

1. 认领本任务线后，优先在 `xp-wx1-simplified` 内按“设计守则冻结 -> 结果链拍平 -> `21` 修复 -> `3x` 链路补齐 -> callback body 记录增强 -> 最终完整回归”的顺序推进；不要先动 `xp-wx1` 正式版。
2. 实施期间保持已稳定的 callback/STS/OSS/signature/retry 链路不变，避免把“结果结构收口”与“网络稳定性改造”混成一轮。
3. 若后续要继续收口公众号或正式版，再基于该任务线新增子需求，不直接覆盖当前冻结方案。
4. 若补跑 AI 标准链路或 OpenAPI 文档样例，默认先从 `41 -> 21 -> 3x -> 1x` 的 `爱吃波客` 稳定基线取数，再决定是否回切 `小鹏汽车` 对照样本。
5. `SB-20` 当前代码已落地，下一步优先补 `s2` 真机专项回归：覆盖 `21/41/3x/1x/51` 与公众号 smoke，确认前后风控时机、真实页面动作、总停留时长与最终 callback 顺序符合冻结口径。
6. 卡死治理推荐顺序先按“流程侧漏洞修复 -> 真机复核 -> Android 运行时硬超时兜底”推进；不要一上来只加 watchdog，否则仍会留下大量流程内黑盒卡点，后续排障证据也不够清晰。

## Progress Log
- 2026-04-13 15:40 +0800 已把“小鹏任务长时间挂住无法结束”的治理方向同步进稳定基线任务线，并明确当前推荐不是只做 Python 层 watchdog，而是双层方案：Android 运行时补绝对超时 watchdog，XP 业务层补 timeout 独立语义与阶段缓存；同时已完成一轮“能否先靠流程修复降低挂死概率”的代码梳理。当前确认的高风险流程漏洞有三类：其一，视频号评论、创作者页搜索、导航搜索等路径仍直接调用 `setText(...)`，若底层 `ACTION_SET_TEXT` 卡住，现有 Python 层无法主动跳出；其二，公众号旧主线 `gongzhonghao/main.py` 仍保留大量直接 `setText + sleep` 的旧式实现，且 `gongzhonghao/executor.py` 当前直接忽略 `act_observer`，意味着执行层暂时拿不到阶段级进展信号；其三，Android 远程状态机当前只对 `TAKING/PREPARING_PACKAGE/WAITING_START/STARTING` 做超时控制，进入 `RUNNING` 后只持续 heartbeat，不会因长时间卡死自动收口。后续建议先做 `SB-22` 的流程侧修复，尽可能把“输入动作黑盒卡住、无阶段心跳、旧主线弱观测”这些可修问题先消掉，再补 `SB-21` 的运行时硬兜底，把 residual 风险收干净。
- 2026-04-14 10:45 +0800 已补充作者主页进片恢复策略收敛：`MMFTSSearchTabWebViewUI` 与 `AppBrandPluginUI` 不再混用同一恢复语义，当前冻结口径为“搜索 WebView 先重试原卡片 1 次，重复命中后再切下一张；AppBrand 继续直接按偏航分支切下一张”。同步已落到项目导航器与开发平台 `wechat_navigator_sdk` 镜像，并补齐案例侧单测。另冻结一条来源规则：`AppBrandPluginUI` 等 Activity 名称的真值来自运行时 `getCurrentActivityName()`，页面语义解释只能作为次级结论。本轮尝试补 `s2` 真机回归，但当前环境下 `adb devices` 与开发平台设备列表均为空，因此只记录为“真机待补”，不冒进写成已验证通过。
- 2026-04-14 11:05 +0800 已按最新约束再次收窄作者主页进片恢复策略：确认当前恢复逻辑不会缩短原 `20s` 的播放页等待；随后删除了“搜索 WebView 重复命中后切下一张”的分支，当前冻结为“原卡片重试 1 次后若仍命中 `MMFTSSearchTabWebViewUI`，直接抛 `网络加载/页面异常: 作者主页视频卡片进入播放页等待超时（命中 MMFTSSearchTabWebViewUI）`”，交由现有 `failReason=30` 体系统一归类。项目导航器、开发平台 `wechat_navigator_sdk`、案例单测、开发平台单测与业务文档均已同步。
- 2026-04-14 20:25 +0800 已把“创作者主页空白页恢复 -> 继续进片”真机证据同步回任务线：`s2(WKDAUGWGEA75KRCM)` 上已用三组探针分别补齐了“精准断网触发 `retry=1/2 -> retry=2/2 -> network/page exception`”、“恢复网络后当前页面单独点击重试可恢复出 `recycler_ready child_size=13`”以及“恢复后继续进入 `FinderProfileTimeLineUI` 播放页成功”三段证据。同步冻结当前结论：作者主页空白页重试逻辑和最终报错文案都已被真机命中，且在网络恢复后可以把同一页面拉回列表态并继续进片；评论 `x3` 弹窗自动返回与去重守卫已落代码和本地测试，但本轮真机记录未额外观测到 `x3`，不把其误记为已在同轮现场命中。
- 2026-04-09 18:20 +0800 已完成本轮上下文与任务线收尾：`30=网络加载/页面异常` 对客收口、`95s + 5s` 搜索结果页等待基线、可复用排障前置规则文档与两次提交均已完成；项目内已新增 `CCOS/context/session-20260409-03.md`，并把 `task-index / session-latest / agent-focus` 路由到 `xpeng-stable-baseline`。后续若继续 `s2` 真机回归，必须先恢复 commander runtime 登录态，否则不要把 `RpaPyJob.onStart()` 的 `currentUser` 空指针误判成小鹏脚本回归。
- 2026-04-09 08:55 +0800 已继续收口视频号 `31/32/3x` 排障信息与运行态守卫：`collect_runtime.py` 回撤了过宽的 hashtag chunk 模糊匹配，只保留截断标题前缀等更稳妥的命中口径；同时为“未命中目标视频”新增结构化失败文案，首版会拼出目标标题摘要、作者页搜索/复核结果、视频迭代停止条件与 `scanned` 计数，并在 `dispatch_common.summarize_user_failure(...)` 对外收口为“目标未命中: ...”，避免再把这类问题统统折叠成难读的脚本异常。同步新增 `videohao/wechat_runtime_guard.py` 与两组回归测试，在流程离开微信、落到登录页或不在视频相关页时直接 fail fast，防止真机排障继续盲跑错误页面。
- 2026-04-08 21:47 +0800 已补齐一轮“云端失败样本 -> 原始 payload 真机回放 -> 代码修复 -> 二次回归”的闭环证据：针对 `workUuid=e823dab092c84b5242b801a4977f662e`，`rpa-dev-platform` 云端排障工作流已新增从 portal engine log 中提取原始 `task_payload` 的能力，并在 `troubleshoot_cloud_execution` 中返回 `observed_task_payloads / observed_task_payload_summaries`，后续 AI 排障遇到云端失败样本时，应优先直接回放云端原始 payload，而不是手写近似参数。本轮已在 `s2(WKDAUGWGEA75KRCM)` 上回放该样本真实 payload，确认历史云端主故障 `content_target_not_found/public_fail_reason=31` 在当前代码上已不再复现，但同时暴露出一个独立本地缺陷：`videohao/risk_control.py` 在 `after_all_acts` 末尾已经回到 `video_play` 后仍会误抛 `RuntimeError: after_all_acts 本地返回视频号播放页失败`。该缺陷已修复并补齐单测，随后二次真机回归 `mcppkg_20260408_213238_956858_57f63436` 已成功闭环，`after_all_acts` 正常结束，且本地 mock callback / snapshot 均返回 `200`。同时再冻结两条排障口径：其一，云端日志中若能提取到原始 `task_payload`，AI 自动排障必须先用该 payload 做真机复测；其二，若 `host_preflight_urls` 因宿主机代理环境导致 `localhost` 误走 SOCKS 或缺失 `socksio`，应归类为主机环境问题，不得误判为业务脚本失败。
- 2026-04-08 21:00 +0800 已把“云端 `workUuid` 真实可查却被工具误判为空记录”的平台残差收口进小鹏稳定基线：`rpa-dev-platform` 侧新增 portal engine log 内置默认配置，并在 `analyze_cloud_execution / troubleshoot_cloud_execution` 返回体里透出 `config.source/config.endpoint`，后续若人工 raw curl 有 records、而 daemon/MCP 返回 `cloud_logs_not_found`，必须先判定为“配置漂移待核对”，而不是直接下“该 `workUuid` 无日志”结论；同时冻结一条排障口径：portal 语境里用户口语说的 `workId`，若实际给出的是 32 位运行主键，应先按 `workUuid` 候选处理。该修复已用真实样本 `workUuid=31f568a9eac85bff67f476af05c699b4` 验证，builtin default 配置下可直接查到 `5` 条 records。相关沉淀已同步到 `rpa-dev-platform-logic`、`rpa-dev-platform-collab-rules-and-pitfalls-v1`、README/API 与仓级 `AGENTS` 规则，避免后续 AI 再把“工具配置不一致”和“云端真空记录”混为一谈。
- 2026-04-08 12:08 +0800 已完成一轮“云端 `workUuid` -> 真机复核 -> 代码修复”的视频号标题排障闭环：针对运营平台失败样本 `workUuid=edc8a0b36c8b1c3c33a1d1ad534c81a3`，先通过新增的云端 engine log 分析能力确认 portal 侧 `targetTitle` 仅保留为截断值 `#95后小鹏店长\n#小鹏汽…`；随后在 `s2(WKDAUGWGEA75KRCM)` 上用诊断包 `XP_VH_DIAG_20260408_C / job_id=mcppkg_20260408_110147_824014_a432c843` 真机复测，确认作者页迭代兜底实际上已经扫描到第 `4` 个候选视频 `#95后小鹏店长\n#小鹏汽车…`，但旧版 `_is_target_video_title_match(...)` 因“当前标题带省略号但前缀未命中时提前 `return False`”而没有继续评估“目标标题也带省略号”的对称分支，最终误判为“未命中目标视频”。本轮已修复该提前返回问题，并补 `test_target_video_title_match_accepts_both_truncated_same_prefix` 回归保护。同时把一条稳定认知冻结到任务线：微信作者页内搜索首个结果存在 App 侧模糊匹配，不能把首条卡片标题反推成真实目标视频标题；诊断 `3x/31/32` 视频未命中问题时，应优先以播放页真实标题和迭代日志为证据，而不是以搜索首条结果做结论。
- 2026-04-01 18:10 +0800 已完成视频号 `41` 评论页发布时间解析修复：`115 / ONYX9X4PZ5FY7LPZ` 上先复现到 `release_time=未知`，确认评论页头部真实文案为 `北京 2025年12月25日`；随后补齐 `YYYY年M月D日` 解析与测试后，再次用 `115` 真机回归，日志已命中“头部文案兜底解析命中：release_time='2025年12月25日'”，并按 `pubTimeGe=2026-03-29 11:00:00` 正常跳过旧视频，最终 callback 成功（`status=1/failReason=0`）。同时补记一条平台排障坑点：本地 daemon / MCP 若继承代理环境，localhost 流程包执行可能报 `socksio` 缺失，需先清理代理变量再做本机联调。
- 2026-03-27 18:25 +0800 已同步 `SB-20` 风控参数口径收敛：删除旧顶层 `riskLevel` 读取与文档兼容描述，调度标准结构固定为 `extraParams.riskLevel`；`xp-wx1-simplified` 执行层、风控单测、稳定基线文档与视频号测试元文档均已同步，且 `test_execution_risk_control.py`、`test_videohao_risk_control.py` 与 `check_rpa_device_test_convention.py` 已通过
- 2026-03-23 21:18 +0800 已同步 `SB-20`：非养号视频号任务的 task 级通用风控已落代码，风控等级支持 `riskLevel=1/2/3`（缺省按 `1`），在视频号播放页执行“前置风控 + 后置风控”，当前动作只保留“刷视频 / 点赞视频 / 喜欢视频”；`actType=51` 已明确忽略 `riskLevel` 并移除内部旧的前后刷视频壳；公众号任务显式跳过本轮通用风控。对应代码提交为 `39fd420 feat(videohao): add common risk control wrapper`，本地保护含 `test_execution_risk_control.py / test_videohao_risk_control.py` 与既有回归已通过，当前待 `s2` 真机回归确认 `21/41/3x/1x/51` 与公众号 smoke
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
