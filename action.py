import time,sched
import datetime
import commands
  

while True:
    order = 'bash action.sh'
    commands.getstatusoutput(order)
    time.sleep(60*60)
