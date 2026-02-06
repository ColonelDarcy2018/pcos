- #+BEGIN_QUOTE
  # KCOS - Knowledge Cognitive Operating System
  
  ## 协议版本
  KCOS v1.0.1 - 极简版
  
  ## 什么是KCOS
  KCOS是一个自演化的知识管理系统，用于AI辅助软件开发。AI通过读取本目录自动理解如何使用。
  
  ## 目录结构
  
  ```
  KCOS/
  ├── README.md              # 本文件（协议说明）
  ├── context/               # 运行时上下文（Git忽略）
  │   ├── current-task.md    # 当前任务状态
  │   ├── session-latest.md  # 最新会话摘要
  │   └── archive/           # 历史会话归档
  ├── knowledge/             # 知识资产（Git跟踪）
  │   ├── business-logic/    # 业务逻辑文档
  │   ├── architecture/      # 架构文档
  │   ├── decisions/         # 决策记录
  │   └── patterns/          # 可复用模式
  ├── templates/             # 模板库（Git跟踪）
  └── assets/                # 资源文件（Git跟踪）
      └── diagrams/          # Mermaid图表等
  ```
  
  ## AI使用指南
  
  ### 1. 会话开始时
  - 读取 `context/current-task.md` 了解当前任务
  - 读取 `context/session-latest.md` 了解上次会话
  
  ### 2. 开发过程中
  - 复杂业务逻辑 → 写入 `knowledge/business-logic/`
  - 架构决策 → 写入 `knowledge/architecture/`
  - 关键决策 → 写入 `knowledge/decisions/`
  - 可复用模式 → 写入 `knowledge/patterns/`
  
  ### 3. 会话结束时
  - 更新 `context/current-task.md`
  - 创建 `context/session-{日期}.md`
  - 更新 `context/session-latest.md` 软链接
  
  ### 4. 使用模板
  - 功能开发 → `templates/feature.md`
  - Bug修复 → `templates/bugfix.md`
  - 代码重构 → `templates/refactor.md`
  - 代码探索 → `templates/explore.md`
  
  ## 全局KCOS
  通用知识存储在 `~/KCOS/`：
  - 高度抽象的模式
  - 跨项目可复用的经验
  - 最佳实践总结
  
  项目级KCOS可以引用全局KCOS中的内容。
  
  ## 文件链接规范
  
  ### 路径格式规则
  
  为了保持跨机器可移植性，文件链接应使用**相对路径**格式：
  
  | 场景 | 推荐格式 | 示例 |
  |------|----------|------|
  | **项目内文件** | 相对路径 | `[run.py](../android/uiautomator/src/main/python/run.py)` |
  | **KCOS内部** | 相对路径 | `[业务逻辑](./knowledge/business-logic/)` |
  | **行号引用** | 追加 `#L{n}-L{m}` | `[run.py#L160-L176](../android/uiautomator/src/main/python/run.py#L160-L176)` |
  
  ### 禁止使用的格式
  
  - ❌ `file:///Users/xxx/...` - 绝对路径，跨机器不可用
  - ❌ `/Users/xxx/...` - 绝对路径
  
  ### 路径基准
  
  所有相对路径以 **KCOS目录** 为基准：
  ```
  /Users/zhuxiaowei/apps/rpa-mobile/
  ├── KCOS/                    # 基准目录
  │   └── knowledge/
  │       └── business-logic/
  ├── android/
  │   └── uiautomator/
  └── src/
  ```
  
  ### 示例
  
  ```markdown
  # 正确示例
  - [run.py](../android/uiautomator/src/main/python/run.py)
  - [flow.py](../android/uiautomator/src/main/python/resource/690-SP3%202/projects/flow.py)
  - [run.py#L160-L176](../android/uiautomator/src/main/python/run.py#L160-L176)
  
  # 错误示例
  - [run.py](file:///Users/zhuxiaowei/apps/rpa-mobile/android/uiautomator/src/main/python/run.py)
  ```
  
  ## 目录README规范
  
  ### 要求
  
  每个 `knowledge/` 下的子目录**必须**包含 `README.md`：
  
  ```
  knowledge/
  ├── README.md              # 知识库总览
  ├── business-logic/
  │   ├── README.md          # 业务逻辑索引
  │   └── *.md
  ├── architecture/
  │   ├── README.md          # 架构文档索引
  │   └── *.md
  └── ...
  ```
  
  ### README内容模板
  
  ```markdown
  # {目录名} 知识索引
  
  ## 目录用途
  [简述该目录存放什么类型的知识]
  
  ## 文件列表
  
  | 文件名 | 描述 | 最后更新 |
  |--------|------|----------|
  | [文件1](文件1.md) | 简述内容 | 2025-02-03 |
  
  ## 架构关系图
  ```mermaid
  [如适用，提供该领域知识的架构图]
  ```
  
  ## AI检索指南
  - 查找X相关逻辑 → 查看 [文件1](文件1.md)
  - 了解Y流程 → 查看 [文件2](文件2.md)
  ```
  
  ### 目的
  
  1. **避免遍历**: AI无需遍历所有文件，通过README快速定位
  2. **知识图谱**: 建立知识间的关联关系
  3. **快速检索**: 提供AI检索的入口指引
  
  ## 演进原则
  1. **增量更新**: 每次会话可以完善和扩展KCOS内容
  2. **保持简洁**: 优先使用图表和结构化数据，减少长文本
  3. **链接优先**: 使用文件链接而非复制内容
  4. **持续归档**: 定期将旧内容归档到 `context/archive/`
  5. **路径可移植**: 使用相对路径确保跨机器可用
  6. **目录索引**: 每个子目录必须维护README索引
  
  ---
  **注意**: 本协议由AI维护，人类只需提供方向性指导。
  
  #+END_QUOTE