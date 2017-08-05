from test_lib import *


def uplink_R001_Nack_query():
	child.result = "pending"
	honsole.log("thread start")
	if "matched" == honsole.corres(pattern = ["## uploaded ## did = %s,sid = %s" % (honsole.id,honsole.child_id[0])],tot = 3600):
		ret = honsole.get_value(ls = ["type = (\d*),","occur_ts = (\d*)\r\n"])
		event_type = int(ret[0])
		get_ts = int(ret[1])
		honsole.log("event type:%s occur ts:%s" % (event_type,get_ts))
		honsole.close("unexpected upload event detected")
		sonsole.close("%s %s" % (test_item,RST[1]))
		os._exit(1)
	else:
		honsole.log("stage 1 complete,start normal test -- F001_heartbeat")
		child.result = 0




def downlink_R001_Nack_query():
	sonsole.corres(cmd = "reply manual query")
	sonsole.corres(cmd = "info")
	start = int(sonsole.get_value(ls = ["query_count = (\d*)\r\n"])[0])
	time.sleep(3600)
	sonsole.corres(cmd = "info")
	end = int(sonsole.get_value(ls = ["query_count = (\d*)\r\n"])[0])
	count = end - start
##check query count
	sonsole.log("check:query count")
	if count > 8 or count < 5:
		sonsole.log("%d query in 1h" % count)
		return 1

##check seq
	sonsole.log("check:seq increasingly")
	if "unmatched" == sonsole.corres(cmd = "info",pattern = ["err_seq_cnt = 0"],tot = 1):
		sonsole.log("Warning: seq error: not increasing")
##result 1 pass
	sonsole.corres(cmd = "reply auto query")

	return 0

if __name__=="__main__":
	honsole = SL_console("homebox")
	sonsole = SL_console("sensor")

	child = SL_thread(uplink_R001_Nack_query)
	sonsole.log("start test")
	child.start()
	result = 1 if downlink_R001_Nack_query() or child.result else 0
	if result != 0:
		honsole.close()
		sonsole.close("%s %s" % (test_item,RST[result]))
		os._exit(result)

	next_test = SL_subtest("P2_sensor_hub_F001_heartbeat")
	mid_str = next_test.get_subtest_result(tot = 3660)
	next_test.log("subtest result:%s" % mid_str)
	if mid_str == "P2_sensor_hub_F001_heartbeat pass":
		result = 0
	else:
		result = 1
	sonsole.close("%s %s" % (test_item,RST[result]))
	honsole.close()
	os._exit(result)

