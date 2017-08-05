#!/usr/bin/env python
# encoding: utf-8

import serial
import random
from sys import *
import pexpect
from pexpect import *
import fdpexpect
import time
import os
from state_switch_lib import *

test_count=1
def normal_case_test():
    for index in range(test_count):
        PRINT("normal case test start\n")
        sl_hb.mag_test_normal_case[random.randint(0,normal_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0)
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("normal case test over\n")

def alarm_case_test():
    for index in range(test_count):
        PRINT("alarm case test start\n")
        sl_hb.test_alarm_case[random.randint(0,alarm_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0)
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("alarm case test over\n")

def disengage_case_test():
    for index in range(test_count):
        PRINT("disengage case test start\n")
        sl_hb.test_disengage_case[random.randint(0,disengage_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0);
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("disengage case test over\n")

ss=state_switch()
sl_hb=ss.hb
sl_hb.hubconsole_init("51111111")

normal_count=sl_hb.mag_test_normal_count
alarm_count=sl_hb.test_alarm_count
disengage_count=sl_hb.test_disengage_count
int_count=sl_hb.test_interrupt_count

PRINT("test full start\n")
for index in range(1):
    ss.mag_enter_normal()
    time.sleep(3)
    normal_case_test()
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ret=ss.mag_normal_to_alarm_ack(sequence)
    if ret:
        PRINT("ERROR:sequence error1\n")
    time.sleep(3)
    ss.mag_crazy_test()
    time.sleep(3)
    ss.mag_normal_to_alarm_noack()
    time.sleep(3)
    alarm_case_test()
    time.sleep(3)
    ss.mag_enter_disengage()
    time.sleep(3)
    disengage_case_test()
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ss.mag_enter_normal()
    time.sleep(3)
    ret=ss.mag_normal_to_alarm_ack(sequence)
    if ret:
        PRINT("ERROR:sequence error2\n")
    time.sleep(3)
    ss.mag_enter_normal()
    PRINT("test full OK\n")







