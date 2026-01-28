# meta ↔ assets 三层认知映射（Evidence / Patterns / Principles）

本文件用于把 PCOS 的“元层（meta）”与 `assets/` 的三层认知结构建立语义一致性，避免系统在演进中变成“目录分类学”，也避免原则只停留在口号。

PCOS 的核心目标是：让知识在真实使用中逐步升维，形成可复利的认知资本；结构只是为了降低摩擦与支持演化。

---

## 1) meta 文档的职责

`meta/` 是系统的“设计源代码”，它不承担日常沉淀的主要入口，而承担长期约束与方向：

- **系统宪法**：约束什么能改、什么不该改，以及如何改（可审计、可回滚、可扩展）。
- **设计源代码**：记录架构动机、边界划分、关键取舍，避免“靠记忆维护系统”。
- **世界观约束**：明确价值取向、判断权归属、对工具的态度（架构优先于工具）。
- **认知原则库**：提供抽象的上限与护栏，防止结构/工具反客为主。

一句话：`meta/` 定义“怎么长期演进才不会走偏”，而不是记录“今天发生了什么”。

---

## 2) meta 与 Evidence / Patterns / Principles 的关系映射

`assets/` 的三层结构是人类资产的成熟度路径：
`Evidence（事实与经验） → Patterns（可复用模式） → Principles（稳定原则）`。

`meta/` 的内容整体更接近 **Principles + Patterns**：它描述的是系统的世界观与架构，而不是具体案例本身。

### 现有 meta 文档建议映射

- `meta/constitution.md` → **Principles**
  - 作为系统长期约束与最低运行法则。
- `meta/v1/0.vision.md` → **Principles**
  - 系统的终局方向与价值锚点。
- `meta/v1/1.real-goals.md` → **Principles**
  - “为什么做”与“做成什么算成功”的抽象目标。
- `meta/v1/2.core-principles.md` → **Principles**
  - 设计原则与反模式警戒线。
- `meta/v1/3.human-ai-cooperation.md` → **Principles**
  - 人机权责、表达层分离、认知安全边界。
- `meta/v1/4.system-architecture.md` → **Patterns**
  - 可复用的系统结构与分层方式。
- `meta/v1/5.information-layers.md` → **Patterns**
  - 信息表达层与翻译层的模型（用于指导 `assets/` 与 `machine/` 的边界）。
- `meta/v1/6.evolution-philosophy.md` → **Principles**
  - 演化的价值观与“允许混乱”的系统哲学。
- `meta/v1/7.long-term-roadmap.md` → **Patterns**
  - 阶段性策略与演进节奏（可随事实修正）。

### 重要强调：meta 与日常沉淀的边界

- `meta/` **不直接参与日常沉淀**：不要把日常材料都写到 meta 里，以免 meta 变成杂物堆。
- `meta/` 为演化提供 **约束与方向**：当你要改目录、加自动化、引入新工具，先问 meta 的原则是否允许，是否需要同步更新 meta 的“设计源代码”。

---

## 3) 知识上升路径（以及反向约束）

### Evidence → Patterns：从真实到可复用

典型触发信号：
- 同类问题反复出现
- 同一类决策反复犹豫
- 重复劳动占比上升
- 某个失败模式一再发生

上升方式（不要求模板）：
- 在 `assets/evidence/` 保留语境与细节（发生了什么、为什么这么做、结果如何）
- 从多个 evidence 中抽出“可迁移的骨架”沉淀到 `assets/patterns/`
- 明确边界：适用/不适用、前提、成本、失败信号（避免把偶然经验包装成规律）

### Patterns → Principles：从可用到可长期一致

当某个 pattern 能跨项目、跨工具、跨时间持续成立时，它往往背后有更稳定的取舍原则：
- 价值取向：什么比什么更重要
- 世界模型：你相信系统如何运作
- 生成规则：面对新情境如何产生新 pattern

把这些沉淀到 `assets/principles/`，它们应当更少谈“怎么做”，更多谈“为什么这样做、这样做守护了什么”。

### Principles → Evidence：原则反向塑造观察与实践

好的 principles 不会停留在宣言，而会改变你写 evidence 的方式：
- 你会更主动记录关键假设与不确定性
- 你会更愿意记录失败与反例
- 你会更注意可复盘的决策依据

这形成闭环：**原则塑造观察，观察产生证据，证据抽出模式，模式沉淀原则**。

