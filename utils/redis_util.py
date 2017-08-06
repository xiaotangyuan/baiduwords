# encoding=utf8


import sys
from optparse import OptionParser
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
queue_name = 'ipinfo:task:queue'
queue_length = 'ipinfo:task:queuelength'


def push_to_queue(ipinfo):
	r.lpush(queue_name, ipinfo)
	if not r.get(queue_length):
		r.set(queue_length, 1)
	else:
		r.incr(queue_length, amount=1)
	print '[redis info] pushed a ipinfo: %s' % ipinfo


def get_ipinfo_from_queue():
	_, ipinfo = r.brpop(queue_name)
	r.decr(queue_length, amount=1)
	return ipinfo


def clean_queue():
	r.delete(queue_name)


def check_ipinfo(ipinfo):
	if ':' not in ipinfo:
		return False
	ip, port = ipinfo.split(':')
	if len(ip.split('.')) != 4:
		return False
	return True


def get_ipinfo_queue_length():
	num = r.get(queue_length)
	if num is None:
		num = 0
	return int(num)


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i', '--ipinfo', dest='ipinfo', help=u'包含ip和端口  如192.168.1.1:20')
	parser.add_option('-g', '--getaipinfo', action='store_true', default=False, dest='getipinfo', help=u'获取一个ip信息  如192.168.1.1:20')
	parser.add_option('-c', '--cleanqueue', action='store_true', default=False, dest='cleanqueue', help=u'清空队列所有ip')
	parser.add_option('-n', '--ipinfonum', action='store_true', default=False, dest='ipinfonum', help=u'ip数量')

	options, args=parser.parse_args()
	ipinfo = options.ipinfo
	getipinfo = options.getipinfo
	cleanqueue = options.cleanqueue
	ipinfonum = options.ipinfonum

	if ipinfonum is True:
		print 'ip num:', get_ipinfo_queue_length()
		sys.exit()

	if cleanqueue is True:
		clean_queue()
		print 'cleaned all ip from queue!'
		sys.exit()

	# print ipinfo
	if getipinfo is True:
		ipinfo = get_ipinfo_from_queue()
		if ipinfo:
			print '[redis info] get success: ', ipinfo
		else:
			print '[redis info] no ipinfo in queue: %s' % ipinfo
	elif ipinfo is not None:
		if check_ipinfo(ipinfo):
			push_to_queue(ipinfo)
		else:
			print '[redis info] ip format error: %s' % ipinfo
