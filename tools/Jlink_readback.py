import pexpect
import sys
import time
image_path = sys.argv[1]
device = sys.argv[2]
print("image_path............%s \n" % image_path)
print("device............%s \n" % device)
p = pexpect.spawn("/home/jenkins/jenkins_test/tools/JLink_Linux_V610a_i386/JLinkExe -if SWD -device %s -speed 500" % device)

def flash_readback():
	global p,image_path,device

	index=p.expect([">","ailed","ERROR","error"])      # wait for prompt
	if (index == 0):
		p.send("connect\n")         # send "pwd" command
	else:
		return 1
	index=p.expect([">","ailed","ERROR","error"])      # wait for prompt
	if (index == 0):
		p.send("savebin %s 0x0 0x40000\n" % image_path)        # send "exit" command
	else:
		return 1
	index=p.expect(["O.K","ailed"])      # wait for prompt
	if (index != 0):
		return 1


	print "-------------"

	print "Done!"
	return 0

for i in range(3):
	if 0 == flash_readback():
		exit(0)
	else:
		p.terminate()
		p.close()
		time.sleep(5)
		p = pexpect.spawn("/home/backup/steven/JLink_Linux_V610a_i386/JLinkExe -if SWD -device %s -speed 500" % device)

exit(1)
