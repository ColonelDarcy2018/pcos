# 技能统一改动对照（2026-03-03）

## 本次执行结论

- 已升级 7 个全局 CCOS 相关技能，统一到“项目目录执行 + CCOS 中枢回写”模式。
- 已将技能中的“联邦模式”表述升级为强制语义（MUST），明确 CCOS 与 CCOS 不是二选一。
- 已保留 `mobile-rpa-script-dev` 的“人机协作元素拾取协议”完整段落。
- 已将 `rpa-mobile/.trae/skills` 切换为全局技能软链接，消除本地技能分叉。
- 已新增统一协议源：`/Users/zhuxiaowei/ccos/meta/ccos-unified-protocol.md`。

## 全局技能改动清单

1. `/Users/zhuxiaowei/.codex/skills/game-requirement-innovation/SKILL.md`
   - 新增：`CCOS 联邦执行约定`。
   - 并入：knowledge 去过程化、版本变更记录表、context/knowledge 边界、最小必要修改。

2. `/Users/zhuxiaowei/.codex/skills/ccos-protocol-bootstrap/SKILL.md`
   - 并入：文档写作规范（面向非对话读者、版本记录、最小修改、删除说明）。
   - 新增：CCOS 联邦模式下的项目执行/中枢管理约定。

3. `/Users/zhuxiaowei/.codex/skills/mobile-rpa-script-dev/SKILL.md`
   - 保留：元素拾取协议（`@rpa.human_pick`、`PICK_TASKS.md`、相关 references）。
   - 新增：`CCOS 联邦执行约定`。
   - 并入：最小必要修改 + 删除逻辑说明要求。

4. `/Users/zhuxiaowei/.codex/skills/上下文管理/SKILL.md`
   - 新增：`CCOS 联邦执行约定`。
   - 并入：context/knowledge 边界、去过程化、最小改动规则。

5. `/Users/zhuxiaowei/.codex/skills/业务逻辑图谱/SKILL.md`
   - 新增：`CCOS 联邦执行约定`。
   - 并入：面向非对话读者、版本记录、最小改动规则。

6. `/Users/zhuxiaowei/.codex/skills/代码审查/SKILL.md`
   - 新增：`CCOS 联邦执行约定`。
   - 并入：审查结论去过程化、单文档迭代、context/knowledge 边界、最小改动规则。

7. `/Users/zhuxiaowei/.codex/skills/任务分解/SKILL.md`
   - 新增：`CCOS 联邦执行约定`（显式三字段 `project_id/task_id/ccos_node`）。
   - 并入：面向非对话读者、版本记录、context/knowledge 边界、最小改动规则。

## 本地技能入口统一改动

- `rpa-mobile`：
  - 原目录备份：`/Users/zhuxiaowei/apps/rpa-mobile/.trae/skills.local-backup-20260303`
  - 现入口：`/Users/zhuxiaowei/apps/rpa-mobile/.trae/skills -> /Users/zhuxiaowei/.codex/skills`

- `AGENTS` 约束已更新：
  - `/Users/zhuxiaowei/apps/rpa-mobile/AGENTS.md`
  - 新增全局技能单源与执行入口规则（项目执行 + CCOS 回写）。

## 审核关注点

1. 是否将软链接模式改为“彻底删除本地备份目录”。
2. 是否在其他项目补充 AGENTS 同类约束（当前仅 rpa-mobile 有 AGENTS）。
3. 是否继续把同类规则同步到 `ccos-protocol-bootstrap/assets/protocol/*.md` 模板，以便新仓初始化即带最新规范。
