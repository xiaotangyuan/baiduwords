# encoding=utf8

"""
获取代理IP

python proxyip.py http://xxx.com/iplist gen_ip_list_csvfile > ip_list.csv
"""

import sys
import csv
from browser import Browser
from bs4 import BeautifulSoup


def save_content_to_file_from_url(url, save_to_file_name):
	content = Browser().get_content(url)
	with open(save_to_file_name, 'w', encoding='utf-8') as f:
		f.write(content)


def get_ip_page_content(filename):
	with open(filename, 'r', encoding='utf-8') as f:
		content = f.read()
	return content


def gen_ip_from_file(filename):
	content = get_ip_page_content(filename)
	soup = BeautifulSoup(content, 'html.parser')
	ip_list = soup.find('table', id='ip_list')
	tr_list = ip_list.findAll('tr')
	for tr in tr_list:
		tds = tr.findAll('td')[1:-4]
		if len(tds) == 0:
			continue
		ip = tds[0].string
		port = tds[1].string
		protocal_type = tds[4].string
		print('%s,%s,%s' % (ip, port, protocal_type))


def get_ip_list_from_csvfile(csvfilename):
	ip_list = []
	with open(csvfilename, 'w', newline='', encoding='utf-8') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			ip_list.append(row)
	return ip_list


if __name__ == '__main__':
	url = sys.argv[1]
	action = sys.argv[2]
	if action == 'gen_ip_list_csvfile':
		save_to_file_name = 'ipsourepagefile.txt'
		save_content_to_file_from_url(url, save_to_file_name)
		gen_ip_from_file(save_to_file_name)

