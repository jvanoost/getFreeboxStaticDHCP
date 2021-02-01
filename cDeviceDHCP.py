
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