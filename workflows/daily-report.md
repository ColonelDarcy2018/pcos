# 日报流程：项目提交优先的联邦汇总

## 适用范围

- 单仓优先读取“当日提交记录”（Commit-First）
- 联邦默认只读取纳管项目的当日提交（Commit-Only）
- 单仓无提交时可回退 `git diff HEAD`（Diff-Fallback）
- 固定输出三部分：`今日完成`、`明日任务`、`工时`

## 口径选择

1. `证据投影日报`
   - 默认口径。
   - 目标是让日报与 Git / taskline 投影保持稳定可审计。
   - 单仓优先看本仓 commit；联邦默认只看纳管项目 commit。
2. `实际工作日报`
   - 仅在用户明确要求“今日实际工作”“包含未提交改动”时使用。
   - 必须跨仓检查相关 taskline 的 `repo_root` 或联邦注册表里的项目仓，不能只扫描 `ccos`。
   - 原因：`ccos` 里的 `docs(taskline)` 往往只是项目仓真实代码修复的 Hub 投影，单看中枢会把真实 bugfix 压缩成“任务线同步”。
3. `对话口头总结`
   - 若用户直接说“今天的日报 / 我的日报”，默认按“个人实际工作日报”解释。
   - 回答时不要把命令执行、索引刷新、扫描项目数等执行说明写进正文。

## 执行步骤

1. 推荐先在项目仓库安装提交规范钩子（一次性）

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl node install-commit-hook --repo-root <repo_root> --mode strict
```

2. 每次提交正文建议包含：

```text
taskline_id: <project_id/ccos_node/task_slug>
work_summary: <本次工作摘要>
next: <下一步动作>
hours: <1.5h>
```

3. 生成联邦日报（中枢统一执行）

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos --prefer commit-only
```

4. 校验提交字段完整性（可选 strict）

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos --prefer commit-only --commit-meta-mode strict --print-only
```

5. 检查当日日报回写结果

- 目标文件：`capture/journals/YYYY_MM_DD.md`
- 目标区块：`- 联邦日报`

## 与 CCOS 的关系

- `capture/journals` 记录“当天上下文与执行结果”
- `assets` 承载“跨天复用模式与原则”
- 日报流程提供每天最小闭环，蒸馏流程（`workflows/distill.md`）负责长期抽象升级
- 中枢汇总默认只吃每个项目的 commit 元数据，避免把当前工作区临时改动或助手执行痕迹写进日报
- 若确实需要兼容旧模式，可显式追加 `--prefer commit-first` 开启无提交项目的 diff 回退
- 若要生成“实际工作日报”，需要额外回看相关 taskline/journal 与项目仓真实提交；不要把 Hub 投影提交直接当成全部工作事实
- 日报正文与执行日志分离：口径、扫描数量、索引刷新等信息保留在命令输出，不落 `今日完成`

## 跨项目模式

当你需要在 CCOS 中枢汇总多个项目（而非单仓）时，使用：

- `workflows/federated-daily-report.md`
