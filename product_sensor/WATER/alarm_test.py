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
sl_hb.hubconsole_init("31111111")

PRINT("start alarm test\n")
ss.water_to_alarm_precheck()

alarm_count=sl_hb.water_test_alarm_count
int_count=sl_hb.test_interrupt_count
for index in range(10):
    sl_hb.water_test_alarm_case[random.randint(0,alarm_count-1)]()
    time.sleep(0.2+random.randint(0,300)/1000.0);
    sl_hb.test_interrupt_case[random.randint(0,1)]()
    time.sleep(2.5+random.randint(0,500)/1000.0);
    PRINT("test %d success\n" %index)
