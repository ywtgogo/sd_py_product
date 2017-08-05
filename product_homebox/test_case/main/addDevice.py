#_*_ coding:utf-8 _*_



import requests
from test_lib import *
import os,time,datetime
from sys  import *
import base64
from Crypto.Cipher import AES
import base64
from Crypto.Cipher import AES
import json
import re





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
    ver1, ver2 = ver2, ver1
    pass


def add_devrice(id, device_function_txt, parent_id_txt, device_type_txt, device_group_txt):
    device_id = base64.b64encode(encryptAes(key, str(id)))
    show_id   = base64.b64encode(encryptAes(key, str(id[-8:])))
    mobile = base64.b64encode(encryptAes(key, '18796541236'))
    #2G    02104001      wifi    02104002
    device_type = base64.b64encode(encryptAes(key, device_type_txt))
    country_id = base64.b64encode(encryptAes(key, '1001'))
    address_id = base64.b64encode(encryptAes(key, '1001001'))
    city_id = base64.b64encode(encryptAes(key, '1001001'))
    street_id = base64.b64encode(encryptAes(key, 'Pudong District, No.22 Bo XiaRd'))
    # company_id  1004  fsmith cloudend   1001 admin
    company_id = base64.b64encode(encryptAes(key, '1001'))
    fw_ver = base64.b64encode(encryptAes(key, '0.5.0.9'))
    parent_id = base64.b64encode(encryptAes(key, parent_id_txt))
    #homebox 01   sensor 02
    device_group = base64.b64encode(encryptAes(key, device_group_txt))
    device_function = base64.b64encode(encryptAes(key, device_function_txt))
    device_status = base64.b64encode(encryptAes(key, '0'))
    device_life_cycle = base64.b64encode(encryptAes(key, '0'))
    type = base64.b64encode(encryptAes(key, '1'))

    deviceInfo = {'device_id':device_id,
                  'show_id':show_id ,
                  'mobile': mobile,
                  'device_type': device_type,
                  'address_id': address_id,
                  'country_id': country_id,
                  'city': city_id,
                  'street_id':street_id,
                  'company_id': company_id,
                  'fw_ver': fw_ver,
                  'parent_id': parent_id,
                  'device_group': device_group,
                  'device_function': device_function,
                  'device_status': device_status,
                  'device_life_cycle': device_life_cycle,
                  'type': type
                  }
    return deviceInfo
    pass

#del devices
get_delurl_encryp = "http://192.168.10.231/devicedp/v1/deviceManage/deldevice"
#add devices   244:15012
post_url_encryp = "http://192.168.10.231/devicedp/v1/deviceManage/addDevice"

if __name__ == "__main__":
    #DID
    HB_id = "A8A80021"
    key = 'SandlacusData#@1SandlacusData#@1'
    update_ver = '0.5.3.0'
    now_ver    = '0.5.0.9'

    DEV_MANU_OCTO = "01"
    DEV_TYPE = {"m1": "01000001",
                "m2": "01000002"}
    DEV_RANUM = "666666"
    sensor_id ={"water": 30000000,
                "smoke": 20000000,
                "pir"  : 40000000,
                "mag"  : 50000000,
                "vol"  : 60000000}
                #"hb"   : 90000000}
    group_list = {"homebox": "01",
                  "sensor": "02",
                  "bridge": "03"}
    fun_list = {"smoke": '101',
                "water": "102",
                "mag": '103',
                "pir": '104',
                "vol": '105',
                "hb": '000'}
    mode_list = {"m1": "001",
                 "m2": "002"}
    count = 1
    sum_id = []
    device_type_txt = ""
    device_group_txt = ""
    rid = []

    #while 1:
    try:
        while 1:
            print sensor_id
            print
            for i in sensor_id:
                print i
                id = DEV_MANU_OCTO + DEV_TYPE["m1"] + DEV_RANUM + str(sensor_id[i])
                print "homebox id:%s" % id
                device_function_txt = fun_list[i]
                #DEV_MANU_OCTO + DEV_TYPE["m1"] + DEV_RANUM + HB_id
                parent_id_txt = cfg.id.long_homebox
                print cfg.alias
                device_type_txt = group_list["sensor"] + fun_list[i] + mode_list["m1"]
                device_group_txt = group_list["sensor"]
                print device_type_txt
                edit_deviceInfo = add_devrice(id,
                                              device_function_txt,
                                              parent_id_txt,
                                              device_type_txt,
                                              device_group_txt)
                #post_url_encryp = "http://192.168.10.244:15012/devicedp/v1/deviceManage/addDevice"
                r = requests.post(post_url_encryp, json = edit_deviceInfo)
                sum_id.append(id)
                #print deviceInfo
                print
                #print r.text
                ret_txt = decryptAes(key, base64.b64decode(r.text))
                print decryptAes(key, base64.b64decode(r.text))
                print "add state:", re.findall("\"msg\":\"(.*?)\"", ret_txt)
                rid.append(re.findall("\"rid\":\"(.*?)\"", ret_txt))
                #print rid
                print r.status_code
                if r.status_code != 200:
                    print datetime.datetime.now(), "We can't post the package to the service, please check"
                    exit(1)
                    pass
                time.sleep(2)
                print "count: %d\n" %count
                count += 1
                if count > 32:
                    break
                    pass
            if count > 32:
                break
                pass
            for k in sensor_id:
                sensor_id[k] += 1
            print sensor_id
            print
            if count > 32:
                break
                pass
    finally:
        print "num:%d" %len(rid)
        #print "rid:", rid
        for i in rid:
            print i
            print decryptAes(key, base64.b64decode(str(i)))
        fd = open('test.sh', 'w+')
        for i in rid:
            fd.write("'")
            fd.write(str(decryptAes(key, base64.b64decode(str(i)))))
            fd.write("', ")

        fd.close()



    for i in range(0, 32):
        print "It will delet %s" %(sum_id[i])
        print "i:%d" %i
       # print "rid[%d]:%s" %(i, str(rid[i]))
        print "rid num:", decryptAes(key, base64.b64decode(str(rid[i])))
        device_id     = base64.b64encode(encryptAes(key, sum_id[i]))
        print "device_id:%s" % (device_id)
        del_id = {'type': '1',
                  'rid': rid[i],
                  'device_id': device_id,
                  'change_reason': 'add for test'}
        #get_delurl_encryp = "http://192.168.10.244:15012/devicedp/v1/deviceManage/deldevice"
        #params=json.dumps(del_id)
        print "del_id:%s" %(del_id)
        ret = requests.get(get_delurl_encryp, params = del_id)
        print ret.text
        #print ret.url
        #print ret.text
        #print decryptAes(key, base64.b64decode(ret.text))
        print ret.status_code
        if r.status_code != 200:
            print datetime.datetime.now(), "We can't post the package to the service, please check"
            exit(1)
            pass
        time.sleep(2)

'''
'1051', '1050', '1054', '1052', '1049', '1057', '1056', '1060', '1058', '1055', '1063', '1062',
'1066', '1064', '1061', '1069', '1068', '1072', '1070', '1067', '1075', '1074', '1078', '1076',
'1073', '1081', '1080', '1082', '1083', '1079', '1084', '1085',
'''