from test_lib import *



def mqtt_hb():
	for i in range(5):
		if "unmatched" == honsole.corres(pattern = ["receive PINGACK"],tot = 70):
			honsole.log("mqtt heartbeat timeout")
			return 1
		honsole.log("mqtt heartbeat received %d" % (i+1))
	return 0






if __name__=="__main__":
	honsole = SL_console("homebox")
	res = mqtt_hb()
	honsole.close("%s %s" %(test_item,RST[res]))
	os._exit(res)

