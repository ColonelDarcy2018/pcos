- 需求池
	- 如何解决实施过程中单元测试操作步骤复杂的问题
	- 支持多文件以便于流程模块化开发
- 路线图
	- 通用流程包结构设计（方便AI生成与测试）
		- 收敛标准通用流程包模板源，实现**MCP/Daemon 调用 App 导出流程包能力**，使App 成为单一真源（SSOT）
	- IDE
		- 设备连接
		- 任务下发
		- 导出流程包
			- vscode插件
				- 导出流程包
					- DONE 支持右键导出rpa流程包功能
					- DONE 支持输入版本号、自定义流程包名称
					- DONE 默认导出通用入参版流程包
					- 流程包说明
						- 支持输入自定义流程包说明
				-
	- 模型辅助脚本开发能力
	- 模型框架能力
		- 流程包管理
			- AI对话导出流程包
				- AI自动管理流程包版本（在流程代码中约定好流程的版本说明注释位置）
				- AI自动识别流程包名称（在流程代码中约定好流程名称的固定注释位置）
				- 支持AI自动生成(根据入参结构)流程包说明
		- 通用传参调度能力
		- apk管理
			- 自动打包apk+运行功能（仅高级开发）
			- 自动安装apk
				- 批量安装apk，需要先实现批量连接设备功能
			-
		- 远程任务调度测试闭环
			- 运营平台开放接口对接（模型具备开放平台接口调用能力，mcp）
				- 上传流程包接口
				- 查询指定设备id接口（在创建任务计划时可以通过下拉列表选择指定设备）
				- 创建任务计划接口
				- 下发任务接口
	-
-
- 总体设计构思
	- 以最小mvp的形式先实现个人开发助手，借用代码开发平台的能力实现自动化的脚本开发，迭代过程中发现问题解决问题，不断优化
	- 需求
		- 让模型能够理解什么是手机rpa脚本开发，学会使用高级指令，具备辅助rpa脚本开发的基础能力
		- 如何最大化减小人工介入？
			- 解决元素拾取相关的问题
				- 引入视觉模型强化自动分析能力（是否有可能实现模型自动拾取元素，自动操作元素实现流程？）
				- 半自动实现方案，人类拾取元素，告知模型，模型编写元素选择器并实现元素操作相关代码
		- 如何提高脚本开发质量？
			- 让模型进行稳定性框架设计，代码优化，总结已实现流程的知识资产
- RPA脚本自动化开发基础
	- 如何让AI以最快的速度掌握RPA脚本开发所需的全部上下文，并切token使用量最小？我现在的思路是设计一套索引+RAG组合的方式，RAG+全量的脚本开发文档（文件内容较多）作为兜底，而优先使用索引上下文的方式，即维护一个常用开发业务+常用api的上下文文档，这样文档会很轻量，用户描述一个需求时，自动根据其需求去命中索引（要求不断优化索引，索引设计要求高）
	- 当前的RPA开发平台的代码还需要人手动去运行才能下发给手机app执行，是否可以实现一套mcp接口，trae/vscode用户将其添加为mcp后，AI就知道如何自动下发脚本而不需要人去手动操作了？这个mcp要怎么设计？
-
	- 关于引入RAG的必要性
	  collapsed:: true
		- **结论**
		- 你现在的“切分结果”本身不是 RAG，它只是 **RAG 的预处理步骤**（文档分块）。
		- 如果没有检索层（向量/关键词索引 + 召回 + 重排），就会变成“模型自己猜该读哪个文件”，复杂场景会不稳。
		- 面向你未来的独立开发平台，建议上 **Hybrid Agentic RAG**，而不是只靠分块文件。
		  
		  **“切分检索” vs RAG（本质区别）**
		- [split_advanced_doc.py](https://file+.vscode-resource.vscode-cdn.net/Users/zhuxiaowei/.vscode/extensions/openai.chatgpt-0.5.71-darwin-arm64/webview/#)：解决“怎么切文档”。
		- RAG：解决“如何在查询时找对片段并可追溯引用”。
		- 完整 RAG 至少包含：ingestion -> indexing -> retrieval -> rerank -> grounding/citation -> eval。
		  
		  **更好的实现方案（独立平台推荐）**
		- 文档层：分块时写入 metadata（章节、主题、版本、来源、更新时间）。
		- 检索层：**混合检索**（Dense + Sparse/BM25）+ RRF 融合 + reranker。
		- 编排层：查询路由（API 查询 / 故障排查 / 复杂脚本设计 / 全局总结）。
		- 记忆层：项目记忆（你的脚本、日志、失败案例）与知识库分开索引。
		- 评估层：离线指标 Recall@k / MRR / nDCG + 在线指标（首答命中率、修复轮次、人工接管率）。
		  
		  **针对手机 RPA 开发平台的分阶段落地**
		- P0（2-4周）：现有切分 + 向量库 + BM25 + RRF + 引用回链。
		- P1（4-8周）：加 reranker、查询分类器、日志/截图联合检索。
		- P2（8周+）：仅对“全局问题”引入 GraphRAG（它对全局总结有价值，但索引成本高）。
		  
		  **市场成熟方案可借鉴**
		- 托管快速起步：OpenAI file_search（官方支持 semantic + keyword、metadata filter）。
		- 自建可控方案：Qdrant/Elastic 的 hybrid + RRF + 多阶段检索。
		- 全局语义总结：Microsoft GraphRAG（注意其索引成本与调参成本）。
		  
		  **参考链接**
		- RAG 论文（经典定义）：[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
		- MCP 规范（2025-11-25）：[https://modelcontextprotocol.io/specification/2025-11-25/basic](https://modelcontextprotocol.io/specification/2025-11-25/basic)
		- OpenAI File Search 指南：[https://platform.openai.com/docs/guides/tools-file-search/](https://platform.openai.com/docs/guides/tools-file-search/)
		- Elastic RRF（混合检索融合）：[https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)
		- Qdrant Hybrid Queries（多阶段/prefetch）：[https://qdrant.tech/documentation/concepts/hybrid-queries/](https://qdrant.tech/documentation/concepts/hybrid-queries/)
		- GraphRAG 论文（全局问题优势）：[https://arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130)
		- GraphRAG 官方仓库（含成本提示）：[https://github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)
		- BEIR（检索基准）：[https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663)
-
- [[手机RPA流程脚本]]