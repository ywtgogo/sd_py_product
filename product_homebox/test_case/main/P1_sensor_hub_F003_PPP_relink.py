from test_lib import *


def F003_ppp_relink():
    honsole.corres(cmd = "ppp_relink")
    time.sleep(10)
    local_ts = int(time.time())
    honsole.corres(cmd = "hb")
    ret = honsole.get_value(ls = ["## uploaded ## did = %s,sid = %s,type = 20,occur_ts = (\d+)\r\n" % (honsole.id,honsole.id)],tot = 120,errlog = False)
    if ret != "ANT":
        if abs(local_ts - int(ret[0])) <= 30:
            return 0
        else:
            honsole.log("ts excceed")
            return 1
    else:
        honsole.log("timeout:no hb event expected ")
        return 1



if __name__=="__main__":
    honsole = SL_console("homebox")
    honsole.log("F003_ppp_relink Start Test:")
    result = F003_ppp_relink()
    honsole.close("%s %s" % (test_item,RST[result]))
    os._exit(result)























