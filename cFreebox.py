import utils
import config
from cDeviceDHCP import *

import time
import requests
import json
import hmac
import hashlib
from datetime import datetime

class cFreebox:

    listDevices = []
    token = ''
    session = requests.session()

    def __init__(self):
        self.listDevices = []
        if self.is_authorization_granted() is not True:
            print("Nous n'avons pas encore de session enregistrée, approchez vous de votre Freebox pour valider l'enregistrement")
            self.register(config.app_id, config.app_id, config.app_name, config.app_version, config.device_name)
        else:
            print("Notre appli est déjà connue, pas besoin de s'engegistrer")
            self.token = config.APP_TOKEN
        if config.DEBUG == True : print("token : ", self.token)
        self.mksession()

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
            if config.DEBUG == True : print("Login 1/2 Ok")
        else:
            if config.DEBUG == True : print('Login 1/2 NOK')
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
        if config.DEBUG == True : utils.fancy_print(content)
        if content["success"] is True:
            if config.DEBUG == True : print("Login 2/2 Ok")
        else:
            if config.DEBUG == True : print('Login 2/2 NOK')
            return False
        s.headers = {"X-Fbx-App-Auth": content["result"]["session_token"]}
        self.session = s
        return s
    
    ###################################################################################    
    ###################################################################################    
    def getAllStaticIp(self):
        content = utils.connexion_get("dhcp/static_lease/", session = self.session)
        
        #fancy_print(content)
        if content["success"] is True:
            # Save to a json file
            now = datetime.now()
            utils.saveJsonToFile("datas/dhcp-" + now.strftime("%Y%m%d%H%M%S"), content["result"])

            return content["result"]
        else:
            print('Erreur récupération baux statiques')
            #debug
            if config.DEBUG == True : utils.fancy_print(content)

            return False

        return content

    def addDeviceDHCP(self, name, macAddress, ipAddress, comm, typeDevice):

        self.listDevices.append(cDeviceDHCP(name, macAddress, ipAddress, comm, typeDevice))
        self.listDevices[-1].addStaticIp(self.session)

    def pushConfigDHCP(self, fileToLoad):
        """Load a DHCP config saved before to the Freebox"""

        with open(fileToLoad, 'r') as datas:
            datas_dict = json.load(datas)
            
            for device in datas_dict["result"]:
                self.addDeviceDHCP(device['hostname'], device['mac'], device['ip'], device['comment'], '')

    ###################################################################################    
    ###################################################################################    
    def getAllPortForwarding(self):
        content = utils.connexion_get("fw/redir/", session = self.session)
        
        #fancy_print(content)
        if content["success"] is True:
            # Save to a json file
            now = datetime.now()
            if content['result']:
                utils.saveJsonToFile("datas/portForwarding-" + now.strftime("%Y%m%d%H%M%S"), content["result"])
            else:
                print("Pas de résultats")

            return content["result"]
        else:
            print('Erreur récupération ports forwarding')
            #debug
            if config.DEBUG == True : utils.fancy_print(content)

            return False

        return content

    def pushPortForwarding(self, fileToLoad):
        """Load a Port forwarding config saved before to the Freebox"""

        with open(fileToLoad, 'r') as datas:
            datas_dict = json.load(datas)
            
            for fw in datas_dict["result"]:
                data ={
                    "enabled": fw['enabled'],
                    "comment": fw['comment'],
                    "lan_port": fw['lan_port'],
                    "wan_port_end":fw['wan_port_end'],
                    "wan_port_start":fw['wan_port_start'],
                    "lan_ip":fw['lan_ip'],
                    "ip_proto":fw['ip_proto'],
                    "src_ip":fw['src_ip']
                }
                content = utils.connexion_post("fw/redir/", data, self.session)
                if content["success"] is True:
                    return content["result"]
                else:
                    print('Erreur ajout de bail statique')
                    print(content["msg"])
                    return False

    ###################################################################################    
    ###################################################################################    
    def getAllWifiGuest(self):
        content = utils.connexion_get("wifi/custom_key/", session = self.session)
        
        #fancy_print(content)
        if content["success"] is True:
            # Save to a json file
            now = datetime.now()
            if content['result']:
                utils.saveJsonToFile("datas/WifiGuest-" + now.strftime("%Y%m%d%H%M%S"), content["result"])
            else:
                print("Pas de résultats")

            return content["result"]
        else:
            print('Erreur récupération wifi guest')
            #debug
            if config.DEBUG == True : utils.fancy_print(content)

            return False

        return content
    
    def pushWifiGuest(self, fileToLoad):
        """Load a wifi guest config saved before to the Freebox"""

        with open(fileToLoad, 'r') as datas:
            datas_dict = json.load(datas)
            
            for fw in datas_dict["result"]:
                data ={
                    "description": fw['params']['description'],
                    "key": fw['params']['key'],
                    "max_use_count": fw['params']['max_use_count'],
                    "duration":fw['remaining'],
                    "access_type":fw['params']['access_type']
                }
                content = utils.connexion_post("wifi/custom_key/", data, self.session)
                if content["success"] is True:
                    return content["result"]
                else:
                    print('Erreur ajout de wifi guest')
                    print(content["msg"])
                    return False
    
    ###################################################################################    
    ###################################################################################    
    def getAllMacFilter(self):
        content = utils.connexion_get("wifi/mac_filter/", session = self.session)
        
        #fancy_print(content)
        if content["success"] is True:
            # Save to a json file
            now = datetime.now()
            if content["result"]:
                utils.saveJsonToFile("datas/MacFilter-" + now.strftime("%Y%m%d%H%M%S"), content["result"])
            else:
                print("Pas de résultats")

            return content["result"]
        else:
            print('Erreur récupération mac filter')
            #debug
            if config.DEBUG == True : utils.fancy_print(content)

            return False

        return content
    
    def pushMacFilter(self, fileToLoad):
        """Load a mac filter config saved before to the Freebox"""

        with open(fileToLoad, 'r') as datas:
            datas_dict = json.load(datas)
            
            for fw in datas_dict["result"]:
                data ={
                    "mac" : fw['mac'],
                    "type" : fw['type'],
                    "comment" : fw['comment'],
                    "hostname" : fw['hostname'],
                    "id" : fw['id']
                }
                content = utils.connexion_post("wifi/customkey/", data, self.session)
                if content["success"] is True:
                    return content["result"]
                else:
                    print('Erreur ajout de mac filter')
                    print(content["msg"])
                    return False