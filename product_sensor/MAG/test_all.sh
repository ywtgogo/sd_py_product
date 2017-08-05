#!/bin/bash
date1=`date +%s`
date_start=`date +%Y%m%d`
echo $date1
echo "normal test start\n"
sudo python normal_test.py
echo "alarm test start\n"
python alarm_test.py
echo "disengage test start\n"
sudo python disengage_test.py
echo "full test start\n"
sudo python full_test.py
date2=`date +%s`
date_end=`date +%Y%m%d`
echo $date2
sh ../LIB/merge_log.sh $date_start $date_end
python ../LIB/cut_sniff.py ./$date_end/sniff.log sniff.log $date1 $date2



