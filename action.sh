#!/bin/sh
python /home/luoyingtian/baiduwords/proxyip.py  http://www.xicidaili.com/nn/  gen_ip_list_csvfile > ip_list.csv
python -u /home/luoyingtian/baiduwords/main.py > action_res_`date "+%y-%m-%d_%H_%M_%S"`.log


