#!/usr/bin/env python
# encoding: utf-8

import serial
import random
from sys import *
import pexpect
from pexpect import *
import fdpexpect
import time
import re
import datetime

def PRINT(arg):
    print "%s" %datetime.datetime.now(),arg

class test_hubconsole:
    """
    class test hubconsole
    """

    def __init__(self):
        self.hbc=None
        self.hbcsp=None
        self.pir_test_normal_count=5
        self.mag_test_normal_count=3
        self.water_test_normal_count=4
        self.test_alarm_count=4
        self.water_test_alarm_count=3
        self.test_disengage_count=2
        self.test_interrupt_count=2
        self.water_alarm_ack_count=2
        self.water_ack_count=2

        self.pir_test_normal_case=[]
        self.mag_test_normal_case=[]
        self.water_test_alarm_case=[]
        self.water_test_alarmack_case=[]
        self.water_test_ack_case=[]
        self.test_alarm_case=[]
        self.test_alarm_case=[]
        self.test_disengage_case=[]
        self.test_interrupt_case=[]
        self.fd=open("console.log",'w')
        self.hbc=serial.Serial("/dev/hub_console",19200)
        self.hbcsp = fdpexpect.fdspawn(self.hbc)
        self.hbcsp.logfile=self.fd
        self.initTestNormalCase()
        self.initTestAlarmCase()
        self.initTestAlarmAckCase()
        self.initTestDisengageCase()
        self.initTestInterruptCase()
        self.initTestAckCase()

    def initTestNormalCase(self):
        self.pir_test_normal_case=[
                self.hub_do_query,self.hub_do_engage,
                self.hub_do_resync,
                self.hub_do_change_low_sensitivity,
                self.hub_do_change_high_sensitivity]
        self.mag_test_normal_case=[
                self.hub_do_query,self.hub_do_engage,
                self.hub_do_resync]
        self.water_test_normal_case=[
                self.hub_do_query,self.hub_do_query_info,
                self.hub_do_resync,self.hub_do_rearm]
    def initTestAlarmCase(self):
        self.test_alarm_case=[
                self.hub_do_query,self.hub_do_engage,
                self.hub_do_disengage,self.hub_do_resync]
        self.water_test_alarm_case=[
                self.hub_do_query,self.hub_do_rearm_noack,
                self.hub_do_resync]
    def initTestAlarmAckCase(self):
        self.water_test_alarmack_case=[
                self.hub_do_query,self.hub_do_rearm_noack,
                self.hub_do_resync]
    def initTestAckCase(self):
        self.water_test_ack_case=[
                self.hub_do_query,
                self.hub_do_resync]
    def initTestDisengageCase(self):
        self.test_disengage_case=[
                self.hub_do_query,self.hub_do_disengage]
    def initTestInterruptCase(self):
        self.test_interrupt_case=[
                self.hub_do_query_other,self.hub_do_random_preamble]

    def hub_do_query(self):
        time.sleep(3)
        self.hbcsp.sendline("")
        time.sleep(3)
        self.hbcsp.sendline("q")
        i=self.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout1\n")

        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout2\n")
    def hub_do_query_info(self):
        time.sleep(3)
        self.hbcsp.sendline("")
        time.sleep(3)
        self.hbcsp.sendline("qin")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query timeout2\n")

    def hub_do_rearm(self):
        self.hbcsp.sendline("rearm")
        i=self.hbcsp.expect(["raa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole rearm timeout1\n")
    def hub_do_rearm_noack(self):
        self.hbcsp.sendline("rearm")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole rearm timeout1\n")

    def hub_do_query_and_check(self,arg):
        time.sleep(3)
        self.hbcsp.sendline("")
        time.sleep(3)
        self.hbcsp.sendline("q")
        i=self.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole querycheck timeout1\n")

        time.sleep(3)
        self.hbcsp.sendline("info")
        i=self.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=10)
        if i==1:
            PRINT("ERROR:sensor not in alarm 2\n")
            alarm_status=int((re.findall(r'\d',self.hbcsp.after)).pop())
            print alarm_status

        alarm_status=int((re.findall(r'\d',self.hbcsp.after)).pop())
        if alarm_status == arg:
            PRINT("ERROR:query check error\n")


    def hub_do_engage(self):
        time.sleep(3)
        self.hbcsp.sendline("")
        time.sleep(3)
        self.hbcsp.sendline("eg")
        i=self.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole engage timeout1\n")

        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole engage timeout2\n")

    def hub_do_disengage(self):
        time.sleep(3)
        self.hbcsp.sendline("")
        time.sleep(3)
        self.hbcsp.sendline("dg")
        i=self.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole disengage timeout1\n")

        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole disengage timeout2\n")

    def hub_do_random_preamble(self):
        self.hbcsp.sendline("rp")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole random preamble timeout\n")

    def hub_do_resync(self):
        self.hbcsp.sendline("rsc")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole resync timeout\n")

    def hub_do_change_low_sensitivity(self):
        self.hbcsp.sendline("ls")
        i=self.hbcsp.expect(["lsa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole low_sensitivity timeout1\n")

        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole low_sensitivity timeout2\n")

    def hub_do_change_high_sensitivity(self):
        self.hbcsp.sendline("hs")
        i=self.hbcsp.expect(["hsa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole high_sensitivity timeout1\n")

        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole high_sensitivity timeout2\n")

    def hub_do_query_other(self):
        self.hbcsp.sendline("qo")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole query other timeout\n")

    def hub_do_enable_alarmack(self):
        self.hbcsp.sendline("eaa")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole enable alarmack timeout\n")

    def hub_do_disable_alarmack(self):
        self.hbcsp.sendline("daa")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole disable alarmack timeout\n")

    def hub_do_alarmack(self):
        self.hbcsp.sendline("saa")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole send alarmack timeout\n")

    def hub_do_garbage(self):
        self.hbcsp.sendline("gb")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole garbage timeout\n")

    def hub_do_de(self):
        self.hbcsp.sendline("de")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole de timeout\n")

    def hub_do_get_sequence(self):
        self.hbcsp.sendline("gs")
        i=self.hbcsp.expect(["sequence=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole de timeout\n")

        sequence=int((re.findall(r'sequence=(.*)\n',self.hbcsp.after)).pop())
        return sequence


    def hub_do_is_alarm(self):
        self.hbcsp.sendline("q")
        i=self.hbcsp.expect(["qa", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole is alarm timeout\n")
            return -1
        time.sleep(3)
        self.hbcsp.sendline("info")
        i=self.hbcsp.expect(["alarm_status=.*\n", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("ERROR:hubconsole is alarm timeout\n")
            return -1
        alarm_status=int((re.findall(r'\d',self.hbcsp.after)).pop())
        if alarm_status == 1:
            return 1
        else:
            return 0



    def hubconsole_init(self,arg):
        self.hbcsp.sendline("info")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=4)
        if i==1:
            PRINT("hubconsole init fail1\n")


        self.hbcsp.sendline("reset")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=4)
        if i==1:
            PRINT("hubconsole init fail1\n")

        time.sleep(3)
        self.hbcsp.sendline("reset")
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=4)
        if i==1:
            PRINT("hubconsole init fail1\n")

        ID_cmd="deploy %s"%arg
        print ID_cmd
        self.hbcsp.sendline(ID_cmd)
        i=self.hbcsp.expect(["#", pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("hubconsole init fail2\n")

        self.hbcsp.sendline("info")
        i=self.hbcsp.expect([arg, pexpect.TIMEOUT], timeout=3)
        if i==1:
            PRINT("deploy %s fail3\n"% arg)


        PRINT("hub console init successfull\n")

