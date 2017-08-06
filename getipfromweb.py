# encoding=utf8

"""
从web上采集获取IP
"""


from bs4 import BeautifulSoup
from utils import redis_util
from browser import Browser
# 西刺代理

def xici():
	url = 'http://www.xicidaili.com/nn/'
	content = Browser(timeout=30).get_content(url)
	# content = Browser(timeout=30).get_content(url, client='requests')
	soup = BeautifulSoup(content, 'html.parser')
	ip_list = soup.find('table', id='ip_list')
	tr_list = ip_list.findAll('tr')
	ipinfo_list = []
	for tr in tr_list:
		tds = tr.findAll('td')[1:-4]
		if len(tds) == 0:
			continue
		ip = tds[0].string
		port = tds[1].string
		protocal_type = tds[4].string
		ipinfo_list.append('%s:%s' % (ip, port))
	return ipinfo_list


ipinfo_list = xici()
for ipinfo in ipinfo_list:
	redis_util.push_to_queue(ipinfo)
