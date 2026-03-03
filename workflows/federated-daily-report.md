# 联邦日报流程（多项目）

目标：在 CCOS 中枢按“项目级 `git diff HEAD`”汇总每日工作，回写 Logseq 日志。

本流程遵循统一协议：`meta/ccos-unified-protocol.md`（CCOS Node 与 CCOS Hub 必须协同使用）。

## 数据来源

1. 项目注册：`machine/federation/project-registry.json`
2. 每个启用项目的未提交改动：`git diff HEAD` / `git status --short`
3. 可选：联邦 CCOS 索引聚合结果 `machine/federation/ccos-index-federated.json`

## 执行命令

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root .
```

## 输出

- 终端输出三段式：
  - `今日完成`
  - `明日任务`
  - `工时`
- 回写文件：`capture/journals/YYYY_MM_DD.md`
- 回写区块：`- 联邦日报`

## 约束

1. 保持“只看 `git diff HEAD`”原则，不引入历史提交噪音。
2. `enabled=false` 的项目或节点不纳入联邦执行。
3. 不自动迁移项目业务文档，项目内 `CCOS` 保持自治。
