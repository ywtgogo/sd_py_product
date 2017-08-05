#!/bin/bash
date1=`date +%s`
log_name=`date +%Y%m%d`
echo $log_name.log
echo $date1
echo "normal test start\n"
sudo python normal_test.py
echo "alarm test start\n"
python alarm_test.py
echo "alarm ack test start\n"
sudo python alarm_ack_test.py
echo "ack test start\n"
sudo python ack_test.py
echo "full test start\n"
sudo python full_test.py
date2=`date +%s`
echo $date2
date_end=`date +%Y%m%d`
echo $date2
sh ../LIB/merge_log.sh $date_start $date_end
#python ../LIB/cut_sniff.py /home/sandlacus/test_station/sniffer_log/$log_name.log sniff.log $date1 $date2
python ../LIB/cut_sniff.py ./$date_end/sniff.log sniff.log $date1 $date2



