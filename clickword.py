# encoding=utf8
"""
模拟浏览器访问

"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import gc
import os
import time, datetime
import selenium
from browser import Browser
from utils import redis_util
from optparse import OptionParser


def log(is_success, keyword, ip, port, info):
	# items = [str(is_success), keyword, ip, port, info]
	# print(','.join(items))
	print is_success, keyword, ip, port, info


def flush_word(keyword, ip, port):
	browser = Browser(ip, port, timeout=30).get_browser_obj()
	browser.get('http://www.baidu.com/')
	# print '[clickword] getting url ···'
	is_success = False
	# 可能代理太慢，需要等待一會
	# time.sleep(2)
	# print('this is current_url:'+browser.current_url)
	# if browser.current_url == 'about:blank':
	# 	return is_success, browser
	browser.find_element_by_id("kw").send_keys(keyword)
	# browser.save_screenshot('screenshot1_send_key.png')
	# time.sleep(5)
	browser.find_element_by_id('su').click()
	is_success = True
	return is_success, browser


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-w', '--keyword', dest='keyword', help=u'关键词')
	parser.add_option('-t', '--testip', dest='testip', action='store_true', help=u'测试库中的ip')
	parser.add_option('-s', '--singleipinfo', dest='singleipinfo', help=u'测试单个ip')
	
	options, args=parser.parse_args()
	keyword = options.keyword
	singleipinfo = options.singleipinfo

	if singleipinfo:
		ip, port = singleipinfo.split(':')
		try:
			print '[clickword] using %s:%s ···' % (ip, port)
			is_success, browser = flush_word('ip', ip, port)
			if is_success is False:
				print browser
				sys.exit()
			from bs4 import BeautifulSoup
			soup = BeautifulSoup(browser.page_source, 'html.parser')
			ip_box = soup.find('div',class_='c-span21 c-span-last op-ip-detail')
			if not ip_box:
				print 'not find the element by BeautifulSoup'
				sys.exit()
			sourcecontent = ip_box.text.replace('\n', '')
			print u'代理IP地址:', sourcecontent
		except selenium.common.exceptions.TimeoutException:
			print 'timeout'
		except selenium.common.exceptions.NoSuchElementException:
			print 'not find the element'
		except Exception as e:
			print '%s' % e
		sys.exit()

	if keyword:
		keyword = keyword.replace('_', ' ')
		keyword = unicode(keyword, 'utf8')
	# print keyword
	
	testip = options.testip

	if testip is True:
		print '====== now is testip ======'
		while True:
			print '[clickword] begin get new ipinfo ···'
			ipinfo = redis_util.get_ipinfo_from_queue()
			if ipinfo is None:
				raise Exception('ipinfo is None from queue, it is an error!')
			ip, port = ipinfo.split(':')
			try:
				print '[clickword] using %s:%s ···' % (ip, port)
				is_success, browser = flush_word('ip', ip, port)
				if is_success is False:
					print browser
					continue
				from bs4 import BeautifulSoup
				soup = BeautifulSoup(browser.page_source, 'html.parser')
				ip_box = soup.find('div',class_='c-span21 c-span-last op-ip-detail')
				if not ip_box:
					print 'not find the element by BeautifulSoup'
					continue
				sourcecontent = ip_box.text.replace('\n', '')
				print 'sourcecontent:', sourcecontent
			except selenium.common.exceptions.TimeoutException:
				print 'timeout'
			except selenium.common.exceptions.NoSuchElementException:
				print 'not find the element'
			except Exception as e:
				print '%s' % e
	else:
		if keyword is None:
			raise Exception('keyword can not be None')
		while True:
			# print '[clickword] begin get new ipinfo ···'
			ipinfo = redis_util.get_ipinfo_from_queue()
			if ipinfo is None:
				raise Exception('ipinfo is None from queue, it is an error!')
			ip, port = ipinfo.split(':')
			try:
				is_success, browser = flush_word(keyword, ip, port)
				info = browser.title
			except selenium.common.exceptions.TimeoutException:
				is_success = False
				info = '[clickword] timeout'
			except selenium.common.exceptions.NoSuchElementException:
				is_success = False
				info = '[clickword] not find the element'
			except Exception as e:
				is_success = False
				info = '[clickword] %s' % e

			log(is_success, keyword, ip, port, info)
			browser = None
			gc.collect()