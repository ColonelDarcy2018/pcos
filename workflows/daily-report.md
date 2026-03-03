# 日报流程：Commit-First 联邦汇总

## 适用范围

- 优先读取“当日提交记录”（Commit-First）
- 单仓无提交时回退 `git diff HEAD`（Diff-Fallback）
- 固定输出三部分：`今日完成`、`明日任务`、`工时`

## 执行步骤

1. 推荐先在项目仓库安装提交规范钩子（一次性）

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl node install-commit-hook --repo-root <repo_root> --mode strict
```

2. 每次提交正文建议包含：

```text
taskline_id: <project/taskline>
work_summary: <本次工作摘要>
next: <下一步动作>
hours: <1.5h>
```

3. 生成联邦日报（中枢统一执行）

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos
```

4. 校验提交字段完整性（可选 strict）

```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos --commit-meta-mode strict --print-only
```

5. 检查当日日报回写结果

- 目标文件：`capture/journals/YYYY_MM_DD.md`
- 目标区块：`- 联邦日报`

## 与 CCOS 的关系

- `capture/journals` 记录“当天上下文与执行结果”
- `assets` 承载“跨天复用模式与原则”
- 日报流程提供每天最小闭环，蒸馏流程（`workflows/distill.md`）负责长期抽象升级
- 中枢汇总只吃每个项目的 commit 元数据，避免大仓 diff 扫描带来的上下文噪音

## 跨项目模式

当你需要在 CCOS 中枢汇总多个项目（而非单仓）时，使用：

- `workflows/federated-daily-report.md`
