import time
import datetime
import commands
import os
from utils import redis_util

pythonpath = os.environ['PYTHONPATH']

while True:
    # time.sleep(10*60)
    dtnow = datetime.datetime.now()
    hour = dtnow.hour
    if hour > 0 and hour < 8:
        time.sleep(60*60)

    remain_ipinfo = redis_util.get_ipinfo_queue_length()
    print '[action.py] ipinfo remain: %s' % remain_ipinfo, type(remain_ipinfo)
    if remain_ipinfo < 10:
        print '[action.py] ipinfo remain: %s, will update ipinfo data!  %s' % (remain_ipinfo, datetime.datetime.now())
        pyfilepath = os.path.join(pythonpath, 'proxyip.py')
        order = 'python %s -s' % pyfilepath
        commands.getstatusoutput(order)
        pyfilepath = os.path.join(pythonpath, 'proxyip.py')
        order = 'python %s -r' % pyfilepath
        commands.getstatusoutput(order)

        time.sleep(10*60)
