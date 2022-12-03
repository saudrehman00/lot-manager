# Module Imports
import mariadb
import MySQLdb
import sys
import os
from dotenv import load_dotenv
 


class ParkingLot:
    load_dotenv()
 
    # Constructor
    def __init__(self, id, name, numfloors, numspaces):
        self.id = id
        self.name = name
        self.numfloors = numfloors
        self.numspaces = numspaces

        try:
            self.conn = MySQLdb.connect(
                user=os.environ['dbuser'],
                password=os.environ['dbpswd'],
                host=os.environ['dbhost'],
                port=3306,
                database=os.environ['db']
        )
        except mariadb.Error as e:
            print(f"Error connecting to Platform: {e}")
            sys.exit(1)

        self.cur = self.conn.cursor()

    def chargeCustomer(self, lotid):
        parkingRate = 0
        overtime = 0
        self.cur.execute(f'SELECT rate FROM rates WHERE lotid={lotid};')
        rates = self.cur.fetchone()
        for (rate) in rates:
            parkingRate = rate

        self.cur.execute(f'SELECT overtimerate FROM rates WHERE lotid={lotid};')
        overtimerate = self.cur.fetchone()
        for (rate) in overtimerate:
            overtime = rate

        parkingRate += overtime
        
        print("Please make a payment of $" , parkingRate)

    def getFullSpaces(self, floor):
        self.cur.execute(f"SELECT floor, spacenumber FROM userticket WHERE lotid = {self.id} AND floor = {floor}")
        spaces = self.cur.fetchall()
        print(spaces)

        spaceList = []
        for(space) in spaces:
            spaceList.append((space[0], space[1]))
        return spaceList

    def validateParkingSpot(self, takenSpaces, floor, spot):
        parkingSpot = (floor, int(spot))
        
        if parkingSpot not in takenSpaces:
            return True
        else:
            return False