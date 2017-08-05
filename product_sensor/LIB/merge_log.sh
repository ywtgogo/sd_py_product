#!/bin/bash
date_start=$1
echo $date_start
date_end=$2
echo $date_end

i=0;

mkdir $date_end
date_temp=$date_end
echo "date_end=${date_end}"
echo "date_temp=${date_temp}"

while [ "${date_temp}" != "${date_start}" ];
do
    echo "enter while"
    logfile=/home/sandlacus/test_station/sniffer_log/${date_temp}".log"
    echo $logfile
    if [ -f "$logfile" ]
    then
        cp $logfile $date_end 
    fi
    date_temp=`date -d -$i"day" +%Y%m%d`
    echo $date_temp
    i=`expr $i + 1`
    echo "i=$i"
done


if [ "${date_temp}" = "${date_start}" ]
then
    logfile=/home/sandlacus/test_station/sniffer_log/${date_temp}".log"
    if [ -f "$logfile" ]
    then
        cp $logfile $date_end 
    fi
fi


`cat ${date_end}/* > ${date_end}/sniff.log`
