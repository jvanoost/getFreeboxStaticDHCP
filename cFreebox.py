import utils
from cDeviceDHCP import *

import time
import requests
import json
import hmac
import hashlib

class cFreebox:

    listDevices = []
    token = ''
    session = requests.session()

    def __init__(self):
        self.listDevices = []
        if self.is_authorization_granted() is not True:
            print("Nous n'avons pas encore de session enregistrée, approchez vous de votre Freebox pour valider l'enregistrement")
            self.register()
        else:
            print("Notre appli est déjà connue, pas besoin de s'engegistrer")
            self.token = config.APP_TOKEN

    def is_authorization_granted(self):
        """
            Return True if an authorization has already been granted on the freebox.
        """
        return True if config.APP_TOKEN != '' else False

    def register(self, id, app_id, app_name, app_version, device_name):

        payload = {'app_id': app_id, 'app_name': app_name, 'app_version': app_version, 'device_name': device_name}

        content = utils.connexion_post('login/authorize/', payload)

        if (content["success"] is not True):
            return None

        track_id = str(content["result"]["track_id"])

        while True:
            authorization = utils.connexion_get('login/authorize/{}'.format(track_id))
            if not authorization["result"]["status"] == 'pending':
                break
            time.sleep(1)

        if authorization["result"]["status"] == "granted":
            self.token = str(content["result"]["app_token"])
            utils.fancy_print(content)
            app_id=str(content["result"]["track_id"])

            open("config.py", 'w').write("APP_TOKEN='" + self.token + "'")

            return self.token
        else:
            return None

    def mksession(self):
        
        s = requests.session()
        content = utils.connexion_get("login/", s)
        #fancy_print(content)
        if content["success"] is True:
            print("Login 1/2 Ok")
        else:
            print('Login 1/2 NOK')
            return False
        challenge = content["result"]["challenge"]
        token_bytes= bytes(self.token , 'latin-1')

        challenge_bytes = bytes(challenge, 'latin-1')
        password_bin = hmac.new(token_bytes, challenge_bytes, hashlib.sha1)
        password = password_bin.hexdigest()

        data={
            "app_id": 'fr.freebox.savestaticip',
            #"app_version":'1',
            "password": password
        }
        
        content = utils.connexion_post("login/session/",data, s)
        utils.fancy_print(content)
        if content["success"] is True:
            print("Login 2/2 Ok")
        else:
            print('Login 2/2 NOK')
            return False
        s.headers = {"X-Fbx-App-Auth": content["result"]["session_token"]}
        self.session = s
        return s
    
    def getAllStaticIp(self):
        content = utils.connexion_get("dhcp/static_lease/", session = self.session)
        
        #fancy_print(content)
        if content["success"] is True:
            return content["result"]
        else:
            print('Erreur récupération baux statiques')
            return False

        return content

    def addDeviceDHCP(self, name, macAddress, ipAddress, comm, typeDevice):

        self.listDevices.append(cDeviceDHCP(name, macAddress, ipAddress, comm, typeDevice))

    def saveConfigDHCP(self):
        pass