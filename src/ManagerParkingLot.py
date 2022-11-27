class ManagerParkingLot:
    def __init__(self, lotid, name,occupiedSpots,totalSpots,rate,overtimeRate):
        self.lotid = lotid
        self.name = name
        self.occupiedSpots =occupiedSpots
        self.totalspots = totalSpots
        self.rate = rate
        self.overtimeRate = overtimeRate
    
    def getlotID(self):
        return self.lotid
    
    def getName(self):
        return self.name

    def getRate(self):
        return self.rate

    def getOvertimeRate(self):
        return self.overtimeRate

    def getOccupancyRate(self):
        return (self.occupiedSpots / (self.totalspots * 1.0)) * 100
    
    # def __str__(self):
    #     return f""

