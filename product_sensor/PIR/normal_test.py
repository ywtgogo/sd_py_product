#!/usr/bin/env python
# encoding: utf-8

import serial
import random
import sys
import pexpect
from pexpect import *
import fdpexpect
import time
from state_switch_lib import *

ss=state_switch()
sl_hb=ss.hb

print "start normal test\n"
ss.enter_normal()
sl_hb.hub_do_ns()

normal_count=sl_hb.test_normal_count
int_count=sl_hb.test_interrupt_count
for index in range(10):
    sl_hb.test_normal_case[random.randint(0,normal_count-1)]()
    time.sleep(0.2+random.randint(0,300)/1000.0)
    sl_hb.test_interrupt_case[random.randint(0,1)]()
    time.sleep(2.5+random.randint(0,500)/1000.0)
    print "test %d success\n" %index

ret=sl_hb.hub_do_is_alarm()
if ret:
    print "ERROR:alarm in normal\n"

sl_hb.hub_do_ne()



