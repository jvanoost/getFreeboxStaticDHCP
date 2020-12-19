from utils import *
##############################################
##############################################

s = mksession()

# get all Datas from the freebox
datas = getAllStaticIp(s)

# save data in a json file
saveJsonToFile("staticDHCP", datas)


#test add a static IP
res = addStaticIp(s, "96:C6:30:58:B2:80", "192.168.1.3", "RedMiNote9Pro-Lu")