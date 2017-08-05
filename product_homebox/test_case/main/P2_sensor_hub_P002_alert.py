from test_lib import *


for i in range(1,51):
	alert_performance = SL_subtest("P1_sensor_hub_F002_alert",arg = [logging_path+"/subtest/"+"%s" % i,cfg.label])
	alert_performance.log("start test")
	result = ""
	result = alert_performance.get_subtest_result(tot = 300)
	if alert_performance.stop() != True:
		alert_performance.log("zombie spawn:spawn can not be closed or terminated")
		os._exit(1)

	if result == "P1_sensor_hub_F002_alert pass":
		alert_performance.log("%s pass" % i)
	else:
		alert_performance.log("%s fail" % i)
		alert_performance.log("matched :%s" % result)
		alert_performance.close("%s %s" % (test_item,RST[1]))
		time.sleep(5)
		homebox_prepare_next_test()


alert_performance.close("%s %s" % (test_item,RST[0]))
os._exit(0)

