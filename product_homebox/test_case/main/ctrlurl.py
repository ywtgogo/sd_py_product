#_*_ coding:utf-8 _*_
from myown_lib import *
from test_lib  import *



#find by DID(AFAFAFAF)还差一个设置值变量赋值
'''
**func name:param_rule
**func：add the parameter rule
**params:*rule_name_txt         rule name you give
         *sensortype_txt        "urlFota", "urlCtrl", "urlEvent", "heartBeatInterval", "fotaInterval", "urlAlert"
         *para_update_info_txt  "http://officelinux.vicp.net:28081/controlService/device-list",
                                "http://officelinux.vicp.net:29992/controlService/device-list"
         *expiration_time_txt   expiration time of the rule
'''
def param_rule(rule_name_txt, sensortype_txt, para_update_info_txt, expiration_time_txt, mode = "wifi"):
    hb_type = re.findall('bronze_(.*?)_', argv[1])
    print hb_type
    rule_type       = base64.b64encode(encryptAes(key, 'R'))
    # upd_device_type  M1(2G) 01000001  M2(WIFI) 01000002
    upd_device_type = base64.b64encode(encryptAes(key, '01000002'))
    homebox_version = base64.b64encode(encryptAes(key, ''))
    sensortype      = base64.b64encode(encryptAes(key, sensortype_txt))
    upd_type        = base64.b64encode(encryptAes(key, '2'))#Upgrade Type:parameter
    rule_name       = base64.b64encode(encryptAes(key, rule_name_txt))
    modid           = base64.b64encode(encryptAes(key, ''))
    upd_version     = base64.b64encode(encryptAes(key, ''))
    prl             = base64.b64encode(encryptAes(key, '1'))
    img_url         = base64.b64encode(encryptAes(key, '0'))
    img_size        = base64.b64encode(encryptAes(key, '0'))
    img_block_num   = base64.b64encode(encryptAes(key, '0'))
    para_update_info = base64.b64encode(encryptAes(key, para_update_info_txt))
    #company_id  1004  fsmith cloudend   1001 admin
    company_id      = base64.b64encode(encryptAes(key, '1001'))
    version_value   = base64.b64encode(encryptAes(key, now_ver))
    expiration_time_encry = base64.b64encode(encryptAes(key, expiration_time_txt))
    #judgment_type   = base64.b64encode(encryptAes(key, '5'))
    #judgment_name   = base64.b64encode(encryptAes(key, 'device_id'))
    #judgment_symbol = base64.b64encode(encryptAes(key, '1'))
    #string_value    = base64.b64encode(encryptAes(key, "AFAFAFAF"))
    type_num        = base64.b64encode(encryptAes(key, '1'))
    if hb_type == "remo2G":
        # upd_device_type  M1(2G) 01000001  M2(WIFI) 01000002
        upd_device_type = base64.b64encode(encryptAes(key, '01000001'))

    # while 1:
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
                                     'judgment_name': 'unique_did',
                                     'judgment_symbol': '1',
                                     'string_value': string_value_txt}],
             }
    return encry




class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


def do_parameter_fota(mode_str):
    time.sleep(100)
    print "Send fota"
    send_ret = honsole.corres(cmd="fota", pattern=["Request is successful"])
    if send_ret == "unmatched":
        honsole.log("I can't match the words: \"Request is successful \",it will not fota img now, please check!!!")
        exit(1)
    ret = honsole.console_spawn.expect(["No device", pexpect.TIMEOUT], timeout=8)
    print "ret:%d" % (ret)
    if (ret != 0):
        honsole.log("It's runing fota parameter updata")
        pass
    else:
        honsole.log("I can't download the img,it might be  not fota img now(No device), please check!!!")
        exit(1)
        pass
    honsole.console_spawn.sendline("showhbbinfo")
    for case in switch(mode_str):
        if case('Ctrl'):
            honsole.console_spawn.expect(["Control url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
            Ctrl_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            print "Ctrl url:%s" % Ctrl_now
            return Ctrl_now
            pass
        if case('Alert'):
            honsole.console_spawn.expect(["Alart url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
            Alert_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            print "Alert url:%s" % Alert_now
            return Alert_now
            pass
        if case('Event'):
            honsole.console_spawn.expect(["Event url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
            Event_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            print "Event url:%s" % Event_now
            return Event_now
            pass
        if case('Fota'):
            honsole.console_spawn.expect(["Fota url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
            Fotaurl_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            print "Fota url:%s" % Fotaurl_now
            return Fotaurl_now
            pass
        if case('Heartbeat'):
            honsole.console_spawn.expect(["Heartbeat interval:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
            Heartbeat_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            print "Heartbeat interval:%s" % Heartbeat_now
            return Heartbeat_now
            pass
        if case('Fotainterval'):
            honsole.console_spawn.expect(["Fota check interval:.*?\r\n", pexpect.TIMEOUT], timeout=3)
            print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
            Fotainterval_now = re.findall('@(.*?)@', honsole.console_spawn.after)
            print "Fota check interval:%s" % Fotainterval_now
            return Fotainterval_now
            pass
        if case():  # default, could also just omit condition or 'if True'
            print "Your mode str is wrong!!!"
            break



#"http://192.168.10.244:15012/devicedp/v1/upddevicerule/addUpgradeRule"
post_url = "http://192.168.10.241/devicedp/v1/upddevicerule/addUpgradeRule"

if __name__ == "__main__":
    honsole = SL_console("homebox")
    honsole.log("HomeBox Parameter Test Start Test:")
    d1 = datetime.datetime.now()
    d3 = d1 + datetime.timedelta(minutes=600)
    exp_time = d3.strftime('%Y-%m-%d %H:%M:%S')
    HB_id = cfg.id.long_homebox
    print "HB_id:%s" % HB_id
    key = 'SandlacusData#@1SandlacusData#@1'
    update_ver = '0.5.3.0'
    now_ver = '0.5.0.9'
    switch_ver = 0
    honsole.console_spawn.sendline("id %s" % (HB_id))

    # find device by DID
    judgment_name_txt = 'unique_did'
    string_value_txt = HB_id
    #post_url = "http://192.168.10.231/devicedp/v1/upddevicerule/addUpgradeRule"
    sensortype = ["urlFota", "urlCtrl", "urlEvent", "heartBeatInterval", "fotaInterval", "urlAlert"]
    sensortype_txt = sensortype[1]
    Event = ["{'urlEvent':'http://officelinux.vicp.net:15580/'}",
             "{'urlEvent':'http://officelinux.vicp.net:15780/'}"]

    Alert = ["{'urlAlert':'http://officelinux.vicp.net:15550/'}",
             "{'urlAlert':'http://officelinux.vicp.net:15750/'}"]

    FOTA = ["{'urlFota':'http://officelinux.vicp.net:15560/fota'}",
            "{'urlFota':'http://officelinux.vicp.net:15760/fota'}"]

    Ctrl = ["{'urlCtrl':'http://officelinux.vicp.net:15570/api/dm/v1/device/list'}",
            "{'urlCtrl':'http://officelinux.vicp.net:15770/api/dm/v1/device/list'}"]

    # The following example is pretty much the exact use-case of a dictionary,
    # but is included for its simplicity. Note that you can include statements
    # in each suite.
    time.sleep(10)
    honsole.console_spawn.sendline("showhbbinfo")
    honsole.console_spawn.expect(["Alart url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Alart url:%s" % id_now
    honsole.console_spawn.expect(["Event url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Event url:%s" % id_now[0]
    print type(id_now)
    honsole.console_spawn.expect(["Fota url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Fota url:%s" % id_now
    honsole.console_spawn.expect(["Heartbeat interval:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Heartbeat interval:%s" % id_now
    honsole.console_spawn.expect(["Fota check interval:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    id_now = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Fota check interval:%s" % id_now
    modif_para = {'ctrl': "",
                        'event': "",
                        'fota': "",
                        'alert': "",
                        'heartval': "",
                        'fotainterval': "",
                        'key': ""}

    modif_para_state = {'ctrl':"",
                         'event': "",
                         'fota':"",
                         'alert': "",
                         'heartval': "",
                         'fotainterval': "",
                         'key': ""}
    modif_para_after = {'ctrl': "",
                         'event': "",
                         'fota': "",
                         'alert': "",
                         'heartval': "",
                         'fotainterval': "",
                         'key': ""}

    try:
        while 1:
            print "1-ctrl/ 2-fota/ 3-alert/4-event/5-heartval/ 6-fotaInterval  port num:0/1 or value(use the space to split)"
            print "eg: 1 1(ctrl's new port)"
            v = raw_input("请输入：")
            val = v.split(" ")
            print val
            for case in switch(val[0]):
                if case('4'):
                    if val[1] == '0':
                        rule_name = 'para_Event_old'

                    if val[1] == '1':
                        rule_name = 'para_Event_new'
                    print "Your rule name is:%s" % (rule_name)
                    para_info_txt = Event[int(val[1])]
                    print Event[int(val[1])]
                    encry = param_rule(rule_name,
                                       sensortype_txt,
                                       para_info_txt,
                                       exp_time)
                    # parameter & fota url 20161212
                    #post_url = "http://192.168.10.231/devicedp/v1/upddevicerule/addUpgradeRule"
                    r = requests.post(post_url, json=encry)
                    print exp_time
                    print decryptAes(key, base64.b64decode(r.text))
                    print
                    print r.status_code

                    if (r.status_code != 200):
                        print "The package post fail"
                        honsole.log("The package post fail")
                        exit(1)
                    modif_para['event'] = do_parameter_fota("Event")
                    print "modif_para['event']:%s" %modif_para['event']
                    print "para_info_txt:%s" %(re.findall(":'(.*?)'", para_info_txt))
                    if modif_para["event"] == (re.findall(":'(.*?)'", para_info_txt)):
                        print "Event parameter success!!!"
                        modif_para_state['event'] = "success"
                    else:
                        print "Event parameter fail!!!"
                        modif_para_state['event'] = "fail"
                    break
                if case('1'):
                    if val[1] == '0':
                        rule_name = 'para_Ctrl_old'

                    if val[1] == '1':
                        rule_name = 'para_Ctrl_new'
                    print "Your rule name is:%s" % (rule_name)
                    para_info_txt = Ctrl[int(val[1])]
                    print Ctrl[int(val[1])]
                    encry = param_rule(rule_name,
                                       sensortype_txt,
                                       para_info_txt,
                                       exp_time)
                    r = requests.post(post_url, json=encry)
                    print exp_time
                    print decryptAes(key, base64.b64decode(r.text))
                    print
                    print r.status_code
                    # print r.content
                    if (r.status_code != 200):
                        print "The package post fail"
                        honsole.log("The package post fail")
                        exit(1)

                    modif_para['ctrl'] = do_parameter_fota("Ctrl")
                    print "modif_para['ctrl']:%s" % modif_para['ctrl']
                    print "para_info_txt:%s" % re.findall(":'(.*?)'", para_info_txt)
                    #print str(modif_para['ctrl'])
                    #print str(re.findall(":'(.*?)'", para_info_txt))
                    if str(modif_para['ctrl']) == str(re.findall(":'(.*?)'", para_info_txt)):
                        print "Ctrl parameter success!!!"
                        modif_para_state['ctrl'] = "success"
                    else:
                        print "Ctrl parameter fail!!!"
                        modif_para_state['ctrl'] = "fail"
                    break
                if case('2'):
                    if val[1] == '0':
                        rule_name = 'para_FOTA_old'

                    if val[1] == '1':
                        rule_name = 'para_FOTA_new'
                    print "Your rule name is:%s" % (rule_name)
                    para_info_txt = FOTA[int(val[1])]
                    print FOTA[int(val[1])]
                    encry = param_rule(rule_name,
                                       sensortype_txt,
                                       para_info_txt,
                                       exp_time)
                    # parameter & fota url 20161212
                    #post_url = "http://192.168.10.231/devicedp/v1/upddevicerule/addUpgradeRule"
                    r = requests.post(post_url, json=encry)
                    print exp_time
                    #print encry
                    # print r.text
                    print decryptAes(key, base64.b64decode(r.text))
                    print
                    print r.status_code
                    if (r.status_code != 200):
                        print "The package post fail"
                        honsole.log("The package post fail")
                        exit(1)

                    modif_para['fota'] = do_parameter_fota("Fota")
                    print "modif_para['fota']:%s" %modif_para['fota']
                    print "para_info_txt:%s" %re.findall(":'(.*?)'", para_info_txt)
                    if modif_para['fota'] == re.findall(":'(.*?)'", para_info_txt):
                        print "fota parameter success!!!"
                        modif_para_state['fota'] = "success"
                    else:
                        print "fota parameter fail!!!"
                        modif_para_state['fota'] = "fail"
                    break
                if case('3'):
                    if val[1] == '0':
                        rule_name = 'para_Alert_old'

                    if val[1] == '1':
                        rule_name = 'para_Alert_new'
                    print "Your rule name is:%s" % (rule_name)
                    para_info_txt = Alert[int(val[1])]
                    print Alert[int(val[1])]
                    encry = param_rule(rule_name,
                                       sensortype_txt,
                                       para_info_txt,
                                       exp_time)
                    r = requests.post(post_url, json=encry)
                    print exp_time
                    print decryptAes(key, base64.b64decode(r.text))
                    print
                    print r.status_code
                    if (r.status_code != 200):
                        print "The package post fail"
                        honsole.log("The package post fail")
                        exit(1)

                    modif_para['alert'] = do_parameter_fota("Alert")
                    print "modif_para['alert']:%s" % modif_para['alert']
                    print "para_info_txt:%s" % re.findall(":'(.*?)'", para_info_txt)
                    if modif_para['alert'] == re.findall(":'(.*?)'", para_info_txt):
                        print "Alert parameter success!!!"
                        modif_para_state['alert'] = "success"
                    else:
                        print "Alert parameter fail!!!"
                        modif_para_state['alert'] = "fail"
                    break
                if case('5'):
                    rule_name = 'para_HeartVal_%ss' %val[1]
                    para_info_txt = "{\"heartBeatInterval\":\"%s\"}" %val[1]
                    print "para_info_txt:%s" %para_info_txt
                    encry = param_rule(rule_name,
                                       sensortype_txt,
                                       para_info_txt,
                                       exp_time)
                    # parameter & fota url 20161212
                    #post_url = "http://192.168.10.231/devicedp/v1/upddevicerule/addUpgradeRule"
                    r = requests.post(post_url, json=encry)
                    print exp_time
                    #print encry
                    # print r.text
                    print decryptAes(key, base64.b64decode(r.text))
                    print
                    print r.status_code
                    if (r.status_code != 200):
                        print "The package post fail"
                        honsole.log("The package post fail")
                        exit(1)

                    modif_para['heartval'] = do_parameter_fota("Heartbeat")
                    print "modif_para['heartval']:%s" % modif_para['heartval']
                    print "para_info_txt:%s" % re.findall(":\"(.*?)\"", para_info_txt)
                    if modif_para['heartval'] == re.findall(":\"(.*?)\"", para_info_txt):
                        print "Heartbeat parameter success!!!"
                        modif_para_state['heartval'] = "success"
                    else:
                        print "Heartbeat parameter fail!!!"
                        modif_para_state['heartval'] = "fail"
                    break
                if case('6'):
                    rule_name = 'para_FotaInterval_%ss' %val[1]
                    para_info_txt = "\"FotaInterval\":\"%s\"" %val[1]
                    encry = param_rule(rule_name,
                                       sensortype_txt,
                                       para_info_txt,
                                       exp_time)
                    r = requests.post(post_url, json=encry)
                    print exp_time
                    print decryptAes(key, base64.b64decode(r.text))
                    print
                    print r.status_code
                    if (r.status_code != 200):
                        print "The package post fail"
                        honsole.log("The package post fail")
                        exit(1)

                    modif_para['fotainterval'] = do_parameter_fota("Fotainterval")
                    print "modif_para['fotainterval']:%s" % (int(modif_para['fotainterval'])/1000)
                    print "para_info_txt:%s" % re.findall(":\"(.*?)\"", para_info_txt)
                    if (int(modif_para['fotainterval'])/1000) == int(re.findall(":\"(.*?)\"", para_info_txt)):
                        print "Fotainterval parameter success!!!"
                        modif_para_state['fotainterval'] = "success"
                    else:
                        print "Fotainterval parameter fail!!!"
                        modif_para_state['fotainterval'] = "fail"
                    break
                if case():  # default, could also just omit condition or 'if True'
                    print "something else!"
                    break
                    # No need to break here, it'll stop anyway

            if val[0] == 'q':
                print "You will exit!!!"
                break
    except KeyboardInterrupt:
        honsole.console_spawn.terminate()
        honsole.close()

        print modif_para_state

    print "modif_para_state:", modif_para_state
    print "modif_para:", modif_para_after

    power_switch = SL_console("power_switch")
    power_switch.console_spawn.sendline("ralarm")
    honsole.log("HomeBox will shutdown!!!!!")
    time.sleep(2)
    power_switch.console_spawn.sendline("talarm")
    honsole.log("HomeBox will open!!!!!")
    time.sleep(20)
    honsole.console_spawn.sendline("showhbbinfo")
    honsole.console_spawn.expect(["DID:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    # print "honsole.console_spawn.before: %s" %honsole.console_spawn.before
    # print "honsole.console_spawn.after: %s"  %honsole.console_spawn.after
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
    honsole.console_spawn.expect(["Alart url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    modif_para_after['alert'] = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Alart url:%s" %modif_para_after['alert']
    honsole.console_spawn.expect(["Event url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    modif_para_after['event'] = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Event url:%s" %modif_para_after['event']
    honsole.console_spawn.expect(["Fota url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    modif_para_after['fota'] = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Fota url:%s" %modif_para_after['fota']
    honsole.console_spawn.expect(["Control url:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    modif_para_after['ctrl'] = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Fota url:%s" % modif_para_after['ctrl']
    honsole.console_spawn.expect(["Heartbeat interval:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    modif_para_after['heartval'] = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Heartbeat interval:%s" %modif_para_after['heartval']
    honsole.console_spawn.expect(["Fota check interval:.*?\r\n", pexpect.TIMEOUT], timeout=3)
    print "honsole.console_spawn.after: %s" % honsole.console_spawn.after
    modif_para_after['fotainterval'] = re.findall('@(.*?)@', honsole.console_spawn.after)
    print "Fota check interval:%s" %modif_para_after['fotainterval']

    print "modif_para_before:", modif_para
    print "modif_para_after:", modif_para_after
    if (modif_para_after == modif_para):
        print "parameter sucess!!!"
        honsole.log("parameter sucess!!!")
    else:
        honsole.log("parameter fail!!!")
    honsole.console_spawn.terminate()
    honsole.close()
    power_switch.console_spawn.terminate()
    power_switch.close()
























































