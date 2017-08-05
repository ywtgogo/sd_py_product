#_*_ coding:utf-8 _*_

import requests
from test_lib import *
import os,time,datetime
from sys  import *
import base64
from Crypto.Cipher import AES
import json



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

def change_version(ver1, ver2):
    temp = ver1
    ver1 = ver2
    ver2 = temp
    pass

def CountDirSize():
    path = "%s/fota_test/0.5.%d.%d/" %(argv[1], cfg.upenv.ver_num, cfg.upenv.type_num)
    ls = os.listdir(path)
    count = 0
    for i in ls:
        if os.path.isfile(os.path.join(path,i)):
            count += 1
    return count


def fota_rule(upd_device_type_txt,
	sensortype_txt,
         rule_name_txt,
         upd_version_txt,
         img_url_txt,
         version_value_txt,
         string_value_txt):
   #string_value = base64.b64encode(encryptAes(key, '01021030016D7D4D5002000D'))
	type_num = base64.b64encode(encryptAes(key, '1'))
	rule_type = base64.b64encode(encryptAes(key, 'R'))
	homebox_version = base64.b64encode(encryptAes(key, 'null'))
	upd_type = base64.b64encode(encryptAes(key, '1'))
	modid = base64.b64encode(encryptAes(key, 'null'))
	prl = base64.b64encode(encryptAes(key, '1'))
	img_block_num = base64.b64encode(encryptAes(key, str(9)))
	img_size = base64.b64encode(encryptAes(key, str(9 * 4096)))
	para_update_info = base64.b64encode(encryptAes(key, 'null'))
	company_id = base64.b64encode(encryptAes(key, '1001'))
	d1 = datetime.datetime.now()
	d3 = d1 + datetime.timedelta(days=1)
	expiration_time = d3.strftime('%Y-%m-%d %H:%M:%S')
	expiration_time_encry = base64.b64encode(encryptAes(key, expiration_time))
	judgment_name_txt = 'unique_did'

	upd_device_type = base64.b64encode(encryptAes(key, upd_device_type_txt))
	sensortype = base64.b64encode(encryptAes(key, sensortype_txt))
	rule_name = base64.b64encode(encryptAes(key, rule_name_txt))
	upd_version = base64.b64encode(encryptAes(key, upd_version_txt))
	img_url = base64.b64encode(encryptAes(key, img_url_txt))
	version_value = base64.b64encode(encryptAes(key, version_value_txt))

	encry = {'type': type_num,
	'rule_type': rule_type,
	'upd_device_type': upd_device_type,
	'homebox_version': homebox_version,
	'sensortype': sensortype,
	'upd_type': upd_type,
	'rule_name': rule_name,
	'modid': modid,
	'upd_version': upd_version,
	'prl': prl,
	'img_url': img_url,
	'img_size_str': img_size,
	'img_block_num_str': img_block_num,
	'para_update_info': para_update_info,
	'company_id': company_id,
	'version_value': version_value,
	'expiration_time': expiration_time_encry,
	'deviceruleitemlist': [{'judgment_type': '5',
	                        'judgment_name': judgment_name_txt,
	                        'judgment_symbol': '1',
	                        'string_value': string_value_txt}],
	}
	return encry
#"http://192.168.10.244:15012/devicedp/v1/upddevicerule/addUpgradeRule"
post_url = "http://192.168.10.244:15012/devicedp/v1/upddevicerule/addUpgradeRule"
sensor_type_dict = {
			"Smoke":"101",
			"Water":"102",
			"Magnetic":"103",
			"Pir":"104"}

if __name__ == "__main__":
	honsole = SL_console("homebox")
	#honsole.init("homebox")
	honsole.log("Sensor Img Fota Test Start Test:")
	post_fail_num = 0
	key = 'SandlacusData#@1SandlacusData#@1'

	#set homebox id
	while 1:
		honsole.console_spawn.sendline("showhbbinfo")
		honsole.console_spawn.expect(["DID:.*?\r\n", pexpect.TIMEOUT], timeout=3)
		#print "honsole.console_spawn.before: %s" %honsole.console_spawn.before
		#print "honsole.console_spawn.after: %s"  %honsole.console_spawn.after
		print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
		id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
		print "honsole.console_spawn.after: %s\n" % honsole.console_spawn.after
		if id_now[0] != cfg.id.homebox:
			honsole.console_spawn.sendline("id %s" %(cfg.id.long_homebox))
			time.sleep(3)
			honsole.console_spawn.sendline("reset")
			time.sleep(30)
		else:
			break

	for i in sensor_type_dict.keys():
		while(1):
			sensortype_origin =  sensor_type_dict[i]
			rule_name_origin = sensortype_origin + "_img"
			upd_device_type_origin = "02" + sensortype_origin + "001"
			honsole.console_spawn.sendline("query %s" %cfg.id.sensor[i])
			honsole.console_spawn.expect(["fw_minor \d\r\n", pexpect.TIMEOUT], timeout=3)
			fw_minor = re.findall('fw_minor (\d)', honsole.console_spawn.after)
			version_value_origin = "2." + str(fw_minor[0]) + ".0.0"
			print "sensor old version is %s" %version_value_origin
			if fw_minor == 0 or fw_minor == 1:
				upd_version_origin = "2.2.0.0"
			else:
				upd_version_origin = "2.1.0.0"


			print "nedd update sensor version is %s" %upd_version_origin
			img_url_origin = cfg.upenv.sensor_fota_url[i] + upd_version_origin
			string_value_origin = cfg.id.long_sensor[i]

			encry = fota_rule(upd_device_type_origin,
                        sensortype_origin,
                        rule_name_origin,
                        upd_version_origin,
                        img_url_origin,
                        version_value_origin,
                        string_value_origin)

			print "++++++++++++++++++++++++++++++++++++++++\n"
			r = requests.post(post_url, json = encry)
			print "post sensor fota rule\n"
			print decryptAes(key, base64.b64decode(r.text))
			if post_fail_num == 3:
				honsole.log("The package post fail(%d), the program will be exit!!!!!") % r.status_code
				exit(1)
				break
			if(r.status_code != 200):
				print "The package post fail"
				post_fail_num += 1
				#fail_cnt += 1
				continue
			post_fail_num = 0
			print "--------------------------\n"
			time.sleep(100)
			print "++++++++++++++++++++++++++++++++++++++++\n"
			print "Send fota"
			send_ret = honsole.corres(cmd="fota", pattern=["Request is successful"])
			if send_ret == "unmatched":
				honsole.log("I can't match the words: \"Request is successful \",it will not fota img now, please check!!!")
				exit(1)
			ret = honsole.console_spawn.expect(["No device", pexpect.TIMEOUT], timeout=3)
			print "ret:%d" %(ret)
			if (ret != 0):
				honsole.log("It's runing fota img updata")
			else:
				honsole.log("I can't download the img,it might be  not fota img now(No device), please check!!!")
				exit(1)

			ret = honsole.console_spawn.expect(["SUCCEED ID: .*\r\n","--send result--",pexpect.TIMEOUT], timeout=3000)
			if ret != 0:
				print "sensor:%s fota fail\n" %cfg.id.sensor[i]
				break
			print "---------------------succeed id: %s------------\n" %cfg.id.sensor[i]
			print "hbafter=%s\n" %honsole.console_spawn.after
			ID_match = re.findall(r'SUCCEED ID: 0x([a-fA-F0-9]*)', honsole.console_spawn.after)
			print ID_match
			print r"ID_match:%s" % ID_match[0].upper()
			print r"cfg_sensor:%s" %cfg.id.sensor[i]
			#print "ID_match: %s upper: %s cfg_sensor:%s\n" %(ID_match[0],ID_match[0].upper(),cfg.id.sensor[i])
			if ID_match[0].upper() == cfg.id.sensor[i]:
				print "sensor:%s fota success\n" %cfg.id.sensor[i]
				ret = honsole.console_spawn.expect(["--send result--", pexpect.TIMEOUT], timeout=3000)
				if ret != 0:
					print "sensor result uplink success\n" %cfg.id.sensor[i]
					break
			else:
				print "fota error\n"
				print "sensor:0x%s fota fail\n" %cfg.id.sensor[i]
				break
	print "sensor fota complete\n"
