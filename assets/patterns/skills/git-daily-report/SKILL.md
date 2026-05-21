---
name: git-daily-report
description: 单仓日报使用 Commit-First（优先读取当日 git 提交）+ Diff-Fallback（无提交时回退 git diff HEAD）；联邦日报默认只基于纳管项目当日提交生成，避免把当前工作区未提交改动写进中枢日报。仅输出“今日完成/明日任务/工时”，并回写 capture/journals/YYYY_MM_DD.md 后可选提交推送。用户提出“日报总结”“根据提交记录出日报”“联邦跨项目日报”“根据 git diff 写日报”时使用。
---

# Git Daily Report

## Overview

面向 CCOS 的日报闭环，采用分层策略：

1. 单仓：Commit-First，优先基于当日提交记录生成日报；必要时可回退 `git diff HEAD`。
2. 联邦：默认 Commit-Only，只基于纳管项目当日提交生成日报，避免把中枢或工作区未提交改动写进去。
3. 固定产物：`今日完成 / 明日任务 / 工时`。
4. 在对话里，若用户说“今天的日报 / 我的日报”，默认解释为“用户个人日报”，不要把助手执行命令、扫描项目、刷新索引等动作写进正文。

额外口径约束：

1. 若用户明确要求“今日实际工作 / 包含未提交改动”，不要只读 `ccos` 中枢仓；必须回看相关 taskline 的 `repo_root` 或联邦注册表中的项目仓。
2. 原因：Hub 里的 `docs(taskline)` 往往只是项目仓真实实现的投影提交，单看中枢会把真实 bugfix 压缩成“任务线同步”。
3. `Diff-Fallback` 的 `DONE/TODO/NOW/WAITING/工时` 提取只应来自文档类文件；代码文件里的 `done/todo` 变量不应参与日报语义抽取。
4. 日报正文只写“用户产出 / 项目进展 / 下一步 / 工时”；扫描项目数量、是否刷新索引、采用何种取数口径等信息应留在执行日志，不进 `今日完成`。

## Workflow

### 1. 先看提交（Commit-First）

- 默认读取当日提交：`git log --since <day-start> --until <day-end>`。
- 推荐在每次提交正文中补充结构化字段（提升日报准确性）：

```text
taskline_id: <project_id/ccos_node/task_slug>
work_summary: <本次工作摘要>
next: <下一步动作>
hours: <1.5h>
```

- 日报脚本会优先提取：提交标题、`taskline_id`、`next`、`hours`。
- 模板文件：`assets/patterns/skills/git-daily-report/templates/commit-message-template.txt`
- 推荐在每个项目仓库安装 `commit-msg` 钩子，提交时前置校验字段完整性：

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl node install-commit-hook --repo-root <repo_root> --mode strict
```

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

- 只按提交生成（不纳入当前工作区未提交改动）：

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --prefer commit-only --print-only
```

### 联邦日报（CCOS Hub）

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root .
```

- 输入：`machine/federation/project-registry.json` 纳管项目。
- 默认策略：逐仓 Commit-Only，只吃项目当日提交，避免把当前工作区未提交改动写入联邦日报。
- 如需兼容旧模式，可显式切回 `--prefer commit-first`，允许无提交项目回退到 `git diff HEAD`。

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

# 联邦显式开启 diff 回退（兼容旧模式）
python3 assets/patterns/skills/git-daily-report/scripts/update_federated_daily_report.py --ccos-root . --prefer commit-first --print-only

# 打印推荐模板
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --print-commit-template

# 或使用 ccosctl 在任意目录打印模板
/Users/zhuxiaowei/ccos/scripts/ccosctl node print-commit-template
```

统一入口（推荐）：

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos --prefer commit-only --commit-meta-mode warn --print-only
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

## Conversation Guardrails

1. 先判断用户要的是哪一类：
   - “联邦日报 / 中枢日报 / 按项目汇总” => 联邦证据投影口径。
   - “今天的日报 / 我的日报 / 帮我总结今天” => 用户个人日报口径。
2. 即使底层脚本输出了执行说明，回复用户时也要先做一次语义清洗：
   - 保留业务事项、任务线进展、提交摘要、下一步。
   - 去掉“联邦扫描了几个项目 / 刷新了索引 / 采用 commit-only / diff-fallback”这类执行痕迹。
3. 若证据不足以支撑“个人实际工作日报”，要直接说明缺口来自哪些项目仓或哪些未提交改动尚未读取，而不是拿 Hub 投影提交硬凑正文。
