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
        sl_hb.water_test_normal_case[random.randint(0,normal_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0)
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("normal case test over\n")

def alarm_case_test():
    for index in range(test_count):
        PRINT("alarm case test start\n")
        sl_hb.water_test_alarm_case[random.randint(0,alarm_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0)
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("alarm case test over\n")

def alarm_ack_case_test():
    for index in range(test_count):
        PRINT("alarm ack case test start\n")
        sl_hb.water_test_alarmack_case[random.randint(0,alarm_ack_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0);
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("alarm ack case test over\n")

def ack_case_test():
    for index in range(test_count):
        PRINT("ack case test start\n")
        sl_hb.water_test_ack_case[random.randint(0,ack_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0);
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        PRINT("ack case test over\n")

ss=state_switch()
sl_hb=ss.hb
sl_hb.hubconsole_init("31111111")

normal_count=sl_hb.water_test_normal_count
alarm_count=sl_hb.water_test_alarm_count
alarm_ack_count=sl_hb.water_alarm_ack_count
ack_count=sl_hb.water_ack_count
int_count=sl_hb.test_interrupt_count

PRINT("test full start\n")
for index in range(1):
    ss.water_enter_normal()
    time.sleep(3)
    normal_case_test()
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ret=ss.water_normal_to_alarm_noack_check(sequence)
    if ret:
        PRINT("ERROR:sequence error1\n")
    time.sleep(3)
    alarm_case_test()
    time.sleep(3)
    ss.water_enter_alarm_ack()
    time.sleep(3)
    alarm_ack_case_test()
    time.sleep(3)
    ss.water_enter_ack()
    time.sleep(3)
    ack_case_test()
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ss.water_enter_normal()
    time.sleep(3)
    ret=ss.water_normal_to_alarm_ack_check(sequence)
    if ret:
        PRINT("ERROR:sequence error2\n")
    time.sleep(3)
    sl_hb.hbcsp.sendline("mcac")
    i=sl_hb.hbcsp.expect(["md", pexpect.TIMEOUT], timeout=70)
    if i==0:
        PRINT("ERROR:should not alarm1\n")
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ss.water_release_alarm()
    time.sleep(3)
    ss.water_trigger_alarm()
    i=sl_hb.hbcsp.expect(["md", pexpect.TIMEOUT], timeout=10)
    if i==0:
        PRINT("ERROR:should not alarm2\n")
    ss.water_release_alarm()
    time.sleep(3)
    ss.water_enter_normal()
    time.sleep(3)
    sl_hb.hbcsp.sendline("mccac")
    ret=ss.water_normal_to_alarm_ack_check(sequence)
    if ret:
        PRINT("ERROR:sequence error3\n")

    PRINT("test full OK\n")







