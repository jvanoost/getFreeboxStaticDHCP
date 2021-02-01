import cDeviceDHCP

class cFreebox:

    listDevices = []

    def __init__(self):
        pass

    def addDeviceDHCP(self, name, macAddress, ipAddress, comm, typeDevice):

        listDevices.append(cDeviceDHCP(name, macAddress, ipAddress, comm, typeDevice))

    def saveConfigDHCP(self):
        pass