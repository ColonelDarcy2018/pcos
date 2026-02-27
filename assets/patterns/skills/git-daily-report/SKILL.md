---
name: git-daily-report
description: 使用 Git 读取“当前未提交改动（git diff HEAD）”生成中文日报，仅输出“今日完成/明日任务/工时”，并回写到 capture/journals/YYYY_MM_DD.md 后提交全部文档并推送。用户提出“根据 git diff 写日报”“日报后同步云端”“每天总结并 commit/push”“只看未提交改动生成日报”等请求时使用。
---

# Git Daily Report

## Overview

面向 PCOS 的日报闭环：严格只看 `git diff HEAD`（未提交改动），避免混入历史提交噪音。产物固定为三段式日报，并沉淀到 `capture/journals` 作为认知演化日志。

## Workflow

### 1. 只看未提交改动

- 固定使用以下命令收集证据：

```bash
date '+%Y-%m-%d'
git rev-parse --abbrev-ref HEAD
git status --short
git -c core.quotepath=false diff --name-status HEAD
git -c core.quotepath=false diff --numstat HEAD
git -c core.quotepath=false diff --unified=0 --no-color HEAD
```

- 仅允许基于 `git diff HEAD` 生成内容，不允许混入 `git log` 历史提交。

### 2. 生成日报三段式内容

- 固定输出三个栏目，且只输出这三项：
  - `今日完成`
  - `明日任务`
  - `工时`
- 必须基于 diff 的“净新增语义”提炼：先抵消同一轮 diff 内的新增/删除同文本行（避免重排导致的误判），再提取 `DONE/TODO/NOW/WAITING`。
- 工时仅从 diff 中提取；如果 diff 没有工时字段，输出 `待补充（git diff 未发现工时字段）`。

### 3. 回写当日日志

- 目标文件：`capture/journals/YYYY_MM_DD.md`（当天日期）。
- 回写规则：
  - 若已有 `- 日报` 块，整块替换，避免重复。
  - 若不存在，追加到文件末尾。
  - 保持 Logseq 缩进风格。

### 4. 提交并推送

- 作为日常一次性闭环，回写后默认提交全部文档并推送：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --sync
```

- `--sync` 行为固定为：
  - `git add -A`
  - `git commit -m "docs: YYYY-MM-DD 日报回写与文档同步"`（可覆盖 commit message）
  - `git push origin <current-branch>`
- 推送失败必须显式报错并重试，不能静默忽略。

## Script

- 每日正式执行（生成 + 回写 + 提交全部 + 推送）：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --sync
```

- 仅预览不回写：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --print-only
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
