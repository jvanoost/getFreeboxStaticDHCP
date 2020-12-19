import urllib3
import requests
import json
import hmac
import hashlib
import pickle
import time
import datetime
import socket
import os

fbx_url = "http://mafreebox.freebox.fr/api/v8/"

APP_TOKEN_FILE = '.app_token'


token=''
id = ''

app_id = 'fr.freebox.savestaticip'
app_name = 'SaveStaticIp'
app_version = '1'
device_name = socket.gethostname()


def fancy_print(data):
	print(json.dumps(data,indent=2,separators=(',', ': ')))

def connexion_post(method,data=None,session=None):
	url = "http://mafreebox.freebox.fr/api/v8/"+method
	if data: 
		data = json.dumps(data)
		if session is None:
			return json.loads(requests.post(url, data=data).text)
		else:
			return json.loads(session.post(url, data=data).text)

def connexion_get(method,session=None):
	url = "http://mafreebox.freebox.fr/api/v8/"+method
	print("Session:", session)
	if session is None:
		return json.loads(requests.get(url).text)
	else:
		return json.loads(session.get(url).text)

def is_authorization_granted():
	"""
		Return True if an authorization has already been granted on the freebox.
	"""
	return True if os.path.isfile(APP_TOKEN_FILE) else False

def register():
	global token,id, app_id, app_name, app_version, device_name
	print('app_id',app_id)
	payload = {'app_id': app_id, 'app_name': app_name, 'app_version': app_version, 'device_name': device_name}

	content=connexion_post('login/authorize/',payload)

	if (content["success"] is not True):
		return None

	track_id = str(content["result"]["track_id"])

	while True:
		authorization = connexion_get('login/authorize/{}'.format(track_id))
		if not authorization["result"]["status"] == 'pending':
			break
		time.sleep(1)

	if authorization["result"]["status"] == "granted":
		token = str(content["result"]["app_token"])
		fancy_print(content)
		app_id=str(content["result"]["track_id"])

		open(APP_TOKEN_FILE, 'w').write(token)

		return token
	else:
		return None

def mksession():
	global token
	
	s = requests.session()
	content = connexion_get("login/", s)
	#fancy_print(content)
	if content["success"] is True:
		print("Login 1/2 Ok")
	else:
		print('Login 1/2 NOK')
		return False
	challenge = content["result"]["challenge"]
	token_bytes= bytes(token , 'latin-1')

	challenge_bytes = bytes(challenge, 'latin-1')
	password_bin = hmac.new(token_bytes, challenge_bytes, hashlib.sha1)
	password = password_bin.hexdigest()

	data={
		  "app_id": 'fr.freebox.savestaticip',
		   #"app_version":'1',
		"password": password
	}
	
	content = connexion_post("login/session/",data, s)
	fancy_print(content)
	if content["success"] is True:
		print("Login 2/2 Ok")
	else:
		print('Login 2/2 NOK')
		return False
	s.headers = {"X-Fbx-App-Auth": content["result"]["session_token"]}
	return s

def getAllStaticIp(session):
	global token
	content = connexion_get("dhcp/static_lease/", session=session)
	
	#fancy_print(content)
	if content["success"] is True:
		return content["result"]
	else:
		print('Erreur récupération baux statiques')
		return False

	return content

def addStaticIp(session, mac, ip, comment):
	global token
	data ={
		"ip": ip,
		"mac": mac,
		"comment": comment
	}
	content = connexion_post("dhcp/static_lease/",data, session)
	if content["success"] is True:
		return content["result"]
	else:
		print('Erreur ajout de bail statique')
		print(content["msg"])
		return False

def saveJsonToFile(fileName, data):
	open("{}.json".format(fileName), 'w').write(str(data))



############################################
############################################

if is_authorization_granted() is not True:
	print("Nous n'avons pas encore de session enregistrée, approchez vous de votre Freebox pour valider l'enregistrement")
	register()
else:
	print("Notre appli est déjà connue, pas besoin de s'engegistrer")
	token = open(APP_TOKEN_FILE, 'r').read()
