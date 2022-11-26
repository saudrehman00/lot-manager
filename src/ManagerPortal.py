from dotenv import load_dotenv
import MySQLdb
import os


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
        sql = "SELECT * FROM "
        result = self.connection.execute("SHOW TABLES;")
        print(self.connection.fetchall())

    def setRate(self, rate):
        sql = ""
        result = self.connection.execute("SHOW TABLES;")
        print(self.connection.fetchall())

    def setOvertimeRate(self, rate):
        sql = ""
        result = self.connection.execute("SHOW TABLES;")
        print(self.connection.fetchall())
    
    def getLotData(self,name):
        sql = ""
        result = self.connection.execute("SHOW TABLES;")
        print(self.connection.fetchall())

    def getOccupancy(self,name):
        sql = ""
        result = self.connection.execute("SHOW TABLES;")
        print(self.connection.fetchall())

    def getOccupancies(self,name):
        sql = ""
        result = self.connection.execute("SHOW TABLES;")
        print(self.connection.fetchall())