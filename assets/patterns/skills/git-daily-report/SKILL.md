---
name: git-daily-report
description: 使用 Commit-First（优先读取当日 git 提交）+ Diff-Fallback（无提交时回退 git diff HEAD）生成中文日报，仅输出“今日完成/明日任务/工时”，并回写 capture/journals/YYYY_MM_DD.md 后可选提交推送。用户提出“日报总结”“根据提交记录出日报”“联邦跨项目日报”“根据 git diff 写日报”时使用。
---

# Git Daily Report

## Overview

面向 CCOS 的日报闭环，采用统一策略：

1. Commit-First：优先基于当日提交记录生成日报（降低大仓 diff 噪音）。
2. Diff-Fallback：若当日无提交，回退到 `git diff HEAD` 生成日报。
3. 固定产物：`今日完成 / 明日任务 / 工时`。

## Workflow

### 1. 先看提交（Commit-First）

- 默认读取当日提交：`git log --since <day-start> --until <day-end>`。
- 推荐在每次提交正文中补充结构化字段（提升日报准确性）：

```text
taskline_id: <project/taskline>
work_summary: <本次工作摘要>
next: <下一步动作>
hours: <1.5h>
```

- 日报脚本会优先提取：提交标题、`taskline_id`、`next`、`hours`。
- 模板文件：`assets/patterns/skills/git-daily-report/templates/commit-message-template.txt`

### 2. 无提交时回退 Diff（Diff-Fallback）

- 回退命令：

```bash
git status --short
git -c core.quotepath=false diff --name-status HEAD
git -c core.quotepath=false diff --numstat HEAD
git -c core.quotepath=false diff --unified=0 --no-color HEAD
```

- 保留旧规则：先做“净新增语义”抵消，再提取 `DONE/TODO/NOW/WAITING`。

### 3. 回写当日日志

- 回写目标：`capture/journals/YYYY_MM_DD.md`。
- 回写区块：
  - 单仓：`- 日报`
  - 联邦：`- 联邦日报`
- 已存在同名区块时整块替换，避免重复。

### 4. 可选提交推送

- 需要闭环时执行 `--sync`：
  - `git add -A`
  - `git commit -m ...`
  - `git push origin <current-branch>`

## Script

### 单仓日报

- 正式执行（Commit-First，自动回退）：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --sync
```

- 仅预览：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --print-only
```

- 强制只用 diff（兼容旧模式）：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --prefer diff-only --print-only
```

### 联邦日报（CCOS Hub）

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root .
```

- 输入：`machine/federation/project-registry.json` 纳管项目。
- 策略：逐仓 Commit-First，项目无提交时自动 Diff-Fallback。

## Commit Meta 校验模式

日报脚本支持 `off/warn/strict` 三种模式：

1. `off`：关闭校验。
2. `warn`（默认）：发现提交缺少 `taskline_id/next/hours` 时提示但不中断。
3. `strict`：发现缺失即退出失败（返回非 0）。

示例：

```bash
# 单仓严格校验
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --commit-meta-mode strict --print-only

# 联邦严格校验
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root . --commit-meta-mode strict --print-only

# 打印推荐模板
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --print-commit-template
```

统一入口（推荐）：

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos --commit-meta-mode warn --print-only
```

## Output Template

```markdown
今日完成
1. ...
2. ...

明日任务
1. ...
2. ...

工时
1. ...
```
