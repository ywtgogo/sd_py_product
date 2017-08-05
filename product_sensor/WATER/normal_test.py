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
sl_hb.hubconsole_init("31111111")


PRINT("start normal test\n")
ss.water_enter_normal()

sl_hb.hub_do_query_and_check(int(1))

normal_count=sl_hb.water_test_normal_count
int_count=sl_hb.test_interrupt_count
for index in range(10):
    sl_hb.water_test_normal_case[random.randint(0,normal_count-1)]()
    time.sleep(0.2+random.randint(0,300)/1000.0)
    sl_hb.test_interrupt_case[random.randint(0,1)]()
    time.sleep(2.5+random.randint(0,500)/1000.0)
    PRINT("test %d success\n" %index)

sl_hb.hub_do_query_and_check(int(1))



