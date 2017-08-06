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

import re


def get_ipinfo_from_text(htmlcontent):
	pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\D+(\d{2,5})")
	match = pattern.findall(htmlcontent)
	if match:
		return match
	else:
		return []


def get_htmlcontent_files():
	pythonpath = os.environ['PYTHONPATH']
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


if __name__ == '__main__':

	ipinfo_list = get_ipinfo_list()
	for ipinfo in ipinfo_list:
		print ipinfo
	print len(ipinfo_list)

