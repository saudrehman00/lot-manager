# Module Imports
import mariadb
import MySQLdb
import sys
from datetime import datetime


# Sample class with init method
class UserTicket:
    # global ticketId
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
            self.conn = MySQLdb.connect(
                user="schooladmin",
                password="HG7PqjbKCWRgeKE",
                host="4471-final.mariadb.database.azure.com",
                port=3306,
                database="lotmanager"
        )
        except MySQLdb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.cur = self.conn.cursor()
        print(self.lotid)
        
        print(self.cur.execute("INSERT INTO userticket (lotid, floor, spacenumber, validitystart, paidtime, validityEnd) VALUES (%s,%s,%s,%s,%s,%s)",
            (self.lotid, self.floor, self.spacenumber, self.startime, self.paidtime, self.endtime)))
        self.conn.commit()

    def updatePaidTime(self, addedPaidTime):
        # self.endtime = self.endtime.replace(self.endtime.hour + addedPaidTime)
        currentEndTime = datetime.strptime(self.endtime, '%Y-%m-%d %H:%M:%S')
        newHour = currentEndTime.hour + addedPaidTime
        self.endtime = currentEndTime.replace(hour=newHour).strftime('%Y-%m-%d %H:%M:%S')

        currentPaidTime = datetime.strptime(self.paidtime, '%H:%M:%S')
        # newPaidTime = currentPaidTime.hour + addedPaidTime
        newPaidTime = datetime.now().time().replace(hour = newHour,minute = 0,second = 0).strftime('%H:%M:%S')
        # newPaidTime = datetime.now().time().replace(hour=datetime.now().time().hour + addedPaidTime,minute=0,second=0).strftime('%H:%M:%S')

        print(f"UPDATE userticket SET paidtime = {newPaidTime} WHERE id = {self.id}")
        print(f"UPDATE userticket SET validityEnd={self.endtime} WHERE id = {self.id}")
        self.cur.execute(f"UPDATE userticket SET paidtime = '{newPaidTime}' WHERE id = {self.id}")
        self.cur.execute(f"UPDATE userticket SET validityEnd='{self.endtime}' WHERE id = {self.id}")
        self.conn.commit()

    # def createTicket(self, floor, spot):
    #     if self.validateParkingSpot():
    #         self.cur.execute(
    #             "INSERT INTO userticket VALUES (2,%s,1,%s,%s,%s,%s)",
    #             (self.lotid, self.startime, self.paidtime, self.endtime))
    #         self.conn.commit()
    #         return True
    #     else:
    #         print("Spot Already Taken")
    #         return False

    def deleteTicket(self):
        self.cur.execute(
            "DELETE FROM userticket WHERE id = %s)",
            self.id)
        self.conn.commit()
        return True



