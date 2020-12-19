from utils import *
##############################################
##############################################
if is_authorization_granted() is not True:
	print("Nous n'avons pas encore de session enregistrée, approchez vous de votre Freebox pour valider l'enregistrement")
	register()
else:
	print("Notre appli est déjà connue, pas besoin de s'engegistrer")
	token = open(APP_TOKEN_FILE, 'r').read()

s = mksession()

datas = getAllStaticIp(s)
#saveJsonToFile("saticDHCP", datas)


res = addStaticIp(s, "96:C6:30:58:B2:80", "192.168.1.3", "RedMiNote9Pro-Lu")
fancy_print(res)
