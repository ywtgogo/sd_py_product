#!/usr/bin/env python

import pexpect
import sys
imagefile = sys.argv[1]
device = sys.argv[2]
print("imagefile............%s \n" % imagefile)
print("device............%s \n" % device)
p = pexpect.spawn("/home/sandlacus/JLink_Linux_V610a_i386/JLinkExe -if SWD -device %s -speed 1000" % device)
p.logfile_read = sys.stdout
index=p.expect([">","FAILED"])      # wait for prompt
if (index == 0):
	p.send("connect\n")         # send "pwd" command
else:
	exit(1)
index=p.expect([">","FAILED"])      # wait for prompt
if (index == 0):
	p.send("erase\n")        # send "exit" command
else:
	exit(1)
index=p.expect([">","FAILED"])      # wait for prompt
if (index == 0):
	p.send("loadbin %s 0x0\n" % imagefile)        # send "exit" command
else:
	exit(1)
index=p.expect([">","FAILED"])      # wait for prompt
if (index == 0):
	p.send("r\n")        # send "exit" command
else:
	exit(1)
index=p.expect([">","FAILED"])      # wait for prompt
if (index == 0):
	p.send("go\n")        # send "exit" command
else:
	exit(1)
index=p.expect([">","FAILED"])      # wait for prompt
if (index == 0):
	p.send("go\n")        # send "exit" command
else:
	exit(1)

p.expect(">")      # wait for prompt

print "-------------"

print "Done!"
