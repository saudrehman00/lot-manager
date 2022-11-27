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
SELECT parkinglot.id, \
       parkinglot.name, \
       parkinglot.numfloors * parkinglot.numspaces \
       totalspaces, \
       (SELECT Count(*) \
        FROM   userticket \
        WHERE  userticket.validityend IS NULL \
               AND userticket.lotid = parkinglot.id) \
       occupiedspots, \
       r2.rate, \
       r2.overtimerate, \
       SUM(( Time_to_sec(userticket.paidtime) / 3600 ) * r1.rate + \
               IF( \
               Timestampdiff(second, userticket.validitystart, IF( \
               userticket.validityend IS NULL, Now(), userticket.validityend)) > \
               Time_to_sec(userticket.paidtime), \
               Timestampdiff(second, \
               userticket.validitystart, IF( \
               userticket.validityend IS NULL, Now(), \
               userticket.validityend)) / 3600 * \
               r1.overtimerate, 0)) revenuegenerated \
FROM   userticket \
       join parkinglot \
         ON userticket.lotid = parkinglot.id \
       join rates r1 \
         ON userticket.lotid = r1.lotid \
            AND userticket.validitystart BETWEEN \
                r1.effective AND IF( \
                r1.expirydate IS NULL, Now( \
                                 ), r1.expirydate) \
       join rates r2 \
         ON parkinglot.id = r2.lotid \
            AND r2.expirydate IS NULL \
WHERE userticket.validitystart > DATE_SUB(NOW(), INTERVAL 1 MONTH) \
GROUP  BY parkinglot.id, \
          parkinglot.name, \
          parkinglot.numfloors * parkinglot.numspaces, \
          (SELECT Count(*) \
           FROM   userticket \
           WHERE  userticket.validityend IS NULL \
                  AND userticket.lotid = parkinglot.id), \
          r2.rate, \
          r2.overtimerate"
        result = self.connection.execute(sql)
        for lot in self.connection.fetchall():
            self.parkingLots[lot['name']] = ManagerParkingLot(lot['id'],lot['name'],lot['occupiedspots'],lot['totalspaces'],lot['rate'],lot['overtimerate'],lot['revenuegenerated'])

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

    def getRevenueGenerated(self,name):
        self.updateLotList()
        return self.parkingLots[name].getPastMonthRevenue()

    def getLots(self):
        self.updateLotList()
        return list(self.parkingLots.keys())

    def createNewLot(self,name,floors,spaceperfloor,standardrate,overtimerate):
        createlotsql = f"INSERT INTO parkinglot (name,numfloors,numspaces) VALUES ('{name}','{floors}','{spaceperfloor}')"
        self.connection.execute(createlotsql)
        setratesql = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{self.connection.lastrowid}','{standardrate}','{overtimerate}')"
        self.connection.execute(setratesql)
        self.db.commit()