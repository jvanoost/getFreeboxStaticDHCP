import utils

class cDeviceDHCP:

    name = ''
    macAddress = ''
    ipAddress = ''
    comm = ''
    typeDevice = ''

    def __init__(self, name, macAddress, ipAddress, comm, typeDevice):

        self.name = name
        self.macAddress = macAddress
        self.ipAddress = ipAddress
        self.comm = comm
        self.typeDevice = typeDevice

    def addStaticIp(self, session):
        data ={
            "ip": self.ipAddress,
            "mac": self.macAddress,
            "comment": self.comm
        }
        content = utils.connexion_post("dhcp/static_lease/", data, session)
        if content["success"] is True:
            return content["result"]
        else:
            print('Erreur ajout de bail statique')
            print(content["msg"])
            return False