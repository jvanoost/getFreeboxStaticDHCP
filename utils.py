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

import config

token=''
id = ''

def fancy_print(data):
	print(json.dumps(data,indent=2,separators=(',', ': ')))

def connexion_post(method,data=None, session=None):
	url = config.FBX_URL + method
	if data: 
		data = json.dumps(data)
		if session is None:
			return json.loads(requests.post(url, data=data).text)
		else:
			return json.loads(session.post(url, data=data).text)

def connexion_get(method, session=None):
	url = config.FBX_URL + method
	print("Session:", session)
	if session is None:
		return json.loads(requests.get(url).text)
	else:
		return json.loads(session.get(url).text)



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


