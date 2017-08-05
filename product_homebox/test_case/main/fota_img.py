#_*_ coding:utf-8 _*_

from test_lib import *
import os,time,datetime


honsole = SL_console("homebox")
honsole.init()
honsole.log("\t\tHomeBox Img Fota Test Start Test:")

honsole.console_spawn.sendline("hb")
time.sleep(5)
honsole.corres(cmd = "fota",pattern = ["Request is successful"])
ret = honsole.console_spawn.expect(["request img", pexpect.TIMEOUT],timeout= 2)
if(ret == 0):
    print "It's runing fota img updata"
    pass
else:
    print "Updata Fail"
    pass
#ret = honsole.console_spawn.expect(["img block NO", pexpect.TIMEOUT], timeout=2)
down_fin = honsole.console_spawn.expect(["bootloader", pexpect.TIMEOUT], timeout=2)
while down_fin:
    num = (re.findall(r'\d',honsole.console_spawn.aftera)).pop()
    print "Downloading No:%s" %num
    down_fin = honsole.console_spawn.expect(["bootloader", pexpect.TIMEOUT], timeout=2)
    pass

print "Restarting!!!!!!!!!!!!!!"
honsole.log("\t\tDownLoad Success, Restarting!!!")


