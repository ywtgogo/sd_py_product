import sys
import subprocess
import datetime
import threading
import signal
import time
import os
import SL_CONFIG


cfg = SL_CONFIG.get_cfg(sys.argv[1])
hbreadback = subprocess.Popen("/usr/bin/kermit /home/jenkins/jenkins_test/tools/kermit_config/%s/homebox_readback" % cfg.serial,shell = True,stdin = subprocess.PIPE,stdout = subprocess.PIPE)
time.sleep(1)
hbreadback.stdin.write("c\r\n")

io_mutex = threading.Lock()

current = datetime.datetime.now()
#dir_path = "/home/sandlacus/test_station/sniffer_log"
date_time = "%s%02d%02d" % (current.year,current.month,current.day)
#log_path = "%s/%s" % (dir_path,date_time)
log_path = "/home/jenkins/jenkins_release/sl_daily_log/homebox_log/%s" % cfg.label
if os.path.exists(log_path) == False:
	os.makedirs(log_path)
log = open("%s/%s.log" % (log_path,date_time),"a")


def override_ctrl_c(sig,frame):
	os._exit(0)


def RTC_polling():
	global log_path,log
	while True:
		now = datetime.datetime.now()
		if now.hour == 0 and now.minute == 0 and now.second == 30:
			if io_mutex.acquire():
				date = "%s%02d%02d" % (now.year,now.month,now.day)
				log.write("date change,please refer to next day\r\n")
				log.close()
				log = open("%s/%s.log" % (log_path,date),"a")
				io_mutex.release()
				time.sleep(2)

		time.sleep(0.3)



if __name__ == "__main__":

	signal.signal(signal.SIGTERM,override_ctrl_c)
	rtc = threading.Thread(target = RTC_polling)
	rtc.setDaemon(True)
	rtc.start()
	while True:
		raw_str = hbreadback.stdout.readline()
		TS = "%s" % (datetime.datetime.now())
		string = "%s---%s : %s\r\n" % (cfg.label,TS,raw_str)
		print("%s" % string)
		if io_mutex.acquire():
			log.write("%s" % string)
			log.flush()
			io_mutex.release()
