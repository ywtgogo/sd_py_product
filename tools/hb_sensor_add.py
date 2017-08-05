#_*_ coding:utf-8 _*_



import requests
import SL_CONFIG
import os,time,datetime
from sys  import *
import base64
from Crypto.Cipher import AES
import base64
from Crypto.Cipher import AES
import json

cfg = SL_CONFIG.get_cfg(argv[1])


DEV_TYPE_M1 = "01000001"
DEV_TYPE_M2 = "01000002"

DEV_MANU_OCTO = "01"

DEV_RANUM = "666666"



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
get_delurl_encryp = "http://192.168.10.241/devicedp/v1/deviceManage/deldevice"
#add devices
post_url_encryp = "http://192.168.10.241/devicedp/v1/deviceManage/addDevice"



if __name__ == "__main__":
    #DID

    key = 'SandlacusData#@1SandlacusData#@1'
    update_ver = '0.5.3.0'
    now_ver    = '0.5.0.9'

    add_Gas_id   = 10000000
    add_Water_id = 30000000
    add_Smoke_id = 20000000
    add_PIR_id   = 40000000
    add_Magne_id = 50000000
    add_Volta_id = 60000000
    add_HB_id    = 90000000
    id_list = [add_Water_id, add_Smoke_id, add_PIR_id, add_Magne_id, add_Volta_id, add_HB_id]
    group_list = {"homebox":"01",
                  "sensor":"02",
                  "bridge":"03"}
    fun_list= {"smoke":'101',
               "water":"102",
               "mag"  :'103',
               "pir"  :'104',
               "vol"  :'105',
               "hb"   :'000'}
    mode_list = {"m1":"001",
                 "m2":"002"}
    count = 1
    device_type_txt = ""
    device_group_txt = ""
    id = cfg.id.long_homebox
    print "homebox id:%s" %id
    device_function_txt = fun_list["hb"]
    parent_id_txt = cfg.id.long_homebox
    print cfg.alias
    device_type_txt = group_list["homebox"] + fun_list["hb"] + mode_list[cfg.alias]
    device_group_txt = group_list["homebox"]
    print device_type_txt
    edit_deviceInfo = add_devrice(id,
                                  device_function_txt,
                                  parent_id_txt,
                                  device_type_txt,
                                  device_group_txt)
    # post_url_encryp = "http://192.168.10.244:15012/devicedp/v1/deviceManage/addDevice"
    r = requests.post(post_url_encryp, json=edit_deviceInfo)
    print decryptAes(key, base64.b64decode(r.text))
    print r.status_code
    if r.status_code != 200:
        print datetime.datetime.now(), "We can't post the package to the service, please check"
        exit(1)
        pass
    print r.status_code

    for i in cfg.id.long_sensor:
        print i
        id = cfg.id.long_sensor[i]
        print "sensor id:%s" % id
        device_function_txt = fun_list[i]
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
        #print decryptAes(key, base64.b64decode(r.text))
        print r.status_code
        print decryptAes(key, base64.b64decode(r.text))
        if r.status_code != 200:
            print datetime.datetime.now(), "We can't post the package to the service, please check"
            exit(1)
            pass
        #time.sleep(100)






