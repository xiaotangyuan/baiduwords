"""
案例http://blog.csdn.net/tcorpion/article/details/70213435
代理IP  http://www.xicidaili.com/

settings.py
example:
target_keywords = [
	'xxx'
]

# (http/https, ip, port)
proxy_ips = [
	('http', '223.13.69.86', '8118'),
]

"""

import time, datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import settings


def log(keyword, protocol, ip, port, res_title, res_page_source):
	items = [keyword, protocol, ip, port, res_title, res_page_source]
	print(','.join(items))


def flush_word(keyword, protocol, ip, port):
	service_args = [
	    '--proxy=%s:%s' % (ip, port),
	    '--proxy-type=%s' % protocol,
	    ]
	print(datetime.datetime.now())
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = (
	    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
	    "(KHTML, like Gecko) Chrome/15.0.87"
	)
	# dcap["phantomjs.page.settings.loadImages"] = False
	# browser = webdriver.PhantomJS(desired_capabilities=dcap)
	browser = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
	browser.set_window_size(1920,1080)
	# browser = webdriver.PhantomJS()
	# browser = webdriver.Chrome()
	browser.get('http://www.baidu.com/')
	time.sleep(15)
	# print('this is current_url:'+browser.current_url)
	# keyword = 'ip'
	browser.find_element_by_id("kw").send_keys(keyword)
	# browser.save_screenshot('screenshot1_send_key.png')
	time.sleep(5)
	browser.find_element_by_id('su').click()
	time.sleep(15)
	# browser.execute_script("$('#su').click()")
	# browser.save_screenshot('screenshot1_click.png')
	log(keyword, protocol, ip, port, browser.title, browser.page_source[:100])
	print(datetime.datetime.now())


for keyword in settings.target_keywords:
	for protocol, ip, port in settings.proxy_ips:
		flush_word(keyword, protocol, ip, port)

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