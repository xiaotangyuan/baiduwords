# encoding=utf8

"""
获取代理IP
"""

import os
import sys
import csv
from browser import Browser
from bs4 import BeautifulSoup
from io import open
from optparse import OptionParser
from utils import redis_util

import re

pythonpath = os.environ['PYTHONPATH']


def get_ipinfo_from_text(htmlcontent):
	pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\D+(\d{2,5})")
	match = pattern.findall(htmlcontent)
	if match:
		return match
	else:
		return []


def get_htmlcontent_files():
	htmldirname = os.path.join(pythonpath, 'htmlcontent')
	htmlfile_list = []
	for dirpath, dirnames, filenames in os.walk(htmldirname):
		filenames = [os.path.join(dirpath, filename) for filename in filenames]
		htmlfile_list.extend(filenames)
	return htmlfile_list


def get_ipinfo_list():
	ipinfo_list = []
	htmlfile_list = get_htmlcontent_files()
	for htmlfile in htmlfile_list:
		try:
			with open(htmlfile, 'r', encoding='utf-8') as f:
				content = f.read()
		except UnicodeDecodeError:
			with open(htmlfile, 'r', encoding='gbk') as f:
				content = f.read()		
		ipinfos = get_ipinfo_from_text(content)
		print htmlfile, len(ipinfos)
		ipinfo_list.extend(ipinfos)
	return ipinfo_list


proxy_web_list = [
	('xici', 'http://www.xicidaili.com/nn/'),
	('ip66', 'http://www.66ip.cn/areaindex_2/1.html'),
	('ip3366', 'http://www.ip3366.net/'),
	('ip3366_page2', 'http://www.ip3366.net/?page=2'),
]


headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
	        "Accept-Encoding":"gzip",
	        "Accept-Language":"zh-CN,zh;q=0.8",
	        "Referer":"http://www.example.com/",
	        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }



def save_proxy_web_content():
	import requests
	for name, url in proxy_web_list:
		content = requests.get(url, headers=headers).text
		filename = os.path.join(pythonpath, 'htmlcontent', '%s.html' % name)
		with open(filename, 'w') as f:
			f.write(content)


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-s', '--saveweb', dest='saveweb', action='store_true', help=u'保存网页内容')
	parser.add_option('-r', '--toredis', dest='toredis', action='store_true', help=u'保存从网页内容提取出来的IP到redis')
	parser.add_option('-t', '--testshowipinfo', dest='testshowipinfo', action='store_true', help=u'打印从网页内容提取出来的IP')

	options, args=parser.parse_args()
	saveweb = options.saveweb
	toredis = options.toredis
	testshowipinfo = options.testshowipinfo

	if saveweb is True:
		save_proxy_web_content()

	if toredis is True:
		ipinfo_list = get_ipinfo_list()
		for ipinfo in ipinfo_list:
			redis_util.push_to_queue(':'.join(ipinfo))

	if testshowipinfo is True:
		ipinfo_list = get_ipinfo_list()
		for ipinfo in ipinfo_list:
			print ':'.join(ipinfo)
		print len(ipinfo_list)
