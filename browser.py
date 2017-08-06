# encoding=utf8

"""
获取浏览器
"""


from selenium import webdriver


class Browser():
	def __init__(self, proxy_ip=None, proxy_port=None, timeout=10):
		self.proxy_ip = proxy_ip
		self.proxy_port = proxy_port
		self.timeout = timeout
		self.browser = None

	def get_browser_obj(self):
		desired_capabilities = webdriver.common.desired_capabilities.DesiredCapabilities.PHANTOMJS.copy()
		if self.proxy_ip is not None and self.proxy_port is not None:
			proxy = webdriver.common.proxy.Proxy(
			    {
			        'proxyType': webdriver.common.proxy.ProxyType.MANUAL,
			        'httpProxy': '%s:%s' % (self.proxy_ip, self.proxy_port)  # 代理ip和端口
			    }
			)
			proxy.add_to_capabilities(desired_capabilities)
		browser = webdriver.PhantomJS(
		    desired_capabilities=desired_capabilities
		)
		browser.set_page_load_timeout(self.timeout)
		# browser.set_window_size(1920,1080)
		return browser

	def get_content(self, url):
		if self.browser is None:
			self.browser = self.get_browser_obj()
		self.browser.get(url)
		return self.browser.page_source
