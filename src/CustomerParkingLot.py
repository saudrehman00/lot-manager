class CustomerParkingLot:
    def __init__(self, lotid, name, numfloors, numspaces):
        self.lotid = lotid
        self.name = name
        self.numfloors = numfloors
        self.numspaces = numspaces
    
    def getlotID(self):
        return self.lotid
    
    def getName(self):
        return self.name

    def __str__(self):
        pass