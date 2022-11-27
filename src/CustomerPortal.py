import sys
from datetime import datetime
from CustomerParkingLot import CustomerParkingLot
from CustomerTicket import CustomerTicket
import MySQLdb
import time
from datetime import datetime, timedelta
import os

class CustomerPortal:
    db = None
    connection = None
    parkingLots = dict()

    def __init__(self, dbhost, dbname, dbuser, dbpswd):
        self.db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser, passwd=dbpswd )
        self.connection = self.db.cursor(MySQLdb.cursors.DictCursor)

    def getLotData(self,name):
        sql = ""
        self.connection.execute("SELECT * FROM parkinglot where name = \"" + name + "\"")
        return self.connection.fetchone()
        
    
    def createParkingLot(self, lotData):
        id = lotData["id"]
        name = lotData["name"]
        numfloors = lotData["numfloors"]
        numspaces = lotData["numspaces"]
        return CustomerParkingLot(id, name, numfloors, numspaces)
    
    def createCustomerTicket(self, id, lotid, floor, spacenumber, timeAdded):
        timestamp = datetime.now()
        self.connection.execute("INSERT INTO userticket VALUES (%s,%s,%s,%s,%s,%s,%s)", (id, lotid, floor, spacenumber, timestamp, timeAdded, timestamp + timedelta(hours=timeAdded)))
        return CustomerTicket(id, lotid, floor, spacenumber, timestamp, timeAdded, timestamp + timeAdded)





def main():    
    portal = CustomerPortal("localhost", "lotmanager", "root", "password")

    lot = portal.createParkingLot(portal.getLotData("Western Parking"))


main()