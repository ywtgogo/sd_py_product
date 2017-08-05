import subprocess
import datetime
import os
import time
import signal
import threading
import sys

freq = None
freq_list = ["865.001","868.65"]
for i in freq_list:
	if sys.argv[1] == i:
		freq = i
if freq == None:
	print "frequency invalid"
	print "valid freq:"
	print freq_list
	exit(1)






sniffer = subprocess.Popen("/usr/bin/kermit /home/jenkins/jenkins_test/tools/kermit_config/%s_sniff_config" % freq,shell = True,stdin = subprocess.PIPE,stdout = subprocess.PIPE)
time.sleep(1)
sniffer.stdin.write("c\n")


io_mutex = threading.Lock()

current = datetime.datetime.now()
#dir_path = "/home/sandlacus/test_station/sniffer_log"
date_time = "%s%02d%02d" % (current.year,current.month,current.day)
#log_path = "%s/%s" % (dir_path,date_time)
log_path = "/home/jenkins/jenkins_release/sl_daily_log/sniffer_log/%s" % freq
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
		raw_str = sniffer.stdout.readline()
		TS = "%s# %s" % (time.time(),datetime.datetime.now())
		string = "%sMhz -> %s : %s\r\n" % (freq,TS,raw_str)
		print("%s" % string)
		if io_mutex.acquire():
			log.write("%s" % string)
			log.flush()
			io_mutex.release()
