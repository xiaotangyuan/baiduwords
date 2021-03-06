# encoding=utf8
"""
测试IP是否可用

案例http://blog.csdn.net/tcorpion/article/details/70213435
代理IP  http://www.xicidaili.com/

1 生成ip_list.csv   python proxyip.py http://xxx.com/iplist gen_ip_list_csvfile > ip_list.csv
2 python main.py  开始执行


settings.py
example:
target_keywords = [
	'xxx'
]

# (http/https, ip, port)
proxy_ips = [
	('http', '223.13.69.86', '8118'),
]

from proxyip import get_ip_list_from_csvfile
csvfilename = 'ip_list.txt'
proxy_ips = get_ip_list_from_csvfile(csvfilename)

"""

import time, datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import settings

settings.target_keywords = [
	'ip'
]

def log(keyword, protocol, ip, port, res_title, res_page_source):
	items = [keyword, protocol, ip, port, res_title, res_page_source]
	print(','.join(items))


def flush_word(keyword, protocol, ip, port):
	proxy = Proxy(
	    {
	        'proxyType': ProxyType.MANUAL,
	        'httpProxy': '%s:%s' % (ip, port)  # 代理ip和端口
	    }
	)
	desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
	proxy.add_to_capabilities(desired_capabilities)
	browser = webdriver.PhantomJS(
	    desired_capabilities=desired_capabilities
	)
	browser.set_page_load_timeout(15)
	browser.set_window_size(1920,1080)
	browser.get('http://www.baidu.com/')
	# 可能代理太慢，需要等待一會
	# time.sleep(10)
	print('this is current_url:'+browser.current_url)
	if browser.current_url == 'about:blank':
		return None
	# keyword = 'ip'
	browser.find_element_by_id("kw").send_keys(keyword)
	browser.save_screenshot('screenshot1_send_key.png')
	time.sleep(5)
	browser.find_element_by_id('su').click()
	time.sleep(5)
	# browser.execute_script("$('#su').click()")
	browser.save_screenshot('screenshot1_click.png')
	return browser
	# print(datetime.datetime.now())


def main():
	for keyword in settings.target_keywords:
		for ip, port, protocol in settings.proxy_ips:
			print('check: %s  %s %s' % (keyword, ip, port))
			try:
				browser = flush_word(keyword, protocol, ip, port)
				if browser is None:
					print('can not use')
					continue
			except selenium.common.exceptions.TimeoutException:
				print('timeout')
				continue
			except selenium.common.exceptions.NoSuchElementException:
				print('not find the element')
				continue
			title = browser.title
			soup = BeautifulSoup(browser.page_source, 'html.parser')
			sourcecontent = soup.find('div',class_='c-span21 c-span-last op-ip-detail').text.replace('\n', '')
			# except:
			# 	title = 'error fail'
			# 	sourcecontent = ''
			log(keyword, protocol, ip, port, title, sourcecontent)


if __name__ == '__main__':
	main()

# dir(browser):
 # 'add_cookie',
 # 'application_cache',
 # 'back',
 # 'capabilities',
 # 'close',
 # 'command_executor',
 # 'create_web_element',
 # 'current_url',
 # 'current_window_handle',
 # 'delete_all_cookies',
 # 'delete_cookie',
 # 'desired_capabilities',
 # 'error_handler',
 # 'execute',
 # 'execute_async_script',
 # 'execute_script',
 # 'file_detector',
 # 'file_detector_context',
 # 'find_element',
 # 'find_element_by_class_name',
 # 'find_element_by_css_selector',
 # 'find_element_by_id',
 # 'find_element_by_link_text',
 # 'find_element_by_name',
 # 'find_element_by_partial_link_text',
 # 'find_element_by_tag_name',
 # 'find_element_by_xpath',
 # 'find_elements',
 # 'find_elements_by_class_name',
 # 'find_elements_by_css_selector',
 # 'find_elements_by_id',
 # 'find_elements_by_link_text',
 # 'find_elements_by_name',
 # 'find_elements_by_partial_link_text',
 # 'find_elements_by_tag_name',
 # 'find_elements_by_xpath',
 # 'forward',
 # 'get',
 # 'get_cookie',
 # 'get_cookies',
 # 'get_log',
 # 'get_screenshot_as_base64',
 # 'get_screenshot_as_file',
 # 'get_screenshot_as_png',
 # 'get_window_position',
 # 'get_window_rect',
 # 'get_window_size',
 # 'implicitly_wait',
 # 'log_types',
 # 'maximize_window',
 # 'mobile',
 # 'name',
 # 'orientation',
 # 'page_source',
 # 'quit',
 # 'refresh',
 # 'save_screenshot',
 # 'service',
 # 'session_id',
 # 'set_page_load_timeout',
 # 'set_script_timeout',
 # 'set_window_position',
 # 'set_window_rect',
 # 'set_window_size',
 # 'start_client',
 # 'start_session',
 # 'stop_client',
 # 'switch_to',
 # 'switch_to_active_element',
 # 'switch_to_alert',
 # 'switch_to_default_content',
 # 'switch_to_frame',
 # 'switch_to_window',
 # 'title',
 # 'w3c',
 # 'window_handles']
