# 日报流程：从未提交改动到当日认知沉淀

目标：每天基于 `git diff HEAD` 生成结构化日报，并回写 `capture/journals`，随后提交全部文档并推送形成可复盘演化轨迹。

## 适用范围

- 只分析当前工作区未提交改动（tracked + untracked），数据源限定为 `git diff HEAD`
- 不读取历史提交日志作为日报输入
- 固定输出三部分：`今日完成`、`明日任务`、`工时`

## 执行步骤

1. 每日执行一次日报脚本（生成 + 回写 + 同步）

```bash
python3 assets/patterns/skills/git-daily-report/scripts/update_daily_report.py --repo . --sync
```

2. 检查当日日报回写结果

- 目标文件：`capture/journals/YYYY_MM_DD.md`
- 目标区块：`- 日报`

## 与 PCOS 的关系

- `capture/journals` 记录“当天上下文与执行结果”
- `assets` 承载“跨天复用模式与原则”
- 日报流程提供每天最小闭环，蒸馏流程（`workflows/distill.md`）负责长期抽象升级
