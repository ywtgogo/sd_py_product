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


def fota_rule(rule_name_txt,
              img_fota_url,
              update_ver,
              expiration_time_txt,
              now_ver,
              judgment_name_txt,
              string_value_txt,
              upd_device_type_txt = "01000001",
              mode = "wifi"):
    hb_type = re.findall('bronze_(.*?)_', argv[1])
    print hb_type
    rule_type = base64.b64encode(encryptAes(key, 'R'))
    #upd_device_type  M1(2G) 01000001  M2(WIFI) 01000002
    upd_device_type = base64.b64encode(encryptAes(key, upd_device_type_txt))
    homebox_version = base64.b64encode(encryptAes(key, 'null'))
    sensortype = base64.b64encode(encryptAes(key, 'null'))
    upd_type = base64.b64encode(encryptAes(key, '1'))
    rule_name = base64.b64encode(encryptAes(key, rule_name_txt))
    modid = base64.b64encode(encryptAes(key, 'null'))
    upd_version = base64.b64encode(encryptAes(key, update_ver))
    prl = base64.b64encode(encryptAes(key, '1'))
    img_url = base64.b64encode(encryptAes(key, img_fota_url))
    number = CountDirSize()
    img_size = base64.b64encode(encryptAes(key, str(number * 4096)))
    img_block_num = base64.b64encode(encryptAes(key, str(number)))
    para_update_info = base64.b64encode(encryptAes(key, 'null'))
    # company_id  1004  fsmith cloudend  \\  1001 admin
    company_id = base64.b64encode(encryptAes(key, '1001'))
    version_value = base64.b64encode(encryptAes(key, now_ver))
    expiration_time_encry = base64.b64encode(encryptAes(key, expiration_time_txt))
    judgment_type = base64.b64encode(encryptAes(key, '5'))
    #judgment_name = base64.b64encode(encryptAes(key, judgment_name_txt))
    judgment_symbol = base64.b64encode(encryptAes(key, '1'))
    #string_value = base64.b64encode(encryptAes(key, string_value_txt))
    type_num = base64.b64encode(encryptAes(key, '1'))

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
post_url = "http://192.168.10.241/devicedp/v1/upddevicerule/addUpgradeRule"


if __name__ == "__main__":

    honsole = SL_console("homebox")
    #honsole.init("homebox")
    honsole.log("HomeBox Img Fota Test Start Test:")
    d1 = datetime.datetime.now()
    d3 = d1 + datetime.timedelta(days=1)
    expiration_time = d3.strftime('%Y-%m-%d %H:%M:%S')
    #DID
    HB_id = cfg.id.long_homebox
    print "HB_id:%s" %HB_id
    key = 'SandlacusData#@1SandlacusData#@1'
    now_ver    = '0.5.0.9'
    switch_ver = 0
    succ_cnt = 0
    fail_cnt = 0
    cir_cnt  = 99
    name = 'img_'
    ver_num = cfg.upenv.ver_num
    type_num = cfg.upenv.type_num
    print "type_num:", type_num
    post_fail_num = 0
    update_ver = "0.5.%d.%d"  %(ver_num, type_num)
    print "update_ver:%s" %update_ver

    honsole.console_spawn.sendline("showhbbinfo")
    honsole.console_spawn.expect(["DID:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    #print "honsole.console_spawn.before: %s" %honsole.console_spawn.before
    #print "honsole.console_spawn.after: %s"  %honsole.console_spawn.after
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "honsole.console_spawn.after: %s\n" % honsole.console_spawn.after
    print "id_now:%s" % id_now[0]
    honsole.console_spawn.expect(["DT:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "id_now:%s" % id_now
    honsole.console_spawn.expect(["Firmware version:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    now_ver = re.findall('@(.*?)@', honsole.console_spawn.after).pop()
    print "now_ver:%s" % now_ver
    ver_num = int(now_ver[-3])
    update_ver = "0.5.%d.%d"  %((ver_num + 1), type_num)
    print "update_ver:%s" % update_ver

    try:
        while 1:
            rule_name = name + str(cir_cnt)
            print rule_name
            cir_cnt -= 1
            judgment_name_txt = 'unique_did'
            string_value_txt = cfg.id.long_homebox
            # dev http://officelinux.vicp.net:28080/fota/img-source   test http://officelinux.vicp.net:15560/fota/img-source
            img_fota_url = "%s%s" % (cfg.upenv.img_fota_url, update_ver)
            print "img_fota_url:%s" %img_fota_url
            upd_device_type_txt = cfg.upenv.upd_device_type
            print "upd_device_type:%s" %upd_device_type_txt
            encry = fota_rule(rule_name, img_fota_url, update_ver,
                              expiration_time,
                              now_ver,
                              judgment_name_txt,
                              string_value_txt,
                              upd_device_type_txt)
            r = requests.post(post_url, json = encry)
            print expiration_time
            #print encry
            #print r.text
            print decryptAes(key, base64.b64decode(r.text))
            print r.status_code
            if post_fail_num == 3:
                honsole.log("The package post fail(%d), the program will be exit!!!!!") % r.status_code
                exit(1)
                break
            if(r.status_code != 200):
                print "The package post fail"
                post_fail_num += 1
                #fail_cnt += 1
                continue
                pass
            post_cnt = 0
            time.sleep(80)
            print type(HB_id)
            honsole.console_spawn.sendline("id %s" %(HB_id))
            honsole.log("send id:%s" %(HB_id))
           #print "honsole.console_spawn.readline(): %s\n" % honsole.console_spawn.readline()
            time.sleep(10)
            honsole.console_spawn.sendline("showhbbinfo")
            honsole.log("send showhbbinfo")
            match_id = honsole.console_spawn.expect(["DID:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "match_id:%s" %match_id
            delay_send1 = datetime.datetime.now()
            delay_send2 = datetime.datetime.now()
            while match_id:
                honsole.console_spawn.sendline("showhbbinfo")
                honsole.log("send showhbbinfo")
                match_id = honsole.console_spawn.expect(["DID:.*?\r\n", pexpect.TIMEOUT], timeout=3)
                print "match_id:%s" % match_id
                delay_send2 = datetime.datetime.now()
            print delay_send2 - delay_send1
            #id_now = re.findall('@(.*?)@', honsole.console_spawn.before)
            #print "id_now:%s" % id_now[0]
            print "honsole.console_spawn.after: %s"   %honsole.console_spawn.after
            id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            #print "honsole.console_spawn.before: %s\n" % honsole.console_spawn.before
            print "id_now:%s" % id_now
            time.sleep(10)
            print "Send fota"
            send_ret = honsole.corres(cmd="fota", pattern=["Request is successful"])
            if send_ret == "unmatched":
                honsole.log("I can't match the words: \"Request is successful \",it will not fota img now, please check!!!")
                exit(1)
            ret = honsole.console_spawn.expect(["No device", pexpect.TIMEOUT], timeout=3)
            print "ret:%d" %(ret)
            if (ret != 0):
                honsole.log("It's runing fota img updata")
                pass
            else:
                honsole.log("I can't download the img,it might be  not fota img now(No device), please check!!!")
                exit(1)
                pass
            down_fin = honsole.console_spawn.expect(["bootloader", pexpect.TIMEOUT], timeout=2)
            print "down_fin:%d" % (down_fin)
            timeout1 = datetime.datetime.now()
            timeout2 = timeout1 + datetime.timedelta(minutes=3)
            while down_fin:
                if datetime.datetime.now() > timeout2:
                    honsole.log("I can't download the img,it might be not fota img now(timeout), please check!!!")
                    exit(1)
                    pass
                ret = honsole.console_spawn.expect(["No device", pexpect.TIMEOUT], timeout=2)
                if ret == 0:
                    honsole.log("I can't download the img,it might be  not fota img now(No device), please check!!!")
                    exit(1)
                    pass
                down_fail = honsole.console_spawn.expect(["IMG block download fail", pexpect.TIMEOUT], timeout=2)
                if down_fail == 0:
                    honsole.log("I can't download the img,it might be  not fota img now(IMG block download fail), please check!!!")
                    exit(1)
                    pass
                down_fin = honsole.console_spawn.expect(["bootloader", pexpect.TIMEOUT], timeout=2)
                pass

            print "Restarting!!!!!!!!!!!!!!"
            honsole.log("\tRestarting!!!")
            setp = honsole.console_spawn.expect(["STEP 4", pexpect.TIMEOUT], timeout=5)
            honsole.log("STEP 4 : Jump into app img")

            print "It will updata to %s" %(update_ver)
            time.sleep(160)
            hwr = honsole.console_spawn.expect([update_ver, pexpect.TIMEOUT], timeout=10)
            print "hwr: %s" %(hwr)
            if(hwr == 0):
                honsole.log(update_ver)
                honsole.log("Fota Img Success")
                succ_cnt += 1
                switch_ver = 1
            else:
                honsole.log("update fail")
                honsole.console_spawn.sendline("eraseall")
                honsole.log("eraseall")
                fail_cnt += 1
                pass
            time.sleep(120)
            if switch_ver:
                honsole.console_spawn.sendline("eraseall")
                honsole.log("eraseall")
                time.sleep(30)
                now_ver = update_ver
                ver_num += 1
                update_ver = '0.5.%d.%d' %(ver_num, cfg.upenv.type_num)
                honsole.log("now it will update form %s to %s"  %(now_ver, update_ver))
                switch_ver = 0


            time.sleep(60)

            if (cir_cnt <= 0) :
                break
                pass
    except KeyboardInterrupt:
        pass
    finally:
        print "Succ: %d,  Fail: %d, Total: %d" % (succ_cnt, fail_cnt, (99 - cir_cnt))
        honsole.log("Succ: %d,  Fail: %d, Total: %d" % (succ_cnt, fail_cnt, (99 - cir_cnt)))
        honsole.console_spawn.terminate()
        honsole.close()
