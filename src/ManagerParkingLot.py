class ManagerParkingLot:
    def __init__(self, lotid, name, occupiedspots, totalSpots, rate, overtimerate, pastmonthrevenue):
        self.lotid = lotid
        self.name = name
        self.occupiedSpots = occupiedspots
        self.totalspots = totalSpots
        self.rate = rate
        self.overtimeRate = overtimerate
        self.pastmonthrevenue = pastmonthrevenue

    # return lot id
    def getlotID(self):
        return self.lotid

    # return lot name
    def getName(self):
        return self.name

    # return current rate
    def getRate(self):
        return self.rate

    # return current overtime rate
    def getOvertimeRate(self):
        return self.overtimeRate

    # return past month revenue
    def getPastMonthRevenue(self):
        return self.pastmonthrevenue

    # return current occupancy percentage
    def getOccupancyRate(self):
        return (self.occupiedSpots / (self.totalspots * 1.0)) * 100

