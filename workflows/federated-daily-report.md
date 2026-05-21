# 联邦日报流程（多项目）

目标：在 CCOS 中枢按“项目级 commit 优先”的口径汇总每日工作，回写 Logseq 日志。

本流程遵循统一协议：`meta/ccos-unified-protocol.md`（CCOS Node 与 CCOS Hub 必须协同使用）。

## 数据来源

1. 项目注册：`machine/federation/project-registry.json`
2. 每个启用项目的当日提交：`git log --since <day-start> --until <day-end>`
3. 兼容旧模式时，可对“当日无提交”的项目回退 `git diff HEAD` / `git status --short`
4. 可选：联邦 CCOS 索引聚合结果 `machine/federation/ccos-index-federated.json`

## 执行命令

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root .
```

兼容旧模式：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root . --prefer commit-first
```

## 输出

- 终端输出三段式：
  - `今日完成`
  - `明日任务`
  - `工时`
- 回写文件：`capture/journals/YYYY_MM_DD.md`
- 回写区块：`- 联邦日报`

## 约束

1. 默认保持“只看纳管项目当日 commit”原则，不把中枢或当前工作区未提交改动直接写进联邦日报。
2. `enabled=false` 的项目或节点不纳入联邦执行。
3. 只有在显式兼容旧模式时，才允许对“无提交项目”回退 `git diff HEAD`。
4. 不自动迁移项目业务文档，项目内 `CCOS` 保持自治。
5. 若用户要求“实际工作日报”，应额外读取相关项目仓和 taskline；联邦日报默认输出仍是证据投影，而不是人工复盘口径。
6. 联邦扫描数量、索引刷新、口径选择等执行说明不写入日报正文；这些信息应作为命令执行日志单独输出。
