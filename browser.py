# encoding=utf8

"""
获取浏览器
"""


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser():
	def get_content(self, url):
		dcap = dict(DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.userAgent"] = (
		    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
		    "(KHTML, like Gecko) Chrome/15.0.87"
		)
		browser = webdriver.PhantomJS(desired_capabilities=dcap)
		browser.set_window_size(1920,1080)
		browser.get(url)
		return browser.page_source
