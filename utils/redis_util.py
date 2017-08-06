# encoding=utf8


from optparse import OptionParser
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
queue_name = 'ipinfo:task:queue'

def push_to_queue(ipinfo):
	r.lpush(queue_name, ipinfo)

def get_ipinfo_from_queue():
	r.brpop(queue_name)

def check_ipinfo(ipinfo):
	if ':' not in ipinfo:
		return False
	ip, port = ipinfo.split(':')
	if len(ip.split('.')) != 4:
		return False
	return True


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i', '--ipinfo', dest='ipinfo', help=u'包含ip和端口  如192.168.1.1:20')
	parser.add_option('-g', '--getaipinfo', action='store_true', default=False, dest='getipinfo', help=u'获取一个ip信息  如192.168.1.1:20')
	options, args=parser.parse_args()
	ipinfo = options.ipinfo
	getipinfo = options.getipinfo
	# print ipinfo
	if getipinfo is True:
		ipinfo = get_ipinfo_from_queue()
		if ipinfo:
			print '[redis info] get success: %s' % ipinfo
		else:
			print '[redis info] no ipinfo in queue: %s' % ipinfo
	if ipinfo is not None:
		if check_ipinfo(ipinfo):
			print '[redis info] will push a ipinfo: %s' % ipinfo
			push_to_queue(ipinfo)
			print '[redis info] push success: %s' % ipinfo
		else:
			print '[redis info] ip format error: %s' % ipinfo
