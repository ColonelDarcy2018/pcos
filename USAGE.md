# CCOS 使用说明（V1）

适用日期：2026-03-03  
适用路径：`/Users/zhuxiaowei/ccos`

## 1. 一句话原则

1. 项目实现与项目知识在项目目录内完成（`<repo>/CCOS/**`）。
2. 跨项目路由、索引、日报在中枢完成（`~/ccos/**`）。
3. 人类阅读与记忆优先，不牺牲认知复利。

## 2. 目录角色

1. `capture/`：Logseq 友好的原始捕获层（任务背景、日报、临时记录）。
2. `assets/`：Obsidian/Markdown 友好的长期知识资产层（evidence/patterns/principles）。
3. `machine/`：机器索引与联邦治理层（schema/index/federation）。
4. `meta/`：规则正文单源（协议、宪法、重构设计）。

## 3. 执行入口（人和 AI 通用）

1. 在项目目录执行开发与协议同步：
```bash
cd <repo_root>
/Users/zhuxiaowei/ccos/scripts/ccosctl node sync --repo-root .
```
2. 在任意目录聚合联邦索引：
```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub sync-index --hub-root /Users/zhuxiaowei/ccos
```
3. 在任意目录执行中枢治理校验：
```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub lint --hub-root /Users/zhuxiaowei/ccos
```
4. 在任意目录生成联邦日报：
```bash
/Users/zhuxiaowei/ccos/scripts/ccosctl hub report-daily --hub-root /Users/zhuxiaowei/ccos
```

### 3.1 项目目录发起任务如何继承中枢元协议

1. 每个项目 `CCOS/protocol/p0-rules.md` 与 `CCOS/protocol/ai-playbook.md` 必须显式锚定：
   - `/Users/zhuxiaowei/ccos/meta/ccos-unified-protocol.md`
2. `ccosctl hub lint` 会强校验上述锚点，缺失即报错，防止项目规则漂移。
3. `ccosctl` 支持在项目目录执行；未显式传 `--hub-root` 时，会按以下顺序定位 Hub：
   - `--hub-root`
   - 环境变量 `CCOS_HUB_ROOT`
   - 当前目录向上查找 Hub 结构
   - 默认回退 `~/ccos`

## 4. 任务闭环（建议）

1. 任务启动：先确定三字段 `project_id/repo_root/ccos_node`。
2. 执行阶段：只在 `repo_root` 做代码与知识改动。
3. 收口阶段：
   - 项目侧执行 `CCOS/scripts/ccos_p0.py sync`
   - 中枢侧更新 `capture/tasklines/**` 摘要
   - 中枢侧执行联邦索引聚合与日报（按需）

## 5. 人类认知流（防能力退化）

1. 原始想法先写 `capture/`，不急着结构化。
2. 可复用内容再蒸馏到 `assets/`，并保留来源链接。
3. 机器索引由脚本生成，避免手工维护导致污染。
4. `capture` 与 `assets` 不互相覆盖，只做链接关联。

## 6. 规则优先级

1. 平台/System/Developer 强约束
2. `~/ccos/meta/**`（规则正文单源）
3. 仓库 `AGENTS.md`（仓库适配差异）
4. 全局 Skills（工作流方法）
5. 会话上下文与任务文档

## 7. 常见错误

1. 在 `~/ccos` 直接修改项目业务代码。
2. 跳过项目侧 `CCOS/scripts/ccos_p0.py sync`。
3. 将项目全文复制到中枢，导致中枢与项目双写冲突。
4. 在项目内保留本地技能副本，破坏全局技能单源。

## 8. 备份与回溯

本次全量迁移前的备份目录：

`/Users/zhuxiaowei/ccos_migration_backups/20260303_161540`

包含 `MANIFEST.txt` 与 `SHA256SUMS.txt`，可用于回溯历史状态。
