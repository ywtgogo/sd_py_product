############################ global define ################################

DEV_TYPE = {"SLHBE101":"01000001",
	"SLHBE102":"01000002"}


DEV_MANU = {"OCTO":"01"}

DEV_RANUM = "666666"

'''
http://officelinux.vicp.net:15560/fota/img-source   TEST

http://officelinux.vicp.net:28080/fota/img-source   DEV

http://device.sandlacus.com/fota/img-source  UAT
'''

total_url = "http://test1.sandlacus.com:15560/fota/img-source##/HomeBox/HomeBox/"
sensor_img_url = "http://officelinux.vicp.net:15560/fota/img-source##/Sensor"
################################# END #####################################



######################## internal configuration class #####################
class id_tuple:
	long_homebox = None
	homebox = None
	long_sensor = None
	sensor = None
	sensor_fota_url_prefix = None


class uplink_env:
	# ver_num indicate the dynamic version number of the image version while in FOTA
	ver_num = None
	# type_num indicate the static version number to sperate 2G HW ver from WIFI HW ver
	type_num = None
	img_fota_url = ""
	sensor_fota_url = None
	sensor_fota_url_prefix = None
	key = 'SandlacusData#@1SandlacusData#@1'
	upd_device_type = None
################################# END #####################################




######################## configuration class ##############################
class SL_config:
	def __init__(self,label):
		self.label = label
		self.alias = None
		self.id = id_tuple()
		self.serial = None
		self.upenv = uplink_env()

################################# END #####################################






######################## configuration list ###############################
config_list = {"FIBCOM":["2g"],
				"FIBCOM_WEEKLY_RELEASE":["2g#"],
				"WIFI":["wifi"],
				"WIFI_WEEKLY_RELEASE":["wifi#"],
				"DEFAULT":["default","df"]
		}
		
################################# END #####################################

for i in config_list.keys():
	exec("%s = SL_config('%s')" % (i,i))


## for remo 2g production
FIBCOM.id.homebox = "00AFAFAF"
FIBCOM.id.sensor = {

					"fake_water":"303F3F3F",
					"fake_smoke":"202F2F2F",
					"fake_pir":"404F4F4F",
					"fake_mag":"505F5F5F",
					"Water":"30020214",
					"Smoke":"2002089D",
					"PIR":"40040260",
					"Magnetic":"50020014"
						}


FIBCOM.id.long_homebox = DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+FIBCOM.id.homebox
FIBCOM.id.long_sensor = {i:DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+FIBCOM.id.sensor[i] for i in FIBCOM.id.sensor.keys()}
FIBCOM.alias = "m1"
FIBCOM.serial = "group1"
FIBCOM.upenv.ver_num = 1
FIBCOM.upenv.type_num = 0
FIBCOM.upenv.sensor_fota_url_prefix = {
					"Water":"Water/SLWSO219",
					"Smoke":"Smoke/SLSSO219",
					"PIR":"PIR/SLPSO219",
					"Magnetic":"Magnetic/SLMSO219"
}

#"http://officelinux.vicp.net:15560/fota/img-source##/HomeBox/HomeBox/M1/img/"
FIBCOM.upenv.img_fota_url = "%sM1/img/"  %total_url
FIBCOM.upenv.sensor_fota_url ={i:"%s/%s/img/" %(sensor_img_url,FIBCOM.upenv.sensor_fota_url_prefix[i]) for i in FIBCOM.upenv.sensor_fota_url_prefix.keys()}
FIBCOM.upenv.upd_device_type = DEV_TYPE["SLHBE101"]





## for remo 2g weekly release
FIBCOM_WEEKLY_RELEASE.id.homebox = "00AEAEAE"
FIBCOM_WEEKLY_RELEASE.id.sensor = {
									"fake_water":"303E3E3E",
									"fake_smoke":"202E2E2E",
									"fake_pir":"404E4E4E",
									"fake_mag":"505E5E5E",
									"Water":"30020214",
									"Smoke":"2002089D",
									"PIR":"40040260",
									"Magnetic":"50020014"}


FIBCOM_WEEKLY_RELEASE.id.long_homebox = DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+FIBCOM_WEEKLY_RELEASE.id.homebox
FIBCOM_WEEKLY_RELEASE.id.long_sensor = {i:DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+FIBCOM_WEEKLY_RELEASE.id.sensor[i] for i in FIBCOM_WEEKLY_RELEASE.id.sensor.keys()}
FIBCOM_WEEKLY_RELEASE.alias = "m1"
FIBCOM_WEEKLY_RELEASE.serial = "group1"
FIBCOM_WEEKLY_RELEASE.upenv.ver_num = 1
FIBCOM_WEEKLY_RELEASE.upenv.type_num = 0
FIBCOM_WEEKLY_RELEASE.upenv.sensor_fota_url_prefix = {
					"Water":"Water/SLWSO219",
					"Smoke":"Smoke/SLSSO219",
					"PIR":"PIR/SLPSO219",
					"Magnetic":"Magnetic/SLMSO219"
}
FIBCOM_WEEKLY_RELEASE.upenv.img_fota_url = "%sM1/img/"  %total_url
#"http://officelinux.vicp.net:15560/fota/img-source##/HomeBox/HomeBox/M1/img/"
FIBCOM_WEEKLY_RELEASE.upenv.sensor_fota_url ={i:"%s/%s/img/" %(sensor_img_url,FIBCOM_WEEKLY_RELEASE.upenv.sensor_fota_url_prefix[i]) for i in FIBCOM_WEEKLY_RELEASE.upenv.sensor_fota_url_prefix.keys()}
FIBCOM_WEEKLY_RELEASE.upenv.upd_device_type = DEV_TYPE["SLHBE101"]





## for wifi produciton
WIFI.id.homebox = "00ADADAD"
WIFI.id.sensor = {
				"fake_water":"303D3D3D",
				"fake_smoke":"202D2D2D",
				"fake_pir":"404D4D4D",
				"fake_mag":"505D5D5D",
				"Water":"30020214",
				"Smoke":"2002089D",
				"PIR":"40040260",
				"Magnetic":"50020014"
				}


WIFI.id.long_homebox = DEV_MANU["OCTO"]+DEV_TYPE["SLHBE102"]+DEV_RANUM+WIFI.id.homebox
WIFI.id.long_sensor = {i:DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+WIFI.id.sensor[i] for i in WIFI.id.sensor.keys()}
WIFI.alias = "m2"
WIFI.serial = "group2"
WIFI.upenv.ver_num = 1
WIFI.upenv.type_num = 0
WIFI.upenv.sensor_fota_url_prefix = {
					"Water":"Water/SLWSO219",
					"Smoke":"Smoke/SLSSO219",
					"PIR":"PIR/SLPSO219",
					"Magnetic":"Magnetic/SLMSO219"
}
#"http://officelinux.vicp.net:15560/fota/img-source##/HomeBox/HomeBox/M2/img/"
WIFI.upenv.img_fota_url = "%sSLHBE102/img/"  %total_url
WIFI.upenv.sensor_fota_url ={i:"%s/%s/img/" %(sensor_img_url,WIFI.upenv.sensor_fota_url_prefix[i]) for i in WIFI.upenv.sensor_fota_url_prefix.keys()}
WIFI.upenv.upd_device_type = DEV_TYPE["SLHBE102"]





## for wifi weekly release
WIFI_WEEKLY_RELEASE.id.homebox = "00ACACAC"
WIFI_WEEKLY_RELEASE.id.sensor = {
								"fake_water":"303C3C3C",
								"fake_smoke":"202C2C2C",
								"fake_pir":"404C4C4C",
								"fake_mag":"505C5C5C",
								"Water":"30020214",
								"Smoke":"2002089D",
								"PIR":"40040260",
								"Magnetic":"50020014"
									}

WIFI_WEEKLY_RELEASE.id.long_homebox = DEV_MANU["OCTO"]+DEV_TYPE["SLHBE102"]+DEV_RANUM+WIFI_WEEKLY_RELEASE.id.homebox
WIFI_WEEKLY_RELEASE.id.long_sensor = {i:DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+WIFI_WEEKLY_RELEASE.id.sensor[i] for i in WIFI_WEEKLY_RELEASE.id.sensor.keys()}
WIFI_WEEKLY_RELEASE.alias = "m2"
WIFI_WEEKLY_RELEASE.serial = "group2"
WIFI_WEEKLY_RELEASE.upenv.ver_num = 1
WIFI_WEEKLY_RELEASE.upenv.type_num = 0
WIFI_WEEKLY_RELEASE.upenv.sensor_fota_url_prefix = {
					"Water":"Water/SLWSO219",
					"Smoke":"Smoke/SLSSO219",
					"PIR":"PIR/SLPSO219",
					"Magnetic":"Magnetic/SLMSO219"
}
#"http://officelinux.vicp.net:15560/fota/img-source##/HomeBox/HomeBox/M2/img/"
WIFI_WEEKLY_RELEASE.upenv.img_fota_url = "%sSLHBE102/img/" %total_url
WIFI_WEEKLY_RELEASE.upenv.sensor_fota_url ={i:"%s/%s/img/" %(sensor_img_url,WIFI_WEEKLY_RELEASE.upenv.sensor_fota_url_prefix[i]) for i in WIFI_WEEKLY_RELEASE.upenv.sensor_fota_url_prefix.keys()}
WIFI_WEEKLY_RELEASE.upenv.upd_device_type = DEV_TYPE["SLHBE102"]






## default
DEFAULT.id.homebox = "00A0A0A0"
DEFAULT.id.sensor = {
					"fake_water":"30303030",
					"fake_smoke":"20202020",
					"fake_pir":"40404040",
					"fake_mag":"50505050"}
DEFAULT.id.long_homebox = DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+DEFAULT.id.homebox
DEFAULT.id.long_sensor = {i:DEV_MANU["OCTO"]+DEV_TYPE["SLHBE101"]+DEV_RANUM+DEFAULT.id.sensor[i] for i in DEFAULT.id.sensor.keys()}
DEFAULT.alias = "DEFAULT"
DEFAULT.serial = "group1"
DEFAULT.alias = "m1"
DEFAULT.upenv.ver_num = 1
DEFAULT.upenv.type_num = 0
#"http://officelinux.vicp.net:15560/fota/img-source##/HomeBox/HomeBox/M1/img/"
DEFAULT.upenv.img_fota_url = "%sM1/img/" %total_url
DEFAULT.upenv.upd_device_type = DEV_TYPE["SLHBE101"]



def get_cfg(arg = None):
	found = False
	for i in config_list.keys():
		if arg == i.upper() or arg == i.lower():
			arg = i
			found = True
			break
		else:
			for j in config_list[i]:
				if arg == j.upper() or arg == j.lower():
					arg = i
					found = True
					break
				else:
					continue
			if found == True:
				break
	if found != True:
		arg = "DEFAULT"

	return eval("%s" % arg.upper())

