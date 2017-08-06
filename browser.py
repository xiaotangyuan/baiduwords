# encoding=utf8

"""
获取浏览器
"""

from optparse import OptionParser
from selenium import webdriver
import requests


userAgent_chrome = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'


class Browser():
	def __init__(self, proxy_ip=None, proxy_port=None, timeout=10):
		self.proxy_ip = proxy_ip
		self.proxy_port = proxy_port
		self.timeout = timeout
		self.browser = None

	def get_browser_obj(self):
		desired_capabilities = webdriver.common.desired_capabilities.DesiredCapabilities.PHANTOMJS.copy()
		desired_capabilities['phantomjs.page.settings.userAgent'] = (
			userAgent_chrome
		)
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
		browser.set_window_size(1920,1080)
		return browser

	def get_content(self, url, client='PhantomJS'):
		if client == 'requests':
			return requests.get(url).text
		if self.browser is None:
			self.browser = self.get_browser_obj()
		self.browser.get(url)
		return self.browser.page_source

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i', '--ipinfo', dest='ipinfo', help=u'包含ip和端口  如192.168.1.1:20')
	
	options, args=parser.parse_args()
	ipinfo = options.ipinfo
	ip, port = ipinfo.split(':')
	url = 'http://www.baidu.com/s?wd=ip'
	content = Browser(ip, port, 30).get_content(url)
	# print content[:100]
	from bs4 import BeautifulSoup
	soup = BeautifulSoup(content, 'html.parser')
	sourcecontent = soup.find('div',class_='c-span21 c-span-last op-ip-detail').text.replace('\n', '')
	print sourcecontent
