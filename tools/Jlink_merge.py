import pexpect
import sys
import time
import re
image_path = sys.argv[1]
device = sys.argv[2]
main_image = sys.argv[3]
BL_image = sys.argv[4]
header = sys.argv[5]
if len(sys.argv) == 7:
	jl_serial_number = sys.argv[6]
else:
	jl_serial_number = None

print("image_path............%s \n" % image_path)
print("device............%s \n" % device)
p = pexpect.spawn("/home/jenkins/jenkins_test/tools/JLink_Linux_V610a_i386/JLinkExe")



def jlink_connect():
	global p,device,jl_serial_number

	p.expect([r'.+',pexpect.TIMEOUT],timeout = 2)
	p.sendline("")
	if p.expect(["J-Link>",pexpect.TIMEOUT],timeout = 1) == 1:
		print "no prompt 1"
		return 1
	p.sendline("ShowEmuList")

	jlink_status = p.expect(["J-Link\[(\d)\]",pexpect.TIMEOUT],timeout = 2)
	jlink_device_num = 0
	while 1 != jlink_status:
		jlink_device_num += 1
		jlink_status = p.expect(["J-Link\[(\d)\]",pexpect.TIMEOUT],timeout = 1)

	if jlink_device_num == 0:
		print "no jlink device"
		return 1

	if jlink_device_num > 1:
		if jl_serial_number == None:
			snls = []
			p.sendline("ShowEmuList")
			for i in range(jlink_device_num):
				exp = "Connection: USB, Serial number: (\d*),"
				p.expect(exp)
				snls.append(int(re.compile(exp).findall(p.after).pop()))
				print "[%s] S/N:" % i,snls[i]
			index = int(raw_input("%s Jlink devices detected,input index:" % jlink_device_num))
			jl_serial_number = snls[index]
		
		exp = "J-Link\[(\d)\]: Connection: USB, Serial number: %s" % jl_serial_number
		p.sendline("ShowEmuList")
		if p.expect([exp,pexpect.TIMEOUT],timeout = 1) == 1:
			print "can not found follow S/N:%s" % jl_serial_number
			return 1
		index = int(re.compile(exp).findall(p.after).pop())


		p.sendline("selemu")
		if 1 == p.expect(["Select emulator index:",pexpect.TIMEOUT],timeout = 1):
			print"could not input emu index"
			return 1
		p.sendline("%s" % index)
		if p.expect(["S/N: %s" % jl_serial_number,pexpect.TIMEOUT],timeout = 1):
			print "could not get switched responsed"
			return 1
	else:
		exp = "Connection: USB, Serial number: (\d*),"
		p.sendline("ShowEmuList")
		if p.expect([exp,pexpect.TIMEOUT],timeout = 1) == 1:
			print "warning:can not get S/N"
		else:
			jl_serial_number = int(re.compile(exp).findall(p.after).pop())
	p.sendline("connect")
	if p.expect(["Device>",pexpect.TIMEOUT],timeout = 1):
		print "connect error"
		return 1
	p.sendline("%s" % device)
	if p.expect(["TIF>",pexpect.TIMEOUT],timeout = 1):
		print "device type error"
		return 1
	p.sendline("S")
	if p.expect(["Speed>",pexpect.TIMEOUT],timeout = 1):
		"set debug mode error"
		return 1
	p.sendline("1000")
	if p.expect(["J-Link>",pexpect.TIMEOUT],timeout = 1):
		print "set speed error"
		return 1
	print "connect O.K. S/N:%s" % jl_serial_number
	return 0




def flash_merge():
	global p,image_path,device,main_image,BL_image,header
	if 1 == jlink_connect():
		return 1
	p.sendline("erase")       

	if 0 != p.expect(["Erasing done","ailed","ERROR","error",pexpect.TIMEOUT],timeout = 5):
		print "Erase error"
		return 1
	print "Erase done"
	p.sendline("loadbin %s/%s 0x3F000" % (image_path,header))

	if 0 != p.expect([r'O.K.',"ailed","ERROR","error",pexpect.TIMEOUT],timeout = 30):
		print "program header error"
		return 1
	print "program header done"
	p.sendline("loadbin %s/%s 0x9000" % (image_path,main_image))

	if 0 != p.expect([r'O.K.',"ailed","ERROR","error",pexpect.TIMEOUT],timeout = 30):
		print "program main image error"
		return 1
	print "program main image done"
	p.sendline("loadbin %s/%s 0x0" % (image_path,BL_image))

	if 0 != p.expect([r'O.K.',"ailed","ERROR","error",pexpect.TIMEOUT],timeout = 30):
		print "program bootloader error"
		return 1
	print "program bootloader done"
	p.sendline("savebin %s/homebox_production.bin 0x0 0x40000" % image_path)

	if 0 != p.expect([r'O.K.',"ailed","ERROR","error",pexpect.TIMEOUT],timeout = 30):
		print "readback image error"
		return 1
	print "read back image done:image file:%s/homebox_production.bin" % image_path
	p.sendline("r")
	p.sendline("go")
	if 1 == p.expect(["J-Link>",pexpect.TIMEOUT],timeout = 5):
		print "start app error"
		return 1
	p.sendline("go")
	if 1 == p.expect(["J-Link>",pexpect.TIMEOUT],timeout = 5):
		print "start app error"
		return 1
	print "app start"


	print "-------------"

	print "Done!"
	return 0

for i in range(3):
	if 0 == flash_merge():
		exit(0)
	else:
		p.terminate()
		p.close()
		time.sleep(2)
		p = pexpect.spawn("/home/jenkins/jenkins_test/tools/JLink_Linux_V610a_i386/JLinkExe")

print "jlink fault"
exit(1)
