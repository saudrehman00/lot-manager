# Module Imports
import mariadb
import sys
from datetime import datetime


# Sample class with init method
class UserTicket:
 
    # init method or constructor
    def __init__(self, id, lotid, floor, spacenumber, startime, paidtime, endtime):
        self.id = id
        self.lotid = lotid
        self.floor = floor
        self.spacenumber = spacenumber
        self.startime = startime
        self.paidtime = paidtime
        self.endtime = endtime

        try:
            self.conn = mariadb.connect(
                user="root",
                password="password",
                host="localhost",
                port=3306,
                database="lotmanager"
        )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()

    def updatePaidTime(self, addedPaidTime):
        # self.endtime = self.endtime.replace(self.endtime.hour + addedPaidTime)
        currentEndTime = datetime.strptime(self.endtime, '%Y-%m-%d %H:%M:%S')
        newHour = currentEndTime.hour + addedPaidTime
        self.endtime = currentEndTime.replace(hour=newHour).strftime('%Y-%m-%d %H:%M:%S')

        currentPaidTime = datetime.strptime(self.paidtime, '%H:%M:%S')
        newPaidTime = currentPaidTime.hour + addedPaidTime
        self.paidtime = currentPaidTime.replace(hour=newPaidTime).strftime('%H:%M:%S')

        self.cur.execute(
            "UPDATE userticket SET paidtime = %s)",
            (addedPaidTime))
        self.cur.execute(
            "UPDATE userticket SET validyEnd = %s)",
            (self.endtime))
        self.conn.commit()


    def createTicket(self, floor, spot):
        if self.validateParkingSpot():
            self.cur.execute(
                "INSERT INTO userticket VALUES (2,%s,1,%s,%s,%s,%s)",
                (self.lotid, 2, self.startime, self.paidtime, self.endtime))
            self.conn.commit()
            return True
        else:
            print("Spot Already Taken")
            return False


