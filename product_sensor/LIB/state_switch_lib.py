#!/usr/bin/env python
# encoding: utf-8

import re
import serial
import random
from sys import *
import pexpect
from pexpect import *
import fdpexpect
import time
from hubconsole_lib import *

class state_switch:
    """
    class sensor state switch
    """
    def __init__(self):
        self.hb=test_hubconsole()
        self.tc=None
        self.tcsp=None
        self.tc = serial.Serial("/dev/trigger_console",19200)
        self.tcsp = fdpexpect.fdspawn(self.tc)

    def normal_to_alarm_noack(self):
        self.hb.hub_do_disable_alarmack()
        time.sleep(3)
        self.trigger_alarm()
        time.sleep(10)
        self.hb.hbcsp.sendline("q")
        i=self.hb.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout in n_to_a_n\n")

        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=10)
        if i==0:
            alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
            print alarm_status
            if alarm_status == 0:
                PRINT("ERROR:sensor not in alarm 2\n")

        else:
            PRINT("ERROR:timeout*********\n")

    def mag_normal_to_alarm_noack(self):
        PRINT("mag_normal_to_alarm_noack 1\n")
        self.hb.hub_do_disable_alarmack()
        time.sleep(3)
        self.mag_trigger_and_release_alarm()
        time.sleep(3)
        self.hb.hub_do_query_and_check(int(1))

    def normal_to_alarm_ack(self,arg):
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.trigger_alarm()
        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==0:
            alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
            print alarm_status
            if alarm_status == 0:
                PRINT("ERROR:sensor not in noraml\n")

        else:
            PRINT("ERROR:timeout*********\n")

        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["sequence=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:info timeout\n")
        sequence=int((re.findall(r'sequence=(.*)\n',self.hb.hbcsp.after)).pop())
        if sequence == arg+1:
            return 0
        else:
            return 1
    def water_normal_to_alarm_noack_check(self,arg):
        PRINT("water_normal_to_alarm_noack 1\n")
        self.hb.hub_do_disable_alarmack()
        time.sleep(3)
        self.water_trigger_alarm()
        time.sleep(70)
        self.hb.hub_do_query_and_check(int(0))
        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["sequence=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:water n_to_a_noa timeout\n")
        sequence=int((re.findall(r'sequence=(.*)\n',self.hb.hbcsp.after)).pop())
        if sequence == arg+1:
            return 0
        else:
            return 1
    def water_normal_to_alarm_ack_check(self,arg):
        PRINT("water_normal_to_alarm_ack 1\n")
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.water_trigger_alarm()
        time.sleep(70)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["sequence=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:water n_to_a_noa timeout\n")
        sequence=int((re.findall(r'sequence=(.*)\n',self.hb.hbcsp.after)).pop())
        if sequence == arg+1:
            return 0
        else:
            return 1

    def to_alarm_noack(self):
        self.enter_normal()
        self.hb.hub_do_disable_alarmack()
        time.sleep(3)
        self.trigger_alarm_check()
        time.sleep(3)
        self.hb.hbcsp.sendline("q")
        i=self.hb.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout in to_a_n\n")

        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=10)
        if i==1:
            PRINT("ERROR:sensor not in alarm 2\n")
            alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
            print alarm_status

    def normal_to_alarm_ack(self,arg):
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.trigger_alarm()
        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==0:
            alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
            print alarm_status
            if alarm_status == 0:
                PRINT("ERROR:sensor not in noraml\n")

        else:
            PRINT("ERROR:timeout*********\n")

        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["sequence=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:info timeout\n")
        sequence=int((re.findall(r'sequence=(.*)\n',self.hb.hbcsp.after)).pop())
        if sequence == arg+1:
            return 0
        else:
            return 1
    def mag_normal_to_alarm_ack(self,arg):
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.mag_trigger_and_release_alarm()
        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==0:
            alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
            print alarm_status
            if alarm_status == 0:
                PRINT("ERROR:sensor not in noraml\n")

        else:
            PRINT("ERROR:timeout*********\n")

        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["sequence=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:info timeout\n")
        sequence=int((re.findall(r'sequence=(.*)\n',self.hb.hbcsp.after)).pop())
        PRINT("sequence=%d,arg=%d\n" %(sequence,arg))
        if sequence == arg+1:
            return 0
        else:
            return 1

    def to_alarm_ack(self):
        self.enter_normal()
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.trigger_alarm()
        time.sleep(10)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=1", pexpect.TIMEOUT], timeout=10)
        if i==1:
            PRINT("ERROR:sensor not in alarm n_to_a 2,%s\n" %self.hb.hbcsp.after)

    def alarm_noack_to_normal(self):
        self.hb.hub_do_alarmack()
        time.sleep(3)
        self.hb.hbcsp.sendline("q")
        i=self.hb.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout in a_n_to_n\n")

        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=0", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:sensor not in noraml\n")

    def enter_disengage(self):
        PRINT("enter disengage\n")
        self.enter_normal()
        self.hb.hub_do_disengage()
    def mag_enter_disengage(self):
        PRINT("enter disengage\n")
        self.mag_enter_normal()
        self.hb.hub_do_disengage()

    def enter_engage(self):
        PRINT("enter engage\n")
        self.enter_normal()
        self.hb.hub_do_engage()
    def mag_enter_engage(self):
        PRINT("enter engage\n")
        self.mag_enter_normal()
        self.hb.hub_do_engage()
    def water_enter_alarm_ack(self):
        PRINT("enter alarm ack\n")
        self.water_enter_normal()
        self.water_trigger_alarm()
        time.sleep(3)
    def water_enter_ack(self):
        PRINT("enter water ack\n")
        self.water_enter_alarm_ack()
        self.water_release_alarm()
        time.sleep(70)

    def enter_normal(self):
        PRINT("enter normal................\n")
        time.sleep(3)
        self.hb.hbcsp.sendline("")
        time.sleep(3)
        self.hb.hbcsp.sendline("q")
        i=self.hb.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout in enter normal 1\n")

        time.sleep(3)
        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:sensor not in noraml\n")
            print self.hb.hbcsp.after

        print self.hb.hbcsp.after
        alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
        print alarm_status
        if alarm_status == 1:
            self.hb.hub_do_alarmack()
            time.sleep(3)
            self.hb.hbcsp.sendline("q")
            i=self.hb.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
            if i==1:
                PRINT("ERROR:hubconsole query timeout in enter normal 2\n")

            time.sleep(3)
            self.hb.hbcsp.sendline("info")
            i=self.hb.hbcsp.expect(["alarm_status=0", pexpect.TIMEOUT], timeout=3)
            if i==1:
                PRINT("ERROR:could not return to noraml\n")

        self.hb.hub_do_disengage()
        time.sleep(3)
        self.hb.hub_do_engage()
        time.sleep(3)
        PRINT("now is in normal state\n")
    def mag_enter_normal(self):
        self.hb.hub_do_alarmack()
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.mag_release_alarm()
        time.sleep(3)
        self.hb.hub_do_disengage()
        time.sleep(3)
        self.hb.hub_do_engage()
        time.sleep(3)
        PRINT("now is in normal state\n")
    def water_enter_normal(self):
        self.water_release_alarm()
        time.sleep(70)
        self.hb.hub_do_alarmack()
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.hb.hub_do_rearm()
        time.sleep(3)
        PRINT("now is in normal state\n")

    def trigger_alarm(self):
        PRINT("trigger alarm\n")
        self.tcsp.sendline("talarm")
        i=self.tcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:trigger alarm fail\n")

        self.hb.hbcsp.sendline("info")
        i=self.hb.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:sensor not in noraml\n")
            print self.hb.hbcsp.after

        alarm_status=int((re.findall(r'\d',self.hb.hbcsp.after)).pop())
        print alarm_status
        if alarm_status == 1:
            return 1
        else:
            return 0
    def trigger_alarm_check(self):
        PRINT("enter trigger alarm and check\n")
        self.hb.hbcsp.sendline("cac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:cac fail\n")

        PRINT("trigger alarm\n")
        self.tcsp.sendline("talarm")
        i=self.hb.hbcsp.expect(["aok", pexpect.TIMEOUT], timeout=10)
        if i==1:
            PRINT("ERROR:trigger alarm check fail1\n")

        time1=time.time()
        i=self.hb.hbcsp.expect(["aok", pexpect.TIMEOUT], timeout=100)
        if i==1:
            PRINT("ERROR:trigger alarm check fail2\n")

        time2=time.time()

        self.hb.hbcsp.sendline("ccac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:ccac fail\n")

        time_interval=time2-time1
        if time_interval < 50 and time_interval > 70:
            PRINT("ERROR:alarm interval in not 60s\n")

    def mag_trigger_alarm(self):
        PRINT("trigger mag alarm\n")
        self.tcsp.sendline("talarm")


    def mag_release_alarm(self):
        PRINT("release mag alarm\n")
        self.tcsp.sendline("ralarm")
    def mag_trigger_and_release_alarm(self):
        PRINT("trigger and release alarm\n")
        self.tcsp.sendline("tralarm")
    def water_trigger_alarm(self):
        PRINT("trigger water alarm\n")
        self.tcsp.sendline("ralarm")
    def water_release_alarm(self):
        PRINT("release water alarm\n")
        self.tcsp.sendline("talarm")

    def check_four_alarm_interval(self):
        i=self.hb.hbcsp.expect(["aok", pexpect.TIMEOUT], timeout=70)
        if i==1:
            PRINT("ERROR:check four alarm fail\n")

        time1=time.time()
        i=self.hb.hbcsp.expect(["aok", pexpect.TIMEOUT], timeout=100)
        if i==1:
            PRINT("ERROR:check four alarm fail2\n")

        time2=time.time()

        self.hb.hbcsp.sendline("ccac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:ccac fail\n")

        time_interval=time2-time1
        if time_interval < 50 and time_interval > 70:
            PRINT("ERROR:alarm interval in not 60s\n")


    def mag_to_alarm_precheck(self):
        PRINT("mag to alarm precheck start")
        self.mag_enter_normal()
        self.hb.hub_do_disable_alarmack()
        time.sleep(3)
        self.hb.hbcsp.sendline("cac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:cac fail\n")

        PRINT("trigger alarm\n")
        self.mag_trigger_and_release_alarm()
        PRINT("start check_four alarm interval")
        self.check_four_alarm_interval()
        PRINT("end check_four alarm interval")
        time.sleep(3)
        self.hb.hub_do_alarmack()
        self.hb.hub_do_query_and_check(int(1))
        time.sleep(3)
        self.hb.hub_do_enable_alarmack()
        time.sleep(3)
        self.hb.hbcsp.sendline("cac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:cac fail\n")

        PRINT("trigger alarm\n")
        self.mag_trigger_alarm()
        time.sleep(3)
        self.hb.hub_do_query_and_check(int(0))

    def water_to_alarm_precheck(self):
        PRINT("water to alarm precheck start")
        self.water_enter_normal()
        self.hb.hub_do_disable_alarmack()
        time.sleep(3)
        self.hb.hbcsp.sendline("cac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:cac fail\n")

        PRINT("trigger alarm\n")
        self.water_trigger_alarm()
        PRINT("start check_four alarm interval")
        self.check_four_alarm_interval()
        PRINT("end check_four alarm interval")

    def mag_crazy_test(self):
        self.hb.hbcsp.sendline("gb")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:garbage set fail\n")

        time.sleep(3)
        self.hb.hbcsp.sendline("mcac")
        i=self.hb.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:mcac fail\n")

        for index in range(20):
            self.mag_trigger_and_release_alarm()
            i=self.hb.hbcsp.expect(["md", pexpect.TIMEOUT], timeout=3)
            if i==1:
                PRINT("ERROR:mag crazy test fail\n")
        self.hb.hbcsp.sendline("mccac")






