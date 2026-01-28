# 蒸馏流程：从 capture → assets + machine

目标：把“原始捕获”转化为可复用的长期资产，并同步维护机器可读索引，便于未来自动化检索、聚合与分析。

## 输入与输出

- **输入**：`capture/` 中的一条想法/一页笔记/一段材料
- **输出（人类层）**：`assets/` 中 1 个或多个 Markdown 资产文件
- **输出（机器层）**：`machine/index.json` 中新增/更新对应条目（以及必要的 schema 演进）

## 最小步骤（建议每次 5–20 分钟）

1. **筛选**
   - 只处理“未来会复用/会影响决策/会反复出现”的内容
   - 其余保留在 `capture/`，不要强行沉淀
2. **定类**
   - 选择落点：`concepts/ models/ methods/ projects/ decisions/ philosophy/ skills`
3. **写资产（最小可用）**
   - 给出清晰标题与一段结论（定义/模型/步骤/决策）
   - 写清边界：适用/不适用、前提、风险（避免泛化）
   - 如有来源，记录引用（URL 或 capture 路径）
4. **建立链接（可选但推荐）**
   - 在资产中用相对链接关联相关资产（形成可导航网络）
5. **更新机器索引**
   - 在 `machine/index.json` 中新增/更新资产条目（见下方字段约定）
6. **提交**
   - 一次提交只做一件事：新增一个资产 / 完成一次蒸馏 / 修正一个模型

## `machine/index.json` 字段约定（V1）

每个资产条目最少包含：

- `id`：稳定标识（建议：`YYYYMMDDHHmm-短名`，不随文件重命名而变化）
- `path`：资产文件相对路径（例如：`assets/methods/gtd.md`）
- `kind`：资产类型（`concept|model|method|project|decision|philosophy|skill`）
- `title`：标题

可选字段（按需添加）：

- `tags`：标签数组
- `updated_at`：最后更新（ISO 8601 字符串）
- `sources`：来源数组（URL 或 `capture/` 路径）
- `links`：关联资产 `id` 数组（后续可用于生成图谱）

Schema 参考：`machine/schema/index.schema.json`（需要变更格式时先改 schema，再改数据）。

