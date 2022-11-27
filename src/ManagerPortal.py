from dotenv import load_dotenv
import MySQLdb
import os
from ManagerParkingLot import *

class ManagerPortal:
    db = None
    connection = None
    parkingLots = dict()

    def __init__(self, dbhost, dbname, dbuser, dbpswd):
        self.db = MySQLdb.connect(host=dbhost,db=dbname,user=dbuser, passwd=dbpswd )
        self.connection = self.db.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        if self.connection:
            self.connection.close()
        if self.db:
            self.db.close()

    def updateLotList(self):
        sql = " \
SELECT \
    parkinglot.id, \
    name, \
    numfloors * numspaces totalspaces, \
    ( \
    SELECT \
        COUNT(*) \
    FROM \
        userticket \
    WHERE \
        userticket.validityEnd IS NULL AND userticket.lotid = parkinglot.id \
) occupiedspots, \
rates.rate, \
rates.overtimerate \
FROM \
    parkinglot \
JOIN rates WHERE parkinglot.id = rates.lotid AND rates.expirydate IS NULL"
        result = self.connection.execute(sql)
        for lot in self.connection.fetchall():
            self.parkingLots[lot['name']] = ManagerParkingLot(lot['id'],lot['name'],lot['occupiedspots'],lot['totalspaces'],lot['rate'],lot['overtimerate'])

    def setRate(self, name,rate):
        lotid = self.parkingLots[name].getlotID()
        overtimeRate = self.parkingLots[name].getRate()
        updateOldRate = f"UPDATE rates SET expirydate=NOW() WHERE lotid='{lotid}'"
        insertNewRate = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{lotid}', '{rate}', '{overtimeRate}')"
        self.connection.execute(updateOldRate)
        self.connection.execute(insertNewRate)
        self.db.commit()

    def setOvertimeRate(self, name,overtimerate):
        lotid = self.parkingLots[name].getlotID()
        rate = self.parkingLots[name].getRate()
        updateOldRate = f"UPDATE rates SET expirydate=NOW() WHERE lotid='{lotid}'"
        insertNewRate = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{lotid}', '{rate}', '{overtimerate}')"
        self.connection.execute(updateOldRate)
        self.connection.execute(insertNewRate)
        self.db.commit()
    
    def setBothRate(self,name,rate,overtimerate):
        lotid = self.parkingLots[name].getlotID()
        updateOldRate = f"UPDATE rates SET expirydate=NOW() WHERE lotid='{lotid}'"
        insertNewRate = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{lotid}', '{rate}', '{overtimerate}')"
        self.connection.execute(updateOldRate)
        self.connection.execute(insertNewRate)
        self.db.commit()

    def getOccupancy(self,name):
        self.updateLotList()
        return self.parkingLots[name].getOccupancyRate()

    def getRate(self,name):
        self.updateLotList()
        return self.parkingLots[name].getRate()

    def getOvertimeRate(self,name):
        self.updateLotList()
        return self.parkingLots[name].getOvertimeRate()

    def getLots(self):
        self.updateLotList()
        return list(self.parkingLots.keys())

    def createNewLot(self,name,floors,spaceperfloor,standardrate,overtimerate):
        createlotsql = f"INSERT INTO parkinglot (name,numfloors,numspaces) VALUES ('{name}','{floors}','{spaceperfloor}')"
        self.connection.execute(createlotsql)
        setratesql = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{self.connection.lastrowid}','{standardrate}','{overtimerate}')"
        self.connection.execute(setratesql)
        self.db.commit()