from test_lib import *

def uplink_R003_Nack_rearm():
	child.result = "pending"
	alert_ts = int(time.time())
	unalert_ts = alert_ts + 160
	unalert_occur = 0
	hb_occur = 0
	honsole.log("thread start")
	if "matched" == honsole.corres(pattern = ["## uploaded ## did = %s,sid = %s,type = 10" % (honsole.id,honsole.child_id[0])],tot = 120):
		get_ts = int(honsole.get_value(ls = ["occur_ts = (\d*)\r\n"])[0])
		if math.fabs(get_ts - alert_ts) > 30:
			honsole.close("ts div excceed 30s")
			sonsole.close("%s %s" % (test_item,RST[1]))
			os._exit(1)
		else:
			honsole.log("alert event matched")

		while True:

			if "matched" == honsole.corres(pattern = ["## uploaded ## did = %s,sid = %s" % (honsole.id,honsole.child_id[0])],tot = 5,errlog = False,refresh = False):
				honsole.log("event matched")
				ret = honsole.get_value(ls = ["type = (\d*),","occur_ts = (\d*)\r\n"])
				event_type = int(ret[0])
				get_ts = int(ret[1])
				honsole.log("event type:%s" % event_type)


				if event_type == UL_UNALERT:

					if unalert_occur == 0:
						if (get_ts - unalert_ts) > 30 or (get_ts - unalert_ts) < 0:
							honsole.close("time stamp diveation unexpected")
							sonsole.close("%s %s" % (test_item,RST[1]))
							os._exit(1)
						else:
							honsole.log("unalert event matched")
							unalert_occur = 1
							child.result = 0
					else:
						honsole.close("detect over 1 time unalert")
						sonsole.close("%s %s" % (test_item,RST[1]))
						os._exit(1)

				elif event_type == UL_INFO:
					if hb_occur == 0:
						hb_occur = 1
					else:
						honsole.close("detect over 1 time heartbeat")
						sonsole.close("%s %s" % (test_item,RST[1]))
						os._exit(1)

				else:
					honsole.close("unexpected event matched: type = %s  occur ts = %s" % (event_type,get_ts))
					sonsole.close("%s %s" % (test_item,RST[1]))
					os._exit(1)
					
	else:
		honsole.close("timeout:no uploaded alert event")
		sonsole.close("%s %s" % (test_item,RST[1]))
		os._exit(1)



def downlink_R003_Nack_rearm():
	sonsole.corres(cmd = "reply manual rearm")
	sonsole.corres(cmd = "set alarm")
	time.sleep(122)
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["alarm_status = 1"],tot = 1):
		honsole.close()
		sonsole.close("console error")
		os._exit(1)
	sonsole.corres(cmd = "set disalarm")
	time.sleep(40)
	sonsole.corres(cmd = "reply auto rearm")
	time.sleep(20)

##check alarm->normal 
	sonsole.log("check:alarm->normal")
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["alarm_status = 0","alarm_sent = 0"],tot = 1):
		sonsole.log("not back to normal")
		return 1
#check seq increasingly
	sonsole.log("check:seq increasingly")
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["err_seq_cnt = 0"],tot = 1):
		sonsole.log("Warning: seq error: not increasing")

	return 0



if __name__=="__main__":
	honsole = SL_console("homebox")
	sonsole = SL_console("sensor")

	child = SL_thread(uplink_R003_Nack_rearm)
	sonsole.log("start test")
	child.start()
	result = 1 if downlink_R003_Nack_rearm() or child.result else 0
	sonsole.close("%s %s" % (test_item,RST[result]))
	honsole.close()
	os._exit(result)
