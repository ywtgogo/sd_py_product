#!/usr/bin/env python
# encoding: utf-8

import serial
import random
from sys import *
import pexpect
from pexpect import *
import fdpexpect
import time
from state_switch_lib import *

ss=state_switch()
sl_hb=ss.hb

print "start disengage test\n"
ss.enter_disengage()
sl_hb.hub_do_ds()

disengage_count=sl_hb.test_disengage_count
int_count=sl_hb.test_interrupt_count
for index in range(10):
    ret=ss.trigger_alarm()
    if ret:
        print "alarm in disengage\n"
        exit(1)
    sl_hb.test_disengage_case[random.randint(0,disengage_count-1)]()
    time.sleep(0.2+random.randint(0,300)/1000.0);
    sl_hb.test_interrupt_case[random.randint(0,1)]()
    time.sleep(2.5+random.randint(0,500)/1000.0);
    print "test >>>\n"

ret=sl_hb.hub_do_is_alarm()
if ret:
    print "ERROR:should no alarm\n"

sl_hb.hub_do_de()


