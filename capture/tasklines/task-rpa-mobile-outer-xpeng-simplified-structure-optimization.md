# 小鹏 simplified 结构优化提案

- taskline_id: `rpa-mobile/outer/xpeng-simplified-structure-optimization`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `done`
- updated_at: `2026-04-16 18:56 +0800`
- updated_by: `codex(agent-codex-main)`

## 当前结论

1. 本任务线是 `xp-wx1-simplified` 结构优化提案与第一刀收口记录，不再作为活跃开发线。
2. 已完成的核心事实：
   - `app.py` 已向薄入口方向收口。
   - `reporting.py` 已承担成功/失败 facade。
   - `dispatch_common.py` 已承接 dispatch 解包、停止判定、snapshot 拆分和 attemptsId 归一等稳定共识。
   - `param_adapter.py`、`planning.py`、`execution.py` 已开始减少重复样板。
3. 剩余“继续减少 executor 内部 single/combo 样板”等结构尾项已并入项目侧 `xpeng-stable-baseline` 的 `SB-19` 口径，不再通过本任务线单独推进。

## 后续路由

1. 若用户要求继续优化 simplified 结构，优先回到：
   - `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-stable-baseline.md`
2. 若只是查阅结构设计原则，继续以项目侧归档文档为事实源：
   - `/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-xpeng-simplified-structure-optimization.md`

## Progress Log

- 2026-04-16 18:56 +0800 补齐 Hub 镜像并标记为 `done`，解决“项目侧有任务档案但 Hub 未登记”的索引漂移。
