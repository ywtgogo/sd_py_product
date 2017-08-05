from test_lib import *

class expect_event:
	def __init__(self,id):
		self.id = id
		self.alert = 0
		self.unalert = 0
		self.hb = 0
		self.alert_ts = 0
		self.unalert_ts = 0





def uplink_F002_alert(expect_list):
	get_list = []
	honsole.log("now start expecting")
	while True:
		result = honsole.get_value(ls = ["## uploaded ## did = %s,sid = ([0-9a-fA-F]*),type = (\d*),occur_ts = (\d*)\r\n" % honsole.id],tot = 60,errlog = False,refresh = False)
		if result == "ANT":
			break
		else:
			resl = result[0]
			get_list.append({"id":resl[0],
					"type":resl[1],
					"ts":int(resl[2])})


	for i in get_list:
		for j in expect_list.values():
			if i["id"] == j.id:
				if i["type"] == UL_EVENT["ALERT"]:
					if j.alert == 0:
						div = abs(i["ts"] - j.alert_ts)
						if div > 30:
							honsole.log("%s:alert ts div exceed 30s -- div:%d" % (i["id"],div))
							return 1
						else:
							j.alert += 1
							break
					else:
						honsole.log("%s:detect alert event exceeding 1 time" % i["id"])
						return 1

				elif i["type"] == UL_EVENT["UNALERT"]:
					if j.unalert == 0:
						div = abs(i["ts"] - j.unalert_ts)
						if div > 120:
							honsole.log("%s:unalert ts div exceed 30s -- div:%d" % (i["id"],div))
							return 1
						else:
							j.unalert += 1
							break

				elif i["type"] == UL_EVENT["ERR"]:
					honsole.log("error upload event detected")
					return 1


	return 0







def downlink_F002_alert(sins):
	base_ts = int(time.time())
	sonsole.log("%s start" % sins.id)
	time.sleep(sins.alert_ts - base_ts)
	sonsole.corres(cmd = "sa %s" % sins.id)


	sonsole.log("%s:trigger alarm" % sins.id)
	if sins.id[0] == "4":
		sins.unalert_ts = sins.alert_ts + 2

	time.sleep(sins.unalert_ts - sins.alert_ts)

	if "unmatched" == sonsole.corres(cmd = "gsi %s" % sins.id,pattern = ["alarm_status = 1"],tot = 1,errlog = False):
		if sins.id[0] == "4":
			return 0
		sonsole.log("%s:console error" % sins.id)
		sonsole.close("%s %s" % (test_item,RST[1]))
		honsole.close()
		os._exit(1)


	if sins.id[0] == "4":

		sonsole.log("%s not back to normal" % sins.id)
		sonsole.close("%s %s" % (test_item,RST[1]))
		honsole.close()
		os._exit(1)


	sonsole.corres(cmd = "sda %s" % sins.id)
	sonsole.log("%s:force disalarm" % sins.id)
	time.sleep(30)

	sonsole.log("check:alarm->normal")
##check alarm->normal 
	if "unmatched" == sonsole.corres(cmd = "gsi %s" % sins.id,pattern = ["alarm_status = 0","alarm_sent = 0"],tot = 1):
		sonsole.log("%s not back to normal" % sins.id)
		sonsole.close("%s %s" % (test_item,RST[1]))
		honsole.close()
		os._exit(1)






if __name__=="__main__":
	honsole = SL_console("homebox")
	sonsole = SL_console("sensor")
	base_ts = int(time.time())
	for i in sonsole.id.keys():
		exec("%s_event = expect_event('%s')" % (i,sonsole.id[i]))
		exec("%s_event.alert_ts = %d" % (i,base_ts+random.randint(5,20)))
		exec("%s_event.unalert_ts = %s_event.alert_ts+%d" % (i,i,random.randint(30,60)))
		exec("%s_thread = SL_thread(downlink_F002_alert,var = (%s_event,))" % (i,i))
		exec("%s_thread.start()" % i)

	expect_list = {i:eval("%s_event" % i) for i in sonsole.id.keys()}

	for i in sonsole.id.keys():
		exec("%s_thread.wait()" % i)

	res = uplink_F002_alert(expect_list)

	sonsole.close("%s %s" % (test_item,RST[res]))
	honsole.close()
	os._exit(res)

