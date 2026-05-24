- > 手机rpa 服务端（项目名称：rpa-mobile-agent-web）相关内容
- 需求池
	- 埋点记录下载信息功能开发
		- 需求分析：记录下载者ip、下载版本、具体的apk包、时间等信息，同时支持查询记录列表、查询下载次数
		- DOING 功能实现
		  :LOGBOOK:
		  CLOCK: [2026-01-30 Fri 18:30:16]
		  :END:
			- 代码开发自测及问题修复
			- 修改数据库，新增数据表
- gpt4接口地址
	- bigmodel:
		- driver: chatGPT4
		- appKey: a4f2e7d9-8c1b-4567-890a-bcdef1234567
		- appSecret: 5f8d2c7b-1a34-5678-b2c1-0123456789ab7d6e5f4c
		- endpoint: http://rpa-algo-chat:8080/openApi/agent/chatGpt/call
-
- apk固定下载地址
	- https://shenyu-bootstrap.ai-indeed.com/rpa-mobile-agent-web/api/agentWeb/version/get-last-version-apk
	- https://shenyu-bootstrap.ai-indeed.com/rpa-mobile-agent-web/api/agentWeb/version/get-last-version-apk?featureSet=Origin&packVersion=Advanced
- 本地调试运行项目方法
	- 在IDE中增加Program arguments：--spring.profiles.active=qa