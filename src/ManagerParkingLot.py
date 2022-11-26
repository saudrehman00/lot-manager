class ManagerParkingLot:
    def __init__(self, lotid, name,occupiedSpots,totalSpots):
        self.lotid = lotid
        self.name = name
        self.occupiedSpots =occupiedSpots
        self.totalspots = totalSpots
    
    def getlotID(self):
        return self.lotid
    
    def getName(self):
        return self.name

    def __str__(self):
        pass

