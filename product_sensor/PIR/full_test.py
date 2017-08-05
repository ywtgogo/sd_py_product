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
        print "normal case test start\n"
        sl_hb.test_normal_case[random.randint(0,normal_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0)
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        print "normal case test over\n"

def alarm_case_test():
    for index in range(test_count):
        print "alarm case test start\n"
        sl_hb.test_alarm_case[random.randint(0,alarm_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0)
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        print "alarm case test over\n"

def disengage_case_test():
    for index in range(test_count):
        print "disengage case test start\n"
        sl_hb.test_disengage_case[random.randint(0,disengage_count-1)]()
        time.sleep(0.2+random.randint(0,300)/1000.0);
        sl_hb.test_interrupt_case[random.randint(0,1)]()
        time.sleep(2.5+random.randint(0,500)/1000.0)
        print "disengage case test over\n"

ss=state_switch()
sl_hb=ss.hb

normal_count=sl_hb.test_normal_count
alarm_count=sl_hb.test_alarm_count
disengage_count=sl_hb.test_disengage_count
int_count=sl_hb.test_interrupt_count

print "test full start\n"
for index in range(1):
    ss.enter_normal()
    time.sleep(3)
    sl_hb.hub_do_ns()
    time.sleep(3)
    normal_case_test()
    sl_hb.hub_do_ne()
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ret=ss.normal_to_alarm_ack(sequence)
    if ret:
        print "ERROR:sequence error1\n"
    sl_hb.hub_do_query()
    time.sleep(3)
    sl_hb.hbcsp.sendline("info")
    i=sl_hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
    if i==1:
        alarm_status=(re.findall(r'\d',self.hb.hbcsp.after)).pop()
        print alarm_status
        print "ack missed\n"
        exit(1)
    time1=time.time()

    sl_hb.hub_do_disable_alarmack()
    while True:
        count = 0;
        ss.trigger_alarm()
        time.sleep(3)
        sl_hb.hub_do_query()
        time.sleep(3)
        sl_hb.hbcsp.sendline("")
        time.sleep(3)
        sl_hb.hbcsp.sendline("info")
        i=sl_hb.hbcsp.expect(["alarm_status=1", pexpect.TIMEOUT], timeout=3)
        if i==0:
            print "silent time ending\n"
            break;
            if time2-time1 < 60*9:
                print "ERROR:alarm int sient time\n"
                exit(1)
            else:
                break;
        else:
            print "sleep 30s\n"
            time.sleep(30)
        count=count+1
        if count > 23:
            print "not alarm after silent\n"
            break;
    count = 0
    sl_hb.hub_do_as()
    time.sleep(3)
    alarm_case_test()
    sl_hb.hub_do_ae()
    time.sleep(3)
    ss.enter_disengage()
    time.sleep(3)
    sl_hb.hub_do_ds()
    time.sleep(3)
    disengage_case_test()
    sl_hb.hub_do_de()
    time.sleep(3)
    sl_hb.hub_do_resync()
    time.sleep(3)
    sequence=sl_hb.hub_do_get_sequence()
    time.sleep(3)
    ss.enter_normal()
    time.sleep(3)
    ss.normal_to_alarm_ack(sequence)
    if ret:
        print "ERROR:sequence error2\n"
    time.sleep(3)
    ss.enter_normal()
    print "test full OK\n"







