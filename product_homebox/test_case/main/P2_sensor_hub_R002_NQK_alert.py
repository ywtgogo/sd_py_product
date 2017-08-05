from test_lib import *


def uplink_R002_Nack_query_alert():
	alert_ts = int(time.time())
	unalert_ts = alert_ts + 210
	hb_valid_ts = alert_ts + 90
	unalert_occur = 0
	hb_occur = 0
	child.result = "pending"
	honsole.log("thread start")
	if "matched" == honsole.corres(pattern = ["## uploaded ## did = %s,sid = %s,type = 10" % (honsole.id,honsole.child_id[0])],tot = 90):
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
							if math.fabs(unalert_ts - get_ts) > 30:
								honsole.close("time stamp diveation excceed 30s")
								sonsole.close("%s %s" % (test_item,RST[1]))
								os._exit(1)
							else:
								honsole.log("unalert event matched")
								unalert_occur = 1
								child.result = 0

					elif event_type == UL_INFO:

						if hb_occur == 0:

							if get_ts < hb_valid_ts:
								honsole.close("hb uploaded before valid ts: valid ts:%s occur ts:%s" % (hb_valid_ts,get_ts))
								sonsole.close("%s %s" % (test_item,RST[1]))
								os._exit(1)
							else:
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







def downlink_R002_Nack_query_alert():
	sonsole.corres(cmd = "reply manual query")
	sonsole.corres(cmd = "info")
	start = int(sonsole.get_value(ls = ["query_count = (\d*)\r\n"])[0])
	sonsole.corres(cmd = "set alarm")
	
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["alarm_status = 1"],tot = 1):
		honsole.close()
		sonsole.close("console error")
		os._exit(1)

	time.sleep(90)
	sonsole.corres(cmd = "info")
	end = int(sonsole.get_value(ls = ["query_count = (\d*)\r\n"])[0])
	count = end - start
##check result1
	sonsole.log("check query count")
	if count > 8 or count < 5:
		sonsole.log("%d query in 1min" % count)
		return 1

	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["err_seq_cnt = 0"],tot = 1):
		sonsole.log("Warning: seq error: not increasing")

##result 1 pass
	sonsole.corres(cmd = "reply auto query")
	time.sleep(120)
	sonsole.log("force disalarm")
	sonsole.corres(cmd = "set disalarm")
	time.sleep(20)
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["alarm_status = 0","alarm_sent = 0"],tot = 1):
		sonsole.log("not back to normal")
		return 1
#check seq increasingly
	sonsole.log("check seq increasingly")
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["err_seq_cnt = 0"]):
		sonsole.log("Warning: seq error: not increasing")
	

	return 0

if __name__=="__main__":
	honsole = SL_console("homebox")
	sonsole = SL_console("sensor")

	child = SL_thread(uplink_R002_Nack_query_alert)
	sonsole.log("start test")
	child.start()
	result = 1 if downlink_R002_Nack_query_alert() or child.result else 0
	sonsole.close("R002_Nack_query_alert %s" % RST[result])
	honsole.close()
	os._exit(result)
