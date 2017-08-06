# encoding-utf8

import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
ippool_queue = 'task:theippool:queue'

def push_ip_to_pool(ip, port):
    ipstring = '%s:%s' % (ip, port)
    r.lpush(ippool_queue, ipstring)



def get_ip_from_pool():
    ipstring = r.blpop(ippool_queue, 0)[1]
    return ipstring
