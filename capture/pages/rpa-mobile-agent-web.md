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
-
- mysql
	- qa
	- 生产
- kubectl
	- 日志查看
		- kubectl -n qa get po | grep rpa-mobile-agent-web
		- kubectl -n qa logs -f rpa-mobile-agent-web-68bcf69f6-5nhxt
		- kubectl -n qa logs rpa-mobile-agent-web-68bcf69f6-5nhxt | grep error
- redis
	- redis-cli -h r-bp15bio5oew2f08a4e.redis.rds.aliyuncs.com -p 6379 -a Iindeed1008
	- select 8
	- get xxx
- apk固定下载地址
	- https://shenyu-bootstrap.ai-indeed.com/rpa-mobile-agent-web/api/agentWeb/version/get-last-version-apk
	- https://shenyu-bootstrap.ai-indeed.com/rpa-mobile-agent-web/api/agentWeb/version/get-last-version-apk?featureSet=Origin&packVersion=Advanced
- 本地调试运行项目方法
	- 在IDE中增加Program arguments：--spring.profiles.active=qa