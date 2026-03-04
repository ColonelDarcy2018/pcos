# RPA 开发平台导出流程包能力迭代

- taskline_id: `rpa-mobile/outer/rpa-dev-platform-export-iteration`
- project_id: `rpa-mobile`
- repo_root: `/Users/zhuxiaowei/apps/rpa-mobile`
- ccos_node: `outer`
- status: `in_progress`
- updated_at: `2026-03-03`

## 背景

项目内原始任务文档：
`/Users/zhuxiaowei/apps/rpa-mobile/CCOS/context/task-rpa-dev-platform-export-iteration.md`。

该任务线聚焦“导出 + 完整流程包下发 + 自动增量调试”统一迭代，目标是形成本地调试与后续远程通道可复用的流程包能力基线。

## 当前进展（同步摘要）

1. `T1` 到 `T7` 已完成，已具备 `project-only` 导出、`execute_flow_package`、`package_patch` 自动识别与回退等核心能力。
2. `T8/T9` 因远程双通道前置信息不足暂缓。
3. `T10` 已完成 v1：新增“元素拾取 -> selector 草案 -> 占位插入 -> PICK_TASKS 回写”协作链路（Android/Daemon/MCP/插件全链路打通）。
4. 当前进入 `T10` v2 准备阶段：真机回归与协作协议收敛。
5. Node 并发路由已迁移为 `task-index + agent-focus`，后续认领/切换按新口径执行。

## 下一步

1. 推进 `T10` v2：沉淀 AI 与人工协作职责矩阵、拾取回填校验和 selector 优先级规则。
2. 补齐 Java 中转服务协议细节后，再重启 `T8/T9` 双通道整合。
3. 持续本地 ADB 链路回归验证，避免后续远程改造引入退化。
