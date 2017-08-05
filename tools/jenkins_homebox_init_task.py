import pexpect
import sys
import time
import threading
import random
import os
import SL_CONFIG

cfg = None
if len(sys.argv) == 2:
	cfg = SL_CONFIG.get_cfg(sys.argv[1])
elif len(sys.argv) == 1:
	cfg = SL_CONFIG.get_cfg("2g")
homebox = pexpect.spawn("/usr/bin/kermit /home/jenkins/jenkins_test/tools/kermit_config/%s/homebox_console" % cfg.serial)
time.sleep(1)
homebox.write("log session /home/jenkins/jenkins_test/tools/homebox_init.log\r\n")
time.sleep(1)
homebox.write("c\r\n")
time.sleep(1)
goon = 1



def show_percentage():
	pass

print "start init"
t = threading.Thread(target = show_percentage)
t.start()




for i in range(3):
	homebox.sendline("")
	if 1 == homebox.expect(["#",pexpect.TIMEOUT],timeout = 5):
		print "homebo:timeout: no # symbol matched in 5s"
	else:
		break
if i == 2:
	goon  = 0
	t.join()
	print "homebox cmd console error: no # symbol matched"
	homebox.terminate()
	homebox.close()
	os._exit(1)	

homebox.sendline("eraseall")
print "erasing"
time.sleep(5)
for i in range(3):
	homebox.sendline("")
	time.sleep(0.5)
if 1 == homebox.expect(["#",pexpect.TIMEOUT],timeout = 30):
	print "erase timeout"
	homebox.terminate()
	homebox.close()
	os._exit(1)	


homebox.sendline("id %s" % cfg.id.long_homebox)
print cfg.id.long_homebox
time.sleep(1)
if 1 == homebox.expect(["## uploaded ## did = %s,sid = %s,type = 20" % (cfg.id.homebox,cfg.id.homebox),pexpect.TIMEOUT],timeout = 300):
	goon = 0
	t.join()
	print "homebox init error: can't match first activity heartbeat"
	homebox.terminate()
	homebox.close()
	os._exit(1)
else:

	t.join()
	print "label:%s" % cfg.label
	print "ID:%s" % cfg.id.homebox 
	print "long ID:%s" % cfg.id.long_homebox
	print "homebox init done!"
	homebox.terminate()
	homebox.close()
	os._exit(0)

