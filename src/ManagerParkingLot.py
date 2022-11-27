class ManagerParkingLot:
    def __init__(self, lotid, name,occupiedspots,totalSpots,rate,overtimerate,pastmonthrevenue):
        self.lotid = lotid
        self.name = name
        self.occupiedSpots =occupiedspots
        self.totalspots = totalSpots
        self.rate = rate
        self.overtimeRate = overtimerate
        self.pastmonthrevenue = pastmonthrevenue
    
    def getlotID(self):
        return self.lotid
    
    def getName(self):
        return self.name

    def getRate(self):
        return self.rate

    def getOvertimeRate(self):
        return self.overtimeRate

    def getPastMonthRevenue(self):
        return self.pastmonthrevenue

    def getOccupancyRate(self):
        return (self.occupiedSpots / (self.totalspots * 1.0)) * 100
    
    # def __str__(self):
    #     return f""

