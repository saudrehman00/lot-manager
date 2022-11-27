class CustomerTicket:
    def __init__(self, id, lotid, floor, spacenumber, validitystart, paidtime, validityEnd):
        self.id = id
        self.lotid = lotid
        self.floor = floor
        self.spacenumber = spacenumber
        self.validitystart = validitystart
        self.validityEnd = validityEnd
    
    def getlotID(self):
        return self.lotid
    
    def getFloor(self):
        return self.floor

    def __str__(self):
        pass