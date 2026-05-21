- 工时占用累计：9h
- 信息备份
	- 17302269678
	- Abc123456!
- 元素点击无效问题
  id:: 697c69c6-ba73-410c-b3b2-a64c31e744a2
	- click无效，没有clickable=true的元素
	- clickCenter无效
		- 排查过程
			- 通过高亮显示目标元素排查，发现选中的元素与目标元素位置不一致
				- 执行命令：UiSelectorHandler.highlightBoundsAnimation(target_uiobj.bounds())
			- 排查发现匹配到了多个元素
				- 排查命令：使用zbot.log(zbot.selector().text("待办事项").visibleToUser().find().size())
			- selector增加visibleToUser后可以唯一定位，问题解决
				- 完整示例：zbot.selector().text("待办事项").visibleToUser().findOne(1000)
	- 总结
		- TODO 整理归档
		- 元素点击失效可能由多个原因造成
			- clickable=false导致常规元素点击失效
			- selector匹配到多个元素，其中findOne默认匹配到的不是目标元素，导致不能点击到目标元素位置
		- 元素选择器不能唯一定位目标元素时，使用findOne指令是十分危险的，当前案例是测试时就匹配到错误元素，如果测试时匹配到正确元素，而上线运行时才匹配到错误元素，后果更严重
		  id:: 697c6e33-2bc3-43ed-a6b2-ea0ccd8ff3c9
			- 解决方案思考
				- 在高级指令文档中明确提示findOne指令的风险
				- 设计标准开发范式，规范脚本开发，避免出现该问题，待设计 [[手机RPA脚本开发范式]]
				- 强制要求执行clickCenter命令时的元素选择器必须增加visibleToUser()
		- click、clickCenter当执行到false、错误目标元素时，缺少反馈信息，导致排查问题较为困难，对新手很不友好
			- 解决方案思考
				- clickCenter方法增加高亮标注点击目标动画效果，实时反馈用户点击的位置，这样当匹配到错误元素时，可以快速排查出原因
				- click执行到clickable=false的元素时，直接抛出异常停止流程，这样用户马上收到不能点击的反馈
		- 关于[[手机RPA脚本开发范式]]的思考
			- 解决findOne指令问题
				- 问题描述
					- ((697c6e33-2bc3-43ed-a6b2-ea0ccd8ff3c9))
				- 目前的开发流程中，通常需要频繁运行打印selector查询到的元素数量来判断是否元素选择器定位唯一元素，如何自动化或者优化该流程？
			- 等待元素刷新的时机问题
				- 问题描述
					- 有些场景需要增加睡眠等待时机才能保证稳定性，比如页面切换后，导致需要增加很多强制睡眠等待的代码，该方式存在难以保证绝对稳定性、降低流程执行效率、降低代码可读性、增加隐性上下文等弊端
				- 解决方案思考
					- 考虑在[[手机RPA脚本开发范式]]中增加页面范式，将脚本代码与页面进行绑定，再通过通用的页面检测方法来判定页面切换是否成功
						- 弊端
							- 增加了流程脚本的整体复杂度
							- 页面切换逻辑通常需要特殊元素判断，需要人工查找判定元素，增加了流程开发的工作量的同时，判定元素的引入也提高了流程稳定性的风险
						- 优势
							- 与页面绑定方便单元测试
							- 代码与页面绑定，耦合性降低，后续可以进行模块化组合，也可能更利于模型理解
- 代码备份：
	- v2
	  collapsed:: true
		- ```
		  """
		  v2版本
		  """
		  def main(zbot, *args, **kwargs):
		      import time
		  
		  
		      def time_cost(func):
		          """
		          计算耗时的通用方法
		          """
		  
		          def wrapper(*args, **kwargs):
		              start_time = time.perf_counter()
		              result = func(*args, **kwargs)
		              zbot.log("耗时：{}".format(time.perf_counter() - start_time) + "秒")
		              return result
		  
		          return wrapper
		  
		  
		      def swipe_and_click():
		          try:
		              zbot.automator.swipeDown()
		              target_uiobj = zbot.selector().text("一件事看板").visibleToUser().findOne(3000).parent()
		              target_uiobj.click()
		              return True
		          except:
		              return False
		  
		  
		      def clickCenterWithHighLight(target_uiobj):
		          from com.aiindeed.mobileagent.handler import UiSelectorHandler
		          UiSelectorHandler.highlightBoundsAnimation(target_uiobj.bounds())
		          zbot.sleep(500)
		          zbot.automator.clickCenter(target_uiobj)
		  
		  
		      @time_cost
		      def findElementTimeCount(inner_selector):
		          if inner_selector.findOne(10000):
		              zbot.log("页面刷新完成")
		          else:
		              zbot.warn("页面刷新失败")
		  
		  
		      def login():
		          zbot.app.launchApp("秦政通预发")
		          # 登陆
		          account = "17302269678"
		          password = "Abc123456!"
		          zbot.selector().id('account').className('android.widget.EditText').findOne(5000).setText(account)
		  
		          zbot.selector().id('tv_psw').className('android.widget.EditText').findOne(5000).setText(password)
		  
		          zbot.selector().className('android.widget.CheckBox').findOne(5000).click()
		  
		          zbot.selector().id('login').className('android.widget.Button').findOne(5000).click()
		  
		  
		      def inner_page_back():
		          target_uiobj = zbot.selector().id("back_layout").visibleToUser().findOne(10000)
		          if target_uiobj:
		              target_uiobj.click()
		          else:
		              raise Exception("未找到返回按钮")
		  
		  
		      # 1.打开秦政通，登陆账号
		      try:
		          login()
		      except:
		          zbot.log("登陆失败，跳过")
		  
		      # 2.检查代办状态
		      clickCenterWithHighLight(zbot.selector().text("待办事项").visibleToUser().findOne(10000).parent())
		      zbot.log("代办事项页面加载")
		      findElementTimeCount(zbot.selector().text("待办").visibleToUser())
		      inner_page_back()
		  
		      # 3.检查音视频状态
		      clickCenterWithHighLight(zbot.selector().text("工作台").visibleToUser().findOne(10000).parent())
		      clickCenterWithHighLight(zbot.selector().text("视频会议").visibleToUser().findOne(10000).parent())
		      zbot.log("视频会议页面加载")
		      findElementTimeCount(zbot.selector().text("Network error").visibleToUser())  # 仅适用于页面加载失败的情况
		      inner_page_back()
		      zbot.automator.back()  # 页面加载失败的情况下需要叠加一次后退操作才能成功
		  
		      # 4.检查VPN打开状态
		      clickCenterWithHighLight(zbot.selector().text("我的").visibleToUser().findOne(10000).parent())
		      zbot.selector().text("VPN").visibleToUser().findOne(10000).parent().click()
		      zbot.log("vpn页面加载")
		      findElementTimeCount(zbot.selector().visibleToUser().id('link_bg'))
		      target_obj = zbot.selector().text("连接VPN").className("android.widget.Button").findOne(2000)
		      if target_obj:
		          target_obj.click()
		          zbot.sleep(2000)
		      inner_page_back()
		      
		          
		  ```
	- v1
	  collapsed:: true
		- ``` 
		  def main(zbot, *args, **kwargs):
		      import time
		      """
		      v1版本
		      """
		      def swipe_and_click():
		          try:
		              zbot.automator.swipeDown()
		              target_uiobj = zbot.selector().text("一件事看板").visibleToUser().findOne(3000).parent()
		              target_uiobj.click()
		              return True
		          except:
		              return False
		  
		  
		      def clickCenterWithHighLight(target_uiobj):
		          from com.aiindeed.mobileagent.handler import UiSelectorHandler
		          UiSelectorHandler.highlightBoundsAnimation(target_uiobj.bounds())
		          zbot.sleep(500)
		          zbot.automator.clickCenter(target_uiobj)
		  
		  
		      clickCenterWithHighLight(zbot.selector().text("待办事项").visibleToUser().findOne(10000).parent())
		      clickCenterWithHighLight(zbot.selector().id("__vconsole").visibleToUser().findOne(10000))
		  
		      zbot.sleep(2000)
		  
		      target_uiobj = zbot.selector().id("back_layout").visibleToUser().findOne(10000)
		      target_uiobj.click()
		  
		      clickCenterWithHighLight(zbot.selector().text("工作台").visibleToUser().findOne(10000).parent())
		  
		      zbot.sleep(3500)
		  
		      for i in range(2):
		          if swipe_and_click():
		              break
		  
		      target_uiobj = zbot.selector().id("back_layout").visibleToUser().findOne(10000)
		      target_uiobj.click()
		      zbot.sleep(2000)
		  
		      zbot.automator.swipeUp()
		      target_uiobj = zbot.selector().text(" 返回工作台 ").visibleToUser().findOne(5000)
		      target_uiobj.click()
		  
		      clickCenterWithHighLight(zbot.selector().text("通讯录").visibleToUser().findOne(10000).parent())
		  
		      target_uiobj = zbot.selector().text("搜索").visibleToUser().findOne(10000)
		      target_uiobj.click()
		  
		      zbot.sleep(3000)
		  
		      zbot.selector().id("contact_search_edit_text").findOne(3000).setText("实在智能")
		  
		      target_uiobj = zbot.selector().text("取消").visibleToUser().findOne(1000)
		      target_uiobj.click()
		  
		      zbot.sleep(2000)
		  
		      clickCenterWithHighLight(zbot.selector().text("我的").visibleToUser().findOne(10000).parent())
		  
		  ```
-