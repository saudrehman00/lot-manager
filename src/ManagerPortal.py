from hashlib import sha256
import MySQLdb
import os
import sys
from ManagerParkingLot import *


class ManagerPortal:
    db = None
    connection = None
    parkingLots = dict()

    # constructor creates db connection and authenticates manager
    def __init__(self, dbhost,  dbuser, dbpswd, manageruname, managerpswd):
        self.db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpswd)
        self.connection = self.db.cursor(MySQLdb.cursors.DictCursor)
        self.connection.execute("SHOW DATABASES;")
        result = self.connection.fetchall()
        if "lotmanager" in [database['Database'] for database in result]:
            self.connection.execute("USE lotmanager;")
            self.connection.execute(
                f"SELECT fullname, password from manager WHERE username LIKE '{manageruname}'")
            result = self.connection.fetchone()
            if result['password'] == sha256(managerpswd.encode()).hexdigest():
                print(f"HELLO {result['fullname']}")
            else:
                print("login failed")
                sys.exit(1)
        else:
            print("database has not been set up")
            sys.exit(1)

    def __del__(self):
        if self.connection:
            self.connection.close()
        if self.db:
            self.db.close()

    # queries the db to get all parking lot data along with revenue generated in the past month
    def updateLotList(self):
        lotSQL = " \
SELECT parkinglot.id, \
       parkinglot.name, \
       parkinglot.numfloors * parkinglot.numspaces   totalspaces, \
       (SELECT Count(*) \
        FROM   userticket \
        WHERE  userticket.validityend IS NULL \
               AND userticket.lotid = parkinglot.id) occupiedspots, \
       rates.rate, \
       rates.overtimerate \
FROM   parkinglot \
       JOIN rates \
         ON parkinglot.id = rates.lotid"
        sqlBilling = " \
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
        result = self.connection.execute(lotSQL)
        for lot in self.connection.fetchall():
            self.parkingLots[lot['name']] = ManagerParkingLot(
                lot['id'], lot['name'], lot['occupiedspots'], lot['totalspaces'], lot['rate'], lot['overtimerate'], 0)
        result = self.connection.execute(sqlBilling)
        for lot in self.connection.fetchall():
            self.parkingLots[lot['name']] = ManagerParkingLot(
                lot['id'], lot['name'], lot['occupiedspots'], lot['totalspaces'], lot['rate'], lot['overtimerate'], lot['revenuegenerated'])

    # takes name and new rates as parameter and updates db record
    def setRate(self, name, rate):
        lotid = self.parkingLots[name].getlotID()
        overtimeRate = self.parkingLots[name].getRate()
        updateOldRate = f"UPDATE rates SET expirydate=NOW() WHERE lotid='{lotid}'"
        insertNewRate = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{lotid}', '{rate}', '{overtimeRate}')"
        self.connection.execute(updateOldRate)
        self.connection.execute(insertNewRate)
        self.db.commit()


    # takes name and new rates as parameter and updates db record
    def setOvertimeRate(self, name, overtimerate):
        lotid = self.parkingLots[name].getlotID()
        rate = self.parkingLots[name].getRate()
        updateOldRate = f"UPDATE rates SET expirydate=NOW() WHERE lotid='{lotid}'"
        insertNewRate = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{lotid}', '{rate}', '{overtimerate}')"
        self.connection.execute(updateOldRate)
        self.connection.execute(insertNewRate)
        self.db.commit()

    # takes name and new rates as parameter and updates db record
    def setBothRate(self, name, rate, overtimerate):
        lotid = self.parkingLots[name].getlotID()
        updateOldRate = f"UPDATE rates SET expirydate=NOW() WHERE lotid='{lotid}'"
        insertNewRate = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{lotid}', '{rate}', '{overtimerate}')"
        self.connection.execute(updateOldRate)
        self.connection.execute(insertNewRate)
        self.db.commit()

    # takes name as a parameter and returns current occupancy of that lot
    def getOccupancy(self, name):
        self.updateLotList()
        return self.parkingLots[name].getOccupancyRate()

    # takes name as a parameter and returns current billing rate
    def getRate(self, name):
        self.updateLotList()
        return self.parkingLots[name].getRate()

    # takes name as a parameter and returns overtime billing rate
    def getOvertimeRate(self, name):
        self.updateLotList()
        return self.parkingLots[name].getOvertimeRate()

    # takes name as a parameter and returns revenue generated by that lot in the past month
    def getRevenueGenerated(self, name):
        self.updateLotList()
        return self.parkingLots[name].getPastMonthRevenue()

    # return list of parking lot names
    def getLots(self):
        self.updateLotList()
        return list(self.parkingLots.keys())

    # function to create a new parking lot
    def createNewLot(self, name, floors, spaceperfloor, standardrate, overtimerate):
        uniquemanagersql = f"SELECT * FROM parkinglot WHERE name like '{name}'"
        self.connection.execute(uniquemanagersql)
        if self.connection.fetchall():
            print("Lot name is not unique. Please pick a different name")
            return
        createlotsql = f"INSERT INTO parkinglot (name,numfloors,numspaces) VALUES ('{name}','{floors}','{spaceperfloor}')"
        self.connection.execute(createlotsql)
        setratesql = f"INSERT INTO rates (lotid, rate, overtimerate) VALUES ('{self.connection.lastrowid}','{standardrate}','{overtimerate}')"
        self.connection.execute(setratesql)
        self.db.commit()

    # function to create a new manager record
    def createNewManager(self, fullname, username, password):
        uniquemanagersql = f"SELECT * FROM manager WHERE username like '{username}'"
        self.connection.execute(uniquemanagersql)
        if self.connection.fetchall():
            print("Username is not unique. Please pick a different username")
            return
        createmanagersql = f"INSERT INTO manager (fullname, username, password) VALUES ('{fullname}', '{username}', '{sha256(password.encode()).hexdigest()}')"
        self.connection.execute(createmanagersql)
        self.db.commit()
