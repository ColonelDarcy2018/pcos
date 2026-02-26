---
name: git-daily-report
description: 使用 Git 分析当日代码与文档改动，生成结构化中文日报（“今日完成/明日任务”），并回填到 capture/journals/YYYY_MM_DD.md 后执行提交与推送。用户提出“分析今天改动”“生成日报”“回填日报”“只看未提交内容”“写完后提交并push”等请求时使用。
---

# Git Daily Report

## Overview

基于 Git 和当日日志文件提炼日报，默认输出“今日完成”和“明日任务”两块。支持两种口径：仅未提交改动，或“已提交 + 未提交”混合分析；在个人认知库场景下，日报回填后默认执行提交并推送。

## Workflow

### 1. 判定口径

- 先确认统计范围：
  - 仅未提交：读取 `git status --short`、`git diff --name-status`、`git diff --numstat`。
  - 含已提交：额外读取 `git log --since='today 00:00'` 和相关提交 `git show --stat`。
- 用户明确“不要管已提交内容”时，只使用未提交信息。

### 2. 收集证据

- 先记录时间与分支，再收集改动面和改动量：

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
git rev-parse --abbrev-ref HEAD
git status --short
git -c core.quotepath=false diff --name-status
git -c core.quotepath=false diff --numstat
```

- 读取 `capture/journals/YYYY_MM_DD.md`，提取 `DONE`、`TODO` 和关键沟通结果作为业务语义补充。
- 遇到中文路径时强制使用 `-c core.quotepath=false`，避免乱码路径影响总结质量。

### 3. 生成日报

- 固定结构输出：
  - `今日完成`：已完成事项、关键决策、联调结论、限制条件。
  - `明日任务`：未完成项、风险处理项、下一步交付物。
- 每条使用一句话描述，优先动词开头，避免“进行中/跟进中”这类空泛表达。
- 明确标注总结范围（例如“基于未提交改动”）。

### 4. 回填文档（按需）

- 用户要求回填时，在 `capture/journals/YYYY_MM_DD.md` 末尾新增独立栏目：

```text
- 日报
    - 今日完成
        - ...
    - 明日任务
        - ...
```

- 保持原文件缩进风格，不改动无关段落。
- 若文件已存在 `- 日报`，优先更新原有块，避免重复新增同名栏目。

### 5. 提交与推送（默认执行）

- 默认策略（个人认知库）：
  - 当日记录完成后执行 `git add -A`，提交当天所有认知沉淀（journal + pages + skills）。
  - 使用清晰提交信息，推荐：`docs: YYYY-MM-DD 日报与当日记录同步`。
- 若用户明确要求“仅提交日报文件”，再改为最小提交范围。

```bash
git add -A
git commit -m "docs: YYYY-MM-DD 日报与当日记录同步"
git push origin <current-branch>
```

- 提交推送后执行复核并回报关键信息：

```bash
git show --stat --oneline -1
git log --oneline --decorate -1
git status --short
```

- 回报内容至少包含：提交哈希、提交文件列表、`push` 结果、当前剩余未提交改动。

## Output Template

```markdown
今日完成
1. ...
2. ...

明日任务
1. ...
2. ...
```
