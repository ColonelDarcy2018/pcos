- trae 版本实现
	- skill
		- 上下文管理
		- 业务逻辑图谱
		- 代码审查
		- 任务分解
	- [[kcos目录协议]] 初始化备份
-
- 目录协议
	- v1
	  collapsed:: true
		- #+BEGIN_QUOTE
		  在你辅助我进行项目迭代的过程中，我有以下问题：
		  
		  如何让你(AI)能够变成更强大的长程软件研发智能体，能够连续的开发项目不丢失上下文，即便面对复杂的业务逻辑需求（可能超出你上下文限制）
		  
		  减少人类重复劳动问题：如何每次用最少的提示词精准的为模型提供当前决策所需的全部背景信息、屏蔽干扰信息
		  
		  人机协作问题：在AI辅助迭代项目的过程中，如何保证人类能力不退化而是变强，对具体的工程不丧失工程感知力
		  #+END_QUOTE
		- #+BEGIN_QUOTE
		  我在使用trae应用（你就是trae）开发，上述内容中，哪些是trae应用本身就具备的能力，哪些需要通过提示词、agentSkill、协议等方式补充
		  #+END_QUOTE
		- #+BEGIN_QUOTE
		  现在让我们设计一个协议，用来补充trae缺失的能力，你可以先尝试设计，如果我的要求有不合理的或者不明确需要澄清的地方，你可以询问我
		  #+END_QUOTE
	- 根目录README定义了一个“文件系统约定 + 工作流”的协议：context/（运行时上下文，Git 忽略）、knowledge/（结构化知识）、templates/、assets/，并规定了相对路径链接与“每个子目录必须有 README 索引”。
	- **优点（设计上做对的点）**
		- 低门槛、可 Git 化、可移植：Markdown + Mermaid + 相对路径规范（[README.md (line 59)](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#)）让“人可读、机器可检索”都成立。
		- 读路径很清晰：目录分层 + README 索引（[README.md (line 101)](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#)）能显著降低 Agent 的“遍历成本”。
		- 有“结构化元数据”的雏形：[.index.json](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#) + 文档 front-matter（例如 [rpa-debug-http-server-logic.md (line 1)](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#)）是把知识变成可查询数据的关键一步。
		- 模板把“怎么写”标准化：[*.md](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#) 把需求/bug/重构/探索的采集字段固化，利于长期演进。
	- **缺点 / 可优化点（为什么还不像成熟协议）**
		- 单一事实源不明确，导致漂移：README 索引、front-matter、[.index.json](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#) 三套信息并存，缺少“谁是权威、谁由谁生成”的约束，久了必然不一致（你现在已经出现了）。
		- 缺少“可验证的规范”：没有 schema、没有校验器、没有 CI gate；成熟协议之所以“能用”，核心是“违背规范会被自动发现/阻止”。
		- 缺少“访问协议/查询契约”：KCOS 现在主要靠 Agent 自己读文件；但成熟生态（MCP/Skill）通常提供标准化 discovery + query + 执行入口，能被不同客户端复用。
		- 安全/边界模型比较弱：context/ 虽然 gitignore（[.gitignore (line 1)](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#)），但还缺少更明确的“敏感信息分级、脱敏、可共享/不可共享边界”约定。
	- **怎么把 KCOS 打造成“同级别的实用协议”（建议路线，优先借鉴成熟方案）**
		- 先把 KCOS 定位成两层：
			- KCOS-Store（存储规范）：目录结构 + front-matter + 链接规则（类似 docs-as-code 规范）。
			- KCOS-Access（访问协议）：直接“借 MCP”，把 KCOS 暴露成 MCP 的 resources/tools（别自造一套传输协议）。