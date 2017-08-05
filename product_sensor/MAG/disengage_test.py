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
sl_hb.hubconsole_init("51111111")

PRINT("start disengage test\n")
ss.mag_enter_disengage()

disengage_count=sl_hb.test_disengage_count
int_count=sl_hb.test_interrupt_count
for index in range(1):
    ss.mag_trigger_and_release_alarm()
    time.sleep(3)
    sl_hb.hub_do_query_and_check(int(1))
    time.sleep(3)
    sl_hb.test_disengage_case[random.randint(0,disengage_count-1)]()
    time.sleep(0.2+random.randint(0,300)/1000.0);
    sl_hb.test_interrupt_case[random.randint(0,1)]()
    time.sleep(2.5+random.randint(0,500)/1000.0);
    PRINT("test >>>\n")

sl_hb.hub_do_query_and_check(int(1))

