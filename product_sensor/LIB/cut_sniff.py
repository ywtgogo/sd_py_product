#!/usr/bin/env python
# encoding: utf-8

from sys import *
import time
import re

re_time=re.compile(r'(.*?)#')
#if argc < 5:
#    print "wrong argument\n"
#    exit(1)

from_sniff=argv[1]
to_sniff=argv[2]

time_start=argv[3]
time_end=argv[4]

fd_fromsniff=open(from_sniff,'r');
fd_tosniff=open(to_sniff,'w');

while True:
    line = fd_fromsniff.readline()
    if line.split():
        time_sniff=(re_time.findall(line)).pop()
        if time_sniff < time_start:
            continue
        elif time_sniff > time_end:
            break
        else:

            fd_tosniff.write(line)
    else:
        line = fd_fromsniff.readline()
        if line.split():
            time_sniff=(re_time.findall(line)).pop()
            if time_sniff < time_start:
                continue
            elif time_sniff > time_end:
                break
            else:
                fd_tosniff.write(line)
        else:
            break;




