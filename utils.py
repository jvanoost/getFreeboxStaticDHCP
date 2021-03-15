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
	if config.DEBUG == True : print("Session:", session)
	if session is None:
		return json.loads(requests.get(url).text)
	else:
		return json.loads(session.get(url).text)

def saveJsonToFile(fileName, data):
	datas = json.dumps(data)
	open("{}.json".format(fileName), 'w').write(datas)
	print("Fichier sauvegardé dans {}.json".format(fileName))

############################################
############################################


