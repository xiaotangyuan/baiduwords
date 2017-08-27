import time,sched
import datetime
import commands
  

while True:
    order = 'bash action.sh'
    dtnow = datetime.datetime.now()
    hour = dtnow.hour
    if hour > 0 and hour < 8:
        time.sleep(60*60)
    else:
        commands.getstatusoutput(order)
        time.sleep(10*60)
