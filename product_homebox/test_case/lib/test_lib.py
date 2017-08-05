import sys
import re
import pexpect
import pexpect.fdpexpect
import os
import subprocess
import time
import threading
import signal
import SL_CONFIG
import requests
import datetime
import base64
from Crypto.Cipher import AES
import json
import random




##########################global define##############################



''' 
test_item
define: py script name without .py postfix
attr: global string
'''

test_item = os.path.splitext(sys.argv[0])[0]

'''
logging_path
define: logging path with paramenter 1 in such format:sys.arg[1]/test_item
attr :global string
'''
logging_path = ("%s/%s" % (sys.argv[1],test_item))

'''
tools_path ##
define: tools folder where toos is on dependency of py script
attr:global string
'''
tools_path = "/home/jenkins/jenkins_test/tools"


'''
get cfg
define: get configuration from SL_CONFIG module which is pre-define in SL_CONFIG.py
Note: to get cfg,user should input sys parameter with arg[2] to choose a configuration to use or cfg will be default cfg
configuration list is defined in SL_CONFIG
attr: global Object(SL_CONFIG.SL_config)
'''
if len(sys.argv) == 3:
	cfg = SL_CONFIG.get_cfg(sys.argv[2])
else:
	cfg = SL_CONFIG.get_cfg()


if os.path.exists(logging_path) == False:
	os.makedirs(logging_path)

'''
logfile
define: log file descriptor named py script name 
attr: global internal Object(file)
'''
logfile = open("%s/%s.log" % (logging_path,test_item),"w+")

'''
io_mutex
define: a mutex to exclude concurrence thread while in I/O operation
nowtime only used in logging
attr: global internal Object(threading.Lock)
'''
io_mutex = threading.Lock()

''' 
result tuple
define: marco tuple to print test result with os._exit() function
attr: global tuple
'''
RST = ("pass","fail",)


'''
global dict macro:define upload eventid
define:uplink event code which is defined in sl_uplink protocol
attr: global dict
'''
UL_EVENT = {"ALERT":"10",
			"UNALERT":"11",
			"INFO":"20",
			"ERR":"30"}



#####################################################################

def general_log(string,source = None):
	TS = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
	if logfile.closed == False:
		tsstr = "%s : %s -> %s\r\n" %(TS,source,string)
		if io_mutex.acquire():
			logfile.write(tsstr)
			logfile.flush()
			io_mutex.release()
	else:
		tsstr = "%s : from %s --- %s --- warning:log fd has been closed,this string was printed sysout only\r\n" % (TS,source,string)

	print (tsstr)


def general_log_close(laststr = None,source = "closed fd"):
	if laststr != None:
		general_log(laststr,source+" End")
	if logfile.closed == False:
		if io_mutex.acquire():
			logfile.close()
			io_mutex.release()


class SL_thread:

	def __init__(self,func,var = ()):
		self.control = None
# this use global class member to show the result of thread
		self.result = "pending"
		self.trd = threading.Thread(target = func,args = var)
		self.trd.setDaemon(True)

	def status(self):
		return self.trd.isAlive()

	def wait(self):
		self.trd.join()

	def start(self):
		self.trd.start()


class SL_console:

	name = None
	console_spawn = None
	spawn_mutex = threading.RLock()

	info_cmd = []
	working_state = "pending"

	def __init__(self,name):
		self.name = name
		self.id = None

		self.console_spawn = pexpect.spawn("/usr/bin/kermit %s/kermit_config/%s/%s_console" % (tools_path,cfg.serial,self.name))
		self.console_spawn.write("log session %s/%s_console.log\r\n" % (logging_path,self.name))
		time.sleep(1)
		self.console_spawn.write("c\r\n")
		time.sleep(1)

####spawn init done

		
## test device init option:
## if any test device (including TBT device) need a initialize sequence by coding,
## please override after this line


## sensor init sequence 
		

		if self.name == "sensor":

			self.id = {}
			id_filter = re.compile("(fake.*)")
			for i in cfg.id.sensor.keys():
				if id_filter.findall(i):
					self.id[i] = cfg.id.sensor[i]





## parent id is depending on sensor console string output
			self.parent_id = cfg.id.homebox

## check sensor console ready to work or not
			base_seq = random.randint(1,int(time.time()))
			fail = 0
			for i in range(3):
				if "matched" == self.corres(cmd = "reset",pattern = ["system boot now"],tot = 1):
						self.corres(cmd = "ss %s" % base_seq)
						break
				fail += 1
				time.sleep(1)
			if fail == 3:
				self.close("reset fail")
				os._exit(1)
			else:

#set sensor console id,which may be a list in some case

				for i in self.id.values():
					self.corres(cmd = "ssi %s" % i)
					if "matched" == self.corres(cmd = "gsi %s" % i,pattern = ["sn_mitt = %s" % i.lower(),"lc_sequence = %s" % base_seq],tot = 1):
						pass

					else:
						self.close("set id fail")
						os._exit(1)



## homebox init sequence

## get homebox id by "ls" command and locate which id group contained
		elif self.name == "homebox":
			self.ready()
			self.id = cfg.id.homebox
			self.child_id = cfg.id.sensor


		elif self.name == "power_switch":

			fail = 0
			for i in range(3):
				if "matched" == self.corres(cmd = "reset",pattern = ["initial done"],tot = 1):
						break
				fail += 1
				time.sleep(1)
			if fail == 3:
				self.close("reset fail")
				os._exit(1)

				
		self.log("-"*30)
		self.log("| label: %s" % cfg.label)
		self.log("| %s console init OK..." % self.name)
		self.log("| console id:%s" % self.id)
		self.log("| log path: %s" % logging_path)
		self.log("-"*30)


## initialize done



	def ready(self):
		if self.spawn_mutex.acquire():
			for i in range(3):
				self.console_spawn.sendline()
				if 0 == self.console_spawn.expect(["#", pexpect.TIMEOUT],timeout=5):
					self.spawn_mutex.release()
					return 0
			self.close("console corrupt:no # symbol expected")

		os._exit(1)
	
	def log(self,string):
		general_log(string,self.name)

	def flush(self):
		if self.spawn_mutex.acquire():
			self.console_spawn.expect([r'.+',pexpect.TIMEOUT],timeout = 2)
			self.spawn_mutex.release()

	def corres(self,cmd = None,pattern = [],mode = "and",tot = 120,errlog = True,refresh = True):
		if self.console_spawn.isalive() != True:
			self.log("no child alive,wait to be terminated")
			time.sleep(3)

		if self.spawn_mutex.acquire():
			argc = len(pattern)
			if refresh == True:
				self.flush()
			if cmd != None:
				self.ready()
				self.console_spawn.sendline(cmd)
			if mode == "and":
				if argc != 0:
					for i in range(argc):
						if 1 == self.console_spawn.expect([pattern[i], pexpect.TIMEOUT],timeout=tot):
							if errlog == True:
								self.log("missing expected:%s" % pattern[i])
								self.log("%s" % self.console_spawn.before)
							self.spawn_mutex.release()
							return "unmatched"
				self.spawn_mutex.release()
				return "matched"
			elif mode == "or":
				pattern.append(pexpect.TIMEOUT)
				timeout_point = len(pattern) - 1
				if timeout_point == self.console_spawn.expect(pattern,timeout = tot):
					if errlog == True:
						self.log("nothing expected,timeout raised")
					self.spawn_mutex.release()
					return "unmatched"
				else:
					self.spawn_mutex.release()
					return self.console_spawn.after

	def get_value(self,ls = [],tot = 1,errlog = True,refresh = True):
		if self.console_spawn.isalive() != True:
			self.log("no child alive,dummy,wait to be terminated")
			time.sleep(3)	
		if self.spawn_mutex.acquire():
			if refresh == True:
				self.flush()
			argc = len(ls)
			ret_value = []
			for i in range(argc):
				if 1 == self.console_spawn.expect([ls[i], pexpect.TIMEOUT],timeout=tot):
					if errlog == True:
						self.log("%s" % self.console_spawn.before)
						self.log("arg is not found:%s" % ls[i])
					self.spawn_mutex.release()
					return "ANT"
				else:
					regular = re.compile(r'%s' % ls[i])
					ret_value.append(regular.findall(self.console_spawn.after).pop())
			self.spawn_mutex.release()
			return ret_value

	def close(self,laststr = None):	
		self.console_spawn.terminate()
		self.console_spawn.close()
		general_log_close(laststr,self.name)


class SL_subtest:
	spawn = None
	subtest = None
	execmd = None
	subtest_arg = None
	def __init__(self,cmd,arg = []):
		global logfile
		if logfile.closed == True:
			logfile = open("%s/%s.log" % (logging_path,test_item),"a+")
		self.execmd = cmd
		self.subtest = os.path.split(cmd)[1]
		self.subtest_arg = arg
		exp = "python -u %s.py" % self.execmd
		if len(self.subtest_arg) != 0:
			for i in self.subtest_arg:
				exp += " %s" % i
		self.log("launch cmd:%s" % exp)
		self.spawn = pexpect.spawn(exp)

	def get_subtest_result(self,pattern = [],tot = 3600):
		if len(pattern) == 0:
			pattern.append("%s %s" % (self.subtest,RST[0]))
			pattern.append("%s %s" % (self.subtest,RST[1]))
		pattern.append(pexpect.TIMEOUT)
		pattern.append(pexpect.EOF)
		timeout_index = len(pattern)-2
		eof_index = len(pattern)-1
		res = self.spawn.expect(pattern,timeout = tot)
 		if res == timeout_index:
 			return "timeout:no pattern expected"
 		elif res == eof_index:
 			return "EOF:spawn exited"
 		else:
 			return self.spawn.after

	def restart(self):
		if self.spawn.isalive() == False:
			for i in range(3):

				exp = "python -u %s.py" % self.execmd
				if len(self.subtest_arg) != 0:
					for i in self.subtest_arg:
						exp += " %s" % i
				self.spawn = pexpect.spawn(exp)
				if self.spawn.isalive() == True:
					break
			if self.spawn.isalive() == False:
				return 1
			else:
				return 0
		else:
			self.spawn.kill(signal.SIGKILL)
			time.sleep(1)
			if self.spawn.isalive() == False:
				for i in range(3):
					exp = "python -u %s.py" % self.execmd
					if len(self.subtest_arg) != 0:
						for i in self.subtest_arg:
							exp += " %s" % i
					self.spawn = pexpect.spawn(exp)

				if self.spawn.isalive() == False:
					return 1
				else:
					return 0
			else:
				return 1

	def stop(self):
		if self.spawn.isalive() == True:
			self.spawn.kill(signal.SIGKILL)
			time.sleep(2)
			if self.spawn.isalive() == False:
				return True
			else:
				return False
		else:
			return True
	def log(self,string):
		general_log(string,"subtest # %s" % self.subtest)



	def close(self,laststr = None):
		general_log_close(laststr,"subtest # %s" % self.subtest)
		self.stop()
	


def homebox_prepare_next_test():
	hb_init = SL_subtest("%s/jenkins_homebox_init_task" % tools_path,arg = [cfg.label])
	res = ""
	res = hb_init.get_subtest_result(pattern = ["homebox init done!"],tot = 120)
	if res == "homebox init done!":
		if hb_init.stop() == True:
			hb_init.close("homebox is ready for next test")
			return 0
	else:
		hb_init.close("homebox init error: %s" % res)
		os._exit(1)







def nrPadBytes(blocksize, size):
    'Return number of required pad bytes for block of size.'
    if not (0 < blocksize < 255):
        print "blocksize must be between 0 and 255!!!!!!!!!!!!!!!!!!!!!!!!!!"
    return blocksize - (size % blocksize)


def appendPadding(blocksize, s):
    '''Append rfc 1423 padding to string.
    RFC 1423 algorithm adds 1 up to blocksize padding bytes to string s. Each
    padding byte contains the number of padding bytes.
    '''
    n = nrPadBytes(blocksize, len(s))
    if n==0:
        return s + (chr(16) * 16)
    else:
        return s + (chr(n) * n)


def removePadding(blocksize, s):
    'Remove rfc 1423 padding from string.'
    n = ord(s[-1])  # last byte contains number of padding bytes
    if n > blocksize or n > len(s):
        print('invalid padding!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return s[:-n]




def encryptAes(key, string):
    mode = AES.MODE_CBC
    #IV = appendPadding(16, 'AES')
    IV = 'SandlacusData#@1'
    encryptor = AES.new(key, mode, IV)
    str_pad = appendPadding(16, string)
    #print "len of str_pad: %d" %len(str_pad)
    result = encryptor.encrypt(str_pad)
    return result


def decryptAes(key, string):
    mode = AES.MODE_CBC
    #IV = appendPadding(16, 'AES')
    IV = 'SandlacusData#@1'
    decryptor = AES.new(key, mode,IV)
    result = decryptor.decrypt(string)
    str_rmpad = removePadding(16, result)
    return str_rmpad



